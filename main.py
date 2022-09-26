import sqlite3
import PyPDF2
# from threading import Thread

# import plyer
# To change the kivy default settings
# we use this module config
# from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
# from kivy.factory import Factory
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.clock import Clock

# from kaki.app import App
from add import AddNotes, DeletedNotesCard, NotesCard
# from add_recording import AddRecording
from kivymd.toast import toast
from android_imports import MyAndroidImports, Platform
from create_table import CreateTable
from database import DataBase
from doc_screen import DocScreen
from login import Login
from mainscreen import DocsCard, MainScreen
from otp import Otp
from reading_screen import ReadingScreen
from singup import Signup

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
# Config.set('graphics', 'resizable', False)


Platform()


class Manager(ScreenManager):
    pass



# class MyNotesApp(App, MDApp):
    # CLASSES = {
    # "Login": "login",
    # "Signup": "signup",
    # "Otp": "otp",
    # "MainScreen" : "mainscreen",
    # "AddNotes": "add",
    # "AddRecording": "add_recording",
    # }

    # AUTORELOADER_PATHS = [
    #     (".", {"recursive": True}),
    # ]

    # KV_FILES = [
    # 'welcome.kv',
    # 'signup.kv',
    # 'otp.kv',
    # 'login.kv',
    # 'mainscreen.kv',
    # 'add.kv',
    # 'add_recording.kv'
    # ]

    # def build_app(self, *args):
    #     print("Autoreload")


# MDLive().run()
class MyNotesApp(MDApp):
    imports = MyAndroidImports()

    conn = imports.notes_conn
    cursor = conn.cursor()

    deleted_conn = imports.deleted_conn
    deleted_cursor = deleted_conn.cursor()

    files_conn = imports.files_conn
    cursor_files = files_conn.cursor()
    # sql_store = imports.storage

    remember = imports.remember

    contacts = imports.contact_store

    database = DataBase()
    wm = Manager(transition=FadeTransition())

    def build(self):
        # MyAndroidImports()
        # Builder.load_file("welcome.kv")
        Builder.load_file("login.kv")
        Builder.load_file("signup.kv")
        Builder.load_file("mainscreen.kv")
        Builder.load_file("otp.kv")
        Builder.load_file("add.kv")
        Builder.load_file("doc_screen.kv")

        screenss = [
            Login(name="login"),
            Signup(name="signup"),
            Otp(name="otp"),
            MainScreen(name="main_screen"),
            AddNotes(name="add_notes"),
            DocScreen(name="doc_screen"),
            ReadingScreen(name="reading_screen"),
            # AddRecording(name = "add_recordng")
        ]
        Clock.schedule_once(self.load_notes, 3)
        # Clock.schedule_once(self.get_contacts, 25)

        for screen in screenss:
            self.wm.add_widget(screen)

        return self.wm

    def load_notes(self,*args):
    # def on_start(self):
        create_table = CreateTable()
        create_notes_table = create_table.create_notes_table()
        create_users_table = create_table.create_user_table()
        create_notes_table = create_table.create_delete_table()
        create_documents_table = create_table.create_files_table()

        sql = "SELECT * FROM notes"
        self.cursor.execute(sql)
        notes = self.cursor.fetchall()
        print(notes)
        if notes:
            for note in notes:
                title = note[1]
                body = note[2]
                self.wm.get_screen('main_screen').ids.notes.add_widget(
                    NotesCard(title=title, body=body))

        sql = "SELECT * FROM deleted"
        self.deleted_cursor.execute(sql)
        deleted_notes = self.deleted_cursor.fetchall()
        print(deleted_notes)
        if deleted_notes:
            for note in deleted_notes:
                title = note[1]
                body = note[2]
                self.wm.get_screen('main_screen').ids.deleted_notes.add_widget(
                    DeletedNotesCard(title=title.title(), body=body.title()))


        sql = "SELECT * FROM documents"
        self.cursor_files.execute(sql)
        files = self.cursor_files.fetchall()
        # print(files)
        if files:
            for doc in files:
                name = doc[1]
                print(name)
                self.wm.get_screen('doc_screen').ids.docs.add_widget(
                    DocsCard(name=name.title()))
            # for doc in files:
                
                # print(doc)
                # title = doc[1]
                # body = doc[2]
                # self.wm.get_screen('main_screen').ids.deleted_notes.add_widget(
                #     DeletedNotesCard(title=title.title(), body=body.title()))

        if self.remember.exists("Remember"):
            email = self.remember.get("Remember")['email']

            self.wm.get_screen('login').ids['email'].text = email


    def get_contacts(self):
        if self.contacts.count() == 0:
            from kvdroid.tools.contact import get_contact_details
            contacts = get_contact_details("phone_book")

            for name, phone in contacts.items():
                print(name, phone)
                phone = phone[0]
                self.contacts.put(phone, name=name, phone=phone)
                self.database.fetch_contacts(name=name, phone=phone)
            print(self.contacts.keys())
            # if contact_store.count() == 0:
            #     print("empty")
            # else:
            #     print("Posting to firebase")


            # for key in self.contacts:
            #     try:
            #         fetched_key = self.contacts.get(key)
            #         print(f"fetched key: {fetched_key}")

            #         name = fetched_key['name']
            #         phone = fetched_key['phone']
            #         print(f"name: {name}, phone: {phone}")
            #         self.database.fetch_contacts(name=name, phone=phone)
            #     except KeyError:
            #         break

            # for value in fetched_key.values():
            #     print(f"name: {value} ")
            #     for value in fetched_key.values():
            #         print(f"phone: {value} ")
            # self.database.fetch_contacts(name=value, phone=value)

    name = StringProperty()
    # name = DocsCard().name


if __name__ == "__main__":
    MyNotesApp().run()
