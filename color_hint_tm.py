import sublime
import os




# print('...............file: tm')

TM_ENTRY = """
<dict>
    <key>name</key>
    <string>{0}</string>
    <key>scope</key>
    <string>{1}</string>
    <key>settings</key>
    <dict>
        <key>background</key>
        <string>{2}</string>
        <key>foreground</key>
        <string>{3}</string>
    </dict>
</dict>
"""



def write_tm():
    print('...............------------------.................. tm write called')
    with open(ChTheme.temppath, mode='w', encoding='utf-8') as tm_file:
        tm_file.write(ChTheme.tm_data)
        tm_file.close()

def make_color(color):
    if(color[:1] == '#'):
        print('0x' + color[1:])

class ChTheme:
    inited = False
    tm_data = ''
    tm_entries = []
    temppath = ''
    TM_PREFIX = 'ch.color.'
    found_colors = set()

    @staticmethod
    def init_tm():

        print('...............tm init')

        try:
            from ColorHint.ch_events import ChSettings
        except ImportError:
            from ch_events import ChSettings

        last_color_scheme = ChSettings.get('last_color_scheme')
        theme_base = ChSettings.prefs.get('color_scheme')
        saved_theme_base = ChSettings.get('base_color_scheme')
        reload_base_theme = True

        ChTheme.temppath = ChSettings.get_tempfile_path(False)

        if(theme_base == saved_theme_base):
            if(len(ChTheme.tm_data) > 0):
                reload_base_theme = False
        else:
            if not saved_theme_base:
                ChSettings.set('base_color_scheme', last_color_scheme)
            ChTheme.tm_data = sublime.load_resource(last_color_scheme)
            write_tm()

        ChSettings.prefs.set('color_scheme', ChSettings.get_tempfile_path())
        sublime.save_settings('Preferences.sublime-settings')

    @staticmethod
    def destroy_tm():
        print('...............tm destroy')

        try:
            from ColorHint.ch_events import ChSettings
        except ImportError:
            from ch_events import ChSettings

        prefs = sublime.load_settings('Preferences.sublime-settings')
        prefs.set('color_scheme', ChSettings.get('last_color_scheme'))
        sublime.save_settings('Preferences.sublime-settings')

    @staticmethod

    @staticmethod
    def get_tm_data():
        return ChTheme.tm_data

    @staticmethod
    def get_found_colors():
        print('found colors: ' + str(len(ChTheme.found_colors)))
        return ChTheme.found_colors

    @staticmethod
    def update_tm(colors):

        print('...............tm update called')
        if not ChTheme.inited:
            ChTheme.init_tm()

        new_colors = set(colors).difference(ChTheme.found_colors)

        if len(new_colors) == 0: return

        for c in new_colors:
            ChTheme.found_colors.add(c)
            #make_color(c)
            oct_color = '0x' + c[1:]
            alt_color = '#000000' if(int(oct_color, 16) > 0xffffff/2) else '#ffffff'
            ChTheme.tm_entries.append(TM_ENTRY.format(c, ChTheme.TM_PREFIX + c, c, alt_color))

            # print('new->' + str(c))

        # for m in tm_entries:
            # print('----')
            # print(m)


        entry_str = ''.join(ChTheme.tm_entries)

        # print(entry_str)
        n = ChTheme.tm_data.find("<array>") + len("<array>")

        try:
            ChTheme.tm_data = ChTheme.tm_data[:n] + entry_str + ChTheme.tm_data[n:]
        except UnicodeDecodeError:
            ChTheme.tm_data = ChTheme.tm_data[:n] + entry_str + ChTheme.tm_data[n:]

        for fc in ChTheme.found_colors:
             print('fc-> ' + fc)

        with open(os.path.join(sublime.packages_path(), 'log.txt'), mode='w', encoding='utf-8') as log_file:
            log_file.write(ChTheme.tm_data)

        write_tm()



