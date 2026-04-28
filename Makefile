CXX = g++
CXXFLAGS = -O3 -std=c++11 -Wall -fopenmp
LDFLAGS = -fopenmp
RM = rm -f

SRC = src/mandelbrot_block_malloc.cpp
OBJ = bench/mandelbrot_block_malloc.o
EXEC = bench/mandelbrot_block_malloc

all: bench $(EXEC)

$(EXEC): $(OBJ)
	$(CXX) $(CXXFLAGS) $(OBJ) -o $(EXEC) $(LDFLAGS)

$(OBJ): $(SRC)
	$(CXX) $(CXXFLAGS) -c $(SRC) -o $(OBJ)

bench:
	mkdir -p bench

clean:
	$(RM) bench/*.o bench/mandelbrot_block_malloc