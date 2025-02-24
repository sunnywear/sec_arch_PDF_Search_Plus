import sqlite3

# Database setup
def create_database(db_name="pdf_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Enable foreign key constraint enforcement (necessary in SQLite)
    cursor.execute("PRAGMA foreign_keys = ON")

    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pdf_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pdf_id INTEGER,
            page_number INTEGER,
            text TEXT,
            FOREIGN KEY(pdf_id) REFERENCES pdf_files(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pdf_id INTEGER,
            page_number INTEGER,
            image_name TEXT,
            image_ext TEXT,
            FOREIGN KEY(pdf_id) REFERENCES pdf_files(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ocr_text (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pdf_id INTEGER,
            page_number INTEGER,
            ocr_text TEXT,
            FOREIGN KEY(pdf_id) REFERENCES pdf_files(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE VIEW summary AS
        SELECT 
            f.file_name || '.pdf' AS file_name,
            GROUP_CONCAT(
                COALESCE(p.text, '') || ' ' || COALESCE(o.ocr_text, ''), 
                ' '
            ) AS combined_text
        FROM 
            pdf_files f
        LEFT JOIN 
            pages p ON f.id = p.pdf_id
        LEFT JOIN 
            ocr_text o ON f.id = o.pdf_id AND p.page_number = o.page_number
        GROUP BY 
            f.file_name
    ''')

    conn.commit()
    conn.close()
    print("Database and tables created successfully with foreign key constraints.")

# Run the function to create the database and tables
if __name__ == "__main__":
    create_database()
