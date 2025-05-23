"""
Original idea https://github.com/DaCoolOne/DumbIdeas/tree/main/reddit_ph_compressor
Release under MIT license
"""

import warnings
from .exception import UnknownCharacterException

__all__ = ["unicode_compress", "unicode_decompress"]


def unicode_compress(input_code: str) -> str:
    if "\t" in input_code:
        warnings.warn(
            "Code cannot contain tabs. Converting each tab to 4 spaces.", stacklevel=2
        )
        input_code = input_code.replace("\t", "    ")

    o = bytearray(b"E")
    line = 1
    for c in input_code.encode("utf-8"):
        
        if c == 13:
            warnings.warn("Non-unix line endings detected", stacklevel=2)
            continue

        if c == 10:
            line += 1

        if (c < 32 or c > 126) and c != 10:
            raise UnknownCharacterException(c, line)

        v = (c - 11) % 133 - 21
        o += ((v >> 6) & 1 | 0b11001100).to_bytes(1, "big")
        o += ((v & 63) | 0b10000000).to_bytes(1, "big")

    return (
        b"b='"
        + o
        + b"'.encode();exec(''.join(chr(((h<<6&64|c&63)+22)%133+10)for h,c in zip(b[1::2],b[2::2])))"
    ).decode("utf-8")


def unicode_decompress(s: str) -> str:
    b = s.encode("utf-8")
    return "".join(
        [
            chr(((h << 6 & 64 | c & 63) + 22) % 133 + 10)
            for h, c in zip(b[1::2], b[2::2])
        ]
    )
