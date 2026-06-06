"""
g2e.py — Casio fx-9860/9750 eActivity (.g2e) file generator

Binary format reference:
  - Casio Standard Container Header: 32 bytes, stored as bitwise NOT
  - EACT header: file size, setup-area length, G2E version marker
  - Setup area: 56-byte block with fixed eActivity settings
  - @EACT / EACT1 sections: nested chunk headers with line count
  - Line directory: array of (type, 3-byte-offset) descriptors + 4-byte terminator
  - Line data: null-terminated, 4-byte-aligned text entries

Sources: Simon CHM fx_legacy_eactivityformat.htm, Cahute project (cahute.org)
"""

import struct
import re
from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Format constants — verified against real fx-9750GIII .g2e files
# ---------------------------------------------------------------------------

_HEADING_WIDTH = 21  # real calculator headings are 21 chars: ======NAME=======
_HEADING_LEFT_PAD = 6
_HEADING_TITLE_MAX = 8  # storage/eActivity title safety: 8.3-style base name

_LS = 0x38  # setup-area length (always 56 bytes in real files)

_VERSION_MARKER = b"\x00\x01\x02\x00\x03\x60\x32\x00"

# Fixed 56-byte setup area — identical in every .g2e created by the calculator
# or by Eact Maker.  Confirmed across DERIVADA, INTEGRAL, FUNCIONE, VECTORES,
# LIMITES, PC~EJEMP.
_SETUP_AREA = bytes.fromhex(
    "000000000000142a3f02c0000000283000000000"
    "010201010103010101010101010101010101"
    "000000000000000000000000000000000000"
)


# ---------------------------------------------------------------------------
# Character encoding
# ---------------------------------------------------------------------------

# Characters that need remapping from Unicode to Casio FONTCHARACTER encoding.
# Basic printable ASCII (0x20-0x7E) maps 1:1; only exceptions listed here.
#
# Keep only verified mappings here. New UI symbols must also be mapped here
# with known Casio byte values.
def _b(hexstr: str) -> bytes:
    """Small readability helper for Casio two-byte FONTCHARACTER values."""
    return bytes.fromhex(hexstr)


