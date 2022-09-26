from kivy.uix.screenmanager import ScreenManager, Screen

from android_imports import MyAndroidImports, Platform
from kivymd.toast import toast
from database import DataBase
from kivy.properties import StringProperty

from kivy.clock import Clock, mainthread
class Login(Screen):
    Platform()
    android_imports = MyAndroidImports()
    user_conn = android_imports.user_conn
    cursor = user_conn.cursor()

    remember = android_imports.remember
    database = DataBase()

    # @mainthread
    def login(self, *args):
        email = self.ids['email'].text
        password = self.ids['password'].text
        sql = f"""SELECT * FROM user WHERE email = '{email}' AND password = '{password}'"""

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if result:
            self.ids['check'].active = False
            self.remember.put("Remember", email = email)
            name = result[0][1]
            self.manager.current = "main_screen"
            self.manager.get_screen("main_screen").ids['toolbar'].title = f" Welcome, {name.title()}"
        else:
            login  = self.database.login(email, password)
            if login:
                self.ids['check'].active = False
                toast("Login successful")
                self.manager.current = "main_screen"
                self.remember.put("Remember", email = email)
            else:
                self.ids['check'].active = False
                toast("invalid email or password")




    def checkbox(self):
        self.ids['check'].active = True
        # Thread(target=self.login).start()
        # self.login()
        Clock.schedule_once(self.login, 1)
        

    # def on_state(self, instance, value):
    #     {
    #         "start": self.root.ids.progress.start,
    #         "stop": self.root.ids.progress.stop,
    #     }.get(value)()