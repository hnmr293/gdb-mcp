#include <stdio.h>
#include <stdlib.h>
#include <immintrin.h>

void compute_averages(float* data, int size) {
    float* results = malloc(size * sizeof(float));
    
    for (int i = 0; i < size - 3; i++) {
        __m128 values = _mm_load_ps(&data[i]);
        __m128 sum = _mm_hadd_ps(values, values);
        sum = _mm_hadd_ps(sum, sum);
        _mm_store_ss(&results[i], sum);
        results[i] /= 4.0f;
    }
    
    printf("Moving averages:\n");
    for (int i = 0; i < size - 3; i++) {
        printf("Position %d: %.2f\n", i, results[i]);
    }
    
    free(results);
}

int main() {
    float* data = malloc(17 * sizeof(float));
    for (int i = 0; i < 17; i++) {
        data[i] = (float)(i * 2 + 1);
    }
    
    compute_averages(data + 1, 16);
    
    free(data);
    return 0;
}