_CASIO_REMAP: dict[str, bytes] = {
    # Single-byte Casio characters / operators.
    "≤": b"\x10", "≠": b"\x11", "≥": b"\x12", "⇒": b"\x13",
    "√": b"\x86", "×": b"\xA9", "÷": b"\xB9", "°": b"\x9C", "∛": b"\x96",

    # Latin / punctuation / currency extensions (E5 block).
    "À": _b("E501"), "Á": _b("E502"), "Â": _b("E503"), "Ã": _b("E504"), "Ä": _b("E505"), "Å": _b("E506"), "Ç": _b("E508"),
    "È": _b("E509"), "É": _b("E50A"), "Ê": _b("E50B"), "Ë": _b("E50C"), "Ì": _b("E50D"), "Í": _b("E50E"), "Î": _b("E50F"), "Ï": _b("E510"),
    "Ñ": _b("E512"), "Ò": _b("E513"), "Ó": _b("E514"), "Ô": _b("E515"), "Õ": _b("E516"), "Ö": _b("E517"), "Ø": _b("E518"),
    "Ù": _b("E519"), "Ú": _b("E51A"), "Û": _b("E51B"), "Ü": _b("E51C"), "Ý": _b("E51D"), "Ÿ": _b("E520"),
    "¡": _b("E590"), "¿": _b("E591"), "€": _b("E592"), "ƒ": _b("E593"), "…": _b("E594"), "‘": _b("E595"), "’": _b("E596"),
    "“": _b("E597"), "”": _b("E598"), "¢": _b("E599"), "£": _b("E59A"), "¤": _b("E59B"), "¥": _b("E59C"), "§": _b("E59D"),
    "¬": _b("E5A0"), "«": _b("E5A3"), "»": _b("E5A4"), "▫": _b("E5A5"), "❌": _b("E5A6"), "·": _b("E5A7"),

    # Greek capitals (E5 block). Full uppercase Greek alphabet, except no E552 slot.
    "Α": _b("E540"), "Β": _b("E541"), "Γ": _b("E542"), "Δ": _b("E543"), "Ε": _b("E544"), "Ζ": _b("E545"), "Η": _b("E546"), "Θ": _b("E547"),
    "Ι": _b("E548"), "Κ": _b("E549"), "Λ": _b("E54A"), "Μ": _b("E54B"), "Ν": _b("E54C"), "Ξ": _b("E54D"), "Ο": _b("E54E"), "Π": _b("E54F"),
    "Ρ": _b("E550"), "Σ": _b("E551"), "Τ": _b("E553"), "Υ": _b("E554"), "Φ": _b("E555"), "Χ": _b("E556"), "Ψ": _b("E557"), "Ω": _b("E558"),

    # Superscripts / subscripts (E5 block).
    "⁰": _b("E5C0"), "¹": _b("E5C1"), "²": _b("E5C2"), "³": _b("E5C3"), "⁴": _b("E5C4"), "⁵": _b("E5C5"), "⁶": _b("E5C6"), "⁷": _b("E5C7"), "⁸": _b("E5C8"), "⁹": _b("E5C9"),
    "⁺": _b("E5CB"), "⁻": _b("E5CC"), "₀": _b("E5D0"), "₁": _b("E5D1"), "₂": _b("E5D2"), "₃": _b("E5D3"), "₄": _b("E5D4"), "₅": _b("E5D5"),
    "₆": _b("E5D6"), "₇": _b("E5D7"), "₈": _b("E5D8"), "₉": _b("E5D9"), "₊": _b("E5DB"), "₋": _b("E5DC"), "ₙ": _b("E5DE"),

    # Latin lowercase accents (E6 block).
    "à": _b("E601"), "á": _b("E602"), "â": _b("E603"), "ã": _b("E604"), "ä": _b("E605"), "å": _b("E606"), "ç": _b("E608"),
    "è": _b("E609"), "é": _b("E60A"), "ê": _b("E60B"), "ë": _b("E60C"), "ì": _b("E60D"), "í": _b("E60E"), "î": _b("E60F"), "ï": _b("E610"),
    "ñ": _b("E612"), "ò": _b("E613"), "ó": _b("E614"), "ô": _b("E615"), "õ": _b("E616"), "ö": _b("E617"), "ø": _b("E618"),
    "ù": _b("E619"), "ú": _b("E61A"), "û": _b("E61B"), "ü": _b("E61C"), "ý": _b("E61D"), "ÿ": _b("E620"),

    # Greek lowercase (E6 block). Casio's first glyph is Latin alpha U+0251; map both ɑ and normal α for usability.
    "ɑ": _b("E640"), "α": _b("E640"), "β": _b("E641"), "γ": _b("E642"), "δ": _b("E643"), "ε": _b("E644"), "ζ": _b("E645"), "η": _b("E646"), "θ": _b("E647"),
    "ι": _b("E648"), "κ": _b("E649"), "λ": _b("E64A"), "μ": _b("E64B"), "ν": _b("E64C"), "ξ": _b("E64D"), "ο": _b("E64E"), "π": _b("E64F"),
    "ρ": _b("E650"), "σ": _b("E651"), "ς": _b("E652"), "τ": _b("E653"), "υ": _b("E654"), "φ": _b("E655"), "χ": _b("E656"), "ψ": _b("E657"), "ω": _b("E658"),

    # Cyrillic capitals / lowercase (E5/E6 blocks). Included because EactMaker exposes the full Casio text catalog.
    "А": _b("E560"), "Б": _b("E561"), "В": _b("E562"), "Г": _b("E563"), "Д": _b("E564"), "Е": _b("E565"), "Ё": _b("E566"), "Ж": _b("E567"), "З": _b("E568"),
    "И": _b("E569"), "Й": _b("E56A"), "К": _b("E56B"), "Л": _b("E56C"), "М": _b("E56D"), "Н": _b("E56E"), "О": _b("E56F"), "П": _b("E570"),
    "Р": _b("E571"), "С": _b("E572"), "Т": _b("E573"), "У": _b("E574"), "Ф": _b("E575"), "Х": _b("E576"), "Ц": _b("E577"), "Ч": _b("E578"),
    "Ш": _b("E579"), "Щ": _b("E57A"), "Ъ": _b("E57B"), "Ы": _b("E57C"), "Ь": _b("E57D"), "Э": _b("E57E"), "Ю": _b("E580"), "Я": _b("E581"), "Є": _b("E582"),
    "а": _b("E660"), "б": _b("E661"), "в": _b("E662"), "г": _b("E663"), "д": _b("E664"), "е": _b("E665"), "ё": _b("E666"), "ж": _b("E667"), "з": _b("E668"),
    "и": _b("E669"), "й": _b("E66A"), "к": _b("E66B"), "л": _b("E66C"), "м": _b("E66D"), "н": _b("E66E"), "о": _b("E66F"), "п": _b("E670"),
    "р": _b("E671"), "с": _b("E672"), "т": _b("E673"), "у": _b("E674"), "ф": _b("E675"), "х": _b("E676"), "ц": _b("E677"), "ч": _b("E678"),
    "ш": _b("E679"), "щ": _b("E67A"), "ъ": _b("E67B"), "ы": _b("E67C"), "ь": _b("E67D"), "э": _b("E67E"), "ю": _b("E680"), "я": _b("E681"), "є": _b("E682"),

    # Arrows / shapes (E6 block).
    "←": _b("E690"), "→": _b("E691"), "↑": _b("E692"), "↓": _b("E693"), "↔": _b("E694"), "↕": _b("E695"), "↖": _b("E696"), "↗": _b("E697"), "↘": _b("E698"), "↙": _b("E699"),
    "◀": _b("E69A"), "▶": _b("E69B"), "▲": _b("E69C"), "▼": _b("E69D"), "▸": _b("E69E"), "▹": _b("E69F"), "⋇": _b("E6A0"), "【": _b("E6A1"), "】": _b("E6A2"),
    "○": _b("E6A3"), "●": _b("E6A4"), "□": _b("E6A5"), "■": _b("E6A6"), "♢": _b("E6A7"), "♦": _b("E6A8"), "⊠": _b("E6A9"), "∙": _b("E6AA"),

    # Relations / calculus / sets / logic (E6 block).
    "≒": _b("E6B0"), "≈": _b("E6B1"), "≡": _b("E6B2"), "≢": _b("E6B3"), "≅": _b("E6B4"), "∽": _b("E6B5"), "∝": _b("E6B6"),
    "∬": _b("E6B7"), "∮": _b("E6B8"), "∂": _b("E6B9"), "∫": _b("E6BB"), "∡": _b("E6BC"), "∈": _b("E6BD"), "∋": _b("E6BE"),
    "⊆": _b("E6BF"), "⊇": _b("E6C0"), "⊂": _b("E6C1"), "⊃": _b("E6C2"), "⋃": _b("E6C3"), "⋂": _b("E6C4"),
    # Convenience aliases for union/intersection glyphs.
    "∪": _b("E6C3"), "∩": _b("E6C4"),
    "∉": _b("E6C5"), "∌": _b("E6C6"), "⊈": _b("E6C7"), "⊉": _b("E6C8"), "⊄": _b("E6C9"), "⊅": _b("E6CA"), "∅": _b("E6CB"), "∃": _b("E6CC"),
    "∟": _b("E6CD"), "∨": _b("E6CE"), "∧": _b("E6CF"), "∀": _b("E6D0"), "⊕": _b("E6D1"), "⊖": _b("E6D2"), "⊗": _b("E6D3"), "⊘": _b("E6D4"),
    "⟂": _b("E6D5"), "≬": _b("E6D6"), "∥": _b("E6D7"), "∦": _b("E6D8"), "⫽": _b("E6D9"), "▽": _b("E6DA"), "∴": _b("E6DB"), "∵": _b("E6DC"), "′": _b("E6DD"), "″": _b("E6DE"),
}


