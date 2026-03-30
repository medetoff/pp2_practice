-- Function 1: Search rows by pattern
CREATE OR REPLACE FUNCTION get_by_pattern(pattern_type TEXT, pattern TEXT)
RETURNS TABLE(
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(15),
    extra_info VARCHAR(255)
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF pattern_type = 'first_name' THEN
        RETURN QUERY
        SELECT contact_first_name, contact_last_name, contact_number, contact_extra_info
        FROM contacts
        WHERE contact_first_name ILIKE '%' || pattern || '%';

    ELSIF pattern_type = 'last_name' THEN
        RETURN QUERY
        SELECT contact_first_name, contact_last_name, contact_number, contact_extra_info
        FROM contacts
        WHERE contact_last_name ILIKE '%' || pattern || '%';

    ELSIF pattern_type = 'number' THEN
        RETURN QUERY
        SELECT contact_first_name, contact_last_name, contact_number, contact_extra_info
        FROM contacts
        WHERE contact_number ILIKE '%' || pattern || '%';

    ELSE
        RAISE NOTICE '[Error]: Invalid attribute_type!';
    END IF;
END;
$$;


-- Function 2: Pagination
CREATE OR REPLACE FUNCTION query_pagination(rows_per_page INT, page_number INT)
RETURNS TABLE(
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(15),
    email VARCHAR(511),
    extra_info VARCHAR(255)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT contact_first_name, contact_last_name, contact_number, contact_email, contact_extra_info
    FROM contacts
    ORDER BY contact_id
    LIMIT rows_per_page
    OFFSET (page_number - 1) * rows_per_page;
END;
$$;