import csv
import json
import os

import psycopg2

from connect import connect

# ── connection (autocommit on, same as P8) ───────────────────
conn = connect()
cur  = conn.cursor()


# ── apply schema + new procedures ────────────────────────────
def init_schema():
    base = os.path.dirname(os.path.abspath(__file__))
    for fname in ('schema.sql', 'procedures.sql'):
        path = os.path.join(base, fname)
        if not os.path.exists(path):
            print(f'File not found: {fname}')
            continue
        with open(path, 'r', encoding='utf-8') as f:
            cur.execute(f.read())
        print(f'Applied {fname}')


# ─────────────────────────────────────────────────────────────
# Helper: pretty-print rows from search_contacts()
# ─────────────────────────────────────────────────────────────
def print_rows(rows):
    if not rows:
        print('  (no results)')
        return
    bar = '-' * 64
    print(bar)
    for r in rows:
        # r = (id, first_name, last_name, email, birthday, grp, phones, created_at)
        print(f'  ID       : {r[0]}')
        print(f'  Name     : {r[1]} {r[2]}')
        print(f'  Email    : {r[3] or "—"}')
        print(f'  Birthday : {r[4] or "—"}')
        print(f'  Group    : {r[5] or "—"}')
        print(f'  Phones   : {r[6] or "—"}')
        print(f'  Added    : {r[7].strftime("%Y-%m-%d %H:%M") if r[7] else "—"}')
        print(bar)


# ─────────────────────────────────────────────────────────────
# 3.2  Filter / sort / paginate
# ─────────────────────────────────────────────────────────────
def filter_by_group():
    cur.execute('SELECT name FROM groups ORDER BY name')
    groups = [row[0] for row in cur.fetchall()]
    if not groups:
        print('No groups in database.')
        return
    print('Available groups:', ', '.join(groups))
    term = input('Group name (or part): ').strip()
    cur.execute("""
        SELECT pb.id, pb.first_name, pb.last_name, pb.email, pb.birthday,
               g.name,
               STRING_AGG(ph.phone || ' (' || COALESCE(ph.type,'?') || ')', ', ' ORDER BY ph.id),
               pb.created_at
        FROM   phonebook pb
        LEFT JOIN groups  g  ON g.id = pb.group_id
        LEFT JOIN phones  ph ON ph.contact_id = pb.id
        WHERE  LOWER(g.name) LIKE %s
        GROUP  BY pb.id, pb.first_name, pb.last_name, pb.email,
                  pb.birthday, g.name, pb.created_at
        ORDER  BY pb.last_name, pb.first_name
    """, (f'%{term.lower()}%',))
    print_rows(cur.fetchall())


def search_by_email():
    term = input('Email search term: ').strip()
    cur.execute("""
        SELECT pb.id, pb.first_name, pb.last_name, pb.email, pb.birthday,
               g.name,
               STRING_AGG(ph.phone || ' (' || COALESCE(ph.type,'?') || ')', ', ' ORDER BY ph.id),
               pb.created_at
        FROM   phonebook pb
        LEFT JOIN groups  g  ON g.id = pb.group_id
        LEFT JOIN phones  ph ON ph.contact_id = pb.id
        WHERE  LOWER(pb.email) LIKE %s
        GROUP  BY pb.id, pb.first_name, pb.last_name, pb.email,
                  pb.birthday, g.name, pb.created_at
        ORDER  BY pb.last_name
    """, (f'%{term.lower()}%',))
    print_rows(cur.fetchall())