def _extract_balanced(text: str, start: int) -> tuple:
    """Return (inner_content, pos_after_closing_brace) for text[start:] inside {}."""
    depth = 1
    i = start
    while i < len(text) and depth > 0:
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
        i += 1
    return text[start:i - 1], i


def _encode_math_expr(text: str) -> bytes:
    """Encode markup text to Casio FONTCHARACTER bytes.

    Math markup:
      \\frac{num}{den}  → fraction (BB 1D 1A num 1B 1A den 1B 1E)
      ^{exp}           → superscript (A8 1A exp 1B)
      \\sqrt{x}        → root symbol + content
      \\int            → integral symbol (E6 BB)
    Plain ASCII and _CASIO_REMAP chars handled as before.
    """
    result = bytearray()
    i = 0
    while i < len(text):
        rest = text[i:]
        if rest.startswith("\\frac{"):
            num, j = _extract_balanced(text, i + 6)
            if j < len(text) and text[j] == "{":
                den, j = _extract_balanced(text, j + 1)
            else:
                den = ""
            result += b"\xbb\x1d\x1a"
            result += _encode_math_expr(num)
            result += b"\x1b\x1a"
            result += _encode_math_expr(den)
            result += b"\x1b\x1e"
            i = j
        elif rest.startswith("\\sqrt["):
            # Nth root: \sqrt[n]{x} → B8 1D 1A [n] 1B 1A [x] 1B 1E
            close_bracket = text.find(']', i + 6)
            if close_bracket == -1:
                result += b"\x00\xbd"
                i += 5
            else:
                n_str = text[i + 6:close_bracket]
                if close_bracket + 1 < len(text) and text[close_bracket + 1] == '{':
                    x_str, j = _extract_balanced(text, close_bracket + 2)
                else:
                    x_str = ""
                    j = close_bracket + 1
                result += b"\xb8\x1d\x1a"
                result += _encode_math_expr(n_str)
                result += b"\x1b\x1a"
                result += _encode_math_expr(x_str)
                result += b"\x1b\x1e"
                i = j
        elif rest.startswith("\\sqrt{"):
            # Square root: \sqrt{x} → 86 1D 1A [x] 1B 1E
            arg, j = _extract_balanced(text, i + 6)
            result += b"\x86\x1d\x1a"
            result += _encode_math_expr(arg)
            result += b"\x1b\x1e"
            i = j
        elif rest.startswith("\\sqrt"):
            result += b"\x00\xbd"
            i += 5
        elif rest.startswith("\\abs{"):
            # Absolute value: \abs{x} → 97 1D 1A [x] 1B 1E
            # Structural form used by calculator math templates.
            arg, j = _extract_balanced(text, i + 5)
            result += b"\x97\x1d\x1a"
            result += _encode_math_expr(arg)
            result += b"\x1b\x1e"
            i = j
        elif rest.startswith("\\int"):
            result += b"\xe6\xbb"
            i += 4
        elif text[i] == "^" and i + 1 < len(text) and text[i + 1] == "{":
            exp, j = _extract_balanced(text, i + 2)
            result += b"\xa8\x1a"
            result += _encode_math_expr(exp)
            result += b"\x1b"
            i = j
        else:
            ch = text[i]
            if ch in _CASIO_REMAP:
                result.extend(_CASIO_REMAP[ch])
            elif ch == "\n":
                result.append(0x0A)
            elif 0x20 <= ord(ch) <= 0x7E:
                result.append(ord(ch))
            else:
                result.append(0x3F)
            i += 1
    return bytes(result)


