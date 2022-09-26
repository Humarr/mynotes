import sqlite3
from kivy.uix.screenmanager import ScreenManager, Screen

from android_imports import MyAndroidImports


class ReadingScreen(Screen):
    android_imports = MyAndroidImports()
    files_conn = android_imports.files_conn
    cursor_files = files_conn.cursor()

    storage = android_imports.storage

    def goback(self):
        self.manager.current = "doc_screen"
