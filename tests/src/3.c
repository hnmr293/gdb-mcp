#include <stdio.h>
#include <stdlib.h>

void analyze_data(int* samples, int size) {
    int histogram[10] = {0};
    int ranges[] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
    
    for (int i = 0; i < size; i++) {
        int index = 0;
        while (samples[i] > ranges[index]) {
            index++;
        }
        histogram[index]++;
    }
    
    printf("Distribution:\n");
    for (int i = 0; i < 10; i++) {
        printf("[%d-%d]: %d samples\n", 
               i == 0 ? 0 : ranges[i-1], 
               ranges[i], 
               histogram[i]);
    }
}

int main() {
    int test_data[] = {5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 100};
    int size = sizeof(test_data) / sizeof(test_data[0]);
    
    analyze_data(test_data, size);
    return 0;
}