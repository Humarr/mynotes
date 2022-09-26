from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore
import plyer
from kivy.properties import StringProperty
from kivymd.uix.behaviors import (FakeRectangularElevationBehavior,
                                  TouchBehavior)
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty
# from kivymd.uix.list import TwoLineAvatarIconListItem




class AudioCard( MDFloatLayout, FakeRectangularElevationBehavior, TouchBehavior):
    title = StringProperty()
    # body = StringProperty()
    # image = StringProperty()

    def on_long_touch(self, touch, *args):
        """Called when the widget is pressed for a long time."""
        print('You long touched me')

    def on_press(self):
        """Called when the widget is pressed for a long time."""
        print('You touched me')




class AddRecording(Screen):
    audio = ObjectProperty()

    if platform == 'android':

        from jnius import autoclass, cast
        from kivymd.toast import toast
        from pythonforandroid.recipes.android.src.android.permissions import (
            PERMISSION_DENIED, PERMISSION_GRANTED, Permission,
            check_permission, request_permissions)

    # try:
        if PERMISSION_DENIED:
            request_permissions(
                [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.RECORD_AUDIO])
            # Permission.READ_CONTACTS, Permission.WRITE_CONTACTS
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Environment = autoclass('android.os.Environment')
            context = cast('android.content.Context',
                            PythonActivity.mActivity)
            storage_audio = context.getExternalFilesDir(
                'notes').getAbsolutePath()
            # # print(context.getExternalFilesDir('.contacts').getAbsolutePath())
            # # print(context.getExternalFilesDir(
            # #     Environment.DIRECTORY_DOCUMENTS).getAbsolutePath())
            # storage_audio = context.getExternalFilesDir(
            #     Environment.DIRECTORY_DOWNLOADS).getAbsolutePath()
            # store = JsonStore(f'{storage}/log.json')
        else:
            from jnius import autoclass
            from time import sleep
            # get the needed Java classes
            MediaRecorder = autoclass('android.media.MediaRecorder')
            AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
            OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
            AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')

            # create out recorder
            mRecorder = MediaRecorder()
            mRecorder.setAudioSource(AudioSource.MIC)
            mRecorder.setOutputFormat(OutputFormat.MPEG_4)
            # mRecorder.setOutputFile('/sdcard/test_recording.mp4')
            # mRecorder.setAudioEncoder(AudioEncoder.AMR_NB)
            # mRecorder.prepare()

            # # record 5 seconds
            # mRecorder.start()
            # sleep(5)
            # mRecorder.stop()
            # mRecorder.release()
    else:
        storage_audio = plyer.storagepath.get_home_dir()
        



    # notes = JsonStore(f'{storage}/notes.json')
    # has_recording = False
    # def start_recording(self):
    #     state = self.audio.state
    #     if state == "ready":
    #         self.audio.start()
    #     if state == "recording":
    #         self.audio.stop()
    #         self.has_recording = True
            
    # def update_labels(self):
    #     record_btn = self.ids['record_btn']
    #     state = self.ids['state']
        
        
    def start_recording(self):

        self.title = self.ids['save_as'].text
        self.mRecorder.setOutputFile(f'{self.storage_audio}/{self.title}.mp4')
        self.mRecorder.setAudioEncoder(self.AudioEncoder.AMR_NB)
        self.mRecorder.prepare()

        # start recording
        self.mRecorder.start()
        self.ids['state'].text = 'Recording'
        # body = self.ids['body'].text


    def stop_recording(self):
        self.mRecorder.stop()
        self.mRecorder.release()
        # self.notes.put(title, body=body, title=title)
        self.manager.get_screen('main_screen').ids.recordings.add_widget(
            AudioCard(title=self.title))
        # self.manager.current = 'main_screen'

