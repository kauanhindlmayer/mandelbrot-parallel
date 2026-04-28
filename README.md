# Mandelbrot OpenMP Benchmark

## Configuração de Hardware

OS: Arch Linux x86_64
Host: Windows Subsystem for Linux - archlinux (2.6.1.0)
Kernel: Linux 6.6.87.2-microsoft-standard-WSL2
Uptime: 3 mins
Packages: 232 (pacman)
Shell: zsh 5.9
WM: WSLg 1.0.66 (Wayland)
Terminal: Windows Terminal
CPU: AMD Ryzen 7 9800X3D (16) @ 4.70 GHz
GPU 1: NVIDIA GeForce RTX 5070 Ti @ 3.09 GHz (15.62 GiB) [Discrete]
GPU 2: AMD Radeon(TM) Graphics (485.77 MiB) [Integrated]
Memory: 1.69 GiB / 15.21 GiB (11%)
Swap: 0 B / 4.00 GiB (0%)
Disk (/): 24.24 GiB / 1006.85 GiB (2%) - ext4

## Carga de Trabalho

```c
int max_row = 3300;
int max_column = 790;
int max_n = 2400;
```

## Como Compilar

```bash
$ make clean
$ make
$ for t in 1 2 4 6 8 10 12 14 16; do export OMP_NUM_THREADS=$t; echo -n "$t threads: "; bench/mandelbrot_block_malloc; done
```

## Resultado

Tabela com tempos e acelerações (Speedup = tempo(1 thread) / tempo(N)) por política de escalonamento. Valores em segundos; speedups arredondados a 3 casas.

| Threads | Static (s) | Static Speedup | Dynamic (s) | Dynamic Speedup | Guided (s) | Guided Speedup | Observação                                    |
| ------: | ---------: | -------------: | ----------: | --------------: | ---------: | -------------: | --------------------------------------------- |
|       1 |     30.361 |          1.000 |     30.4999 |           1.000 |    30.1888 |          1.000 | base                                          |
|       2 |    15.3669 |          1.976 |     15.3654 |           1.986 |     15.209 |          1.986 |                                               |
|       4 |    12.7741 |          2.376 |     7.81323 |           3.904 |    9.08753 |          3.323 |                                               |
|       6 |    9.65894 |          3.144 |     5.23152 |           5.831 |    6.35357 |          4.753 |                                               |
|       8 |    7.85828 |          3.865 |     3.94768 |           7.728 |     4.7565 |          6.345 |                                               |
|      10 |     6.4655 |          4.696 |     3.21844 |           9.478 |    3.80683 |          7.934 |                                               |
|      12 |    5.44194 |          5.579 |     2.68715 |          11.353 |    3.19327 |          9.457 |                                               |
|      14 |    4.73802 |          6.409 |     2.33589 |          13.060 |    2.81699 |         10.720 |                                               |
|      16 |    4.18095 |          7.264 |     2.19076 |          13.929 |    2.52801 |         11.942 | Dynamic apresenta maior aceleração neste caso |

Observação: os speedups foram calculados usando o tempo de 1 thread da mesma estratégia (por exemplo, speedup static = tempo_static(1) / tempo_static(N)). Valores arredondados; para reprodutibilidade use os scripts em `scripts/` e `tools/`.

### Plots

O gráfico "Aceleração vs Número de Threads" foi gerado manualmente a partir dos tempos registrados na seção **Resultado**. O gráfico "Tamanho do Chunk vs Aceleração" pode ser reproduzido automaticamente usando o script abaixo, ele executa a varredura de chunks e grava `data/chunks_dynamic.csv` e `data/serial_time.txt`.

```bash
chmod +x scripts/run_chunks.sh
./scripts/run_chunks.sh 16 5 bench/mandelbrot_block_malloc
```

Para gerar o gráfico "Tamanho do Chunk vs Aceleração":

```bash
python tools/chunks_vs_speedup.py
```

Para gerar o gráfico "Aceleração vs Número de Threads" automaticamente a partir dos dados disponíveis:

```bash
python tools/num_of_threads_vs_speedup.py
```
