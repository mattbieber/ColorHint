'''
ch_view_collection

'''

import sublime

try:
    from ColorHint.ch_view import ChView
except ImportError:
    from ch_view import ChView

class ChViewCollection:
    views = {}

    @staticmethod
    def proc_view(view):
        if view.size() == 0: return
        print('-------- proc view')
        key = view.id()
        is_new = key not in ChViewCollection.views

        if is_new:
            ChViewCollection.views[view.id()] = ChView(view)

        found = view.find_all('#(?:[0-9a-fA-F]{3}){1,2}', sublime.IGNORECASE)
        found.extend(view.find_all('rgb\([^)]*\)'))

        wrapped_view = ChViewCollection.views[view.id()]

        print(str(len(found)) + ':' + str(wrapped_view.wrapped_regions_count()))

        for f in found:
            wrapped_view.proc_region(f)

        wrapped_view.commit()
        wrapped_view.highlight_view()

    @staticmethod
    def highlight_views():
        for key in ChViewCollection.views:
            ChViewCollection.views[key].view_needs_update = True
            ChViewCollection.views[key].highlight_view()

    @staticmethod
    def clear_views():
        print('clearviews')
        for key in ChViewCollection.views:
            ChViewCollection.views[key].unhighlight_view()

        print(str(len(ChViewCollection.views.keys())))

        ChViewCollection.views.clear()

        print(str(len(ChViewCollection.views.keys())))

    @staticmethod
    def diff(view):
        key = ChViewCollection.get_key(view)
        return ChViewCollection.views[key].diff()

