import random

def theoretical_probability(pattern: str, p: float = 0.5) -> float:
    """Calculate theoretical probability of a binary pattern assuming i.i.d. Bernoulli trials."""
    theo_prob = 1.0
    for bit in pattern:
        theo_prob *= p if bit == '1' else (1 - p)
    return theo_prob

def count_pattern_occurrences(stream: str, pattern: str) -> int:
    """Count overlapping occurrences of a pattern in a binary stream."""
    count = 0
    for i in range(len(stream) - len(pattern) + 1):
        if stream[i:i+len(pattern)] == pattern:
            count += 1
    return count

def simulate_stream(length: int, p: float = 0.5) -> str:
    """Generate a random binary stream of given length."""
    return ''.join(random.choices(['0', '1'], weights=[1 - p, p], k=length))

def run_simulation(pattern: str, stream_length: int, trials: int = 1000, p: float = 0.5):
    """Run multiple simulations and compare empirical vs theoretical probability."""
    theoretical = theoretical_probability(pattern, p)
    expected_count = (stream_length - len(pattern) + 1) * theoretical

    total_occurrences = 0
    for _ in range(trials):
        stream = simulate_stream(stream_length, p)
        total_occurrences += count_pattern_occurrences(stream, pattern)

    empirical_prob = total_occurrences / (trials * (stream_length - len(pattern) + 1))

    print(f"Pattern: {pattern}")
    print(f"Theoretical Probability: {theoretical:.6f}")
    print(f"Expected Count per Stream: {expected_count:.2f}")
    print(f"Empirical Probability (avg over {trials} trials): {empirical_prob:.6f}")
    print(f"Total Occurrences: {total_occurrences}")
    return empirical_prob, theoretical

# Example usage
pattern='101'
empirical_prob, theoretical = run_simulation(pattern, stream_length=100, trials=1000, p=0.5)

import matplotlib.pyplot as plt

def plot_results(pattern, theoretical_prob, empirical_probs):
    trials = list(range(1, len(empirical_probs) + 1))
    
    plt.figure(figsize=(10, 6))
    plt.plot(trials, empirical_probs, label='Empirical Probability', color='blue')
    plt.axhline(y=theoretical_prob, color='red', linestyle='--', label='Theoretical Probability')
    
    plt.title(f"Convergence of Empirical Probability for Pattern '{pattern}'")
    plt.xlabel("Trial")
    plt.ylabel("Probability")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_results(pattern, theoretical, empirical_prob)