def encode_casio_text(text: str) -> bytes:
    """Backwards-compatible alias for _encode_math_expr."""
    return _encode_math_expr(text)


def _line_math_type(text: str) -> tuple:
    """Return (is_math_line, height_byte) for a content line.

    is_math_line → emit as type 0x82 with 4-byte formula prefix.
    height_byte  → display height hint used in that prefix.
    """
    has_frac  = "\\frac{" in text
    has_sqrt  = "\\sqrt{" in text or "\\sqrt[" in text
    has_super = "^{" in text
    has_abs   = "\\abs{" in text
    if not (has_frac or has_sqrt or has_super or has_abs):
        return False, 0x08
    if has_frac and (has_sqrt or has_abs):
        return True, 0x1A   # 26 px: taller nested expressions
    if has_frac:
        return True, 0x16   # 22 px: fraction only
    if has_abs:
        return True, 0x0C
    return True, 0x0C       # 12 px: root or superscript


def _strip_markup_for_width(text: str) -> str:
    """Very small markup-to-visible-text approximation for width estimation."""
    out = []
    i = 0
    while i < len(text):
        rest = text[i:]
        if rest.startswith("\\frac{"):
            num, j = _extract_balanced(text, i + 6)
            den = ""
            if j < len(text) and text[j] == "{":
                den, j = _extract_balanced(text, j + 1)
            out.append(max(_strip_markup_for_width(num), _strip_markup_for_width(den), key=len))
            i = j
        elif rest.startswith("\\sqrt["):
            close_bracket = text.find(']', i + 6)
            if close_bracket != -1 and close_bracket + 1 < len(text) and text[close_bracket + 1] == '{':
                arg, j = _extract_balanced(text, close_bracket + 2)
                out.append("√" + _strip_markup_for_width(arg))
                i = j
            else:
                out.append("√")
                i += 5
        elif rest.startswith("\\sqrt{"):
            arg, j = _extract_balanced(text, i + 6)
            out.append("√" + _strip_markup_for_width(arg))
            i = j
        elif rest.startswith("\\sqrt"):
            out.append("√")
            i += 5
        elif rest.startswith("\\abs{"):
            arg, j = _extract_balanced(text, i + 5)
            out.append("|" + _strip_markup_for_width(arg) + "|")
            i = j
        elif rest.startswith("\\int"):
            out.append("∫")
            i += 4
        elif text[i] == "^" and i + 1 < len(text) and text[i + 1] == "{":
            exp, j = _extract_balanced(text, i + 2)
            out.append(_strip_markup_for_width(exp))
            i = j
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def _estimate_math_width(text: str) -> int:
    """Estimate the first 2 bytes of a 0x82 formula prefix.

    Real calculator-created files do not keep this fixed at 0x0080; it is a
    rendered-width/cache hint.  Keeping it closer to the expression length makes
    generated files less scroll-heavy and closer to native eActivities.
    """
    visible = _strip_markup_for_width(text)
    # fx-9750GIII text cells are roughly 6 px wide.  0x80 is a safe cap observed
    # in real files; very small formulas still get a small minimum.
    width = len(visible) * 6 + 8
    if "\\frac{" in text:
        width += 8
    if "\\sqrt" in text or "\\abs{" in text:
        width += 4
    return max(0x08, min(0x80, width))


