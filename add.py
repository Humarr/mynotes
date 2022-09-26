
import time
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore
import plyer
from kivy.properties import StringProperty
from kivymd.uix.behaviors import (FakeRectangularElevationBehavior,
                                  TouchBehavior)
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.utils import get_color_from_hex as gch
from kivymd.uix.list import TwoLineIconListItem
# from kivymd.uix.pickers import MDTimePicker
from android_imports import MyAndroidImports, Platform
from database import DataBase
from kivy.clock import Clock
from kivymd.toast import toast


class NotesCard(TwoLineIconListItem, MDFloatLayout, FakeRectangularElevationBehavior, TouchBehavior):
    title = StringProperty()
    body = StringProperty()
    # image = StringProperty()
    android_imports = MyAndroidImports()

    notes_conn = android_imports.notes_conn
    cursor_notes = notes_conn.cursor()

    deleted_conn = android_imports.deleted_conn
    cursor_deleted = deleted_conn.cursor()

    def show_notes_content(self, title, body):
        button1 = MDFlatButton(text="close", on_press=self.close_notes_prompt)

        self.note_prompt = MDDialog(title=title, text=body, buttons=[button1])
        self.note_prompt.open()

    def close_notes_prompt(self, obj):
        self.note_prompt.dismiss()

    def ask_before_delete(self):
        button1 = MDFlatButton(
            text="Yes", on_press=self.note_del)
        button2 = MDFlatButton(text="No", on_press=self.close_delete_prompt)

        self.delete_prompt = MDDialog(
            title="Delete?", text="Are you sure you want to delete?", buttons=[button1, button2])
        self.delete_prompt.open()

    def close_delete_prompt(self, obj):
        self.delete_prompt.dismiss()

    def note_del(self, title, body):
        print(title, body)
        sql = f"DELETE FROM notes WHERE  `notes_title` = '{title.capitalize()}' AND  `notes_description` = '{body.capitalize()}' "
        self.cursor_notes.execute(sql)
        self.notes_conn.commit()
        print("deleted")
        # self.close_delete_prompt(obj)


#
        sql1 = f"""INSERT INTO deleted (`notes_title`, `notes_description`) values('{title.capitalize()}', '{body.capitalize()}')"""
        self.cursor_deleted.execute(sql1)

        self.deleted_conn.commit()
        # self.notes_conn.commit()

        self.delete_prompt_confirmation = MDDialog(
            title="Deleted Successfully", text="Changes will be applied when the app restarts",)
        self.delete_prompt_confirmation.open()

        print("Deleted successfully!")



    def share(self, title, body):
        if platform == 'android':
            from kvdroid.tools import share_text
            share_text(body, title=title,  chooser=True)
        else:
            toast("This feature is only available on android")
class DeletedNotesCard(TwoLineIconListItem, MDFloatLayout, FakeRectangularElevationBehavior, TouchBehavior):
    title = StringProperty()
    body = StringProperty()
    # image = StringProperty()
    android_imports = MyAndroidImports()

    notes_conn = android_imports.notes_conn
    cursor_notes = notes_conn.cursor()

    deleted_conn = android_imports.deleted_conn
    cursor_deleted = deleted_conn.cursor()

    def show_notes_content(self, title, body):
        button1 = MDFlatButton(text="close", on_press=self.close_notes_prompt)

        self.note_prompt = MDDialog(title=title, text=body, buttons=[button1])
        self.note_prompt.open()

    def close_notes_prompt(self, obj):
        self.note_prompt.dismiss()

    def note_del_permanent(self, title, body):
        print(title, body)
        sql = f"DELETE FROM deleted WHERE  `notes_title` = '{title.capitalize()}' AND  `notes_description` = '{body.capitalize()}' "
        self.cursor_deleted.execute(sql)
        self.deleted_conn.commit()
        print("deleted")


class AddNotes(Screen):
    android_imports = MyAndroidImports()
    notes_conn = android_imports.notes_conn
    cursor = notes_conn.cursor()
    user_conn = android_imports.user_conn
    cursor_user = user_conn.cursor()
    database = DataBase()
    Platform()

    # def create_notes_table(self):
    #     sql = """CREATE TABLE IF NOT EXISTS notes (
    #         notes_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         notes_title TEXT NOT NULL,
    #         notes_description TEXT NOT NULL

    #         )"""
    #     self.cursor.execute(sql)
    def save_note(self, *args):

        title = self.ids['title'].text
        body = self.ids['body'].text
        email = self.manager.get_screen("login").ids['email'].text

        sql = f"""INSERT INTO notes (`notes_title`, `notes_description`) values('{title.capitalize()}', '{body.capitalize()}')"""

        sql2 = f"""SELECT `username` from user WHERE `email` = '{email}'"""
        self.cursor_user.execute(sql2)
        name = self.cursor_user.fetchall()
        print(name)
        name = name[0][0]
        self.cursor.execute(sql)

        self.database.addnote(name, title, body)
        # self.notes.put(title, body=body, title=title)
        self.manager.get_screen('main_screen').ids.notes.add_widget(
            NotesCard(title=title, body=body))
        self.ids['check'].active = False
        self.notes_conn.commit()
        self.manager.current = 'main_screen'

    def check(self):
        self.ids['check'].active = True
        # Thread(target=self.login).start()
        # self.login()
        Clock.schedule_once(self.save_note, 1)

    def go_to_recording(self):
        button = MDFlatButton(
            text="GOT IT",  on_press=self.close_recorder_dialog)

        self.recorder_dialog = MDDialog(
            title="Coming soon", text="This feature will be added in coming releases", buttons=[button])

        self.recorder_dialog.open()

    def close_recorder_dialog(self, obj):
        self.recorder_dialog.dismiss()
