'''
color_hint

'''

import sublime
import sublime_plugin

try:
    from ColorHint.ch_events import ChEvents
    from ColorHint.ch_settings import ChSettings
except ImportError:
    from ch_events import ChEvents
    from ch_settings import ChSettings

class ColorHintToggleCommand(sublime_plugin.WindowCommand):
    def run(self):

        ChSettings.toggle_enabled()

    def description(self):
        cap = 'Show Color Hinting'
        if ChSettings.get('disabled') == False:
            cap = 'Hide Color Hinting'

        return cap

class ColorHintListFoundCommand(sublime_plugin.WindowCommand):
    def run(self):
        print('---- printing found')

        try:
            from ColorHint.ch_theme import ChTheme
        except ImportError:
            from ch_theme import ChTheme

        found = ChTheme.get_found_colors()
        for f in found:
            print('>>>>>> found: ' + str(f))