def sanitize_casio_filename(name: str, fallback: str = "EACT") -> str:
    """Return a calculator-safe 8.3-style .g2e filename.

    The generated binary does not store the file name, but the calculator's
    storage browser is more reliable with an 8-character ASCII base name.
    Letter case is preserved because the calculator accepts mixed-case names
    when the file is renamed manually.
    """
    base = (name or fallback).strip()
    if base.lower().endswith(".g2e"):
        base = base[:-4]
    base = base.replace(" ", "_")
    base = re.sub(r"[^A-Za-z0-9_~\-]", "_", base)
    base = base.strip("._- ") or fallback
    return base[:_HEADING_TITLE_MAX] + ".g2e"


def _safe_heading_text(title: str, fallback: str = "EACT") -> str:
    """Build the exact 21-character heading used by native eActivities."""
    safe = sanitize_casio_filename(title or fallback, fallback=fallback)[:-4]
    safe = safe[:_HEADING_TITLE_MAX] or fallback[:_HEADING_TITLE_MAX]
    right = _HEADING_WIDTH - _HEADING_LEFT_PAD - len(safe)
    if right < 1:
        safe = safe[:_HEADING_WIDTH - _HEADING_LEFT_PAD - 1]
        right = _HEADING_WIDTH - _HEADING_LEFT_PAD - len(safe)
    return "=" * _HEADING_LEFT_PAD + safe + "=" * right


