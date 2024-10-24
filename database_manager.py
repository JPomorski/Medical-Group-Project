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

# kod do czyszczenia bazy danych
def delete_data():
    db_path = os.path.join('instance', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Usuń starą tabelę
    cursor.execute('DROP TABLE patient')

    # Zatwierdź zmiany i zamknij połączenie
    conn.commit()
    conn.close()

if __name__ == '__main__':
    delete_data()