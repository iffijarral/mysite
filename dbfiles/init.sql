-- Start transaction
BEGIN;

-- Create users table
CREATE TABLE IF NOT EXISTS users(
    user_pk                 VARCHAR PRIMARY KEY,
    user_username           VARCHAR,
    user_name               VARCHAR,
    user_last_name          VARCHAR,
    user_email              VARCHAR UNIQUE,
    user_password           BYTEA,
    user_role               VARCHAR,
    user_created_at         BIGINT,
    user_updated_at         BIGINT,
    user_is_verified        INTEGER,
    user_is_blocked         INTEGER
);

-- Insert data into users table
INSERT INTO users VALUES 
('5771140287e94089965ec363933a0c0f','naeem','Muhammad','Naeem','iffijarral@gmail.com',decode(CAST('2432622431322470464e576335336c436e43566a59746b50464462472e5349767973342f324f4f304239324956466a554b794968686d67482f467057' AS TEXT), 'hex'),'customer',1721045697,0,1,0),
('589f51c98d7748cc912a379811e0267f','xyz','Muhammad','Zubair','iffi_kunjahi@yahoo.com',decode(CAST('243262243132244e556d52376d6f6938723534583656616e7963516275596c615547447834584a306e56482e3968773446335058476e726a654e4347' AS TEXT), 'hex'),'partner',1720973783,0,1,0),
('a3d0a851ac5c4d59a696079d225421bd','iffijarral','Iftikhar','Ahmed','iffidk@gmail.com',decode(CAST('2432622431322442326153763644587243656c38515779534e6f4f656532374b5754663345786a697334527a6b68336b393867354337324639797769' AS TEXT),'hex'),'admin',1720644178,0,1,0),
('c41e0836051d48a9b6a63bdb967cc5d2','palwashadk','Palwasha','Iftikhar','palwashadk@gmail.com',decode(CAST('24326224313224736137795550386f6a754e62706d302e4f4f43464965756d4e524c436c61397078706469394258625056636c79496a614b2e68564b' AS TEXT), 'hex'),'partner',1720986259,0,1,0);

-- Create email_verifications table
CREATE TABLE IF NOT EXISTS email_verifications (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR REFERENCES users(user_pk),
    verification_key TEXT,
    verification_timestamp BIGINT
);

CREATE TABLE IF NOT EXISTS items (
    item_pk                 TEXT PRIMARY KEY,
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
    FOREIGN KEY (owner_id) REFERENCES users(user_pk)
);

