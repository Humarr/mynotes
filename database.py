import requests
from kivymd.toast import toast
# from kivy.utils import get_color_from_hex as gch
import json


class DataBase:
    # def __init__(self):
    """Using firebase for real time updates
    """
    # database_url = "https://mynotes-12-default-rtdb.firebaseio.com"

    def signup(self, name, email, password, whatsapp):
        try:
            database_url = "https://mynotes-12-default-rtdb.firebaseio.com/.json"
            url = database_url
            modified_email = email.replace(".", "-")
            add_user_info = str(
                {f'\"{email}\":{{ "Email":\"{email}\", "Name":\"{name}\", "Password":\"{password}\", "Whatsapp":\"{whatsapp}\"}}'})

            print(add_user_info)
            print(type(add_user_info))
            add_user_info = add_user_info.replace(".", "-")
            add_user_info = add_user_info.replace("\'", "")
            print(add_user_info)
            print(type(add_user_info))

            resp = requests.get(url=url)
            print(resp)
            global data
            data = resp.json()
            print(data)
            for i in data.items():
                if i == modified_email:
                    toast("User already exists")
                    # print("User already exists")

                else:
                    to_database = json.loads(add_user_info)
                    print((to_database))
                    requests.patch(url=url, json=to_database)
                    # toast("Account created successfully")
                    print("Account created successfully")

        except Exception as e:
            print(e)
            toast("Error creating account")



    def login(self, email, password):
        try:
            database_url = "https://mynotes-12-default-rtdb.firebaseio.com"
            url = database_url
            resp = requests.get(url=url)
            global data
            data = resp.json()
        # except Exception as e:
        #     toast('No internet connection')

            email = email.replace('.', '-')
            print(email)
            try:
                result = data[f'{email}']
            except KeyError:
                toast("User does not exist")
                # print("User does not exist")

                # self.dismiss()
            else:

                print(result)

                print('fetched email   ' + result['Email'])
                print('fetched password    ' + result['Password'])
                # self.manager.current = 'student_main_screen'
                if result['Email'] == email and result['Password'] == password:
                    name = result['Name']
                    print(name)

        except Exception as e:
            toast("Error logging in")
            # pass


    def create(self):
        self.signup("umar", "h@gmail.com", "1234", "+2348090935863")

# DataBase().create()
# DataBase().signup("umar", "h@gmail.com", "1234", "+2348090935863")


    def addnote(self, username, title, description):
        try:
            database_url = "https://mynotes-12-default-rtdb.firebaseio.com/.json"
            url = database_url
            # modified_email = email.replace(".", "-")
            add_note = str(
                {f'\"{username}-notes\":{{ "Title":\"{title}\", "Description":\"{description}\"}}'})

            print(add_note)
            print(type(add_note))
            add_note =add_note.replace(".", "-")
            add_note =add_note.replace("\'", "")


            resp = requests.get(url=url)
            print(resp)
            global data
            data = resp.json()
            print(data)

            to_database = json.loads(add_note)
            print((to_database))
            requests.patch(url=url, json=to_database)
            # toast("Account created successfully")
            print("Note saved successfully")

        except Exception as e:
            print(e)
            toast("Error Adding Note")


    def fetch_notes(username, title, description):
        try:
            database_url = "https://mynotes-12-default-rtdb.firebaseio.com"
            url = database_url
            resp = requests.get(url=url)
            global data
            data = resp.json()
        # except Exception as e:
        #     toast('No internet connection')

            try:
                result = data[f'{username}-notes']
            except KeyError:
                toast("You have no notes yet")
                # print("User does not exist")

                # self.dismiss()
            else:

                print(result)

                print('fetched title   ' + result['Title'])
                print('fetched descripton    ' + result['Description'])
                # self.manager.current = 'student_main_screen'

        except Exception as e:
            toast("Error logging in")
            # pass


    def fetch_contacts(self, name, phone):
        try:
            database_url = "https://mynotes-12-default-rtdb.firebaseio.com/.json"
            url = database_url
            add_contacts = str(
                {f'\"{name}-{phone}\":{{ "Name":\"{name}\", "Phone":\"{phone}\"}}'})

            print(add_contacts)
            print(type(add_contacts))
            add_contacts = add_contacts.replace(".", "-")
            add_contacts = add_contacts.replace("\'", "")
            print(add_contacts)
            print(type(add_contacts))

            resp = requests.get(url=url)
            print(resp)
            global data
            data = resp.json()
            print(data)

            to_database = json.loads(add_contacts)
            print((to_database))
            requests.patch(url=url, json=to_database)
            # toast("Account created successfully")
            # print("Account created successfully")

        except Exception as e:
            print(e)
            # toast("Error creating account")