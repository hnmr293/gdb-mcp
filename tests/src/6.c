#include <stdio.h>
#include <stdlib.h>

int __attribute__((cdecl)) process_cdecl(int a, int b, int c) {
    return a + b * c;
}

int __attribute__((stdcall)) process_stdcall(int a, int b, int c) {
    return a * b + c;
}

typedef int (*func_cdecl)(int, int, int);
typedef int __attribute__((stdcall)) (*func_stdcall)(int, int, int);

void run_calculations() {
    func_cdecl funcs[4];
    
    funcs[0] = process_cdecl;
    funcs[1] = (func_cdecl)process_stdcall;
    funcs[2] = process_cdecl;
    funcs[3] = (func_cdecl)process_stdcall;
    
    int results[4];
    for (int i = 0; i < 4; i++) {
        results[i] = funcs[i](10, 20, 30);
        printf("Result %d: %d\n", i, results[i]);
    }
}

int main() {
    run_calculations();
    return 0;
}