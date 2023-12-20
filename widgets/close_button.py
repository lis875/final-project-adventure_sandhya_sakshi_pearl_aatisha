from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.button import MDIconButton


class CloseButton(AnchorLayout):
    """Custom close button widget.

    Args:
        AnchorLayout (_type_): Inherits AnchorLayout for positing the close button
    """

    def __init__(self, app: MDApp, **kwargs):
        super(CloseButton, self).__init__(**kwargs)
        if app:
            self.size_hint = (None, None)
            self.width = 50
            self.height = 50
            self.anchor_x = 'right'
            self.anchor_y = 'bottom'

            # Creating a BoxLayout for horizontal arrangement of widgets and styling it
            box_layout = BoxLayout(
                orientation='horizontal', spacing=5, size_hint=(None, None), size=(50, 50)
            )
            close_button = MDIconButton( # Creating an MDIconButton for the close button
                icon="power", # Setting the icon of the button to "power"
                on_press=app.stop, # Setting the on_press event to stop the App
                text_color=(1, 1, 1, 1),
                theme_text_color="Custom",
            )

            box_layout.add_widget(close_button) # Adding the close button to the BoxLayout
            self.add_widget(box_layout)
            self.pos_hint = {'right': 0.97, 'bottom': 0}
