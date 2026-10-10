"""Exact quotient of the published host; twin positions are stored by weight.

Zero-based nodes; row and column order are separate. No third alphabet symbol.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    kind: str
    depth: int = -1
    sign: str = ""
    node: int = -1
    mode: tuple = ()
    group: int = -1
    weight: int = 1


def modes(h):
    return [(kind, i, sign, parity)
            for i in range(1, h + 1)
            for kind, sign, parity in [("V", "+", -1), ("V", "-", -1),
                                      ("W", "+", 0), ("W", "+", 1),
                                      ("W", "-", 0), ("W", "-", 1)]]


def variables(h, axis):
    def visit(i, p):
        if i == h:
            return [Position("variable", i, "L", p, weight=1)]
        before, after = ("-", "+") if axis == "row" else ("+", "-")
        weight = 2 ** (h - i)
        return ([Position("variable", i, before, p, weight=weight)]
                + visit(i + 1, 2 * p) + visit(i + 1, 2 * p + 1)
                + [Position("variable", i, after, p, weight=weight)])
    return visit(0, 0)


def nonanchors(h, axis):
    dummy = Position("dummy", weight=2 ** h)
    vs = variables(h, axis)
    return vs + [dummy] if axis == "row" else [dummy] + vs


def anchor(s=13, bits=3):
    assert s >= 2 ** bits
    return [[((u - (s - 2 ** bits)) >> (s - 1 - v)) & 1
             if u >= s - 2 ** bits and v >= s - bits else int(u != v)
             for v in range(s)] for u in range(s)]


def in_sign(x, sign):
    return x.sign in (sign, "L")


def role(x, mode, axis):
    kind, i, sign, parity = mode
    if kind == "V":
        if axis == "column":
            if x.kind == "dummy":
                return 1
            return 2 if x.depth == i - 1 and in_sign(x, sign) else 0
        if x.kind != "variable" or not in_sign(x, sign):
            return 0
        if sign == "+":
            return 1 if x.depth == i else 2 if x.depth == i - 1 else 0
        return 1 if x.depth == i - 1 else 2 if x.depth == i else 0
    if axis == "row":
        if x.kind == "dummy":
            return 2
        return 1 if x.depth == i and in_sign(x, sign) and x.node % 2 == parity else 0
    if x.kind != "variable" or not in_sign(x, sign):
        return 0
    child = x.depth == i and x.node % 2 == parity
    parent = x.depth == i - 1
    if sign == "+":
        return 1 if parent else 2 if child else 0
    return 1 if child else 2 if parent else 0


def nonanchor_entry(r, c):
    if r.kind == "dummy" or c.kind == "dummy":
        return 1
    if r.depth == c.depth:
        if r.sign in ("+", "L") and c.sign in ("+", "L"):
            return int(r.node <= c.node)
        if r.sign == c.sign == "-":
            return int(r.node < c.node)
    if r.depth == c.depth + 1:
        if in_sign(r, "+") and c.sign == "+":
            return int(r.node // 2 <= c.node)
        if in_sign(r, "-") and c.sign == "-":
            return int(r.node // 2 < c.node)
    return 0


def full_axis(h, s, axis):
    anchors = [Position("anchor", mode=t, group=u, weight=2 ** h)
               for t in modes(h) for u in range(s)]
    return anchors + nonanchors(h, axis)


def entry(r, c, S):
    if r.kind == c.kind == "anchor":
        return S[r.group][c.group] if r.mode == c.mode else 0
    if r.kind == "anchor":
        return int(role(c, r.mode, "column") == r.group + 1)
    if c.kind == "anchor":
        return int(role(r, c.mode, "row") == c.group + 1)
    return nonanchor_entry(r, c)
