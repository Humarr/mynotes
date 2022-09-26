import sqlite3
from kivy.uix.screenmanager import ScreenManager, Screen

from android_imports import MyAndroidImports
from kivymd.uix.card import MDCard
from kivy.uix.textinput import TextInput


class ReaderCard(TextInput, MDCard):
    pass


class DocScreen(Screen):
    android_imports = MyAndroidImports()
    files_conn = android_imports.files_conn
    cursor_files = files_conn.cursor()

    storage = android_imports.storage

    def goback(self):
        self.manager.current = "main_screen"
