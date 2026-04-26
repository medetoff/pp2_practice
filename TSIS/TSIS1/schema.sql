-- =============================================================
-- schema.sql  –  TSIS 1 extensions
-- Extends the Practice-8 `phonebook` table (first_name,
-- last_name, phone) with groups, multiple phones, email, birthday.
-- Safe to re-run: uses IF NOT EXISTS and DO $$ guards.
-- =============================================================

-- 1. Groups table
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

-- 2. Add new columns to the existing phonebook table
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'phonebook' AND column_name = 'email'
    ) THEN
        ALTER TABLE phonebook ADD COLUMN email VARCHAR(100);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'phonebook' AND column_name = 'birthday'
    ) THEN
        ALTER TABLE phonebook ADD COLUMN birthday DATE;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'phonebook' AND column_name = 'group_id'
    ) THEN
        ALTER TABLE phonebook ADD COLUMN group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'phonebook' AND column_name = 'created_at'
    ) THEN
        ALTER TABLE phonebook ADD COLUMN created_at TIMESTAMP DEFAULT NOW();
    END IF;
END;
$$;

-- 3. Phones table (1-to-many; old `phone` column stays for P7-8 compat)
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES phonebook(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) DEFAULT 'mobile'
                           CHECK (type IN ('home', 'work', 'mobile'))
);

-- Migrate existing single phone values into phones table (run once)
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'phonebook' AND column_name = 'phone'
    ) THEN
        INSERT INTO phones (contact_id, phone, type)
        SELECT id, phone, 'mobile'
        FROM   phonebook
        WHERE  phone IS NOT NULL AND phone <> ''
          AND  id NOT IN (SELECT DISTINCT contact_id FROM phones)
        ON CONFLICT DO NOTHING;
    END IF;
END;
$$;