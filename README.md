# Mod Math

Remainder and modulo arithmetic. -7 divided by 3 leaves -1 or 2, depending on whether the quotient rounds toward zero or down.

## What it computes

- **The sign truth** - one division shown three ways: truncated (quotient rounds toward zero), floored (quotient rounds down) and Euclidean (remainder never negative), with quotient and remainder for each.
- **The ring truth** - start on a ring of slots numbered from 0, move any number of steps forward or back, and see the landing slot and how many times it wrapped.
- **The match truth** - whether two numbers land on the same slot of a ring, with their never-negative remainders and their difference.

Entries are whole numbers from -1000000000000 to 1000000000000 (ring sizes and moduli from 1).

## Boundary

Arithmetic only, on whole numbers. It does not know how any real language, database or chip rounds a division, and gives no verdict on which kind of remainder your code should use. Every figure is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (BigInt integer division with explicit rounding).
- `oracle.py` - the Python mirror (Fraction rounding and a search for the Euclidean quotient) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (81 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/modmath/
Repo: https://github.com/iLanis-agent/modmath
