SELECT title FROM movies
WHERE ID IN (SELECT movie_id FROM stars
JOIN people ON people.id = stars.person_id
WHERE name = "Helena Bonham Carter" AND movie_id IN (SELECT movie_id FROM stars 
WHERE person_id IN (SELECT id FROM people 
WHERE name = "Johnny Depp")));