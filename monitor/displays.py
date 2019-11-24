import enum


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


class Tags(enum.Enum):
    ALERT = 1
    NORMAL = 2
    STATS = 3


class Display(object):
    def show_string(self, msg: str, color: Color):
        print(f'{color}{repr(msg)}{ENDC}')

    def show_stats(self, msg):
        chars_num = 12
        sep_line = '|{}|{}|'.format('-' * chars_num, '-' * (len('HITS') + 2))
        fill_line = '|' + str(RED) + '{:^10}' + str(ENDC) + '|' + str(BLUE) + '{:^4}' + str(ENDC) + '|'

        res = [f'{sep_line} {sep_line} {sep_line}',
               f'{fill_line.format("SECTIONS", "HITS")} {fill_line.format("METHODS", "HITS")} {fill_line.format("USERS", "HITS")}']
        for section, method, user in zip(msg.section_stats(), msg.method_stats(), msg.user_stats()):
            res.append(f'{sep_line} {sep_line} {sep_line}')
            res.append(f'{fill_line.format(section[0], section[1])} {fill_line.format(method[0], method[1])} {fill_line.format(user[0], user[1])}')
        res.append(f'{sep_line} {sep_line} {sep_line}')

        print('\n'.join(res), end='\n\n')

    def push(self, msg, tag: Tags):
        if tag == Tags.ALERT:
            self.show_string(msg, RED)
        elif tag == Tags.NORMAL:
            self.show_string(repr(msg), GREEN)
        elif tag == Tags.STATS:
            self.show_stats(msg)
