#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    // 1. التحقق من وجود كلمة واحدة بعد اسم البرنامج
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    // 2. التحقق من أن المفتاح يتكون من 26 حرفاً
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // 3. التحقق من أن جميع الرموز حروف أبجدية، وعدم وجود حروف مكررة
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }

        for (int j = i + 1; j < 26; j++)
        {
            if (toupper(key[i]) == toupper(key[j]))
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }

    // 4. طلب النص الأصلي من المستخدم
    string plaintext = get_string("plaintext:  ");

    // 5. التشفير وطباعة النتيجة
    printf("ciphertext: ");

    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        // إذا كان الحرف كبيراً
        if (isupper(plaintext[i]))
        {
            int index = plaintext[i] - 'A';
            printf("%c", toupper(key[index]));
        }
        // إذا كان الحرف صغيراً
        else if (islower(plaintext[i]))
        {
            int index = plaintext[i] - 'a';
            printf("%c", tolower(key[index]));
        }
        // إذا كان مسافة أو علامة ترقيم أو رقم (يطبع كما هو)
        else
        {
            printf("%c", plaintext[i]);
        }
    }

    printf("\n");
    return 0;
}
