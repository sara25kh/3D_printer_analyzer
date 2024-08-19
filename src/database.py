import sqlite3

def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

def init_test_table(test_name, test_params):
    print("test_params", test_params)
    conn = create_connection()
    cursor = conn.cursor()
    cols = ""
    for k in test_params.keys():
        cols += f"{k} INTEGER, "
    cols += "profile_name TEXT"
    print('k:',cols)
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {test_name}
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      {cols})''')
    conn.commit()
    conn.close()


