-- contoso-backend/db/init.sql
-- Initializes users and tickets tables for Contoso backend

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(1024) NOT NULL,
    role VARCHAR(50) NOT NULL,
    is_suspended BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create tickets table
CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    "when" TIMESTAMP NOT NULL,
    link VARCHAR(2048) DEFAULT '' NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    user_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE '+08'),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE '+08'),
    changer_id INTEGER
);

-- Index to speed up queries by user_id
CREATE INDEX IF NOT EXISTS ix_tickets_user_id ON tickets (user_id);

-- Optional foreign keys (commented out to match "logical but not enforced" requirement)
-- ALTER TABLE tickets
--   ADD CONSTRAINT fk_tickets_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE;
-- ALTER TABLE tickets
--   ADD CONSTRAINT fk_tickets_changer FOREIGN KEY (changer_id) REFERENCES users (id) ON DELETE SET NULL;