INSERT INTO items VALUES('26998a758efa414387310b2b7aefe24c','589f51c98d7748cc912a379811e0267f','Guesthouse in Jyllinge','Year-round home in 3310 beer place','./images/5dbce622fa2b4f22a6f6957d07ff4955.webp','Jyllinge','55.750503','12.106834',3.0,600.0,1723017733,0,0);
INSERT INTO items VALUES('56275abd32d342c5a33a17efa2f69e4e','589f51c98d7748cc912a379811e0267f','Tiny home in Slagelse','Cozy Tiny House in a rural setting','./images/582451438.jpg','Slagelse','55.403417','11.353739',4.0,750.0,1723017209,1723017347,0);
INSERT INTO items VALUES('6aee31d723384ef5b5a0bc4b5857bba3','589f51c98d7748cc912a379811e0267f','Apartment in Vesterbro','Charming oasis in the middle of the city','./images/5dbce622fa2b4f22a6f6957d07ff4951.webp','København','55.672828','12.551497',4.0,1000.0,1722969816,1723024713,0);
INSERT INTO items VALUES('76069e5c863649adbf46b404b4c701cb','589f51c98d7748cc912a379811e0267f','Apartment in Hvidovre','Cozy Apartment with beautiful bedroom view  Share  Save','./images/582451427.jpg','Hvidovre','55.623514','12.480542',4.0,700.0,1723018183,1723024579,0);
INSERT INTO items VALUES('998b647f40c3447ebb9d595601278829','589f51c98d7748cc912a379811e0267f','Guesthouse in Roskilde','Entire guesthouse in Roskilde','./images/5dbce622fa2b4f22a6f6957d07ff4957.webp','Roskilde','55.641833','12.109624',5.0,900.0,1723052599,0,0);
INSERT INTO items VALUES('9ff18add999b40e29d16e0bac40f8d2c','589f51c98d7748cc912a379811e0267f','The Hug House','Private room in home in Glostrup, Denmark','./images/5dbce622fa2b4f22a6f6957d07ff4955.webp','Glostrup','55.667068','12.415824',5.0,1000.0,1723052795,0,0);
INSERT INTO items VALUES('b5357ff15d9d4d69957697dd73a91724','589f51c98d7748cc912a379811e0267f','Cabin in Lyngby','Lovely cottage on Orø','./images/5dbce622fa2b4f22a6f6957d07ff4955.webp','Kongens Lyngby','55.76749','12.507685',4.0,800.0,1723052445,0,0);
INSERT INTO items VALUES('e359d7b48381412e98c1ec7ccc7e8f3f','589f51c98d7748cc912a379811e0267f','Room in Copenhagen','Bright room downtown CPH','./images/582451436.jpg','København','55.680064','12.582401',3.5,800.0,1722970046,0,0);
INSERT INTO items VALUES('e56dfacfb1ab4f79ae0574441bc145fd','589f51c98d7748cc912a379811e0267f','Condo in Frederiksberg','Sunny 2 rooms apartment in Frederiksberg','./images/5dbce622fa2b4f22a6f6957d07ff4910.webp','Frederiksberg','55.681654','12.532383',4.0,400.0,1722969336,0,1);
INSERT INTO items VALUES('fff72bea24c345a19f326d60168eb8f2','589f51c98d7748cc912a379811e0267f','Apartment in Frederikssund','Penthouse retreat in Frederikssund','./images/5dbce622fa2b4f22a6f6957d07ff4954.webp','Frederikssund','55.835898','12.062787',4.5,850.0,1723017527,0,0);

CREATE TABLE IF NOT EXISTS property_images (
    id INTEGER PRIMARY KEY,
    property_id TEXT REFERENCES items(item_pk),
    path TEXT NOT NULL
);

