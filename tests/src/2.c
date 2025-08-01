#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int data;
    struct Node* next;
    struct Node* shared;
} Node;

Node* create_list(int* values, int size) {
    Node* head = NULL;
    Node* tail = NULL;
    Node* special = NULL;
    
    for (int i = 0; i < size; i++) {
        Node* node = malloc(sizeof(Node));
        node->data = values[i];
        node->next = NULL;
        node->shared = NULL;
        
        if (values[i] % 10 == 0) {
            special = node;
        }
        
        if (!head) {
            head = node;
            tail = node;
        } else {
            tail->next = node;
            tail = node;
        }
    }
    
    Node* current = head;
    while (current) {
        if (current->data > 50) {
            current->shared = special;
        }
        current = current->next;
    }
    
    return head;
}

void cleanup_list(Node* head) {
    while (head) {
        Node* temp = head;
        head = head->next;
        if (temp->shared) {
            free(temp->shared);
        }
        free(temp);
    }
}

int main() {
    int values[] = {30, 45, 60, 20, 75, 80};
    Node* list = create_list(values, 6);
    
    Node* current = list;
    while (current) {
        printf("Value: %d\n", current->data);
        current = current->next;
    }
    
    cleanup_list(list);
    return 0;
}