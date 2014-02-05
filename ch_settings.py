import sublime
import os

try:
    from ColorHint.ch_theme import ChTheme
    from ColorHint.ch_view_collection import ChViewCollection
except ImportError:
    from ch_theme import ChTheme
    from ch_view_collection import ChViewCollection

# --- ChSettings ---
class ChSettings:
    settings = None
    status = 'ColorHint: Disabled'
    syntaxes = None
    prefs = None

    @staticmethod
    def init_settings(s):
        ChSettings.settings = s
        ChSettings.prefs = sublime.load_settings('Preferences.sublime-settings')
        ChSettings.prefs.add_on_change('color_hint_theme_change', ChSettings.on_prefs_changed)
        ChSettings.syntaxes = [x.lower() for x in ChSettings.get('syntax_types')]

        if(ChSettings.get('last_color_scheme') == ""):
            ChSettings.set('last_color_scheme', ChSettings.prefs.get('color_scheme'))
        else:
            if(ChSettings.get('last_color_scheme') != ChSettings.prefs.get('color_scheme')):
                ChTheme.destroy_tm()


        if(ChSettings.get('disabled') == False):
            ChSettings.on_off(False)

    @staticmethod
    def on_prefs_changed():
        try:
            from ColorHint.ch_events import ChEvents
        except ImportError:
            from ch_events import ChEvents

        new_file = ChSettings.prefs.get('color_scheme')
        ChViewCollection.clear_views()

        if(os.path.basename(new_file).lower() == 'color_hint.tmtheme'):

            for w in sublime.windows():
                ChEvents.flag_view(w.active_view())
        else:
            ChSettings.set('last_color_scheme', ChSettings.prefs.get('color_scheme'))

    @staticmethod
    def toggle_enabled():
        print('--------------> toggle enabled called')
        disabled = ChSettings.get('disabled')
        ChSettings.set('disabled', not disabled)
        ChSettings.on_off(not disabled)

    @staticmethod
    def on_off(val):
        print('--------------> on_off called')
        if(val == True):
            ChSettings.status = 'ColorHint: Disabled'
            ChViewCollection.clear_views()
            ChTheme.destroy_tm()
        else:
            ChSettings.status = 'ColorHint: Enabled'
            ChTheme.init_tm()

    @staticmethod
    def plugin_enabled():
        return ChSettings.settings.get('disabled') == False
   
    @staticmethod
    def get(item):
        return ChSettings.settings.get(item)

    @staticmethod
    def set(item, val):
        ChSettings.settings.set(item, val)
        sublime.save_settings('color_hint.sublime-settings')

    @staticmethod
    def get_tempfile_path(relative=True):
        result = os.path.join(os.path.dirname(__file__), 'color_hint.tmTheme')
        if not relative: return result
        return result[result.index('Packages'):]

        # os.path.join(sublime.packages_path(), 'color_hint.tmTheme')

    @staticmethod
    def get_syntaxes():
        return ChSettings.syntaxes


# --- api callbacks ---
def plugin_loaded():
    s = sublime.load_settings('color_hint.sublime-settings')

    ChSettings.init_settings(s)
