#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// تعريف نوع بيانات بحجم بايت واحد
typedef uint8_t BYTE;
#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // التأكد من أن المستخدم أدخل اسم الملف
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // فتح بطاقة الذاكرة
    FILE *raw_file = fopen(argv[1], "r");
    if (raw_file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    // المتغيرات التي ستحتاجها
    BYTE buffer[BLOCK_SIZE];
    FILE *img = NULL;
    char filename[8]; // مساحة كافية لاسم الملف "000.jpg" + \0
    int file_count = 0;

    // حلقة القراءة (تقرأ 512 بايت في كل مرة حتى ينتهي الملف)
    while (fread(buffer, 1, BLOCK_SIZE, raw_file) == BLOCK_SIZE)
    {
        // 1. فحص هل البايتات الأربعة الأولى تمثل توقيع صورة JPEG؟
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // إذا كنا نكتب في صورة بالفعل، نغلقها أولاً لنبدأ الجديدة
            if (img != NULL)
            {
                fclose(img);
            }

            // 2. تكوين اسم الملف الجديد (مثل: 000.jpg, 001.jpg)
            sprintf(filename, "%03i.jpg", file_count);

            // 3. فتح الملف الجديد للكتابة فيه
            img = fopen(filename, "w");

            // 4. زيادة العداد للصورة القادمة
            file_count++;
        }

        // 5. الاستمرار في كتابة البيانات (512 بايت) إذا كان هناك ملف صورة مفتوح
        if (img != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
    }

    // إغلاق الملفات
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(raw_file);

    return 0;
}
