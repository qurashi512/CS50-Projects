#include <cs50.h> 
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // 1. اطلب النص من المستخدم
    string text = get_string("Text: ");

    // 2. احسب عدد الحروف، الكلمات، والجمل باستخدام الدوال
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // 3. طبق معادلة (Coleman-Liau)
    // حساب المتوسطات لكل 100 كلمة (نستخدم float لتجنب حذف الكسور)
    float L = ((float) letters / words) * 100;
    float S = ((float) sentences / words) * 100;

    // حساب المؤشر وتقريب الرقم
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = round(index);

    // 4. اطبع النتيجة
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

int count_letters(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    // نبدأ بـ 1 لأن الكلمة الأخيرة لا تنتهي بمسافة دائماً
    int count = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isspace(text[i]))
        {
            count++;
        }
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // الجملة تنتهي بنقطة، علامة تعجب، أو علامة استفهام
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count++;
        }
    }
    return count;
}
