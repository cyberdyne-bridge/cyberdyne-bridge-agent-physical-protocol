#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal RFC 8785 (JCS) serializer.

Only JSON data types are accepted.  Object keys are sorted by UTF-16 code
units, arrays preserve order, strings use JSON escaping, and finite numbers use
the ECMAScript JSON number formatting required by JCS.

This module is intentionally dependency-free so the PoC can run as a Gist.
"""
from __future__ import annotations

import json
import math
from decimal import Decimal

__all__ = ["dumps"]


def _number(value: int | float) -> str:
    if isinstance(value, bool):
        raise TypeError("bool is not a number")
    if isinstance(value, int):
        if abs(value) > 9007199254740991:
            # JSON numbers are IEEE-754 doubles in JCS.  Large Python ints
            # must be converted through the same representation.
            value = float(value)
        else:
            return str(value)
    if not isinstance(value, float):
        raise TypeError(f"unsupported number type: {type(value).__name__}")
    if not math.isfinite(value):
        raise ValueError("JCS does not permit NaN or Infinity")
    if value == 0:
        return "0"

    sign = "-" if value < 0 else ""
    d = Decimal(repr(abs(value)))
    digits = "".join(str(x) for x in d.as_tuple().digits)
    exp = d.as_tuple().exponent

    # Remove trailing zeros from the coefficient while preserving the value.
    while len(digits) > 1 and digits.endswith("0"):
        digits = digits[:-1]
        exp += 1

    first_exp = exp + len(digits) - 1

    # ECMAScript uses fixed notation for 1e-6 <= |x| < 1e21.
    if -6 <= first_exp < 21:
        point = first_exp + 1
        if point <= 0:
            out = "0." + ("0" * -point) + digits
        elif point >= len(digits):
            out = digits + ("0" * (point - len(digits)))
        else:
            out = digits[:point] + "." + digits[point:]
        if "." in out:
            out = out.rstrip("0").rstrip(".")
        return sign + out

    coeff = digits[0]
    if len(digits) > 1:
        coeff += "." + digits[1:]
    e = f"+{first_exp}" if first_exp >= 0 else str(first_exp)
    return f"{sign}{coeff}e{e}"


def _string(value: str) -> str:
    # json.dumps with ensure_ascii=False matches ECMAScript JSON string
    # escaping for the characters used by MCP definitions (quotes, slash,
    # controls, Unicode).  Do not allow lone surrogates into UTF-8 output.
    return json.dumps(value, ensure_ascii=False)


def _write(value, out: list[str]) -> None:
    if value is None:
        out.append("null")
    elif value is True:
        out.append("true")
    elif value is False:
        out.append("false")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        out.append(_number(value))
    elif isinstance(value, str):
        out.append(_string(value))
    elif isinstance(value, (list, tuple)):
        out.append("[")
        for i, item in enumerate(value):
            if i:
                out.append(",")
            _write(item, out)
        out.append("]")
    elif isinstance(value, dict):
        out.append("{")
        keys = sorted(value, key=lambda k: k.encode("utf-16-be") if isinstance(k, str) else b"")
        for i, key in enumerate(keys):
            if not isinstance(key, str):
                raise TypeError("JSON object keys must be strings")
            if i:
                out.append(",")
            out.append(_string(key))
            out.append(":")
            _write(value[key], out)
        out.append("}")
    else:
        raise TypeError(f"unsupported JSON type: {type(value).__name__}")


def dumps(value) -> str:
    out: list[str] = []
    _write(value, out)
    return "".join(out)
