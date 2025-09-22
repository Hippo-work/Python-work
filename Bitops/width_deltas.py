import numpy as np
import matplotlib.pyplot as plt
from statistics import median
#check if the patterns are periodic, clustered or random

pattern_indices = np.random.randint(0, 1000, size=500)
pattern = [470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600]

pattern_indices[50:64] = pattern
pattern_indices[150:164] = pattern
pattern_indices[250:264] = pattern
pattern_indices[350:364] = pattern
pattern_indices[450:464] = pattern
deltas = np.diff(pattern_indices)
# injecting a periodic pattern for testing

mean_delta = np.mean(deltas)
std_delta = np.std(deltas)
coefficient_of_variation = std_delta / mean_delta if mean_delta != 0 else float('inf')

print(coefficient_of_variation)
if -0.5 <coefficient_of_variation < 0.5:
    print("Patterns are likely periodic.")
elif 0.5 <= coefficient_of_variation < 1.0:
    print("Patterns are likely clustered.")
else:
    print("Patterns are likely random.")


from scipy.signal import find_peaks

peaks, _ = find_peaks(deltas, distance=1)
print("Peaks in delta spacing:", peaks)


acf = np.correlate(deltas - np.mean(deltas), deltas - np.mean(deltas), mode='full')
acf = acf[acf.size // 2:]
plt.plot(acf)
plt.title("Autocorrelation of Deltas")
plt.show()

from scipy.stats import entropy

hist, _ = np.histogram(deltas, bins='auto', density=True)
delta_entropy = entropy(hist)
print("Delta Entropy:", delta_entropy)

mean_delta = np.mean(deltas)
median_delta = median(deltas)

print(mean_delta) #closer mean is to 0, the more random i think
print(median_delta) #good at eliminating outliers and finding the frame width / patterns in the delta


#looks like entropy < 2 seems to be a reasonable measure
#the coefficent of variant seems odd
#find peaks i dont quite know how to interpret it
#auto correlation is the same
pat = [1,0,1,1,0,0,1]
print(f"pattern {np.array(pat)}")
print(f"flipped?: {1-np.array(pat)}")

