import sqlite3
"""basic SQLITE Database with add, delete, search, update, and display features. uses
    context manager (with) and Parameterized Statements in appropiate places.
     uses errer handling as well"""

db = 'record_db.sqlite' 


def create_table():
    try:
        with sqlite3.connect(db) as conn:# connect to the database file or create one if it doesn't exist
            conn.execute('CREATE TABLE IF NOT EXISTS records (Name text, Country text, Catches integer)')
    except sqlite3.Error as e:
        print(f'error creating table because {e}')
    finally:
        conn.close()

 # this function adds       
def add_test_data():
    records_info = [("Janne Mustonen", "Finland", 98),
                ("Ian Stewart", "Canada", 94),
                ("Aoron Gregg", "Canada", 88),
                ("Chad Taylor", "USA", 78)]
    try:
        with sqlite3.connect(db) as conn:
            conn.executemany('INSERT INTO records VALUES (?, ?, ?)', records_info)
    except sqlite3.Error:
        print('Error adding rows')
    finally:
        conn.close()

def add_record():
    name = input("Enter a new record holder name? ")
    country = input("Enter the country they representing? ")
    number_of_catches = int(input("Enter number of catches? "))
        
    try:
        with sqlite3.connect(db) as conn: 
            conn.execute('INSERT INTO records VALUES (?, ?, ?)', (name, country, number_of_catches))
    except sqlite3.Error:
        print('Error adding rows')
    finally:
        conn.close()

def search_record():
    holder_name = input("Enter record holder name to be searched ? ")
    try:
        conn = sqlite3.connect(db)
        res = conn.execute('SELECT * FROM records WHERE name = ?', (holder_name, ))
        first_row = res.fetchone()
        if first_row:
            print(first_row)
        else:
            print("Name Not found ")
    except sqlite3.Error as e:
        print('Error searching rows', e)
    finally:
        conn.close()

def update_record():
    row_id = int(input("Enter row ID to be updated "))
    num_of_catches = int(input("Enter the number of catches "))

    try:
        conn = sqlite3.connect(db)
        updated = conn.execute('UPDATE records SET Catches = ? WHERE rowid = ?', (num_of_catches, row_id, ))
        rows_modified = updated.rowcount
        if rows_modified == 0:
            print("no rows has been updated")
    except sqlite3.Error as e:
        print('Error updating', e)
    finally:
        conn.commit()
        conn.close()
def delete_record():
    holder_name = input("Enter record holder name to be deleted ")

    try:
        conn = sqlite3.connect(db)
        deleted = conn.execute('DELETE FROM records WHERE name = ?', (holder_name, ))
        deleted_count = deleted.rowcount
        if deleted_count == 0:
            print("no data has been deleted")
    except sqlite3.Error as e:
        print('Error deleting', e)
    finally:
        conn.commit()
        conn.close()

def display_all():
    try:
        conn = sqlite3.connect(db)
        all_rows = conn.execute('SELECT * FROM records')
        for row in all_rows:
            name, country, catches = row
            print(name, "| ", country, "| ", catches)
    except sqlite3.Error as e:
        print('Error deleting', e)
    finally:
        conn.commit()
        conn.close()


def main():
    create_table()
    add_test_data()
    add_record()
    search_record()
    update_record()
    delete_record()
    display_all()

main()