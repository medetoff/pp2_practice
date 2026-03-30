import psycopg2
import csv
from psycopg2 import sql
from config import load_config

allowed_search_attributes = ['first_name', 'last_name', 'number']
allowed_attributes = [
    'contact_id',
    'contact_first_name',
    'contact_last_name',
    'contact_number',
    'contact_email',
    'contact_extra_info'
]
allowed_sort_types = ['asc', 'desc', '']


def load_sql_files():
    config = load_config()
    conn = None
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                for file in ['functions.sql', 'procedures.sql']:
                    with open(file, 'r', encoding='utf-8') as f:
                        cursor.execute(f.read())
            conn.commit()
        print("[Success] SQL files loaded successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        if conn:
            conn.rollback()
        print("[Error loading SQL files]:", error)


# =========================
# INSERTION
# =========================
def insert_contact(contact: dict):
    config = load_config()
    conn = None
    new_id = None

    try:
        sql_query = """
            INSERT INTO contacts(
                contact_first_name,
                contact_last_name,
                contact_number,
                contact_email,
                contact_extra_info
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING contact_id;
        """

        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query, (
                    contact['first_name'],
                    contact.get('last_name', None),
                    contact['phone_number'],
                    contact.get('email', None),
                    contact.get('additional_info', None)
                ))
                new_id = cursor.fetchone()[0]
                print(f"[Success] Successfully inserted a contact with id: {new_id}")
            conn.commit()

    except Exception as error:
        if conn:
            conn.rollback()
        print("[Error]:", error)

    return new_id


