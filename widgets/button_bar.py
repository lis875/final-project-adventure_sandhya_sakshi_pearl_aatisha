from typing import List, Dict, Union
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.button import MDFillRoundFlatButton


class ButtonBar(AnchorLayout):
    """Custom button bar widget. Renders the list of buttons horizontally

    Args:
        AnchorLayout (_type_): Inherits AnchorLayout for positioning the buttons 
    """

    def __init__(self, buttons: List[Dict[str, Union[str, int]]], app: MDApp, **kwargs):
        super(ButtonBar, self).__init__(**kwargs)
        if app:
            box_layout = BoxLayout(
                orientation='horizontal', spacing=30, size_hint=(None, None), height=150
            )

            for button_info in buttons:
                button = MDFillRoundFlatButton(
                    text=button_info['text'],
                    on_press=lambda _, button_info=button_info: app.switch_to_scene(button_info['target_scene_id']),
                    size_hint=(None, None),
                    height=50,
                    font_style='Subtitle1',
                    line_color=(0.01960784313,0.85098039215,0.90980392156,1),
                    line_width=1.1,
                    md_bg_color=(1,0.16470588235,0.42745098039,1),
                )
                button.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
                box_layout.add_widget(button)

            box_layout.bind(minimum_width=box_layout.setter('width'))
            self.pos_hint = {'center_y': 0.18}
            self.add_widget(box_layout)
