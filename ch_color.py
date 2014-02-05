# -*- coding: utf-8 -*-


"""
    livecss.color
    ~~~~~~~~~

    This module implements some useful utilities.

"""

import struct

try:
    from ColorHint.ch_named_colors import ChNamedColors
except ImportError:
    from ch_named_colors import ChNamedColors


class ChColor(object):
    """Convenience to work with colors"""

    def __init__(self, color):
        prefix = color[:4]

        if prefix[0] == '#':
            print('hex')
        elif prefix == 'rgba':
            print('rgba')
        elif prefix[:3] == 'rgb':

            print('rgb')
        else:
            print('named')

        self.color = color

    @property
    def hex(self):
        color = self.color
        if color in ChNamedColors:
            hex_color = ChNamedColors[color]
        elif not color.startswith('#'):
            # if rgb
            color = color.split(',')
            hex_color = self._rgb_to_hex(tuple(color))
        else:
            if len(color) == 4:
                # 3 sign hex
                color = "#{0[1]}{0[1]}{0[2]}{0[2]}{0[3]}{0[3]}".format(color)
            hex_color = color

        return hex_color

    @property
    def undash(self):
        return self.hex.lstrip('#')

    @property
    def opposite(self):
        r, g, b = self._hex_to_rgb(self.undash)
        brightness = (r + r + b + b + g + g) / 6
        if brightness > 130:
            return '#000000'
        else:
            return '#ffffff'

    def __repr__(self):
        return self.hex

    def __str__(self):
        return self.hex

    def __eq__(self, other):
        return self.hex == other

    def __hash__(self):
        return hash(self.hex)

    def _rgb_to_hex(self, rgb):
        if str(rgb[0])[-1] == '%':
            # percentage notation
            r = int(rgb[0].rstrip('%')) * 255 / 100
            g = int(rgb[1].rstrip('%')) * 255 / 100
            b = int(rgb[2].rstrip('%')) * 255 / 100
            return self._rgb_to_hex((r, g, b))

        if len(rgb) == 4:
            #rgba
            rgb = rgb[0:3]

        return '#%02x%02x%02x' % tuple(int(x) for x in rgb)

    def _hex_to_rgb(self, hex):
        hex_len = len(hex)
        return tuple(int(hex[i:i + hex_len / 3], 16) for i in range(0, hex_len, hex_len / 3))

    @staticmethod
    def evalute_color(color):
        prefix = color[:4]

        if prefix[0] == '#':
            if(len(color) == 4):
                return '#{0}{0}{1}{1}{2}{2}'.format(color[1], color[2],color[3])
            return(color)

        elif prefix == 'rgba':
            print('rgba')
        elif prefix[:3] == 'rgb':

            val = color[4:]
            split = val.split(",")
            split[2] = ''.join(split[2].split(")")[0])
            r = int(split[0])
            g = int(split[1])
            b = int(split[2])
            tu = (r, g, b)

            return ('#%02x%02x%02x' % tu)

        else:
            print('named')
