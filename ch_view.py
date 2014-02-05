import os
import sublime
import re

# print('...............file: wrapper')

try:
    from ColorHint.ch_theme import ChTheme
    from ColorHint.ch_color import ChColor
except ImportError:
    from ch_theme import ChTheme
    from ch_color import ChColor


class ChView:

    def __init__(self, view):
        self.view = view
        self.regions_need_update = False
        self.view_needs_update = False
        self.wrapped_regions = {}
        self.region_count = 0

    def _get_view_encoding(self):
        encoding = self.view.encoding()

    def on_disk(self):
        return self.view.file_name() is not None

    def proc_region(self, reg):

        color = self.view.substr(reg)
        key = ChColor.evalute_color(color)

        if not key in self.wrapped_regions:
            self.wrapped_regions[key] = []

        if(reg in self.wrapped_regions[key]):
            return

        self.region_count += 1
        self.wrapped_regions[key].append(reg)
        self.regions_need_update = True

    def get_wrapped_regions(self):
        return self.wrapped_regions

    def wrapped_regions_count(self):
        return self.region_count

    def commit(self):
        if self.regions_need_update:
            print('...............wrapped needs update')

            ChTheme.update_tm(self.wrapped_regions.keys())
            self.regions_need_update = False
            self.view_needs_update = True

    def highlight_view(self):
        print('...............wrapped view highlight_view(): ' + str(len(self.wrapped_regions.keys())))

        for key in self.wrapped_regions.keys():
            self.view.add_regions(key, self.wrapped_regions[key], ChTheme.TM_PREFIX + key, "",
            sublime.DRAW_EMPTY | sublime.DRAW_NO_OUTLINE)

        self.view_needs_update = False

    def unhighlight_view(self):
        self.view.erase_status('colorhint_status')
        for key in self.wrapped_regions.keys():
            self.view.erase_regions(key)
