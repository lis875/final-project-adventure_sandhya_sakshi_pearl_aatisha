from typing import List, Dict, Union
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
import json
from configs.constants import GAME_TITLE, INTRO_SCENE_ID, DEFAULTS

# Widget Import
from widgets.scene import Scene

Window.size = (960, 540) # 1920x1080 aspect ratio of the window


class App(MDApp):
    """Main application class of the game which orchestrates the entire game.

    Args:
        MDApp (_type_): Inherits MDApp class for creating the application.
    """

    def build(self) -> ScreenManager:
        """Build the application.

        Returns:
            ScreenManager: returns the ScreenManager instance
        """
        self.title = GAME_TITLE # Setting the application title
        self.sm = ScreenManager()
        self.scenes = self.load_scenes_from_config()
        self.current_scene_id = INTRO_SCENE_ID
        self.current_scene = None

        self.switch_to_scene(self.current_scene_id)
        return self.sm

    def switch_to_scene(self, scene_id: str) -> None:
        """Switch to the specified scene id.

        Args:
            scene_id (str): scene id to switch the scene to
        """
        # If there's a current scene, exit it and remove it from the ScreenManager
        if self.current_scene:
            self.current_scene.on_exit()
            self.sm.remove_widget(self.sm.get_screen(self.current_scene_id))

        # Finding the data for the specified scene id
        scene_data = next(
            (scene_data for scene_data in self.scenes if scene_data.scene_id == scene_id), None
        )
        if not scene_data:
            return

        # Creating a new Scene instance with the scene data
        self.current_scene = Scene(
            self,
            scene_id=scene_id,
            media_source=scene_data.media_source,
            media_type=scene_data.media_type,
            audio_source=scene_data.audio_source,
            button_config=scene_data.button_config,
            text_style=scene_data.text_style,
            bg_color=scene_data.bg_color,
            audio_repeat_count=scene_data.audio_repeat_count,
            backoff_rate=scene_data.backoff_rate,
            has_text=scene_data.has_text,
        )
        self.current_scene_id = scene_id

        # Creating a new Screen and add the current scene's widget to it
        screen = Screen(name=scene_id)
        screen.add_widget(self.current_scene.build())
        self.sm.add_widget(screen) # Adding the new Screen to the ScreenManager

    def load_scenes_from_config(self) -> List[Scene]:
        """Load scenes from configuration json which has the list of scenes.

        Returns:
            List[Scene]: returns the list of scene objects
        """
        try:
            with open('./configs/scenes_config.json', 'r') as file: # Loading scenes data from the scenes_config.json file
                scenes_data = json.load(file)
            scenes = [self.create_scene_from_data(scene_data) for scene_data in scenes_data]
            return scenes
        except Exception as e:
            print(f"Error loading scenes from JSON: {e}")
            return []

    def create_scene_from_data(self, scene_data: Dict[str, Union[str, int]]) -> Scene:
        """Create a Scene instance from JSON data.

        Args:
            scene_data (Dict[str, Union[str, int]]): scene data from the json file

        Returns:
            Scene: Scene class instance
        """
        return Scene(
            self,
            scene_id=scene_data['scene_id'],
            media_source=scene_data['media_source'],
            media_type=scene_data['media_type'],
            audio_source=scene_data['audio_source'],
            button_config=scene_data.get('button_config', None),
            text_style=scene_data.get('text_style', None),
            bg_color=scene_data.get('bg_color', DEFAULTS['BG_COLOR']),
            audio_repeat_count=scene_data.get('audio_repeat_count', DEFAULTS['AUDIO_REPEAT']),
            backoff_rate=scene_data.get('backoff_rate', DEFAULTS['BACKOFF_RATE']),
            has_text=scene_data.get('has_text', True),
        )


if __name__ == '__main__':
    # Starts invocation of the game
    App().run()
