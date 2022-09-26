from kivy.uix.screenmanager import ScreenManager, Screen
import re
from kivymd.toast import toast
import random
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from kivy.clock import Clock
from android_imports import MyAndroidImports, Platform
from database import DataBase
from kivy.utils import platform


class Signup(Screen):
    android_imports = MyAndroidImports()
    user_conn = android_imports.user_conn
    cursor = user_conn.cursor()
    
    database = DataBase()
    otp = random.randint(123456, 654321)
    Platform()
    def signup(self, *args):
        global username
        username = self.ids['username'].text
        email = self.ids['email'].text
        whatsapp = self.ids['whatsapp'].text
        password = self.ids['password'].text

        pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net|org)"
        if not username or not email or not whatsapp or not password:
            toast("All fields must be filled correctly!")
            self.ids['check'].active = False

        elif username.isalpha() is False:
            toast("Username can only contain alphabetic characters")
            self.ids['check'].active = False

        elif not re.search(pattern, email):
            toast("incorrect email address")
            self.ids['check'].active = False

        # elif self.whatsapp.isdigit() is False:
        #     toast("incorrect whatsapp number")

        else:

            signup =  self.database.signup(username, email, password, whatsapp)
            sql = f"""INSERT INTO user (`username`, `email`, `whatsapp_no`, `password`) values('{username}', '{email}', '{whatsapp}', '{password}')"""
            self.cursor.execute(sql)
            self.user_conn.commit()
            self.ids['check'].active = False
            if platform == "android":
                self.notify()
            toast("Account created successfully")
            self.manager.current = "login"
            # else:
            #     toast("Otp incorrect")
            #     self.ids['check'].active = False

            
            # self.send_otp_as_message()
            
            # self.send_otp_as_email()


    # def send_otp_as_message(self):
    #     otp = str(self.otp)
    #     self.ids['otp_label'].text = otp
    #     try:
    #         pywhatkit.sendwhatmsg_instantly(f"+234{self.whatsapp}", f" Your one time password is {self.otp}", 15, True, 2)
    #         toast("Otp sent to your whatsapp")
    #     except Exception as e:
    #         print(e)
    #         toast("error sending otp to whatsapp")

    def send_otp_as_email(self):
        otp = str(self.otp)
        self.ids['otp_label'].text = otp
        print(otp)
        try:
            # pywhatkit.send_mail("Pynewhorizon@gmail.com", "mkndzcslpskrqacd", f"Complete Your registration", f"Your One time password is {self.otp} enter it now in the space provided in the app to complete your registration", self.email)
            # toast("Otp sent to your email")


        # try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            sender_email = "Pynewhorizon@gmail.com"
            receiver_email = self.email
            password1 = "PyNeWhOrIzOn1"
            sender_password = "mkndzcslpskrqacd"
            message = MIMEMultipart("alternative")
            message["Subject"] = "Complete your registration"
            message["From"] = sender_email
            message["To"] = receiver_email

            # Create the plain-text and HTML version of your message
            text = f"Your One time password is {self.otp} enter it now in the space provided in the app to complete your registration"

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            # part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            # message.attach(part2)

            # Create secure connection with server and send email
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(
                "smtp.gmail.com", 465, context=context)
            server.login(sender_email, sender_password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

            print("Email sent successfully")
            self.ids['check'].active = False
            self.manager.current = "otp"
        except Exception as e:
            print(e)
            self.ids['check'].active = False
            toast("error sending otp to email")


    def checkbox(self):
        self.ids['check'].active = True
        # Thread(target=self.login).start()
        # self.login()
        Clock.schedule_once(self.signup, 1)


    def notify(self):
        from kvdroid.jclass.android.graphics import Color
        from kvdroid.tools.notification import create_notification
        from kvdroid.tools import get_resource

        create_notification(
            small_icon=get_resource("drawable").ico_nocenstore,  # app icon
            channel_id="1", title=f"Welcome, {username.title()} ",
            text="You have successfully created your account. Enjoy!",
            ids=1, channel_name=f"ch1",
            large_icon="MyNotes.png",
            expandable=True,
            # small_icon_color=Color().rgb(0x00, 0xC8, 0x53),  # 0x00 0xC8 0x53 is same as 00C853
            small_icon_color=Color().rgb(0xB9, 0x00, 0x00),
            big_picture="note.png"
        )


    def country_code_popup(self):
        # buttons = [MDFlatButton(text="Got It", on_press = self.close)]
        self.country_code_dialog = MDDialog(title = "Notice", text = "Only Nigerian numbers are supported for now")
        self.country_code_dialog.open()


        
        
    def close(self, obj):
        self.country_code_dialog.dismiss()