def list_sorted():
    print('Sort by:  1 - Last name   2 - Birthday   3 - Date added')
    choice = input('>> ').strip()
    order = {
        '1': 'pb.last_name, pb.first_name',
        '2': 'pb.birthday NULLS LAST',
        '3': 'pb.created_at',
    }.get(choice, 'pb.last_name, pb.first_name')

    cur.execute(f"""
        SELECT pb.id, pb.first_name, pb.last_name, pb.email, pb.birthday,
               g.name,
               STRING_AGG(ph.phone || ' (' || COALESCE(ph.type,'?') || ')', ', ' ORDER BY ph.id),
               pb.created_at
        FROM   phonebook pb
        LEFT JOIN groups  g  ON g.id = pb.group_id
        LEFT JOIN phones  ph ON ph.contact_id = pb.id
        GROUP  BY pb.id, pb.first_name, pb.last_name, pb.email,
                  pb.birthday, g.name, pb.created_at
        ORDER  BY {order}
    """)
    print_rows(cur.fetchall())


def paginated_browse():
    """
    Console page-by-page browser.
    Uses the existing get_paginated() function from Practice 8.
    """
    PAGE = 5
    page = 0
    while True:
        offset = page * PAGE
        try:
            cur.execute('SELECT * FROM get_paginated(%s, %s)', (PAGE, offset))
        except psycopg2.errors.UndefinedFunction:
            print('get_paginated() not found — run Practice 8 SQL first.')
            return
        rows = cur.fetchall()

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'--- Page {page + 1}  (rows {offset + 1}–{offset + len(rows)}) ---')
        if rows:
            for r in rows:
                print(r)
        else:
            print('  (end of contacts)')

        nav = input('\n[n]ext  [p]rev  [q]uit >> ').strip().lower()
        if nav == 'q':
            break
        elif nav == 'n':
            if len(rows) < PAGE:
                print('Already on the last page.')
                input('Press Enter…')
            else:
                page += 1
        elif nav == 'p':
            if page == 0:
                print('Already on the first page.')
                input('Press Enter…')
            else:
                page -= 1


# ─────────────────────────────────────────────────────────────
# 3.3  Import / Export
# ─────────────────────────────────────────────────────────────
def export_to_json():
    filename = input('Output filename [contacts_export.json]: ').strip() or 'contacts_export.json'
    cur.execute("""
        SELECT
            pb.first_name, pb.last_name, pb.email,
            TO_CHAR(pb.birthday, 'YYYY-MM-DD') AS birthday,
            g.name AS grp,
            COALESCE(
                JSON_AGG(
                    JSON_BUILD_OBJECT('phone', ph.phone, 'type', ph.type)
                    ORDER BY ph.id
                ) FILTER (WHERE ph.id IS NOT NULL),
                '[]'::json
            ) AS phone_list,
            pb.created_at
        FROM  phonebook pb
        LEFT JOIN groups  g  ON g.id = pb.group_id
        LEFT JOIN phones  ph ON ph.contact_id = pb.id
        GROUP BY pb.id, pb.first_name, pb.last_name, pb.email,
                 pb.birthday, g.name, pb.created_at
        ORDER BY pb.last_name, pb.first_name
    """)
    rows = cur.fetchall()

    records = []
    for r in rows:
        records.append({
            'first_name': r[0],
            'last_name':  r[1],
            'email':      r[2],
            'birthday':   r[3],
            'group':      r[4],
            'phones':     r[5],
            'created_at': r[6].isoformat() if r[6] else None,
        })

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f'Exported {len(records)} contact(s) → {filename}')


