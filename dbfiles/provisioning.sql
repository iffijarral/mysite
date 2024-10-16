DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_pk              TEXT PRIMARY KEY,
    user_username        TEXT,
    user_name            TEXT,
    user_last_name       TEXT,
    user_email           TEXT UNIQUE,
    user_password        TEXT,
    user_role            TEXT,
    user_created_at      TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    user_updated_at      TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    user_is_verified     BOOLEAN DEFAULT FALSE,
    user_is_blocked      BOOLEAN DEFAULT FALSE
);