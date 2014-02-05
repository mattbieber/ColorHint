# -*- coding: utf-8 -*-

"""
ch_events

"""

import sublime
import sublime_plugin
import os
import time
import json

try:
    from ColorHint.ch_view_collection import ChViewCollection
    from ColorHint.ch_theme import ChTheme
    from ColorHint.ch_settings import ChSettings
except ImportError:
    from ch_view_collection import ChViewCollection
    from ch_theme import ChTheme
    from ch_settings import ChSettings

# --- ChEvents ---
class ChEvents(sublime_plugin.EventListener):

    def __init__(self):
        self._inited = False        
        self.async = False
        self.run_mode = ''
        self.syntaxes = []
        self.plugin_enabled = False
        self.last_view_id = 0

    def on_load(self, view):
        print('{0}...............{1}: {2}'.format(str(time.time()), 'on load', view.file_name()))

    def on_load_async(self, view):
        print('{0}...............{1}: {2}'.format(str(time.time()), 'on load async', view.file_name()))

    def on_activated(self, view):
        if not self.async:
            view.set_status('colorhint_status', ChSettings.status)
            if(view.id() == 0 or view.file_name() is None): return
            print('{0}...............{1}: {2} - {3}'.format(str(time.time()), 'on activated', str(view.id()), view.file_name()))
            self.activated_handler(view)

    def on_activated_async(self, view):
        if self.async:
            view.set_status('colorhint_status', ChSettings.status)
            if(view.id() == 0 or view.file_name() is None): return
            print('{0}...............{1}: {2} - {3}'.format(str(time.time()), 'on activated async', str(view.id()), view.file_name()))
            self.activated_handler(view)

    def activated_handler(self, view):
        if self.settings_loaded():
            ChEvents.flag_view(view)

    def settings_loaded(self):

        if(self._inited): 
            return True
        else: 
            return self.load_settings()

    def load_settings(self):
        self.plugin_enabled = ChSettings.plugin_enabled()
        self.async = ChSettings.get('async')
        self.run_mode = ChSettings.get('run_mode')

        if self.run_mode is None: self.run_mode = 'on_focus'
        if self.async is None or int(sublime.version()) < 3014: self.async = False
        self._inited = True
        return True

    @staticmethod
    def flag_view(view):
        print('flagview')
        if not ChSettings.plugin_enabled(): return
        if not ChEvents.file_is_hinted(view): return

        ChViewCollection.proc_view(view)

    @staticmethod
    def file_is_hinted(view):
        syntax_path = str(os.path.basename(view.settings().get('syntax')))
        syntax_name = os.path.splitext(syntax_path)[0].lower()

        if syntax_name in ChSettings.get_syntaxes():
            return True
        else:
            return False





    # ChTheme.destroy_tm()

# if not ST3:
#     plugin_loaded()

