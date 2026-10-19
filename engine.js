// Mod Math engine: exact remainder and modulo arithmetic on BigInt integers.
var LIM = 1000000000000n;
var INT_ERR = "each entry must be a whole number from -1000000000000 to 1000000000000";
var ZERO_ERR = "the divisor must not be zero";
var RING_ERR = "the number of slots must be a whole number from 1 to 1000000000000";
var MOD_ERR = "the modulus must be a whole number from 1 to 1000000000000";

function _int(t, err) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^-?[0-9]{1,13}$/.test(t)) throw new Error(err || INT_ERR);
  var v = BigInt(t);
  if (v > LIM || v < -LIM) throw new Error(err || INT_ERR);
  return v;
}
function _floorDiv(a, b) {
  var q = a / b;
  if (a % b !== 0n && (a < 0n) !== (b < 0n)) q -= 1n;
  return q;
}
function _times(k) { return k + (k === 1n ? " time" : " times"); }

// The sign truth: one division, three ways to round the quotient.
function signTruth(a, n) {
  var x = _int(a), d = _int(n);
  if (d === 0n) throw new Error(ZERO_ERR);
  var q1 = x / d, r1 = x - d * q1;
  var q2 = _floorDiv(x, d), r2 = x - d * q2;
  var q3 = d > 0n ? q2 : -_floorDiv(x, -d), r3 = x - d * q3;
  var out = x + " divided by " + d + ": truncated division (quotient rounds toward zero) gives quotient " + q1 + " and remainder " + r1 +
    ", floored division (quotient rounds down) gives " + q2 + " and " + r2 + ", and Euclidean division (remainder never negative) gives " + q3 + " and " + r3 + ".";
  return out + (r1 === r2 && r2 === r3 ? " All three remainders agree." : " The remainders differ, so the choice of division matters for these numbers.");
}

// The ring truth: moving around a ring of slots numbered from 0.
function ringTruth(slots, start, steps) {
  var n = _int(slots, RING_ERR);
  if (n < 1n) throw new Error(RING_ERR);
  var s = _int(start, "the start must be a whole number from 0 to " + (n - 1n));
  if (s < 0n || s >= n) throw new Error("the start must be a whole number from 0 to " + (n - 1n));
  var m = _int(steps);
  var t = s + m, laps = _floorDiv(t, n), x = t - laps * n;
  var range = n === 1n ? "slot 0 only" : "0 to " + (n - 1n);
  var wrap = laps === 0n ? " without wrapping." : laps > 0n ? ", after wrapping past the end " + _times(laps) + "." : ", after wrapping past the start " + _times(-laps) + ".";
  var unit = (m === 1n || m === -1n) ? " step" : " steps";
  return "On a ring of " + n + (n === 1n ? " slot" : " slots") + " (" + range + "), starting at " + s + " and moving " + m + unit + " lands on slot " + x + wrap;
}

// The match truth: do two numbers land on the same slot of a ring.
function matchTruth(a, b, n) {
  var x = _int(a), y = _int(b), m = _int(n, MOD_ERR);
  if (m < 1n) throw new Error(MOD_ERR);
  var rx = x - m * _floorDiv(x, m), ry = y - m * _floorDiv(y, m), diff = x - y;
  var head = x + " and " + y + " mod " + m + ": ";
  if (rx === ry) return head + "both leave " + rx + " (never negative), so they land on the same slot. Their difference " + diff + " is " + (diff / m) + " x " + m + ".";
  return head + rx + " and " + ry + " (never negative), so they land on different slots. Their difference " + diff + " is not a multiple of " + m + ".";
}
