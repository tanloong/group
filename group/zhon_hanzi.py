#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# https://github.com/tsroten/zhon/blob/main/src/zhon/hanzi.py

import sys

#: Character code ranges for pertinent CJK ideograph Unicode blocks.
characters = cjk_ideographs = (
    "\u3007"  # Ideographic number zero, see issue #17
    "\u4e00-\u9fff"  # CJK Unified Ideographs
    "\u3400-\u4dbf"  # CJK Unified Ideographs Extension A
    "\uf900-\ufaff"  # CJK Compatibility Ideographs
)
if sys.maxunicode > 0xFFFF:
    characters += (
        "\U00020000-\U0002a6df"  # CJK Unified Ideographs Extension B
        "\U0002a700-\U0002b73f"  # CJK Unified Ideographs Extension C
        "\U0002b740-\U0002b81f"  # CJK Unified Ideographs Extension D
        "\U0002f800-\U0002fa1f"  # CJK Compatibility Ideographs Supplement
    )

#: Character code ranges for the Kangxi radicals and CJK Radicals Supplement.
radicals = "\u2f00-\u2fd5\u2e80-\u2ef3"

#: A string containing Chinese punctuation marks (non-stops).
non_stops = (
    # Fullwidth ASCII variants
    "\uff02\uff03\uff04\uff05\uff06\uff07\uff08\uff09\uff0a\uff0b\uff0c\uff0d"
    "\uff0f\uff1a\uff1b\uff1c\uff1d\uff1e\uff20\uff3b\uff3c\uff3d\uff3e\uff3f"
    "\uff40\uff5b\uff5c\uff5d\uff5e\uff5f\uff60"
    # Halfwidth CJK punctuation
    "\uff62\uff63\uff64"
    # CJK symbols and punctuation
    "\u3000\u3001\u3003"
    # CJK angle and corner brackets
    "\u3008\u3009\u300a\u300b\u300c\u300d\u300e\u300f\u3010\u3011"
    # CJK brackets and symbols/punctuation
    "\u3014\u3015\u3016\u3017\u3018\u3019\u301a\u301b\u301c\u301d\u301e\u301f"
    # Other CJK symbols
    "\u3030"
    # Special CJK indicators
    "\u303e\u303f"
    # Dashes
    "\u2013\u2014"
    # Quotation marks and apostrophe
    "\u2018\u2019\u201b\u201c\u201d\u201e\u201f"
    # General punctuation
    "\u2026\u2027"
    # Overscores and underscores
    "\ufe4f"
    # Small form variants
    "\ufe51\ufe54"
    # Latin punctuation
    "\u00b7"
)

#: A string of Chinese stops.
stops = (
    "\uff0e"  # Fullwidth full stop
    "\uff01"  # Fullwidth exclamation mark
    "\uff1f"  # Fullwidth question mark
    "\uff61"  # Halfwidth ideographic full stop
    "\u3002"  # Ideographic full stop
)

#: A string containing all Chinese punctuation.
punctuation = non_stops + stops

# A sentence end is defined by a stop followed by zero or more
# container-closing marks (e.g. quotation or brackets).
_sentence_end = "[{stops}][」﹂”』’》）］｝〕〗〙〛〉】]*".format(stops=stops)

#: A regular expression pattern for a Chinese sentence. A sentence is defined
#: as a series of characters and non-stop punctuation marks followed by a stop
#: and zero or more container-closing punctuation marks (e.g. apostrophe or
# brackets).
sent = sentence = "[{characters}{radicals}{non_stops}]*{sentence_end}".format(
    characters=characters,
    radicals=radicals,
    non_stops=non_stops,
    sentence_end=_sentence_end,
)