INSERT INTO property_images VALUES(30,'e56dfacfb1ab4f79ae0574441bc145fd','5dbce622fa2b4f22a6f6957d07ff4910.webp');
INSERT INTO property_images VALUES(31,'e56dfacfb1ab4f79ae0574441bc145fd','582451436.jpg');
INSERT INTO property_images VALUES(32,'e56dfacfb1ab4f79ae0574441bc145fd','582451438.jpg');
INSERT INTO property_images VALUES(33,'e56dfacfb1ab4f79ae0574441bc145fd','582451440.jpg');
INSERT INTO property_images VALUES(34,'e56dfacfb1ab4f79ae0574441bc145fd','582451442.jpg');
INSERT INTO property_images VALUES(35,'e56dfacfb1ab4f79ae0574441bc145fd','582451445.jpg');
INSERT INTO property_images VALUES(36,'e56dfacfb1ab4f79ae0574441bc145fd','582451448.jpg');
INSERT INTO property_images VALUES(37,'e56dfacfb1ab4f79ae0574441bc145fd','582451451.jpg');
INSERT INTO property_images VALUES(38,'e56dfacfb1ab4f79ae0574441bc145fd','582451452.jpg');
INSERT INTO property_images VALUES(39,'e56dfacfb1ab4f79ae0574441bc145fd','582451453.jpg');
INSERT INTO property_images VALUES(40,'e56dfacfb1ab4f79ae0574441bc145fd','582451454.jpg');
INSERT INTO property_images VALUES(42,'6aee31d723384ef5b5a0bc4b5857bba3','582451438.jpg');
INSERT INTO property_images VALUES(43,'6aee31d723384ef5b5a0bc4b5857bba3','582451448.jpg');
INSERT INTO property_images VALUES(44,'6aee31d723384ef5b5a0bc4b5857bba3','582451451.jpg');
INSERT INTO property_images VALUES(45,'6aee31d723384ef5b5a0bc4b5857bba3','582451453.jpg');
INSERT INTO property_images VALUES(46,'6aee31d723384ef5b5a0bc4b5857bba3','582451454.jpg');
INSERT INTO property_images VALUES(47,'6aee31d723384ef5b5a0bc4b5857bba3','582451458.jpg');
INSERT INTO property_images VALUES(48,'6aee31d723384ef5b5a0bc4b5857bba3','582451460.jpg');
INSERT INTO property_images VALUES(49,'6aee31d723384ef5b5a0bc4b5857bba3','582451462.jpg');
INSERT INTO property_images VALUES(50,'6aee31d723384ef5b5a0bc4b5857bba3','582451465.jpg');
INSERT INTO property_images VALUES(51,'6aee31d723384ef5b5a0bc4b5857bba3','582451476.jpg');
INSERT INTO property_images VALUES(52,'e359d7b48381412e98c1ec7ccc7e8f3f','582451436.jpg');
INSERT INTO property_images VALUES(53,'e359d7b48381412e98c1ec7ccc7e8f3f','582451438.jpg');
INSERT INTO property_images VALUES(54,'e359d7b48381412e98c1ec7ccc7e8f3f','582451440.jpg');
INSERT INTO property_images VALUES(55,'e359d7b48381412e98c1ec7ccc7e8f3f','582451442.jpg');
INSERT INTO property_images VALUES(56,'e359d7b48381412e98c1ec7ccc7e8f3f','582451445.jpg');
INSERT INTO property_images VALUES(57,'e359d7b48381412e98c1ec7ccc7e8f3f','582451448.jpg');
INSERT INTO property_images VALUES(58,'e359d7b48381412e98c1ec7ccc7e8f3f','582451451.jpg');
INSERT INTO property_images VALUES(59,'e359d7b48381412e98c1ec7ccc7e8f3f','582451452.jpg');
INSERT INTO property_images VALUES(60,'e359d7b48381412e98c1ec7ccc7e8f3f','582451453.jpg');
INSERT INTO property_images VALUES(61,'e359d7b48381412e98c1ec7ccc7e8f3f','582451454.jpg');
INSERT INTO property_images VALUES(62,'e359d7b48381412e98c1ec7ccc7e8f3f','582451456.jpg');
INSERT INTO property_images VALUES(63,'e359d7b48381412e98c1ec7ccc7e8f3f','582451458.jpg');
INSERT INTO property_images VALUES(102,'56275abd32d342c5a33a17efa2f69e4e','582451438.jpg');
INSERT INTO property_images VALUES(103,'56275abd32d342c5a33a17efa2f69e4e','582451442.jpg');
INSERT INTO property_images VALUES(104,'56275abd32d342c5a33a17efa2f69e4e','582451445.jpg');
INSERT INTO property_images VALUES(105,'56275abd32d342c5a33a17efa2f69e4e','582451451.jpg');
INSERT INTO property_images VALUES(106,'56275abd32d342c5a33a17efa2f69e4e','582451452.jpg');
INSERT INTO property_images VALUES(107,'56275abd32d342c5a33a17efa2f69e4e','582451453.jpg');
INSERT INTO property_images VALUES(108,'56275abd32d342c5a33a17efa2f69e4e','582451454.jpg');
INSERT INTO property_images VALUES(109,'56275abd32d342c5a33a17efa2f69e4e','582451456.jpg');
INSERT INTO property_images VALUES(110,'56275abd32d342c5a33a17efa2f69e4e','582451458.jpg');
INSERT INTO property_images VALUES(111,'56275abd32d342c5a33a17efa2f69e4e','582451459.jpg');
INSERT INTO property_images VALUES(112,'56275abd32d342c5a33a17efa2f69e4e','582451461.jpg');
INSERT INTO property_images VALUES(113,'56275abd32d342c5a33a17efa2f69e4e','582451464.jpg');
INSERT INTO property_images VALUES(114,'fff72bea24c345a19f326d60168eb8f2','5dbce622fa2b4f22a6f6957d07ff4954.webp');
INSERT INTO property_images VALUES(115,'fff72bea24c345a19f326d60168eb8f2','582451438.jpg');
INSERT INTO property_images VALUES(116,'fff72bea24c345a19f326d60168eb8f2','582451442.jpg');
INSERT INTO property_images VALUES(117,'fff72bea24c345a19f326d60168eb8f2','582451451.jpg');
INSERT INTO property_images VALUES(118,'fff72bea24c345a19f326d60168eb8f2','582451452.jpg');
INSERT INTO property_images VALUES(119,'fff72bea24c345a19f326d60168eb8f2','582451454.jpg');
INSERT INTO property_images VALUES(120,'fff72bea24c345a19f326d60168eb8f2','582451456.jpg');
INSERT INTO property_images VALUES(121,'fff72bea24c345a19f326d60168eb8f2','582451458.jpg');
INSERT INTO property_images VALUES(122,'fff72bea24c345a19f326d60168eb8f2','582451460.jpg');
INSERT INTO property_images VALUES(123,'fff72bea24c345a19f326d60168eb8f2','582451462.jpg');
INSERT INTO property_images VALUES(124,'fff72bea24c345a19f326d60168eb8f2','582451464.jpg');
INSERT INTO property_images VALUES(125,'26998a758efa414387310b2b7aefe24c','5dbce622fa2b4f22a6f6957d07ff4955.webp');
INSERT INTO property_images VALUES(126,'26998a758efa414387310b2b7aefe24c','582451438.jpg');
INSERT INTO property_images VALUES(127,'26998a758efa414387310b2b7aefe24c','582451442.jpg');
INSERT INTO property_images VALUES(128,'26998a758efa414387310b2b7aefe24c','582451445.jpg');
INSERT INTO property_images VALUES(129,'26998a758efa414387310b2b7aefe24c','582451451.jpg');
INSERT INTO property_images VALUES(130,'26998a758efa414387310b2b7aefe24c','582451453.jpg');
INSERT INTO property_images VALUES(131,'26998a758efa414387310b2b7aefe24c','582451456.jpg');
INSERT INTO property_images VALUES(132,'26998a758efa414387310b2b7aefe24c','582451459.jpg');
INSERT INTO property_images VALUES(143,'76069e5c863649adbf46b404b4c701cb','582451438.jpg');
INSERT INTO property_images VALUES(144,'76069e5c863649adbf46b404b4c701cb','582451440.jpg');
INSERT INTO property_images VALUES(145,'76069e5c863649adbf46b404b4c701cb','582451451.jpg');
INSERT INTO property_images VALUES(146,'76069e5c863649adbf46b404b4c701cb','582451453.jpg');
INSERT INTO property_images VALUES(147,'76069e5c863649adbf46b404b4c701cb','582451456.jpg');
INSERT INTO property_images VALUES(148,'76069e5c863649adbf46b404b4c701cb','582451459.jpg');
INSERT INTO property_images VALUES(149,'76069e5c863649adbf46b404b4c701cb','582451460.jpg');
INSERT INTO property_images VALUES(150,'76069e5c863649adbf46b404b4c701cb','582451461.jpg');
INSERT INTO property_images VALUES(151,'76069e5c863649adbf46b404b4c701cb','582451427.jpg');
INSERT INTO property_images VALUES(152,'6aee31d723384ef5b5a0bc4b5857bba3','5dbce622fa2b4f22a6f6957d07ff4951.webp');
INSERT INTO property_images VALUES(153,'b5357ff15d9d4d69957697dd73a91724','5dbce622fa2b4f22a6f6957d07ff4955.webp');
INSERT INTO property_images VALUES(154,'b5357ff15d9d4d69957697dd73a91724','582451438.jpg');
INSERT INTO property_images VALUES(155,'b5357ff15d9d4d69957697dd73a91724','582451440.jpg');
INSERT INTO property_images VALUES(156,'b5357ff15d9d4d69957697dd73a91724','582451445.jpg');
INSERT INTO property_images VALUES(157,'b5357ff15d9d4d69957697dd73a91724','582451451.jpg');
INSERT INTO property_images VALUES(158,'b5357ff15d9d4d69957697dd73a91724','582451453.jpg');
INSERT INTO property_images VALUES(159,'b5357ff15d9d4d69957697dd73a91724','582451456.jpg');
INSERT INTO property_images VALUES(160,'b5357ff15d9d4d69957697dd73a91724','582451458.jpg');
INSERT INTO property_images VALUES(161,'b5357ff15d9d4d69957697dd73a91724','582451459.jpg');
INSERT INTO property_images VALUES(162,'b5357ff15d9d4d69957697dd73a91724','582451460.jpg');
INSERT INTO property_images VALUES(163,'b5357ff15d9d4d69957697dd73a91724','582451461.jpg');
INSERT INTO property_images VALUES(164,'998b647f40c3447ebb9d595601278829','5dbce622fa2b4f22a6f6957d07ff4957.webp');
INSERT INTO property_images VALUES(165,'998b647f40c3447ebb9d595601278829','582451440.jpg');
INSERT INTO property_images VALUES(166,'998b647f40c3447ebb9d595601278829','582451445.jpg');
INSERT INTO property_images VALUES(167,'998b647f40c3447ebb9d595601278829','582451451.jpg');
INSERT INTO property_images VALUES(168,'998b647f40c3447ebb9d595601278829','582451453.jpg');
INSERT INTO property_images VALUES(169,'998b647f40c3447ebb9d595601278829','582451454.jpg');
INSERT INTO property_images VALUES(170,'998b647f40c3447ebb9d595601278829','582451456.jpg');
INSERT INTO property_images VALUES(171,'998b647f40c3447ebb9d595601278829','582451458.jpg');
INSERT INTO property_images VALUES(172,'998b647f40c3447ebb9d595601278829','582451460.jpg');
INSERT INTO property_images VALUES(173,'998b647f40c3447ebb9d595601278829','582451462.jpg');
INSERT INTO property_images VALUES(174,'998b647f40c3447ebb9d595601278829','582451465.jpg');
INSERT INTO property_images VALUES(175,'9ff18add999b40e29d16e0bac40f8d2c','5dbce622fa2b4f22a6f6957d07ff4955.webp');
INSERT INTO property_images VALUES(176,'9ff18add999b40e29d16e0bac40f8d2c','582451436.jpg');
INSERT INTO property_images VALUES(177,'9ff18add999b40e29d16e0bac40f8d2c','582451440.jpg');
INSERT INTO property_images VALUES(178,'9ff18add999b40e29d16e0bac40f8d2c','582451445.jpg');
INSERT INTO property_images VALUES(179,'9ff18add999b40e29d16e0bac40f8d2c','582451451.jpg');
INSERT INTO property_images VALUES(180,'9ff18add999b40e29d16e0bac40f8d2c','582451453.jpg');
INSERT INTO property_images VALUES(181,'9ff18add999b40e29d16e0bac40f8d2c','582451454.jpg');
INSERT INTO property_images VALUES(182,'9ff18add999b40e29d16e0bac40f8d2c','582451458.jpg');
INSERT INTO property_images VALUES(183,'9ff18add999b40e29d16e0bac40f8d2c','582451460.jpg');
INSERT INTO property_images VALUES(184,'9ff18add999b40e29d16e0bac40f8d2c','582451462.jpg');
INSERT INTO property_images VALUES(185,'9ff18add999b40e29d16e0bac40f8d2c','582451464.jpg');





-- Commit transaction
COMMIT;
