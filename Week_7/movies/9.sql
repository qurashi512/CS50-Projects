-- 9. Names of all people who starred in a movie released in 2004, ordered by birth year
SELECT name, id
FROM people
WHERE id IN (
    SELECT person_id
    FROM stars
    JOIN movies ON stars.movie_id = movies.id
    WHERE movies.year = 2004
)
ORDER BY birth;
