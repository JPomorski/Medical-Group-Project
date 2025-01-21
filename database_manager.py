import sqlite3
import os

# def add_data():
#     db_path = os.path.join('instance', 'database.db')
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#
#
#     # Commit changes and close connection
#     conn.commit()
#     conn.close()

def delete_data():
    db_path = os.path.join('instance', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE patient')
    #cursor.execute('DROP TABLE svg_record')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    delete_data()