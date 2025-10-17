#!/usr/bin/env python3
"""
alphabet_reverse.py

Reverse converter: reads a line of text composed with the special-symbol alphabet
and converts it back into Latin letters (best-effort, deterministic).

This script inverts the forward mapping used previously. Some symbol -> Latin
mappings are ambiguous (multiple Latin letters map to the same symbol). For
those cases the script uses a configurable preference table (see PREFERENCES).

Default preference choices (changeable):
- "ヲ" -> "K"   (C/K/Q all mapped to ヲ forward; default chosen: K)
- "Z"  -> "L"   (L/R both mapped to Z forward; default chosen: L)
- "A"  -> "Z"   (X/Z both mapped to A forward; default chosen: Z)
- "V"  -> "V"   (V/W both mapped to V forward; default chosen: V)

The converter matches the longest symbol sequence first (so multi-character
symbols like "V́", "V̀", "V̄", "ﾚ̀" and "ﾚ" are recognized correctly).
Unrecognized characters are preserved unchanged.

Usage:
    python3 alphabet_reverse.py
    Enter text to translate: <paste converted text>
    Result: <latin output>
"""

# Forward mapping (same mapping used previously)
FORWARD = {
    # Digraphs (matched first in forward conversion)
    "CH": "T",
    "SH": "ﾚ",

    # Single letters
    "A": "V́",
    "B": "Г",
    "C": "ヲ",
    "D": "コ",
    "E": "H",
    "F": "∀",
    "G": "7",
    "H": "X",
    "I": "И",
    "J": "ﾚ̀",
    "K": "ヲ",
    "L": "Z",
    "M": "П",
    "N": "L",
    "O": "V̀",
    "P": "F",
    "Q": "ヲ",
    "R": "Z",
    "S": "Λ",
    "T": "E",
    "U": "V̄",
    "V": "V",
    "W": "V",
    "X": "A",
    "Y": "K",
    "Z": "A",
}

# Default disambiguation preferences for symbols that have multiple possible Latin origins.
# Changed per your request: ヲ now defaults to "K" (was "C").
PREFERENCES = {
    "ヲ": "K",  # could be C, K, or Q — default now set to K
    "Z": "L",  # could be L or R
    "A": "Z",  # could be Z or X
    "V": "V",  # could be V or W
}

def build_reverse_map(forward_map):
    """Invert forward_map producing symbol -> [latin1, latin2, ...] lists."""
    rev = {}
    for latin, sym in forward_map.items():
        # group by symbol
        rev.setdefault(sym, []).append(latin)
    return rev

REVERSE = build_reverse_map(FORWARD)

# Precompute list of symbol keys sorted by descending length to match longest-first.
SYMBOLS_SORTED = sorted(REVERSE.keys(), key=len, reverse=True)

def choose_latin_for_symbol(symbol, preferences=None):
    """Return a chosen Latin string for the given symbol using preferences if needed."""
    options = REVERSE.get(symbol)
    if not options:
        return None
    if len(options) == 1:
        return options[0]
    # If preferences provided and contain this symbol, use it if valid.
    if preferences and symbol in preferences and preferences[symbol] in options:
        return preferences[symbol]
    # Fallback deterministic choice: first option sorted alphabetically
    return sorted(options)[0]

def reverse_convert(s: str, preferences=None) -> str:
    """
    Convert a string s composed of symbols back into Latin letters according to REVERSE.
    preferences is a dict mapping symbol -> preferred latin (string).
    """
    out = []
    i = 0
    n = len(s)
    while i < n:
        matched = False
        for sym in SYMBOLS_SORTED:
            if s.startswith(sym, i):
                latin = choose_latin_for_symbol(sym, preferences)
                if latin is None:
                    # should not happen, but preserve symbol
                    out.append(sym)
                else:
                    out.append(latin)
                i += len(sym)
                matched = True
                break
        if not matched:
            # No known symbol matched at this position: preserve char as-is
            out.append(s[i])
            i += 1
    return "".join(out)

def interactive():
    try:
        text = input("Enter symbol-text to convert back to Latin: ")
    except EOFError:
        return
    result = reverse_convert(text, preferences=PREFERENCES)
    print("Result:")
    print(result)
    # After printing, also show any ambiguity report so user can adjust preferences
    ambiguities = {sym: opts for sym, opts in REVERSE.items() if len(opts) > 1}
    if ambiguities:
        print("\nAmbiguous symbol mappings (symbol -> possible Latin origins):")
        for sym, opts in ambiguities.items():
            chosen = PREFERENCES.get(sym, "(no preference)")
            print(f"  {sym!r} -> {opts}  (chosen: {chosen!r})")
        print("\nTo change choices, edit PREFERENCES in this script (e.g. set PREFERENCES['ヲ']='C').")

if __name__ == "__main__":
    interactive()