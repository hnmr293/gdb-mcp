#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Student {
    char name[32];
    int score;
    struct Student* partner;
};

struct Student* create_student(const char* name, int score) {
    struct Student* s = malloc(sizeof(struct Student));
    strncpy(s->name, name, 31);
    s->name[31] = '\0';
    s->score = score;
    s->partner = NULL;
    return s;
}

void process_results(struct Student** students, int count) {
    int total = 0;
    for (int i = 0; i < count; i++) {
        total += students[i]->score;
        if (students[i]->score > 80) {
            struct Student* partner = students[(i + 1) % count];
            students[i]->partner = partner;
            printf("%s paired with %s\n", students[i]->name, partner->name);
        }
    }
    printf("Average: %.2f\n", (float)total / count);
}

int main() {
    struct Student* class[5];
    class[0] = create_student("Alice", 85);
    class[1] = create_student("Bob", 72);
    class[2] = create_student("Carol", 90);
    class[3] = create_student("Dave", 65);
    class[4] = NULL;
    
    process_results(class, 5);
    
    for (int i = 0; i < 4; i++) {
        free(class[i]);
    }
    return 0;
}