def import_from_json():
    filename = input('JSON file to import [contacts_export.json]: ').strip() or 'contacts_export.json'
    if not os.path.exists(filename):
        print(f'File not found: {filename}')
        return

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    inserted = skipped = overwritten = 0
    for entry in data:
        first    = (entry.get('first_name') or '').strip()
        last     = (entry.get('last_name')  or '').strip()
        email    = entry.get('email')    or None
        birthday = entry.get('birthday') or None
        grp_name = entry.get('group')    or None
        phones   = entry.get('phones')   or []

        if not first or not last:
            print(f'  Skipping entry with no name: {entry}')
            skipped += 1
            continue

        cur.execute(
            'SELECT id FROM phonebook WHERE LOWER(first_name)=LOWER(%s) AND LOWER(last_name)=LOWER(%s)',
            (first, last)
        )
        existing = cur.fetchone()

        if existing:
            ans = input(f"  '{first} {last}' exists.  [s]kip / [o]verwrite? ").strip().lower()
            if ans != 'o':
                skipped += 1
                continue
            contact_id = existing[0]
            cur.execute(
                'UPDATE phonebook SET email=%s, birthday=%s WHERE id=%s',
                (email, birthday, contact_id)
            )
            cur.execute('DELETE FROM phones WHERE contact_id=%s', (contact_id,))
            overwritten += 1
        else:
            cur.execute(
                'INSERT INTO phonebook (first_name, last_name, email, birthday) VALUES (%s,%s,%s,%s) RETURNING id',
                (first, last, email, birthday)
            )
            contact_id = cur.fetchone()[0]
            inserted += 1

        # resolve group
        if grp_name:
            cur.execute('INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING', (grp_name,))
            cur.execute('SELECT id FROM groups WHERE LOWER(name)=LOWER(%s)', (grp_name,))
            gid = cur.fetchone()[0]
            cur.execute('UPDATE phonebook SET group_id=%s WHERE id=%s', (gid, contact_id))

        # insert phones
        for ph in phones:
            if isinstance(ph, dict):
                pnum  = (ph.get('phone') or '').strip()
                ptype = ph.get('type') or 'mobile'
            else:
                pnum  = str(ph).strip()
                ptype = 'mobile'
            if pnum:
                cur.execute(
                    'INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)',
                    (contact_id, pnum, ptype)
                )

    print(f'JSON import done — inserted: {inserted}, overwritten: {overwritten}, skipped: {skipped}')


def import_from_csv():
    filename = input('CSV file to import [contacts.csv]: ').strip() or 'contacts.csv'
    if not os.path.exists(filename):
        print(f'File not found: {filename}')
        return

    # Expected columns: first_name,last_name,email,birthday,group,phone,phone_type
    inserted = phones_added = errors = 0
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            first      = (row.get('first_name') or '').strip()
            last       = (row.get('last_name')  or '').strip()
            email      = (row.get('email')      or '').strip() or None
            birthday   = (row.get('birthday')   or '').strip() or None
            grp_name   = (row.get('group')      or '').strip() or None
            phone_num  = (row.get('phone')      or '').strip() or None
            phone_type = (row.get('phone_type') or 'mobile').strip().lower()

            if not first or not last:
                print(f'  Skipping row (missing name): {row}')
                errors += 1
                continue

            if phone_type not in ('home', 'work', 'mobile'):
                phone_type = 'mobile'

            # upsert contact
            cur.execute(
                'SELECT id FROM phonebook WHERE LOWER(first_name)=LOWER(%s) AND LOWER(last_name)=LOWER(%s)',
                (first, last)
            )
            existing = cur.fetchone()

            if existing:
                contact_id = existing[0]
                # fill in missing fields only
                cur.execute("""
                    UPDATE phonebook
                    SET email    = COALESCE(email,    %s),
                        birthday = COALESCE(birthday, %s)
                    WHERE id = %s
                """, (email, birthday, contact_id))
            else:
                cur.execute(
                    'INSERT INTO phonebook (first_name, last_name, email, birthday) VALUES (%s,%s,%s,%s) RETURNING id',
                    (first, last, email, birthday)
                )
                contact_id = cur.fetchone()[0]
                inserted += 1

            # resolve group
            if grp_name:
                cur.execute('INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING', (grp_name,))
                cur.execute('SELECT id FROM groups WHERE LOWER(name)=LOWER(%s)', (grp_name,))
                gid = cur.fetchone()[0]
                cur.execute('UPDATE phonebook SET group_id=%s WHERE id=%s', (gid, contact_id))

            # insert phone if not duplicate
            if phone_num:
                cur.execute(
                    'SELECT 1 FROM phones WHERE contact_id=%s AND phone=%s',
                    (contact_id, phone_num)
                )
                if not cur.fetchone():
                    cur.execute(
                        'INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)',
                        (contact_id, phone_num, phone_type)
                    )
                    phones_added += 1

    print(f'CSV import done — new contacts: {inserted}, phones added: {phones_added}, errors: {errors}')


