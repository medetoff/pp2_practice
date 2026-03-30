-- Procedure 1: insert or update one user
CREATE OR REPLACE PROCEDURE insert_user(
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    cnumber VARCHAR(15),
    email VARCHAR(511),
    extra_info VARCHAR(255)
)
LANGUAGE plpgsql
AS $$
DECLARE
    existing_id INT;
BEGIN
    SELECT contact_id
    INTO existing_id
    FROM contacts
    WHERE contact_first_name = first_name
      AND (
            (contact_last_name = last_name)
            OR (contact_last_name IS NULL AND last_name IS NULL)
          );

    IF FOUND THEN
        UPDATE contacts
        SET contact_number = cnumber,
            contact_email = email,
            contact_extra_info = extra_info
        WHERE contact_id = existing_id;
    ELSE
        INSERT INTO contacts(
            contact_first_name,
            contact_last_name,
            contact_number,
            contact_email,
            contact_extra_info
        )
        VALUES (first_name, last_name, cnumber, email, extra_info);
    END IF;
END;
$$;


-- Safe creation of composite type
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_type
        WHERE typname = 'user_type'
    ) THEN
        CREATE TYPE user_type AS (
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            phone_number VARCHAR(15),
            email VARCHAR(511),
            extra_info VARCHAR(255)
        );
    END IF;
END $$;


-- Procedure 2: multiple insertion through array
CREATE OR REPLACE PROCEDURE multiple_insertion(users user_type[])
LANGUAGE plpgsql
AS $$
DECLARE
    u user_type;
    invalid_users user_type[] := '{}';
BEGIN
    FOREACH u IN ARRAY users LOOP
        -- validate phone: only digits, length 5..15
        IF u.phone_number IS NULL OR u.phone_number !~ '^[0-9]{5,15}$' THEN
            invalid_users := array_append(invalid_users, u);
            CONTINUE;
        END IF;

        IF EXISTS (
            SELECT 1
            FROM contacts
            WHERE contact_first_name = u.first_name
              AND (
                    (contact_last_name = u.last_name)
                    OR (contact_last_name IS NULL AND u.last_name IS NULL)
                  )
        ) THEN
            UPDATE contacts
            SET contact_number = u.phone_number,
                contact_email = u.email,
                contact_extra_info = u.extra_info
            WHERE contact_first_name = u.first_name
              AND (
                    (contact_last_name = u.last_name)
                    OR (contact_last_name IS NULL AND u.last_name IS NULL)
                  );
        ELSE
            INSERT INTO contacts(
                contact_first_name,
                contact_last_name,
                contact_number,
                contact_email,
                contact_extra_info
            )
            VALUES (
                u.first_name,
                u.last_name,
                u.phone_number,
                u.email,
                u.extra_info
            );
        END IF;
    END LOOP;

    IF array_length(invalid_users, 1) > 0 THEN
        RAISE NOTICE '[Warning]: Invalid users: %', invalid_users;
    END IF;
END;
$$;


-- Procedure 3: Delete user by user_name or phone_number
CREATE OR REPLACE PROCEDURE delete_user(
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(15)
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE (contact_first_name = first_name AND contact_last_name = last_name)
           OR (contact_number = phone_number)
    ) THEN
        DELETE FROM contacts
        WHERE (contact_first_name = first_name AND contact_last_name = last_name)
           OR (contact_number = phone_number);
    ELSE
        RAISE NOTICE '[Error] The contact with first_name %, last_name % and phone_number % not found',
            first_name, last_name, phone_number;
    END IF;
END;
$$;