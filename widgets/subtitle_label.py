from kivy.graphics import Color, Rectangle
from kivymd.uix.label import MDLabel


class SubtitleLabel(MDLabel):
    """Creates a custom label for subtitle

    Args:
        MDLabel (_type_): Inherits the MDLabel class
    """

    def __init__(self, subtitle, padding=(10, 5), **kwargs):
        super(SubtitleLabel, self).__init__(text=subtitle, **kwargs)
        self.padding = padding
        with self.canvas.before:
            Color(0, 0, 0, 0.6)  # Set background color with alpha (transparency)
            self.bg_rect = Rectangle(pos=self.pos, size=self.get_updated_rect_size())

        self.bind(pos=self.update_bg_rect_pos, size=self.update_bg_rect_size)

    def get_updated_rect_size(self):
        return self.width + self.padding[0], self.height + self.padding[1]

    def update_bg_rect_pos(self, _, value):
        self.bg_rect.pos = value

    def update_bg_rect_size(self, _, value):
        self.bg_rect.size = self.get_updated_rect_size()
