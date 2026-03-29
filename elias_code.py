#!/usr/bin/env python3
"""elias_code - Elias gamma and delta universal integer codes."""
import sys

def gamma_encode(n):
    if n < 1: raise ValueError("n must be >= 1")
    binary = bin(n)[2:]
    return "0" * (len(binary) - 1) + binary

def gamma_decode(bits):
    zeros = 0
    while bits[zeros] == "0": zeros += 1
    val = int(bits[zeros:zeros + zeros + 1], 2)
    return val, 2 * zeros + 1

def delta_encode(n):
    if n < 1: raise ValueError("n must be >= 1")
    binary = bin(n)[2:]
    length = len(binary)
    return gamma_encode(length) + binary[1:]

def delta_decode(bits):
    length, consumed = gamma_decode(bits)
    val = int("1" + bits[consumed:consumed + length - 1], 2)
    return val, consumed + length - 1

def encode_sequence(nums):
    return "".join(gamma_encode(n) for n in nums)

def decode_sequence(bits, count):
    result = []
    pos = 0
    for _ in range(count):
        val, consumed = gamma_decode(bits[pos:])
        result.append(val)
        pos += consumed
    return result

def test():
    assert gamma_encode(1) == "1"
    assert gamma_encode(2) == "010"
    assert gamma_encode(3) == "011"
    assert gamma_encode(4) == "00100"
    v, c = gamma_decode("00100")
    assert v == 4 and c == 5
    for n in [1, 5, 10, 100, 1000]:
        bits = gamma_encode(n)
        val, _ = gamma_decode(bits)
        assert val == n
    for n in [1, 5, 10, 100, 1000]:
        bits = delta_encode(n)
        val, _ = delta_decode(bits)
        assert val == n
    seq = encode_sequence([3, 7, 1, 15])
    assert decode_sequence(seq, 4) == [3, 7, 1, 15]
    print("elias_code: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: elias_code.py --test")