def validate_g2e(data: bytes) -> None:
    """Raise ValueError if the generated .g2e breaks core structural rules."""
    if len(data) < 0x90:
        raise ValueError("Generated file is too small to be a valid .g2e")
    if int.from_bytes(data[0x20:0x24], "big") != len(data):
        raise ValueError("FileSize field does not match real byte length")
    if int.from_bytes(data[0x24:0x28], "big") != _LS:
        raise ValueError("Invalid setup-area length (LS)")
    if data[0x28:0x30] != _VERSION_MARKER:
        raise ValueError("Invalid G2E version marker")
    if data[0x30:0x30 + _LS] != _SETUP_AREA:
        raise ValueError("Setup area differs from verified 56-byte block")
    if data.find(b"@EACT") != 0x68:
        raise ValueError("@EACT chunk is not at offset 0x68")
    if data[0x78:0x80] != b"EACT1\x00\x00\x00":
        raise ValueError("Missing EACT1 subchunk")
    length1 = int.from_bytes(data[0x74:0x78], "big")
    length2 = int.from_bytes(data[0x84:0x88], "big")
    if length1 != len(data) - 0x78:
        raise ValueError("Outer @EACT length is inconsistent")
    if length2 != len(data) - 0x8C:
        raise ValueError("Inner EACT1 length is inconsistent")
    if data[0x88:0x8C] != b"\xD4\x00\x00\x66":
        raise ValueError("Unexpected EACT1 body marker")

    base = 0x8C
    lc = int.from_bytes(data[base:base + 4], "big")
    if lc <= 0:
        raise ValueError("Line count must be positive")
    dir_start = base + 4
    term_start = dir_start + lc * 4
    if term_start + 4 > len(data):
        raise ValueError("Line directory overflows file")
    if data[term_start:term_start + 4] != b"\x00\x00\x00\x00":
        raise ValueError("Line directory terminator is missing")

    offsets = []
    for i in range(lc):
        pos = dir_start + i * 4
        typ = data[pos]
        off = int.from_bytes(data[pos + 1:pos + 4], "big")
        if typ not in (0x07, 0x81, 0x82):
            raise ValueError(f"Unsupported line type 0x{typ:02X} at entry {i}")
        offsets.append(off)
    first_data_offset = 8 + lc * 4
    if offsets[0] != first_data_offset:
        raise ValueError("First data offset does not match line directory size")
    if offsets != sorted(offsets):
        raise ValueError("Line data offsets are not monotonic")
    if any(base + off > len(data) for off in offsets):
        raise ValueError("A line data offset points past EOF")

    first_end = offsets[1] if lc > 1 else len(data) - base
    first_line = data[base + offsets[0]:base + first_end]
    zero = first_line.find(b"\x00")
    if data[dir_start] != 0x07 or zero != _HEADING_WIDTH:
        raise ValueError("First entry must be a 21-character 0x07 heading")


# ---------------------------------------------------------------------------
# File-builder
# ---------------------------------------------------------------------------

def _align4(data: bytes) -> bytes:
    """Pad data to the next 4-byte boundary with zero bytes."""
    pad = (4 - len(data) % 4) % 4
    return data + b"\x00" * pad


@dataclass
class TextStrip:
    """One strip (section) inside an eActivity document."""
    title: str = ""
    lines: List[str] = field(default_factory=list)


