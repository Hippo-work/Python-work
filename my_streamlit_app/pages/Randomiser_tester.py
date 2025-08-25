import streamlit as st
import numpy as np

st.title("LFSR Randomizer Tester 🎲")

def lfsr(seed, taps, n_bits):
    sr = seed.copy()
    out = []
    for _ in range(n_bits):
        new_bit = sum([sr[t] for t in taps]) % 2
        out.append(sr[-1])
        sr = [new_bit] + sr[:-1]
    return out

seed = [1, 0, 0, 1]
taps = [0, 3]
n_bits = st.slider("Number of bits", 10, 100, 32)

output = lfsr(seed, taps, n_bits)
st.write("Output bitstream:", output)
st.line_chart(output)