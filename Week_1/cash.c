#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int cents;

    // 1. طلب المبلغ من المستخدم (يجب ألا يكون رقماً سالباً)
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    int coins = 0;

    // 2. حساب كم عملة من فئة 25 سنت يمكن استخدامها
    while (cents >= 25)
    {
        cents = cents - 25;
        coins++;
    }

    // 3. حساب كم عملة من فئة 10 سنت يمكن استخدامها
    while (cents >= 10)
    {
        cents = cents - 10;
        coins++;
    }

    // 4. حساب كم عملة من فئة 5 سنت يمكن استخدامها
    while (cents >= 5)
    {
        cents = cents - 5;
        coins++;
    }

    // 5. حساب كم عملة من فئة 1 سنت يمكن استخدامها
    while (cents >= 1)
    {
        cents = cents - 1;
        coins++;
    }

    // 6. طباعة النتيجة النهائية (أقل عدد من العملات)
    printf("%i\n", coins);
}