class G2EBuilder:
    """Builds a Casio .g2e eActivity binary from text strips."""

    def __init__(self, default_title: str = "EACT") -> None:
        self.strips: List[TextStrip] = []
        self.default_title = default_title

    def add_strip(self, title: str = "", lines: Optional[List[str]] = None) -> "G2EBuilder":
        self.strips.append(TextStrip(title=title, lines=lines or []))
        return self

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self) -> bytes:
        """Return the complete .g2e file as a bytes object."""
        # --- Build line entries: list of (type, aligned_data) --------
        # type 0x07 = strip heading   type 0x81 = pure text line   type 0x82 = math line
        # Real and PC-generated files always have:
        #   - Heading stored as a fixed 21-character row, e.g. "======TITLE======="
        #   - One blank TEXT entry (4 null bytes) immediately after each heading
        _BLANK = (0x81, b"\x00\x00\x00\x00")

        line_entries: List[tuple[int, bytes]] = []

        for idx, strip in enumerate(self.strips):
            # Native .g2e files use a fixed-width, 21-character heading such as
            # "======DERIVADA=======".  The previous generator allowed an empty
            # or variable-length 0x07 heading; those files could open once, but
            # were unsafe when the calculator rewrote/closed the eActivity.
            heading = _safe_heading_text(
                strip.title,
                fallback=self.default_title if idx == 0 else f"STRIP{idx + 1}",
            )
            heading_raw = encode_casio_text(heading) + b"\x00"
            line_entries.append((0x07, _align4(heading_raw)))
            line_entries.append(_BLANK)  # blank line after heading (matches calculator behavior)

            for line in strip.lines:
                line = line.replace("\t", "    ").rstrip("\r")
                is_math, height = _line_math_type(line)
                encoded = _encode_math_expr(line) + b"\x00"
                if is_math:
                    width = _estimate_math_width(line)
                    prefix = struct.pack(">H", width) + b"\x00" + bytes([height])
                    line_entries.append((0x82, _align4(prefix + encoded)))
                else:
                    line_entries.append((0x81, _align4(encoded)))

        LC = len(line_entries)

        # --- Line directory + data ------------------------------------
        # Offsets in each descriptor are relative to (0x54 + LS), i.e.,
        # the absolute position of the LC field.
        # Layout at that base:
        #   +0x00  LC (4 bytes)
        #   +0x04  directory entries (LC × 4 bytes each)
        #   +0x04 + LC×4  terminator (4 bytes)
        #   +0x08 + LC×4  line data starts  ← first_data_offset

        first_data_offset = 8 + LC * 4
        cumulative = first_data_offset

        line_dir = bytearray()
        line_data = bytearray()
        for etype, edata in line_entries:
            line_dir += bytes([etype]) + struct.pack(">I", cumulative)[1:]  # 3-byte BE
            line_data += edata
            cumulative += len(edata)
        line_dir += b"\x00\x00\x00\x00"  # terminator

        content = struct.pack(">I", LC) + bytes(line_dir) + bytes(line_data)

        # --- @EACT / EACT1 nested chunk structure ---------------------
        # With _LS=0x38, absolute offsets in the file body:
        #   0x68  "@EACT\x00\x00\x00"
        #   0x70  00 00 00 01
        #   0x74  length1
        #   0x78  "EACT1\x00\x00\x00"
        #   0x80  00 00 00 14   (fixed sub-header size)
        #   0x84  length2
        #   0x88  D4 00 00 66
        #   0x8C  LC + line_dir + line_data

        inner_body = b"\xd4\x00\x00\x66" + content
        # IMPORTANT: native fx-9750GIII/eAct Maker files store length2 as the
        # size of LC + directory + line data only. It does NOT include the
        # preceding D4 00 00 66 marker. The previous generator wrote +4 here;
        # that produced files that could open once but were unsafe after close.
        length2 = len(content)

        eact1_block = (
            b"EACT1\x00\x00\x00"
            + struct.pack(">I", 0x14)
            + struct.pack(">I", length2)
            + inner_body
        )
        length1 = len(eact1_block)

        eact_section = (
            b"@EACT\x00\x00\x00"
            + struct.pack(">I", 1)
            + struct.pack(">I", length1)
            + eact1_block
        )

        # --- Assemble body (everything after the 32-byte container hdr)
        body = (
            b"\x00\x00\x00\x00"     # FileSize placeholder @ 0x20
            + struct.pack(">I", _LS) # LS @ 0x24
            + _VERSION_MARKER        # @ 0x28
            + _SETUP_AREA            # @ 0x30, _LS bytes
            + eact_section           # @ 0x30+_LS = 0x68
        )

        file_size = 0x20 + len(body)
        body = struct.pack(">I", file_size) + body[4:]  # patch FileSize

        # --- Casio Standard Container Header (32 bytes, stored as ~NOT) -
        # Values verified against real fx-9750GIII files.
        hdr = bytearray(32)
        hdr[0:8] = b"USBPower"
        hdr[8]  = 0x49   # file-type: eActivity
        hdr[9]  = 0x00
        hdr[10] = 0x10   # subtype (Cahute: USBPower\x49\0\x10\0\x10\0)
        hdr[11] = 0x00
        hdr[12] = 0x10
        hdr[13] = 0x00
        hdr[0x0E] = (file_size + 0x41) & 0xFF   # control byte C1
        hdr[0x0F] = 0x01                          # fixed 0x01 in all real files
        struct.pack_into(">I", hdr, 0x10, file_size)
        hdr[0x14] = (file_size + 0xB8) & 0xFF   # control byte C2
        # 0x15–0x1F: all 0xFF in real files (stored as 0x00 after NOT)
        for i in range(0x15, 0x20):
            hdr[i] = 0xFF

        not_hdr = bytes([~b & 0xFF for b in hdr])
        return not_hdr + body


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------

