import sqlite3

def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

def init_test_table(test_name, test_params):
    print("test_params", test_params)
    conn = create_connection()
    cursor = conn.cursor()
    
    # Create columns definition
    cols = ""
    for k in test_params.keys():
        if k != "profile_name":
            cols += f"{k} TEXT, "
    # Make profile_name the primary key
    cols += "profile_name TEXT PRIMARY KEY"
    
    print('cols:', cols)
    
    # Create table with profile_name as the primary key
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {test_name}
                      ({cols})''')
    
    conn.commit()
    conn.close()


def insert_row(test_name, row_data):
    conn = create_connection()
    cursor = conn.cursor()

    # Extract the column names and values from the dictionary
    columns = ', '.join(row_data.keys())
    placeholders = ', '.join(['?' for _ in row_data])
    values = tuple(row_data.values())

    profile_name = row_data.get("profile_name")

    # Check if the profile_name already exists
    cursor.execute(f"SELECT COUNT(1) FROM {test_name} WHERE profile_name = ?", (profile_name,))
    exists = cursor.fetchone()[0]

    try:
        if exists:
            # If the profile_name exists, update the row
            update_columns = ', '.join([f"{k} = ?" for k in row_data.keys()])
            values = tuple(row_data.values()) + (profile_name,)
            print("update_columns:", update_columns)
            print("values:", values)
            cursor.execute(f"UPDATE {test_name} SET {update_columns} WHERE profile_name = ?", values)
            print(f"Updated row with profile_name: {profile_name}")
        else:
            # If the profile_name does not exist, insert a new row
            columns = ', '.join(row_data.keys())
            placeholders = ', '.join(['?' for _ in row_data])
            values = tuple(row_data.values())
            cursor.execute(f"INSERT INTO {test_name} ({columns}) VALUES ({placeholders})", values)
            print(f"Inserted new row with profile_name: {profile_name}")


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.commit()
        conn.close()


def delete_row(test_name, profile_name):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Check if the profile_name exists
        cursor.execute(f"SELECT COUNT(1) FROM {test_name} WHERE profile_name = ?", (profile_name,))
        exists = cursor.fetchone()[0]

        if exists:
            # Delete the row where profile_name matches
            cursor.execute(f"DELETE FROM {test_name} WHERE profile_name = ?", (profile_name,))
            print(f"Deleted row with profile_name: {profile_name}")
        else:
            print(f"No row found with profile_name: {profile_name}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.commit()
        conn.close()


def fetch_test_data(test_name):
    conn = create_connection()
    cursor = conn.cursor()
    
    # Fetch the column names
    cursor.execute(f"PRAGMA table_info({test_name})")
    columns = [col[1] for col in cursor.fetchall()]

    # Fetch all rows from the table
    cursor.execute(f"SELECT * FROM {test_name}")
    rows = cursor.fetchall()

    # Convert each row to a dictionary using column names as keys
    data = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return data




