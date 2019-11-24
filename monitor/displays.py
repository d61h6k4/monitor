
class Color(object):
    def __init__(self, text_color_code: int, text_style_code: int, bg_color_code: int):
        if text_color_code < 30 or text_color_code > 37:
            raise ValueError(f'Wrong text color code {text_color_code}')
        if text_style_code < 0 or text_style_code > 5:
            raise ValueError(f'Wrong text style code {text_style_code}')
        if bg_color_code < 40 or bg_color_code > 47:
            raise ValueError(f'Wrong bg color code {bg_color_code}')

        self.__color = f'\033[{text_style_code};{text_color_code};{bg_color_code}m '

    def __repr__(self):
        return self.__color

    def __str__(self):
        return self.__color


RED = Color(31, 1, 40)
ENDC = Color(37, 1, 40)
BLUE = Color(34, 1, 40)
GREEN = Color(32, 1, 40)
WHITE = Color(37, 1, 40)


class Display(object):
    def push(self, msg, color: Color = WHITE, end='\n'):
        print(f'{color}{repr(msg)}{ENDC}', end=end)
