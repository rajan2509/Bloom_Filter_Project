
-- 1. Count total records
SELECT COUNT(*) AS total_records
FROM checked_items;


-- 2. Count usernames and URLs separately
SELECT item_type, COUNT(*) AS total_items
FROM checked_items
GROUP BY item_type;


-- 3. Display all usernames
SELECT id, item_value, created_at
FROM checked_items
WHERE item_type = 'username';


-- 4. Display all URLs
SELECT id, item_value, created_at
FROM checked_items
WHERE item_type = 'url';


-- 5. Search for a specific username
SELECT *
FROM checked_items
WHERE item_type = 'username'
AND item_value = 'registered_user_10';


-- 6. Search for a specific URL
SELECT *
FROM checked_items
WHERE item_type = 'url'
AND item_value = 'https://example10.com';


-- 7. Find records inserted today
SELECT *
FROM checked_items
WHERE DATE(created_at) = DATE('now');


-- 8. Find duplicate item values across different item types
SELECT item_value, COUNT(*) AS occurrences
FROM checked_items
GROUP BY item_value
HAVING COUNT(*) > 1;
