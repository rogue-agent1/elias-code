#!/usr/bin/env python3
"""Elias gamma and delta coding for positive integers."""

def elias_gamma_encode(n: int) -> str:
    if n < 1: raise ValueError("Must be positive")
    bits = bin(n)[2:]
    return "0" * (len(bits) - 1) + bits

def elias_gamma_decode(s: str) -> tuple:
    i = 0
    while i < len(s) and s[i] == "0":
        i += 1
    length = i + 1
    if i + length > len(s):
        raise ValueError("Invalid encoding")
    val = int(s[i:i + length], 2)
    return val, s[i + length:]

def elias_delta_encode(n: int) -> str:
    if n < 1: raise ValueError("Must be positive")
    bits = bin(n)[2:]
    L = len(bits) - 1
    return elias_gamma_encode(L + 1) + bits[1:]

def elias_delta_decode(s: str) -> tuple:
    L_plus_1, rest = elias_gamma_decode(s)
    L = L_plus_1 - 1
    if len(rest) < L:
        raise ValueError("Invalid encoding")
    val = int("1" + rest[:L], 2)
    return val, rest[L:]

def encode_sequence(nums: list, method: str = "gamma") -> str:
    enc = elias_gamma_encode if method == "gamma" else elias_delta_encode
    return "".join(enc(n) for n in nums)

def decode_sequence(s: str, count: int, method: str = "gamma") -> list:
    dec = elias_gamma_decode if method == "gamma" else elias_delta_decode
    result = []
    rest = s
    for _ in range(count):
        val, rest = dec(rest)
        result.append(val)
    return result

def test():
    # Gamma
    assert elias_gamma_encode(1) == "1"
    assert elias_gamma_encode(2) == "010"
    assert elias_gamma_encode(5) == "00101"
    v, r = elias_gamma_decode("010")
    assert v == 2 and r == ""
    # Delta
    assert elias_delta_encode(1) == "1"
    v2, r2 = elias_delta_decode(elias_delta_encode(10))
    assert v2 == 10
    # Sequence
    nums = [1, 3, 7, 15, 100]
    for method in ["gamma", "delta"]:
        encoded = encode_sequence(nums, method)
        decoded = decode_sequence(encoded, len(nums), method)
        assert decoded == nums, f"{method}: {decoded} != {nums}"
    print("  elias_code: ALL TESTS PASSED")

if __name__ == "__main__":
    test()
