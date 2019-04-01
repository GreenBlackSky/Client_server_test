CREATE TABLE users (
    name TEXT PRIMARY KEY,
    credits INT
);
INSERT INTO users VALUES
    ('Jon', 108),
    ('Dany', 129),
    ('Cersei', 250);
CREATE TABLE users_items (
    user_name TEXT,
    item_name TEXT,
    amount INTEGER,
    FOREIGN KEY(user_name) REFERENCES users(name),
    UNIQUE(user_name, item_name)
);
INSERT INTO users_items VALUES
    ('Jon', 'Longclaw', 1),
    ('Dany', 'dragon', 2),
    ('Cersei', 'Mountain', 1);