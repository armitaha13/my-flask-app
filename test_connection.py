# test_connection.py (Version 3 using PyMySQL)
import pymysql
from pymysql import Error

# --- اطلاعات اتصال خود را اینجا وارد کن ---
db_host = "localhost"
db_user = "root"
db_password = "4142431234"  # <--- رمز صحیح را اینجا بگذار
db_name = "dental_clinic"
# ---------------------------------------------------------

try:
    print("--- 1. Attempting to connect using PyMySQL...")
    
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    print("--- 2. Connection object created.")
    
    with connection.cursor() as db_cursor:
        db_cursor.execute("SELECT DATABASE();")
        record = db_cursor.fetchone()
        print(f"--- 3. You are connected to database: {record[0]}")
        print("\n✅✅✅ SUCCESS! PyMySQL connected successfully! ✅✅✅")

except Error as e:
    print(f"\n❌❌❌ FAILED to connect with PyMySQL. Error: ❌❌❌")
    print(e)

finally:
    if 'connection' in locals() and connection.open:
        connection.close()
        print("\n--- Connection closed. ---")