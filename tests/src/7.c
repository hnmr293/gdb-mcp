#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    char tag[8];
    int value;
    char description[32];
} Record;

void parse_input(const char* input, Record* record) {
    char buffer[40];
    int pos = 0;
    
    for (int i = 0; input[i] && input[i] != ':'; i++) {
        buffer[pos++] = input[i];
    }
    buffer[pos] = '\0';
    strcpy(record->tag, buffer);
    
    const char* value_start = strchr(input, ':');
    if (value_start) {
        record->value = atoi(value_start + 1);
        
        const char* desc_start = strchr(value_start + 1, ':');
        if (desc_start) {
            strcpy(record->description, desc_start + 1);
        }
    }
}

int main() {
    Record records[3] = {0};
    const char* inputs[] = {
        "ITEM001:100:Standard item",
        "SPECIALPROMOTION2023:500:Limited time offer for valued customers",
        "DATA:200:Test entry"
    };
    
    for (int i = 0; i < 3; i++) {
        parse_input(inputs[i], &records[i]);
        printf("Tag: %s, Value: %d, Desc: %s\n", 
               records[i].tag, records[i].value, records[i].description);
    }
    
    return 0;
}