# ─────────────────────────────────────────────────────────────
# 3.4  Stored-procedure callers
# ─────────────────────────────────────────────────────────────
def add_phone():
    first = input('First name: ').strip()
    last  = input('Last name : ').strip()
    phone = input('Phone     : ').strip()
    ptype = input('Type [home/work/mobile] (default mobile): ').strip().lower() or 'mobile'
    try:
        cur.execute('CALL add_phone(%s, %s, %s, %s)', (first, last, phone, ptype))
        print('Done.')
    except psycopg2.Error as e:
        print(f'DB error: {e}')


def move_to_group():
    first = input('First name    : ').strip()
    last  = input('Last name     : ').strip()
    group = input('Destination group: ').strip()
    try:
        cur.execute('CALL move_to_group(%s, %s, %s)', (first, last, group))
        print('Done.')
    except psycopg2.Error as e:
        print(f'DB error: {e}')


def search_contacts():
    query = input('Search (name / email / phone): ').strip()
    try:
        cur.execute('SELECT * FROM search_contacts(%s)', (query,))
        print_rows(cur.fetchall())
    except psycopg2.Error as e:
        print(f'DB error: {e}')


def delete_contact():
    print('Удалить по:  1 - Имени   2 - Фамилии   3 - Номеру телефона')
    choice = input('>> ').strip()

    if choice == '1':
        val = input('Введи имя: ').strip()
    elif choice == '2':
        val = input('Введи фамилию: ').strip()
    elif choice == '3':
        val = input('Введи номер: ').strip()
    else:
        print('Неверный выбор.')
        return

    if not val:
        return

    # показать что найдено перед удалением
    cur.execute(
        'SELECT id, first_name, last_name, phone FROM phonebook '
        'WHERE first_name=%s OR last_name=%s OR phone=%s',
        (val, val, val)
    )
    found = cur.fetchall()
    if not found:
        print(f'Контакт "{val}" не найден.')
        return

    print(f'\nБудет удалено ({len(found)} шт.):')
    for r in found:
        print(f'  [{r[0]}] {r[1]} {r[2]}  {r[3]}')

    confirm = input('\nТочно удалить? [y/n]: ').strip().lower()
    if confirm != 'y':
        print('Отменено.')
        return

    try:
        cur.execute('CALL delete_user(%s)', (val,))
        print(f'Удалено: {len(found)} контакт(ов).')
    except psycopg2.Error as e:
        print(f'DB error: {e}')


# ─────────────────────────────────────────────────────────────
# Main menu
# ─────────────────────────────────────────────────────────────
init_schema()   # apply schema.sql + procedures.sql on startup

while True:
    print("""
MENU
 0  Initialise / re-apply schema & procedures
--- Search & Filter ---
 1  Filter by group
 2  Search by email
 3  List all (sorted)
 4  Browse page by page
--- Import / Export ---
 5  Export to JSON
 6  Import from JSON
 7  Import from CSV
--- Stored Procedures ---
 8  Add phone number to contact
 9  Move contact to group
10  Search contacts (name / email / phone)
11  Delete contact
 q  Quit""")

    choice = input('>> ').strip().lower()

    if   choice == '0':  init_schema()
    elif choice == '1':  filter_by_group()
    elif choice == '2':  search_by_email()
    elif choice == '3':  list_sorted()
    elif choice == '4':  paginated_browse()
    elif choice == '5':  export_to_json()
    elif choice == '6':  import_from_json()
    elif choice == '7':  import_from_csv()
    elif choice == '8':  add_phone()
    elif choice == '9':  move_to_group()
    elif choice == '10': search_contacts()
    elif choice == '11': delete_contact()
    elif choice == 'q':
        break
    else:
        print('Unknown option.')

cur.close()
conn.close()