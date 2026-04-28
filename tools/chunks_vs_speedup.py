import csv
import matplotlib.pyplot as plt
import os
import sys

csv_path = 'data/chunks_dynamic.csv'
serial_path = 'data/serial_time.txt'

if not os.path.exists(csv_path):
    print(f"CSV file not found: {csv_path}")
    sys.exit(1)

if not os.path.exists(serial_path):
    print(f"Serial time file not found: {serial_path}. Run scripts/run_chunks.sh first.")
    sys.exit(1)

with open(serial_path) as f:
    serial_time = float(f.read().strip())

chunks = []
times = []
with open(csv_path) as f:
    reader = csv.DictReader(f)
    for r in reader:
        chunks.append(int(r['chunk']))
        times.append(float(r['median_time']))

speedup = [serial_time / t for t in times]

plt.figure(figsize=(8,5))
plt.plot(chunks, speedup, marker='o')
plt.xscale('log', base=2)
plt.xlabel('Chunk size')
plt.ylabel('Speedup (vs 1 thread)')
plt.title('Chunk size vs Speedup (schedule=dynamic)')
plt.grid(True, which='both', ls='--')

out_dir = 'plots'
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'chunks_vs_speedup.png')
plt.tight_layout()
plt.savefig(out_path, dpi=200)
print(f"Saved plot to {out_path}")
plt.show()