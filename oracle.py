#!/usr/bin/env python3
# Mod Math oracle - mirrors engine.js. Quotients come from Fraction rounding (trunc, floor) and a search for the Euclidean remainder, not the engine's integer tricks.
import json, re
from fractions import Fraction
from math import floor, trunc

LIM = 10**12
INT_ERR = "each entry must be a whole number from -1000000000000 to 1000000000000"
ZERO_ERR = "the divisor must not be zero"
RING_ERR = "the number of slots must be a whole number from 1 to 1000000000000"
MOD_ERR = "the modulus must be a whole number from 1 to 1000000000000"

def num(t, err=INT_ERR):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"-?[0-9]{1,13}", t): raise ValueError(err)
    v = int(t)
    if abs(v) > LIM: raise ValueError(err)
    return v

def times(k): return f"{k} " + ("time" if k == 1 else "times")

def sign(a, n):
    x = num(a); d = num(n)
    if d == 0: raise ValueError(ZERO_ERR)
    f = Fraction(x, d)
    q1 = trunc(f); q2 = floor(f)
    # Euclidean: the one quotient whose remainder lands in [0, |d|)
    q3 = next(q for q in (q2, q2 + 1) if 0 <= x - d * q < abs(d))
    r1, r2, r3 = x - d * q1, x - d * q2, x - d * q3
    out = (f"{x} divided by {d}: truncated division (quotient rounds toward zero) gives quotient {q1} and remainder {r1}, "
           f"floored division (quotient rounds down) gives {q2} and {r2}, and Euclidean division (remainder never negative) gives {q3} and {r3}.")
    return out + (" All three remainders agree." if r1 == r2 == r3 else " The remainders differ, so the choice of division matters for these numbers.")

def ring(slots, start, steps):
    n = num(slots, RING_ERR)
    if n < 1: raise ValueError(RING_ERR)
    s = num(start, f"the start must be a whole number from 0 to {n - 1}")
    if s < 0 or s >= n: raise ValueError(f"the start must be a whole number from 0 to {n - 1}")
    m = num(steps)
    t = s + m
    laps = floor(Fraction(t, n)); x = t - laps * n
    assert 0 <= x < n
    rng = "slot 0 only" if n == 1 else f"0 to {n - 1}"
    if laps == 0: wrap = " without wrapping."
    elif laps > 0: wrap = f", after wrapping past the end {times(laps)}."
    else: wrap = f", after wrapping past the start {times(-laps)}."
    unit = "step" if abs(m) == 1 else "steps"
    return f"On a ring of {n} {'slot' if n == 1 else 'slots'} ({rng}), starting at {s} and moving {m} {unit} lands on slot {x}{wrap}"

def match(a, b, n):
    x = num(a); y = num(b); m = num(n, MOD_ERR)
    if m < 1: raise ValueError(MOD_ERR)
    rx = x % m; ry = y % m; diff = x - y
    head = f"{x} and {y} mod {m}: "
    if rx == ry:
        assert diff % m == 0
        return head + f"both leave {rx} (never negative), so they land on the same slot. Their difference {diff} is {diff // m} x {m}."
    assert diff % m != 0
    return head + f"{rx} and {ry} (never negative), so they land on different slots. Their difference {diff} is not a multiple of {m}."

FNS = {"signTruth": sign, "ringTruth": ring, "matchTruth": match}
CASES = [
    ("signTruth", ["-7", "3"]), ("signTruth", ["7", "3"]), ("signTruth", ["7", "-3"]), ("signTruth", ["-7", "-3"]), ("signTruth", ["6", "3"]),
    ("signTruth", ["-6", "3"]), ("signTruth", ["0", "5"]), ("signTruth", ["0", "-5"]), ("signTruth", ["2", "5"]), ("signTruth", ["-2", "5"]),
    ("signTruth", ["2", "-5"]), ("signTruth", ["-2", "-5"]), ("signTruth", ["5", "1"]), ("signTruth", ["-5", "1"]), ("signTruth", ["-5", "-1"]),
    ("signTruth", ["1000000000000", "7"]), ("signTruth", ["-1000000000000", "7"]), ("signTruth", ["-1000000000000", "-1000000000000"]), ("signTruth", ["1", "1000000000000"]), ("signTruth", ["-1", "1000000000000"]),
    ("signTruth", [" -7 ", " 3 "]), ("signTruth", ["-0", "3"]), ("signTruth", ["007", "3"]), ("signTruth", ["7", "0"]), ("signTruth", ["x", "3"]),
    ("signTruth", ["7", ""]), ("signTruth", ["1.5", "3"]), ("signTruth", ["1000000000001", "3"]), ("signTruth", ["7", "-1000000000001"]), ("signTruth", ["+7", "3"]),
    ("ringTruth", ["12", "9", "7"]), ("ringTruth", ["12", "9", "3"]), ("ringTruth", ["12", "9", "2"]), ("ringTruth", ["12", "0", "-1"]), ("ringTruth", ["12", "0", "1"]),
    ("ringTruth", ["12", "3", "0"]), ("ringTruth", ["12", "3", "-3"]), ("ringTruth", ["12", "3", "-4"]), ("ringTruth", ["12", "3", "-15"]), ("ringTruth", ["12", "3", "-27"]),
    ("ringTruth", ["12", "11", "13"]), ("ringTruth", ["12", "11", "1"]), ("ringTruth", ["12", "5", "24"]), ("ringTruth", ["12", "5", "-24"]), ("ringTruth", ["1", "0", "5"]),
    ("ringTruth", ["1", "0", "0"]), ("ringTruth", ["1", "0", "-1"]), ("ringTruth", ["7", "6", "1"]), ("ringTruth", ["7", "6", "-1"]), ("ringTruth", ["10", "0", "-10"]),
    ("ringTruth", ["1000000000000", "999999999999", "1000000000000"]), ("ringTruth", ["3", "1", "-1000000000000"]), ("ringTruth", [" 12 ", " 9 ", " 7 "]), ("ringTruth", ["0", "0", "1"]), ("ringTruth", ["12", "12", "1"]),
    ("ringTruth", ["12", "-1", "1"]), ("ringTruth", ["-3", "0", "1"]), ("ringTruth", ["12", "x", "1"]), ("ringTruth", ["12", "9", ""]), ("ringTruth", ["1000000000001", "0", "1"]),
    ("matchTruth", ["17", "5", "6"]), ("matchTruth", ["17", "4", "6"]), ("matchTruth", ["-1", "5", "6"]), ("matchTruth", ["-7", "2", "3"]), ("matchTruth", ["-7", "-1", "3"]),
    ("matchTruth", ["0", "0", "1"]), ("matchTruth", ["5", "5", "9"]), ("matchTruth", ["5", "-5", "10"]), ("matchTruth", ["5", "-5", "7"]), ("matchTruth", ["100", "0", "10"]),
    ("matchTruth", ["0", "100", "10"]), ("matchTruth", ["1", "2", "1"]), ("matchTruth", ["-3", "3", "6"]), ("matchTruth", ["1000000000000", "-1000000000000", "7"]), ("matchTruth", ["999999999999", "-1", "1000000000000"]),
    ("matchTruth", [" 17 ", " 5 ", " 6 "]), ("matchTruth", ["17", "5", "0"]), ("matchTruth", ["17", "5", "-6"]), ("matchTruth", ["x", "5", "6"]), ("matchTruth", ["17", "", "6"]),
    ("matchTruth", ["17", "5", "1000000000001"]),
]
out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
