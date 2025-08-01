#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char* data;
    int length;
    int capacity;
} StringBuffer;

typedef struct {
    StringBuffer* buffers[10];
    int count;
    StringBuffer* current;
} BufferManager;

void init_manager(BufferManager* manager) {
    manager->count = 0;
    for (int i = 0; i < 10; i++) {
        manager->buffers[i] = NULL;
    }
}

StringBuffer* add_buffer(BufferManager* manager, const char* initial) {
    if (manager->count >= 10) return NULL;
    
    StringBuffer* buf = malloc(sizeof(StringBuffer));
    buf->capacity = 64;
    buf->data = malloc(buf->capacity);
    strcpy(buf->data, initial);
    buf->length = strlen(initial);
    
    manager->buffers[manager->count] = buf;
    manager->count++;
    
    return buf;
}

void process_buffers(BufferManager* manager) {
    for (int i = 0; i < manager->count; i++) {
        if (manager->buffers[i]->length > 10) {
            manager->current = manager->buffers[i];
        }
    }
    
    if (manager->current) {
        printf("Current buffer contains: %s\n", manager->current->data);
    }
}

void append_to_current(BufferManager* manager, const char* text) {
    int new_len = manager->current->length + strlen(text);
    if (new_len < manager->current->capacity) {
        strcat(manager->current->data, text);
        manager->current->length = new_len;
    }
}

int main() {
    BufferManager manager;
    init_manager(&manager);
    
    add_buffer(&manager, "Hello");
    add_buffer(&manager, "World");
    add_buffer(&manager, "This is a test");
    
    process_buffers(&manager);
    append_to_current(&manager, " - appended");
    
    printf("Final result: %s\n", manager.current->data);
    
    for (int i = 0; i < manager.count; i++) {
        free(manager.buffers[i]->data);
        free(manager.buffers[i]);
    }
    
    return 0;
}