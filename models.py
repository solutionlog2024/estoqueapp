import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='solution_bi.mysql.dbaas.com.br',
            database='solution_bi',
            user='solution_bi',
        password='J3aQqCZ5j32Eq@'
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def add_log_entry(barcode):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO log_entries (barcode, timestamp) VALUES (%s, NOW())', (barcode,))
        conn.commit()
        cursor.close()
        conn.close()

def get_all_log_entries():
    conn = get_db_connection()
    entries = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM log_entries ORDER BY timestamp DESC')
        entries = cursor.fetchall()
        cursor.close()
        conn.close()
    return entries

def delete_log_entry(entry_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM log_entries WHERE id = %s', (entry_id,))
        conn.commit()
        cursor.close()
        conn.close()

def update_log_entry(entry_id, new_barcode):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE log_entries SET barcode = %s WHERE id = %s', (new_barcode, entry_id))
        conn.commit()
        cursor.close()
        conn.close()