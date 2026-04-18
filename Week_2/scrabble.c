#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// مصفوفة النقاط لكل حرف أبجدي
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

// الإعلان عن الدالة التي ستحسب النقاط
int compute_score(string word);

int main(void)
{
    // 1. اطلب الكلمة من اللاعب الأول
    string word1 = get_string("Player 1: ");

    // 2. اطلب الكلمة من اللاعب الثاني
    string word2 = get_string("Player 2: ");

    // 3. احسب نقاط اللاعب الأول (باستخدام الدالة)
    int score1 = compute_score(word1);

    // 4. احسب نقاط اللاعب الثاني (باستخدام الدالة)
    int score2 = compute_score(word2);
    // 5. قارن بين النقطتين واطبع الفائز أو التعادل
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    // متغير لحفظ المجموع
    int score = 0;

    // حلقة للمرور على كل حرف في الكلمة
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        // إذا كان الحرف كبيراً
        if (isupper(word[i]))
        {
            score += POINTS[word[i] - 'A'];
        }
        // إذا كان الحرف صغيراً
        else if (islower(word[i]))
        {
            score += POINTS[word[i] - 'a'];
        }
        // علامات الترقيم والأرقام يتم تجاهلها تلقائياً (لا تضاف نقاط)
    }

    return score;
}
