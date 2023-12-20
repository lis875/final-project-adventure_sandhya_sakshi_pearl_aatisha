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
        """
        Initialize a ButtonBar object.

        Parameters:
        - buttons: List of dictionaries containing button information.
        - app: Reference to the main application.
        - **kwargs: Additional keyword arguments.

        """
        super(ButtonBar, self).__init__(**kwargs)# Call the constructor of the parent class (BoxLayout).
        if app:# Check if the app reference is provided.
            # Create a horizontal BoxLayout with specified properties.
            box_layout = BoxLayout(
                orientation='horizontal',  # Set the orientation to horizontal.
                spacing=30,  # Set the spacing between widgets.
                size_hint=(None, None),  # Allow explicit control over size.
                height=150  # Set the height of the BoxLayout.
            )


            # Iterating through the list of button information dictionaries
            for button_info in buttons:
                button = MDFillRoundFlatButton(
                    # Create a button with the specified properties
                    text=button_info['text'],  # Setting the text of the button
                    on_press=lambda _, button_info=button_info: app.switch_to_scene(button_info['target_scene_id']),  # Define on_press behavior using a lambda function to capture button_info
                    size_hint=(None, None),  # Allowing explicit control over the button size
                    height=50,  # Setting the height of the button
                    font_style='Subtitle1',  # Setting the font style of the button text
                    line_color=(0.01960784313, 0.85098039215, 0.90980392156, 1),  # Setting the color of the button border
                    line_width=1.1,  # Setting the width of the button border
                    md_bg_color=(1, 0.16470588235, 0.42745098039, 1),  # Setting the background color of the button

                )
                button.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
                box_layout.add_widget(button) # Adding the button to the BoxLayout

            # box_layout.bind(minimum_width=box_layout.setter('width'))
            # self.pos_hint = {'center_y': 0.18}
            # self.add_widget(box_layout)
                
            box_layout.bind(minimum_width=box_layout.setter('width'))# Bind the minimum width of the box_layout to the width property.
            self.pos_hint = {'center_y': 0.18}# Set the position hint for the widget to be centered vertically at 18% of the total height. 
            self.add_widget(box_layout)# Add the box_layout widget as a child to the current widget.

