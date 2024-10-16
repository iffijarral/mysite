-- Hashed passsword is: $2b$12$V/cXqWN/M2vTnYUcXMB9oODcNBX/QorJekmaDkq1Z7aeD3I5ZAjfu

DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_pk                 TEXT,
    user_username           TEXT,
    user_name               TEXT,
    user_last_name          TEXT,
    user_email              TEXT UNIQUE,
    user_password           TEXT,
    user_role               TEXT,
    user_created_at         INTEGER,
    user_updated_at         INTEGER,
    user_is_verified        INTEGER,
    user_is_blocked         INTEGER,
    PRIMARY KEY(user_pk)
) WITHOUT ROWID;

INSERT INTO users VALUES(
    "d11854217ecc42b2bb17367fe33dc8f4",
    "johndoe",
    "Jhon",
    "Doe",
    "admin@company.com",
    "$2b$12$V/cXqWN/M2vTnYUcXMB9oODcNBX/QorJekmaDkq1Z7aeD3I5ZAjfu",
    "admin",
    1712674758,
    0,
    1,
    0
);

SELECT * FROM users; 
UPDATE users SET user_is_blocked = 0 WHERE user_pk = '5771140287e94089965ec363933a0c0f'
DELETE FROM users WHERE user_pk = 'cddf313bd8b94825b81d3b9e1f9fb0b9';

DROP TABLE IF EXISTS items;

CREATE TABLE items(
    item_pk                 TEXT,
    owner_id                TEXT,
    item_name               TEXT,
    item_description        TEXT,
    item_splash_image       TEXT,
    item_city               TEXT,
    item_lat                TEXT,
    item_lon                TEXT,
    item_stars              REAL,
    item_price_per_night    REAL,
    item_created_at         INTEGER,
    item_updated_at         INTEGER,
    item_is_blocked         INTEGER,
    PRIMARY KEY(item_pk),
    FOREIGN KEY(owner_id) REFERENCES users(user_pk)
) WITHOUT ROWID;

INSERT INTO items VALUES
("5dbce622fa2b4f22a6f6957d07ff4951", "589f51c98d7748cc912a379811e0267f", "Christiansborg Palace", "Christiansborg Palace", "5dbce622fa2b4f22a6f6957d07ff4951.webp", "Copenhagen", 55.6761, 12.5770, 5, 2541, 1, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4952", "589f51c98d7748cc912a379811e0267f", "Tivoli Gardens", "Christiansborg Palace", "5dbce622fa2b4f22a6f6957d07ff4952.webp", "Copenhagen", 55.6736, 12.5681, 4.97, 985, 2, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4953", "589f51c98d7748cc912a379811e0267f", "Nyhavn", "Christiansborg Palace", "5dbce622fa2b4f22a6f6957d07ff4953.webp", "Copenhagen", 55.6794, 12.5918, 3.45, 429, 3, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4954", "589f51c98d7748cc912a379811e0267f", "The Little Mermaid statue", "Christiansborg Palace", "5dbce622fa2b4f22a6f6957d07ff4954.webp", "Odense", 55.6929, 12.5998, 4, 862, 4, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4955", "589f51c98d7748cc912a379811e0267f", "Amalienborg Palace", "Christiansborg Palace", "5dbce622fa2b4f22a6f6957d07ff4955.webp", "Odense", 55.6846, 12.5949, 2.67, 1200, 5, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4956", "589f51c98d7748cc912a379811e0267f", "Copenhagen Opera House", "Christiansborg Palace", "5dbce622fa2b4f22a6f6957d07ff4956.webp", "Kolding",  55.6796, 12.6021, 4.57, 1965, 6, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4957", "589f51c98d7748cc912a379811e0267f", "Rosenborg Castle", "Christiansborg Palace", "5dbce622fa2b4f22a6f6957d07ff4957.webp", "Kolding", 55.6867, 12.5734, 4, 1700, 7, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4958", "589f51c98d7748cc912a379811e0267f", "The National Museum of Denmark", "Christiansborg Palace", "5dbce622fa2b4f22a6f6957d07ff4958.webp", "Copenhagen", 55.6772, 12.5784, 5, 2100, 8, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4959", "589f51c98d7748cc912a379811e0267f", "Church of Our Saviour", "Christiansborg Palace", "5dbce622fa2b4f22a6f6957d07ff4959.webp", "Valby", 55.6732, 12.5986, 4.3, 985, 9, 0, 0),
("5dbce622fa2b4f22a6f6957d07ff4910", "589f51c98d7748cc912a379811e0267f", "Round Tower", "Christiansborg Palace", "5dbce622fa2b4f22a6f6957d07ff4910.webp", "Valby",  55.6813, 12.5759, 4.8, 1200, 10, 0, 0);

SELECT * FROM items;
DELETE FROM items WHERE item_pk='9bd6646feda045e495db0f01f454696b'

ALTER TABLE items ADD COLUMN item_city TEXT;

DROP TABLE IF EXISTS property_images;
CREATE TABLE property_images(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id TEXT REFERENCES items(item_pk),
    path TEXT NOT NULL        
);
INSERT INTO property_images (property_id, path) VALUES ('589f51c98d7748cc912a379811e0267f', '5dbce622fa2b4f22a6f6957d07ff4959.webp');
UPDATE property_images SET property_id = '5dbce622fa2b4f22a6f6957d07ff4951'
SELECT * FROM property_images;
DELETE FROM property_images WHERE property_id = '9bd6646feda045e495db0f01f454696b'

-- (page_number - 1) * items_per_page
-- (1 - 1) * 3 = 10 1 2
-- (2 - 1) * 3 = 3 4 5
-- (3 - 1) * 3 = 6 7 8

5dbce622fa2b4f22a6f6957d07ff4956.webp
5dbce622fa2b4f22a6f6957d07ff4957.webp
5dbce622fa2b4f22a6f6957d07ff4959.webp
-- Page 4
-- 0 3 6 9

SELECT * FROM items 
ORDER BY item_created_at
LIMIT 9,3;


-- offset = (currentPage - 1) * itemsPerPage
-- page 1 = 1 2 3+
-- page 2 = 4 5 6
-- page 3 = 7 8 9
-- page 4 = 10
SELECT * FROM items 
ORDER BY item_created_at
LIMIT 3 OFFSET 9;

DROP TABLE IF EXISTS email_verifications;

CREATE TABLE email_verifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_pk),
    verification_key TEXT,
    verification_timestamp INTEGER
);

SELECT * FROM email_verifications;

DROP TABLE IF EXISTS bookings;
CREATE TABLE bookings (
    user_id INTEGER NOT NULL,
    checkin DATE NOT NULL,
    checkout DATE NOT NULL,
    guests INTEGER NOT NULL,
    property_id TEXT NOT NULL,
    PRIMARY KEY (user_id, checkin)  -- Composite primary key
    FOREIGN KEY (property_id) REFERENCES items(item_pk)
) WITHOUT ROWID;

SELECT * FROM bookings;
DELETE FROM bookings;






