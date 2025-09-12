import ahocorasick

A = ahocorasick.Automaton()
for idx, pat in enumerate(patterns):
    A.add_word(pat, (idx, pat))
A.make_automaton()

for end_index, (idx, pat) in A.iter(data):
    print(f"Found {pat} at {end_index - len(pat) + 1}")