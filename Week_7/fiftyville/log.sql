-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Step 1: ابحث عن تقرير الجريمة في Humphrey Street
SELECT description FROM crime_scene_reports
WHERE street = 'Humphrey Street' AND month = 7 AND day = 28;

-- النتيجة: السرقة كانت 10:15am في المخبز. 3 شهود ذكروا المخبز.

-- Step 2: اقرأ شهادات الشهود
SELECT name, transcript FROM interviews
WHERE month = 7 AND day = 28
AND transcript LIKE '%bakery%';

-- الأدلة من الشهود:
-- 1. الحارق خرج من parking lot خلال 10 دقايق (10:15 - 10:25)
-- 2. سحب فلوس من ATM في Leggett Street قبل الجريمة
-- 3. اتصل بحد لمدة أقل من دقيقة، وطلب منه يحجز أول رحلة اليوم التاني

-- Step 3: لوحات السيارات اللي خرجت من الـ parking بين 10:15 و 10:25
SELECT license_plate FROM bakery_security_logs
WHERE month = 7 AND day = 28
AND activity = 'exit'
AND hour = 10 AND minute > 15 AND minute < 25;

-- Step 4: الأشخاص اللي سحبوا من ATM في Leggett Street يوم الجريمة
SELECT name, phone_number, license_plate FROM people
WHERE id IN (
    SELECT person_id FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number FROM atm_transactions
        WHERE month = 7 AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
    )
);

-- Step 5: المكالمات اللي أقل من دقيقة يوم الجريمة
SELECT caller, receiver FROM phone_calls
WHERE month = 7 AND day = 28 AND duration < 60;

-- Step 6: أول رحلة طيران من Fiftyville يوم 29
SELECT id, destination_airport_id FROM flights
WHERE origin_airport_id = (
    SELECT id FROM airports WHERE city = 'Fiftyville'
)
AND month = 7 AND day = 29
ORDER BY hour ASC, minute ASC
LIMIT 1;

-- Step 7: المدينة اللي سافر إليها
SELECT city FROM airports
WHERE id = (
    SELECT destination_airport_id FROM flights
    WHERE origin_airport_id = (
        SELECT id FROM airports WHERE city = 'Fiftyville'
    )
    AND month = 7 AND day = 29
    ORDER BY hour ASC, minute ASC
    LIMIT 1
);

-- Step 8: ضيق قائمة المشتبه بيهم — تقاطع كل الأدلة
SELECT name FROM people
WHERE license_plate IN (
    SELECT license_plate FROM bakery_security_logs
    WHERE month = 7 AND day = 28 AND activity = 'exit'
    AND hour = 10 AND minute > 15 AND minute < 25
)
AND id IN (
    SELECT person_id FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number FROM atm_transactions
        WHERE month = 7 AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
    )
)
AND phone_number IN (
    SELECT caller FROM phone_calls
    WHERE month = 7 AND day = 28 AND duration < 60
)
AND id IN (
    SELECT person_id FROM passengers
    WHERE flight_id = (
        SELECT id FROM flights
        WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
        AND month = 7 AND day = 29
        ORDER BY hour ASC, minute ASC LIMIT 1
    )
);
-- النتيجة: Bruce

-- Step 9: المتواطئ (اللي استقبل المكالمة وحجز التذكرة)
SELECT name FROM people
WHERE phone_number IN (
    SELECT receiver FROM phone_calls
    WHERE month = 7 AND day = 28 AND duration < 60
    AND caller = (SELECT phone_number FROM people WHERE name = 'Bruce')
);
-- النتيجة: Robin
