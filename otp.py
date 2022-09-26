from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.toast import toast
from kivy.clock import Clock

from android_imports import MyAndroidImports, Platform
from database import DataBase
# from threading import Thread
class Otp(Screen):
    Platform()
    android_imports = MyAndroidImports()
    user_conn = android_imports.user_conn
    cursor = user_conn.cursor()
    
    database = DataBase()
    
    

    def create_account(self, *args):
        self.whatsapp = self.manager.get_screen("signup").ids['whatsapp'].text
        # self.whatsapp = int(self.whatsapp)
        otp1 = self.ids['otp1'].text
        otp2 = self.ids['otp2'].text
        otp3 = self.ids['otp3'].text
        otp4 = self.ids['otp4'].text
        otp5 = self.ids['otp5'].text
        otp6 = self.ids['otp6'].text

        otp = otp1 + otp2 + otp3 + otp4 + otp5 + otp6
        print(otp)
        self.username = self.manager.get_screen("signup").ids['username'].text
        self.email = self.manager.get_screen("signup").ids['email'].text
        self.whatsapp = self.manager.get_screen("signup").ids['whatsapp'].text
        self.password = self.manager.get_screen("signup").ids['password'].text

        if self.manager.get_screen("signup").ids['otp_label'].text == otp:
            # Thread(target=self.signup).start()
            signup =  self.database.signup(self.username, self.email, self.password, self.whatsapp)
            sql = f"""INSERT INTO user (`username`, `email`, `whatsapp_no`, `password`) values('{self.username}', '{self.email}', '{self.whatsapp}', '{self.password}')"""
            self.cursor.execute(sql)
            self.user_conn.commit()
            self.ids['check'].active = False
            toast("Account created successfully")
            self.manager.current = "login"
        else:
            toast("Otp incorrect")
            self.ids['check'].active = False

    # def signup(self):
    #     DataBase.signup(self, name=self.username, email=self.email, password=self.password, whatsapp=self.whatsapp)
        

    def checkbox(self):
        self.ids['check'].active = True
        # Thread(target=self.login).start()
        # self.login()
        Clock.schedule_once(self.create_account, 1)