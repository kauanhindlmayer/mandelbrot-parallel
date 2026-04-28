#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/run_chunks.sh [threads] [reps] [program]
# Default threads: $(nproc), reps: 5, program: bench/mandelbrot_block_malloc

threads=${1:-$(nproc)}
reps=${2:-5}
prog=${3:-bench/mandelbrot_block_malloc}
out_csv=${4:-data/chunks_dynamic.csv}

chunks=(1 2 4 8 16 32 64 128)

echo "Running dynamic schedule benchmark: threads=$threads reps=$reps prog=$prog"

if [ ! -x "$prog" ]; then
  echo "Program $prog not found or not executable" >&2
  exit 1
fi

# Measure serial baseline (1 thread)
export OMP_NUM_THREADS=1
export OMP_SCHEDULE="dynamic,1"
echo "Measuring serial baseline (1 thread) x $reps reps..."
serial_times=()
for i in $(seq 1 $reps); do
  t=$($prog)
  serial_times+=("$t")
done
serial_median=$(printf "%s\n" "${serial_times[@]}" | python3 -c 'import sys,statistics;print(statistics.median([float(x.strip()) for x in sys.stdin]))')
mkdir -p data
printf "%s\n" "$serial_median" > data/serial_time.txt
echo "Serial median time: $serial_median"

mkdir -p data
echo "chunk,median_time,threads,reps,raw_times" > "$out_csv"

for chunk in "${chunks[@]}"; do
  export OMP_NUM_THREADS=$threads
  export OMP_SCHEDULE="dynamic,$chunk"
  echo "Running chunk=$chunk..."
  times=()
  for i in $(seq 1 $reps); do
    t=$($prog)
    times+=("$t")
  done
  median=$(printf "%s\n" "${times[@]}" | python3 -c 'import sys,statistics;print(statistics.median([float(x.strip()) for x in sys.stdin]))')
  # join raw times with semicolon
  raw=$(IFS=';'; echo "${times[*]}")
  echo "$chunk,$median,$threads,$reps,\"$raw\"" >> "$out_csv"
done

echo "Results written to $out_csv and data/serial_time.txt"
