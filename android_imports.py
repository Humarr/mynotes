from kivy.utils import platform
import plyer
import sqlite3
from kivy.storage.jsonstore import JsonStore


class Platform:
    from kivy.core.window import Window
    from kivy.utils import platform
    if platform == "android":
        # Window.softinput_mode = "below_target"
        Window.softinput_mode = "pan"

    else:
        Window.size = (350, 600)


class MyAndroidImports:

    if platform == 'android':
        from jnius import autoclass, cast
        from kivymd.toast import toast
        from kvdroid.tools.contact import get_contact_details
        from pythonforandroid.recipes.android.src.android.permissions import (
            PERMISSION_DENIED, PERMISSION_GRANTED, Permission,
            check_permission, request_permissions)

    # try:
        if PERMISSION_DENIED:
            # if not check_permission(Permission.READ_EXTERNAL_STORAGE) or not check_permission(Permission.WRITE_EXTERNAL_STORAGE):
            request_permissions(
                [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_CONTACTS])
            # , Permission.WRITE_CONTACTS, Permission.READ_CONTACTS])
        # elif PERMISSION_GRANTED:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Environment = autoclass('android.os.Environment')
            context = cast('android.content.Context',
                           PythonActivity.mActivity)
            storage = context.getExternalFilesDir(
                'Notes').getAbsolutePath()

            # File TEST = new File(Environment.getExternalStorageDirectory(), "TEST");
            # TEST.mkdir(); // make directory may want to check return value
            # String path = TEST.getAbsolutePath(); // get absolute path

            # print(context.getExternalFilesDir('.contacts').getAbsolutePath())
            # print(context.getExternalFilesDir(
            #     Environment.DIRECTORY_DOCUMENTS).getAbsolutePath())
            # print(context.getExternalFilesDir(
            #     Environment.DIRECTORY_PICTURES).getAbsolutePath())

            # # get_contact_details("name")
            # contacts = json.dumps(contacts)
            # contact_store.put("List of contacts", name = "Nice Guy", phone = "08090935863")
            # contact_store.put(contacts)
            # store = JsonStore(f'{storage}/log.json')
            # btn = JsonStore(f'{storage}/btn_log.json')
            remember = JsonStore(f'{storage}/remember.json')
            notes_conn = sqlite3.connect(
                f'{storage}/notes.sql', check_same_thread=False)
            user_conn = sqlite3.connect(
                f'{storage}/user.sql', check_same_thread=False)
            deleted_conn = sqlite3.connect(
                f'{storage}/deleted.sql', check_same_thread=False)
            contact_store = JsonStore(f'{storage}/contacts.json')
            files_conn = sqlite3.connect(
                f'{storage}/files.sql', check_same_thread=False)

        # else:
        #     pass

    else:
        storage = plyer.storagepath.get_home_dir()
        contact_store = JsonStore(f'{storage}/contacts.json')

        remember = JsonStore(f'{storage}/remember.json')
        notes_conn = sqlite3.connect(
            f'{storage}/notes.sql', check_same_thread=False)
        user_conn = sqlite3.connect(
            f'{storage}/user.sql', check_same_thread=False)
        deleted_conn = sqlite3.connect(
            f'{storage}/deleted.sql', check_same_thread=False)
        files_conn = sqlite3.connect(
            f'{storage}/files.sql', check_same_thread=False)

    # credentials_store = JsonStore(f'{storage}/credentials.json')
    # cursor = notes_conn.cursor()
