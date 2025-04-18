import sqlite3
import os
import random

def corrupt_db(path='test.db'):
    # Create a test database
    conn = sqlite3.connect(path)
    c = conn.cursor()
    try:
        # Create a test table
        c.execute('''CREATE TABLE IF NOT EXISTS test
                     (id INTEGER PRIMARY KEY, data TEXT)''')
        conn.commit()
        
        # Insert some test data
        for i in range(100):
            c.execute("INSERT INTO test (data) VALUES (?)", (f"test_data_{i}",))
        conn.commit()
        conn.close()
        
        # Corrupt the database file
        with open(path, 'r+b') as f:
            # Seek to random positions and write random bytes
            for _ in range(10):
                pos = random.randint(0, os.path.getsize(path))
                f.seek(pos)
                f.write(os.urandom(10))
        
        # Try to read from corrupted database
        try:
            conn = sqlite3.connect(path)
            c = conn.cursor()
            c.execute("SELECT * FROM test LIMIT 5")
            print("Database still readable (unexpected)")
        except sqlite3.DatabaseError as e:
            print(f"Caught expected DB corruption: {e}")
        
    except Exception as e:
        print(f"Test setup error: {e}")
    finally:
        try:
            conn.close()
        except:
            pass
        # Clean up test database
        if os.path.exists(path):
            os.remove(path)