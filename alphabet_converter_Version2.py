#!/usr/bin/env python3
"""
alphabet_converter.py

Reads a line of text from the user and converts it using the provided alphabet mapping.

Mapping (case-insensitive):
A  = V́
B  = Г
CH = T
D  = コ
E  = H
F  = ∀
G  = 7
H  = X
I  = И
J  = ﾚ̀
C/K/Q = ヲ
L/R = Z
M  = П
N  = L
O  = V̀
P  = F
S  = Λ
SH = ﾚ
T  = E
U  = V̄
V  = V
W  = V
X  = A
Y  = K
Z  = A

Rules:
- Digraphs "CH" and "SH" are matched first (so "CH" becomes "T", not "C" + "H").
- "C", "K", and "Q" all map to ヲ.
- "L" and "R" both map to Z.
- Non-mapped characters (digits, punctuation, emoji, whitespace, etc.) are preserved unchanged.
- Conversion is case-insensitive.
"""

MAPPING = {
    # Digraphs (matched first)
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

def convert_text(s: str) -> str:
    """
    Convert the input string s according to MAPPING.
    Handles digraphs CH and SH first.
    """
    out = []
    i = 0
    n = len(s)
    while i < n:
        # Try two-character digraph (case-insensitive)
        if i + 1 < n:
            two = (s[i] + s[i+1]).upper()
            if two in MAPPING:
                out.append(MAPPING[two])
                i += 2
                continue
        # Single character
        ch = s[i]
        up = ch.upper()
        if up in MAPPING:
            out.append(MAPPING[up])
        else:
            # Preserve characters we don't have mappings for
            out.append(ch)
        i += 1
    return "".join(out)

def main():
    try:
        text = input("Enter text to convert: ")
    except EOFError:
        return
    result = convert_text(text)
    print("Converted:")
    print(result)

if __name__ == "__main__":
    main()