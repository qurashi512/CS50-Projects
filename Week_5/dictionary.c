// Implements a dictionary's functionality

#include <ctype.h> 
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table

const unsigned int N = 1000;

// Hash table
node *table[N];
unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // الخطوة 1: هاش الكلمة
    int index = hash(word);

    // الخطوة 2: روح الرف ده
    node *cursor = table[index];

    // الخطوة 3: دور في الـ linked list
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int sum = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        sum += tolower(word[i]);
    }
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // 1. افتح ملف القاموس
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
        return false;

    char word[LENGTH + 1];

    // 2. اقرا كل كلمة
    while (fscanf(file, "%s", word) != EOF)
    {
        // 3. اعمل node جديد
        node *n = malloc(sizeof(node));
        if (n == NULL)
            return false;

        // 4. حط الكلمة في الـ node
        strcpy(n->word, word);

        // 5. احسب الـ index
        int index = hash(word);

        // 6. حط الـ node في الـ table
        n->next = table[index];
        table[index] = n;

        word_count++;
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
