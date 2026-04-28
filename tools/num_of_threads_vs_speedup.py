import matplotlib.pyplot as plt
import os

threads = [1, 2, 4, 6, 8, 10, 12, 14, 16]

# Execution times (from README.md)
static = [
    30.361, 15.3669, 12.7741, 9.65894, 7.85828,
    6.4655, 5.44194, 4.73802, 4.18095
]

dynamic = [
    30.4999, 15.3654, 7.81323, 5.23152, 3.94768,
    3.21844, 2.68715, 2.33589, 2.19076
]

guided = [
    30.1888, 15.209, 9.08753, 6.35357, 4.7565,
    3.80683, 3.19327, 2.81699, 2.52801
]

# Speedup function
def speedup(times):
    base = times[0]
    return [base / t for t in times]

plt.figure(figsize=(9,5))

plt.plot(threads, speedup(static), marker='o', label='static')
plt.plot(threads, speedup(dynamic), marker='o', label='dynamic')
plt.plot(threads, speedup(guided), marker='o', label='guided')

# Ideal linear speedup reference
plt.plot(threads, threads, '--', color='gray', label='ideal linear')

plt.xlabel("Number of Threads")
plt.ylabel("Speedup")
plt.title("Speedup vs Number of Threads (Mandelbrot OpenMP)")

plt.grid(True)
plt.legend()
plt.tight_layout()

out_dir = 'plots'
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'num_of_threads_vs_speedup.png')
plt.savefig(out_path)
print(f"Saved plot to {out_path}")
