-- =============================================================
-- procedures.sql  –  TSIS 1 new stored objects only
-- P8 already has: search_pattern, insert_or_update, insert_many,
--                 get_paginated, delete_user
-- Do NOT re-create those here.
-- =============================================================

-- -------------------------------------------------------------
-- 1.  add_phone  –  add a phone number to an existing contact
-- -------------------------------------------------------------
CREATE OR REPLACE PROCEDURE add_phone(
    p_first  VARCHAR,
    p_last   VARCHAR,
    p_phone  VARCHAR,
    p_type   VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Type must be home, work, or mobile. Got: %', p_type;
    END IF;

    SELECT id INTO v_id
    FROM   phonebook
    WHERE  LOWER(first_name) = LOWER(TRIM(p_first))
      AND  LOWER(last_name)  = LOWER(TRIM(p_last))
    LIMIT  1;

    IF v_id IS NULL THEN
        RAISE EXCEPTION 'Contact "% %" not found.', p_first, p_last;
    END IF;

    IF EXISTS (
        SELECT 1 FROM phones WHERE contact_id = v_id AND phone = TRIM(p_phone)
    ) THEN
        RAISE NOTICE 'Phone "%" already exists for "% %". Skipping.', p_phone, p_first, p_last;
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, TRIM(p_phone), p_type);

    RAISE NOTICE 'Added "%" (%) to "% %".', p_phone, p_type, p_first, p_last;
END;
$$;


-- -------------------------------------------------------------
-- 2.  move_to_group  –  assign contact to a group (create if new)
-- -------------------------------------------------------------
CREATE OR REPLACE PROCEDURE move_to_group(
    p_first      VARCHAR,
    p_last       VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    -- Upsert group
    INSERT INTO groups (name)
    VALUES (TRIM(p_group_name))
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM   groups
    WHERE  LOWER(name) = LOWER(TRIM(p_group_name));

    -- Find contact
    SELECT id INTO v_contact_id
    FROM   phonebook
    WHERE  LOWER(first_name) = LOWER(TRIM(p_first))
      AND  LOWER(last_name)  = LOWER(TRIM(p_last))
    LIMIT  1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "% %" not found.', p_first, p_last;
    END IF;

    UPDATE phonebook SET group_id = v_group_id WHERE id = v_contact_id;

    RAISE NOTICE '"% %" moved to group "%".', p_first, p_last, p_group_name;
END;
$$;


-- -------------------------------------------------------------
-- 3.  search_contacts  –  extends P8 search_pattern to also
--     match email and all rows in the phones table
-- -------------------------------------------------------------
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id         INTEGER,
    first_name VARCHAR,
    last_name  VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    grp        VARCHAR,
    phones     TEXT,
    created_at TIMESTAMP
)
LANGUAGE plpgsql AS $$
DECLARE
    v_pat TEXT := '%' || LOWER(TRIM(p_query)) || '%';
BEGIN
    RETURN QUERY
    SELECT
        pb.id,
        pb.first_name,
        pb.last_name,
        pb.email,
        pb.birthday,
        g.name  AS grp,
        STRING_AGG(
            ph.phone || ' (' || COALESCE(ph.type, '?') || ')',
            ', ' ORDER BY ph.id
        )       AS phones,
        pb.created_at
    FROM  phonebook pb
    LEFT JOIN groups  g  ON g.id  = pb.group_id
    LEFT JOIN phones  ph ON ph.contact_id = pb.id
    WHERE
        LOWER(pb.first_name) LIKE v_pat OR
        LOWER(pb.last_name)  LIKE v_pat OR
        LOWER(pb.email)      LIKE v_pat OR
        LOWER(ph.phone)      LIKE v_pat
    GROUP BY pb.id, pb.first_name, pb.last_name, pb.email,
             pb.birthday, g.name, pb.created_at
    ORDER BY pb.last_name, pb.first_name;
END;
$$;