def create_g2e(strips: List[tuple[str, List[str]]], default_title: str = "EACT") -> bytes:
    """Shortcut: create_g2e([("Title", ["line1", "line2"]), ...]) → bytes."""
    builder = G2EBuilder(default_title=default_title)
    for title, lines in strips:
        builder.add_strip(title=title, lines=lines)
    data = builder.build()
    validate_g2e(data)
    return data


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _cli() -> None:
    import argparse, sys, pathlib

    parser = argparse.ArgumentParser(
        description="Generate a Casio fx-9860/9750 eActivity (.g2e) file from a text file."
    )
    parser.add_argument("input", help="Input .txt file (use '=== Title ===' to start a new strip)")
    parser.add_argument("output", nargs="?", help="Output .g2e file (default: same name as input)")
    args = parser.parse_args()

    src = pathlib.Path(args.input)
    if not src.exists():
        print(f"Error: '{src}' not found.", file=sys.stderr)
        sys.exit(1)

    dst = pathlib.Path(args.output) if args.output else src.with_suffix(".g2e")

    raw_text = src.read_text(encoding="utf-8", errors="replace")
    strips = _parse_text(raw_text)

    data = create_g2e(strips, default_title=dst.stem)
    dst.write_bytes(data)
    print(f"Written {len(data)} bytes → {dst}")


def _parse_text(text: str) -> List[tuple[str, List[str]]]:
    """Parse plain text into strips.

    A line matching '=== ... ===' or '--- ... ---' starts a new strip and
    its content (trimmed) becomes the strip title.  If no such markers are
    present, the whole text goes into a single unnamed strip.
    """
    import re
    strips: List[tuple[str, List[str]]] = []
    current_title = ""
    current_lines: List[str] = []

    for raw_line in text.splitlines():
        m = re.match(r"^[=\-]{3,}\s*(.*?)\s*[=\-]{3,}$", raw_line.strip())
        if m:
            if current_lines or current_title:
                strips.append((current_title, current_lines))
            current_title = m.group(1)
            current_lines = []
        else:
            current_lines.append(raw_line)

    if current_lines or current_title:
        strips.append((current_title, current_lines))

    if not strips:
        strips = [("", [])]

    return strips


if __name__ == "__main__":
    _cli()
