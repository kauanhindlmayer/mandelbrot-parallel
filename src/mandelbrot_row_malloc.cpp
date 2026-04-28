#include <complex>
#include <iostream>
#include <omp.h>

using namespace std;

int main(){
    int max_row = 3300, max_column = 790, max_n = 2400;
    // cin >> max_row;
    // cin >> max_column;
    // cin >> max_n;

    char **mat = (char**)malloc(sizeof(char*)*max_row);

    for (int i=0; i<max_row;i++)
        mat[i]=(char*)malloc(sizeof(char)*max_column);

    double start_time = omp_get_wtime();
    #pragma omp parallel for collapse(2) schedule(static) // 12.82942
    // #pragma omp parallel for collapse(2) schedule(dynamic, 10) // 6.869133
    // #pragma omp parallel for collapse(2) schedule (guided) // 8.338723
    for(int r = 0; r < max_row; ++r){
        for(int c = 0; c < max_column; ++c){
            complex<float> z;
            int n = 0;
            while(abs(z) < 2 && ++n < max_n)
                z = pow(z, 2) + decltype(z)(
                    (float)c * 2 / max_column - 1.5,
                    (float)r * 2 / max_row - 1
                );
            mat[r][c]=(n == max_n ? '#' : '.');
        }
    }

    double end_time = omp_get_wtime();
    std::cout << end_time - start_time;
    cout << '\n'; 

    // for(int r = 0; r < max_row; ++r){
    //  for(int c = 0; c < max_column; ++c)
    //      std::cout << mat[r][c];
    //  cout << '\n';
    // } 
}
