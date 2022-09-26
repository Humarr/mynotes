

import sqlite3

import plyer
import PyPDF2
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.toast import toast
from kivymd.uix.behaviors import (FakeRectangularElevationBehavior,
                                  TouchBehavior)
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineIconListItem

from add import NotesCard
from android_imports import MyAndroidImports, Platform


class DocsCard(OneLineIconListItem, MDFloatLayout, FakeRectangularElevationBehavior, TouchBehavior):
    name = StringProperty()

    android_imports = MyAndroidImports()
    user_conn = android_imports.user_conn
    cursor = user_conn.cursor()

    files_conn = android_imports.files_conn
    cursor_files = files_conn.cursor()
    # image = StringProperty()

    def show_file_name(self, name):
        button1 = MDFlatButton(text="close", on_press=self.close_name_prompt)

        self.name_prompt = MDDialog(title="", text=name, buttons=[button1])
        self.name_prompt.open()

    def close_name_prompt(self, obj):
        self.name_prompt.dismiss()

    def read_pdf(self, name):
        # print(args)
        # name = DocsCard().name
        print(name)
        # self.ids['check'].active = True
        try:
            sql = "SELECT `path` FROM documents WHERE `name` Like ?"
            tuple_ = (name,)
            print(name)
            self.cursor_files.execute(sql, tuple_)
            path = self.cursor_files.fetchall()
            print(path)
            filepath = path[0][0]
            print(filepath)
            myFile = open(filepath, "rb")
            # output_file = open("output.txt", "w")
            pdfReader = PyPDF2.PdfFileReader(myFile)
            numOfPages = pdfReader.numPages
            print("The number of pages in the pdf file is:", numOfPages)
            print("Uploading")
            # creating a page object
            page = 0
            while page < numOfPages:
                pageObj = pdfReader.getPage(page)
                page += 1

                # extracting text from page
                pages = pageObj.extractText()
                # print(pages)

            # closing the pdf file object

            myFile.close()

            # self.ids['check'].active = False
            # self.manager.current = "doc_screen"

        except PyPDF2.errors.PdfReadError:
            toast("Uploading file failed")




class MainScreen(Screen):
    Platform()
    android_imports = MyAndroidImports()
    user_conn = android_imports.user_conn
    cursor = user_conn.cursor()

    files_conn = android_imports.files_conn
    cursor_files = files_conn.cursor()

    name = StringProperty()

    def read_pdf(self, name):
        # print(args)
        # self.ids['check'].active = True
        name = DocsCard().name
        try:
            sql = "SELECT `path` FROM documents WHERE `name` Like ?"
            tuple_ = (name,)
            print(name)
            self.cursor_files.execute(sql, tuple_)
            path = self.cursor_files.fetchall()
            print(path)
            filepath = path[0][0]
            print(filepath)
            myFile = open(filepath, "rb")
            # output_file = open("output.txt", "w")
            pdfReader = PyPDF2.PdfFileReader(myFile)
            numOfPages = pdfReader.numPages
            print("The number of pages in the pdf file is:", numOfPages)
            print("Uploading")
            # creating a page object
            page = 0
            while page < numOfPages:
                pageObj = pdfReader.getPage(page)
                page += 1

                # extracting text from page
                pages = pageObj.extractText()
                print(pages)
                

            # closing the pdf file object

            myFile.close()

            self.ids['check'].active = False
            # self.manager.current = "doc_screen"

        except PyPDF2.errors.PdfReadError:
            toast("Uploading file failed")

    def about(self):
        self.about_dialog = MDDialog(
            title="About Developer", text="Umar Sa'ad is a python developer with experience with developing useful applications for both mobile and desktop platforms.\n\nEmail: Saaduumar42@gmail.com\nPhone: +2348090935863")

        self.about_dialog.open()

    def profile(self):
        email = self.manager.get_screen("login").ids['email'].text
        password = self.manager.get_screen("login").ids['password'].text

        sql = f"""SELECT * FROM user WHERE email = '{email}' AND password = '{password}'"""

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print(result)
        if result:
            name = result[0][1]
            email = result[0][2]
            whatsapp = result[0][3]
            self.profile_dialog = MDDialog(
                title="Profile", text=f"""Name: {name}\n Email: {email} \n WhatsApp: {whatsapp}""")
            self.profile_dialog.open()
        else:
            toast("No Profile")

    def goto_delete(self):
        # change to the MainScreen and switch to the spcified MDBottomNavigationItem
        s = self.manager.get_screen('main_screen')
        s.ids.bottom_nav.switch_tab('delete_screen')

        self.ids['nav_drawer'].state = "close"

    # path = ""

    def upload(self, *args):
        # global path
        self.path = plyer.filechooser.open_file(
            filters=["*pdf", "*docx", "*doc"], on_selection=self.open_file)
        # print(self.path)

    def open_file(self, *args):
        # print(args)
        # self.ids['check'].active = True
        try:
            if len(args[0]) >= 1 and ".pdf" in args[0][0]:
                filepath = str(args[0][0])
                print(filepath)
                myFile = open(filepath, "rb")
                # output_file = open("output.txt", "w")
                pdfReader = PyPDF2.PdfFileReader(myFile)
                numOfPages = pdfReader.numPages
                print("The number of pages in the pdf file is:", numOfPages)
                print("Uploading")
                # assuming filename = C:\Users\USER\Desktop\workbook.pdf
                filepath = filepath.replace("\\", "/")
                # get the last index of /
                a = filepath.rindex("/")
                # retrieve a substring from filename
                doc_name = filepath[a + 1:]
                print(doc_name)
                self.insertBLOB(filepath, filepath, doc_name)
                self.manager.get_screen('doc_screen').ids.docs.add_widget(
                    DocsCard(name=doc_name.title()))
                self.ids['check'].active = False
                # self.manager.current = "doc_screen"
                toast("Upload successful")
            else:
                self.ids['check'].active = False
                toast("Upload cancelled")
        except PyPDF2.errors.PdfReadError:
            toast("Uploading file failed")

    def check(self):
        self.ids['check'].active = True
        # Thread(target=self.login).start()
        # self.login()
        Clock.schedule_once(self.upload, 1)

    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def insertBLOB(self, docFile, path, doc_name):
        try:
            print("Connected to SQLite")
            sqlite_insert_blob_query = """ INSERT INTO documents
                                        (`name`, `path`, `document`) VALUES ( ?,?,?)"""

            document = self.convertToBinaryData(docFile)
            # Convert data into tuple format
            data_tuple = (doc_name, path, document,)
            self.cursor_files.execute(sqlite_insert_blob_query, data_tuple)
            self.files_conn.commit()
            print(" file uploaded successfully")
            self.cursor_files.close()

        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)
        finally:
            if self.files_conn:
                # self.files_conn.close()
                print("the sqlite connection is closed")
