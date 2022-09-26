from android_imports import MyAndroidImports


class CreateTable:
    android_imports = MyAndroidImports()

    notes_conn = android_imports.notes_conn
    cursor_notes = notes_conn.cursor()

    user_conn = android_imports.user_conn
    cursor_user = user_conn.cursor()

    deleted_conn = android_imports.deleted_conn
    cursor_deleted = deleted_conn.cursor()

    files_conn = android_imports.files_conn
    cursor_files = files_conn.cursor()

    def create_notes_table(self):
        sql = """CREATE TABLE IF NOT EXISTS notes (
            notes_id INTEGER PRIMARY KEY AUTOINCREMENT,
            notes_title TEXT NOT NULL, 
            notes_description TEXT NOT NULL

            )"""
        self.cursor_notes.execute(sql)

    def create_user_table(self):
        sql = """CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR NOT NULL, 
            email VARCHAR NOT NULL,
            whatsapp_no VARCHAR NOT NULL,
            password VARCHAR NOT NULL

            )"""
        self.cursor_user.execute(sql)

    def create_delete_table(self):
        sql = """CREATE TABLE IF NOT EXISTS deleted (
            notes_id INTEGER PRIMARY KEY AUTOINCREMENT,
            notes_title TEXT NOT NULL,
            notes_description TEXT NOT NULL
            )"""
        self.cursor_deleted.execute(sql)

    def create_files_table(self):
        sql = """CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR NOT NULL,
                    path VARCHAR NOT NULL,
                    document BLOB
                    )"""
        self.cursor_files.execute(sql)

    def delete(self):
        sql = """DELETE FROM notes WHERE `notes_description` = 'i am a boy' AND `notes_title` = 'Hey'"""
        self.cursor_notes.execute(sql)
        self.notes_conn.commit()
        print("deleted")

# CreateTable().delete()
# CreateTable().create_delete_table()
# CreateTable().create_notes_table()
# CreateTable().create_user_table()
