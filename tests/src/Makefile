all: a1 a2 a3 a4 a5 a6 a7

run: ../1 ../2 ../3 ../4 ../5 ../6 ../7
	@echo "=== 1 ==="
	@-../1
	@echo "=== 2 ==="
	@-../2
	@echo "=== 3 ==="
	@-../3
	@echo "=== 4 ==="
	@-../4
	@echo "=== 5 ==="
	@-../5
	@echo "=== 6 ==="
	@-../6
	@echo "=== 7 ==="
	@-../7

OPT := -O2 -s
CFLAGS := -Wall -Wextra -Werror -std=c11

a1:
	gcc $(OPT) $(CFLAGS) 1.c -o ../1

a2:
	gcc $(OPT) $(CFLAGS) 2.c -o ../2

a3:
	gcc $(OPT) $(CFLAGS) 3.c -o ../3

a4:
	gcc $(OPT) $(CFLAGS) 4.c -o ../4

a5:
	gcc $(OPT) $(CFLAGS) -march=native 5.c -o ../5

a6:
	@# needs libc6-dev-i386
	gcc $(OPT) $(CFLAGS) -m32 6.c -o ../6

a7:
	gcc $(OPT) $(CFLAGS) 7.c -o ../7