def import_contacts_from_csv(csv_file_path):
    inserted_count = 0
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                new_id = insert_contact(row)
                if new_id is not None:
                    inserted_count += 1
                    print(f"[I] Inserted contact {row['first_name']} with ID {new_id}")

        print(f"[Success] Successfully inserted {inserted_count} contacts from CSV.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("[Error]:", error)


# =========================
# UPDATE
# =========================
def update_contact(contact_change_attribute, contact_new_info, contact_number=None, contact_first_name=None):
    config = load_config()
    conn = None
    updated_row_count = 0

    if contact_change_attribute not in allowed_attributes:
        print(f"[Error] Invalid attribute: {contact_change_attribute}")
        return 0

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                if contact_number is not None and contact_first_name is None:
                    query = sql.SQL("""
                        UPDATE contacts
                        SET {field} = %s
                        WHERE contact_number = %s
                    """).format(field=sql.Identifier(contact_change_attribute))
                    cursor.execute(query, (contact_new_info, contact_number))

                elif contact_first_name is not None and contact_number is None:
                    query = sql.SQL("""
                        UPDATE contacts
                        SET {field} = %s
                        WHERE contact_first_name = %s
                    """).format(field=sql.Identifier(contact_change_attribute))
                    cursor.execute(query, (contact_new_info, contact_first_name))
                else:
                    print("[Error] Provide either contact_number or contact_first_name.")
                    return 0

                updated_row_count = cursor.rowcount

            conn.commit()

            if updated_row_count == 0:
                print("[Error] There is no row updated. Make sure you inputted the data correctly!")
            else:
                print(f"[Success] Updated {contact_change_attribute} -> {contact_new_info}")

    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print("[Error]:", error)

    return updated_row_count


# =========================
# QUERY
# =========================
def get_info(filter_value, sort_key, sort_type, sort_aggregate_value):
    config = load_config()
    conn = None

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                if filter_value.lower() in ['*', 'all']:
                    if sort_key == '':
                        query = sql.SQL("SELECT * FROM contacts")
                        cursor.execute(query)
                    else:
                        if sort_key not in allowed_attributes or sort_type.lower() not in allowed_sort_types:
                            print("Key/type error.")
                            print("Allowed attributes:", *allowed_attributes)
                            print("Allowed sort_types:", *allowed_sort_types)
                            return

                        query = sql.SQL("SELECT * FROM contacts ORDER BY {field} {direction}").format(
                            field=sql.Identifier(sort_key),
                            direction=sql.SQL(sort_type.upper()) if sort_type else sql.SQL("")
                        )
                        cursor.execute(query)

                elif filter_value.lower() in allowed_attributes:
                    query = sql.SQL("SELECT * FROM contacts WHERE {field} = %s").format(
                        field=sql.Identifier(filter_value)
                    )
                    cursor.execute(query, (sort_aggregate_value,))
                else:
                    print("[Error]: Invalid filter.")
                    return

                rows = cursor.fetchall()
                print("The number of parts:", len(rows))
                for row in rows:
                    print(row)

    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print("[Error]:", error)


# =========================
# DELETE
# =========================
def delete_contact(first_name=None, number=None):
    config = load_config()
    conn = None

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                if first_name is not None and number is None:
                    sql_query = "DELETE FROM contacts WHERE contact_first_name = %s"
                    cursor.execute(sql_query, (first_name,))
                    deleted_row_count = cursor.rowcount

                    if deleted_row_count == 0:
                        print("[Error] No contact deleted. Please ensure you've typed the data correctly!")
                    else:
                        print(f"[Success] Successfully deleted row with first name '{first_name}'")

                elif number is not None and first_name is None:
                    sql_query = "DELETE FROM contacts WHERE contact_number = %s"
                    cursor.execute(sql_query, (number,))
                    deleted_row_count = cursor.rowcount

                    if deleted_row_count == 0:
                        print("[Error] No contact deleted. Please ensure you've typed the data correctly!")
                    else:
                        print(f"[Success] Successfully deleted row with number '{number}'")
                else:
                    print("[Error] Provide either first_name or number.")

            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print("[Error]:", error)


# =========================
# PRACTICE 8
# =========================
def insert_contact2(contact: dict):
    config = load_config()
    conn = None

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                first_name = contact['first_name']
                last_name = contact.get('last_name', None)
                phone_number = contact['phone_number']
                email = contact.get('email', None)
                extra_info = contact.get('additional_info', None)

                sql_query = "CALL insert_user(%s, %s, %s, %s, %s)"
                cursor.execute(sql_query, (first_name, last_name, phone_number, email, extra_info))

            conn.commit()
            print(f"[Success] The contact {first_name} {last_name} was inserted/updated!")

    except (psycopg2.DatabaseError, Exception) as error:
        if conn:
            conn.rollback()
        print("[Error]:", error)


def insert_multiple_contacts(users: list):
    config = load_config()
    conn = None

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                array_elements = []
                for u in users:
                    first_name = (u.get('first_name') or '').replace("'", "''")
                    last_name = (u.get('last_name') or '').replace("'", "''")
                    phone = (u.get('phone_number') or '').replace("'", "''")
                    email = (u.get('email') or '').replace("'", "''")
                    extra = (u.get('extra_info') or u.get('additional_info') or '').replace("'", "''")

                    array_elements.append(
                        f"ROW('{first_name}','{last_name}','{phone}','{email}','{extra}')::user_type"
                    )

                array_literal = "ARRAY[" + ",".join(array_elements) + "]"
                sql_query = f"CALL multiple_insertion({array_literal});"
                cursor.execute(sql_query)

            conn.commit()

            if conn.notices:
                print("\n[Server notices]")
                for notice in conn.notices:
                    print(notice)

            print(f"[Success] {len(users)} contacts processed via multiple_insertion procedure.")

    except (psycopg2.DatabaseError, Exception) as error:
        if conn:
            conn.rollback()
        print("[Error]:", error)


def delete_contact2(first_name, last_name, phone_number):
    config = load_config()
    conn = None

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = "CALL delete_user(%s, %s, %s)"
                cursor.execute(sql_query, (first_name, last_name, phone_number))
            conn.commit()

            if conn.notices:
                for notice in conn.notices:
                    print(notice.strip())
            else:
                print("[Success] Delete procedure executed successfully.")

    except (psycopg2.DatabaseError, Exception) as error:
        if conn:
            conn.rollback()
        print("[Error]:", error)


def search_by_pattern(pattern_type, pattern_value):
    config = load_config()
    conn = None

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = "SELECT * FROM get_by_pattern(%s, %s);"
                cursor.execute(sql_query, (pattern_type, pattern_value))
                rows = cursor.fetchall()

                print(f"Number of rows: {len(rows)}")
                if len(rows) == 0:
                    print("No data found or invalid attribute_type.")
                for row in rows:
                    print(row)

    except (psycopg2.DatabaseError, Exception) as error:
        if conn:
            conn.rollback()
        print("[Error]:", error)


def query_pagination(rows_per_page, page_index):
    config = load_config()
    conn = None

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql_query = "SELECT * FROM query_pagination(%s, %s);"
                cursor.execute(sql_query, (rows_per_page, page_index))
                rows = cursor.fetchall()

                print(f"Number of rows: {len(rows)}")
                for row in rows:
                    print(row)

    except (psycopg2.DatabaseError, Exception) as error:
        if conn:
            conn.rollback()
        print("[Error]:", error)


# =========================
# MAIN
# =========================
print("Welcome to the terminal of parsing data. Here you can insert, update, get information, search, paginate, or delete your contacts")

load_sql_files()

while True:
    contact = {}
    command = input("Insert a command (insert/update/get/search/page/delete/exit): ").lower()

    if command in ['insert', 'i']:
        insertion_type = input("Enter the type of insertion (csv - for csv, b - basic, m - multiple): ").lower()

        if insertion_type in ['', 'basic', 'b']:
            first_name = input("Input the first_name: ")
            if first_name == '':
                print("[Error] First name can't be empty!")
                continue

            last_name = input("Input the last_name (optional): ")
            phone_number = input("Input the phone_number: ")
            if phone_number == '':
                print("[Error] Phone number can't be empty!")
                continue

            email = input("Input the email (optional): ")
            additional_info = input("Input the additional information (optional): ")

            contact["first_name"] = first_name
            contact["last_name"] = last_name if last_name != '' else None
            contact["phone_number"] = phone_number
            contact["email"] = email if email != '' else None
            contact["additional_info"] = additional_info if additional_info != '' else None

            insert_contact2(contact)

        elif insertion_type in ['csv', 'c']:
            path = input("Input CSV file path: ")
            import_contacts_from_csv(path)

        elif insertion_type in ['multiple', 'm']:
            count = int(input("How many users do you want to insert? "))
            users = []

            for i in range(count):
                print(f"\nUser {i+1}")
                user = {
                    "first_name": input("First name: "),
                    "last_name": input("Last name: ") or None,
                    "phone_number": input("Phone number: "),
                    "email": input("Email: ") or None,
                    "extra_info": input("Extra info: ") or None
                }
                users.append(user)

            insert_multiple_contacts(users)

    elif command in ['update', 'u']:
        changing_attribute = input(
            f"Input which attribute (column) you want to change\nThe list of all attributes: {allowed_attributes[1:]}\n"
        )

        if changing_attribute not in allowed_attributes:
            print(f"[Error] Attribute {changing_attribute} not found.")
            continue

        new_value = input("Input a value you want to set: ")
        anchor_attribute = input("Choose by which attribute do you want to search (number/first name): ")

        if anchor_attribute.lower() in ["number", "num"]:
            phone_number = input("Now input a phone number: ")
            update_contact(changing_attribute, new_value, contact_number=phone_number, contact_first_name=None)

        elif anchor_attribute.lower() in ["first name", "first_name", "name"]:
            first_name = input("Now input a first name: ")
            update_contact(changing_attribute, new_value, contact_number=None, contact_first_name=first_name)

        else:
            print("[Error] Incorrect search attribute type!")

    elif command in ["get", "g"]:
        filter_value = input(
            f"Input the filter you want to apply\n'*' - displays all data\nOr, you can write attribute's name\nList of all attributes: {allowed_attributes}\n"
        ).lower()

        if filter_value == '':
            print("[Error] You didn't input the filter!")
            continue

        sort_key = input("Now, input a key by which your data will be sorted: ")
        sort_type = input("Input a type of sort (asc/desc): ").lower()
        sort_aggregation_value = input("Input a value that will specify and filter the data (optional): ")

        get_info(filter_value, sort_key, sort_type, sort_aggregation_value)

    elif command == "search":
        attribute = input("Input the attribute (first_name, last_name, or number): ")
        pattern_value = input("Input the search value: ")
        search_by_pattern(attribute, pattern_value)

    elif command == "page":
        rows_per_page = int(input("Input number of rows per page: "))
        page_index = int(input("Input page number: "))
        query_pagination(rows_per_page, page_index)

    elif command in ["delete", "d"]:
        first_name = input("Input first name: ") or None
        last_name = input("Input last name: ") or None
        number = input("Input phone number: ") or None
        delete_contact2(first_name, last_name, number)

    elif command in ["quit", "q", "exit"]:
        print("[Exit] Exiting the program...")
        break

    else:
        print("[Error] Wrong command! Please try again.")