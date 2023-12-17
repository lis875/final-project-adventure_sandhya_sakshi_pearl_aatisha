from typing import List, Optional, Dict, Tuple, Union
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.core.audio import SoundLoader
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.clock import Clock

from configs.constants import DEFAULTS
from utils.helper import read_file

# Widgets Import
from widgets.button_bar import ButtonBar
from widgets.close_button import CloseButton
from widgets.subtitle_label import SubtitleLabel


class Scene(RelativeLayout):
    """Custom scene widget. Creates a scene for the game.

    Args:
        RelativeLayout (_type_): Inherits the RelativeLayout for positioning the widgets on the canvas.
    """

    def __init__(self, app: MDApp, scene_id: str, media_source: str, media_type: str, audio_source: Optional[str],
                    button_config: Optional[List[Dict[str, Union[str, int]]]], text_style: Optional[Dict[str, Union[str, Tuple[float, float, float, float]]]],
                    bg_color: Tuple[float, float, float, float] = DEFAULTS['BG_COLOR'], audio_repeat_count: int = DEFAULTS['AUDIO_REPEAT'],
                    backoff_rate: int = DEFAULTS['BACKOFF_RATE'], has_text: bool = True, **kwargs):
        super(Scene, self).__init__(**kwargs)
        self.app = app
        self.scene_id = scene_id
        self.bg_color = bg_color
        self.media_source = media_source
        self.media_type = media_type
        self.audio_source = audio_source
        self.button_config = button_config
        if text_style:
            self.text_style = text_style
        else:
            self.text_style = DEFAULTS['DEFAULT_TEXT_STYLE']
        self.media_player = None
        self.audio = None
        self.audio_repeat_count = audio_repeat_count
        self.audio_play_count = 0
        self.scene_ended = False
        self.has_text = has_text
        self.backoff_rate = backoff_rate
        self.timer_duration = DEFAULTS['TIMER']
        self.bind(pos=self.redraw)
        self.bind(size=self.redraw)

    def redraw(self, *args) -> None:
        """Redraw the scene."""
        with self.canvas.before:
            Window.clearcolor = self.bg_color

    def build(self) -> None:
        """Build the scene."""
        self.build_media_player()
        self.build_subtitle()
        self.build_button_bar()
        self.build_close_button()
        self.build_timer_label()
        self.audio_player_scheduler = Clock.schedule_once(self.build_audio_player, 1)

        return self

    def build_media_player(self) -> None:
        """Build the media player."""
        media_path = f'assets/{self.scene_id}/{self.media_source}'
        if self.media_type == 'video':
            self.media_player = Video(
                source=media_path, state='play', options={'eos': 'loop', 'hide_controls': True}
            )
        elif self.media_type == 'image':
            self.media_player = Image(source=media_path)

        self.add_widget(self.media_player)

    def build_subtitle(self) -> None:
        """Build the label."""
        if self.has_text:
            subtitle_path = f'assets/{self.scene_id}/subtitle.txt'
            subtitle = read_file(subtitle_path)
            label = SubtitleLabel(
                subtitle=subtitle,
                pos_hint={'center_x': 0.5, 'center_y': 0.25},  # Adjust y value to position the label
                size_hint=(0.9, None),  # Set width to 70%, height to 10%
                halign="center",
                theme_text_color="Custom",
                **self.text_style
            )
            self.add_widget(label)

    def build_button_bar(self) -> None:
        """Build the button bar."""
        if self.button_config:
            button_bar = ButtonBar(self.button_config, app=self.app)
            self.add_widget(button_bar)

    def build_audio_player(self, _) -> None:
        """Build the audio player."""
        audio_path = f'assets/{self.scene_id}/{self.audio_source}'
        if self.audio_source:
            self.audio = SoundLoader.load(audio_path)
            if self.audio:
                self.audio.loop = False
                self.audio.bind(on_stop=self.on_audio_stop)
                self.audio.play()

    def build_close_button(self) -> None:
        """Build the close button."""
        close_button = CloseButton(self.app)
        self.add_widget(close_button)

    def build_timer_label(self) -> None:
        """Build the timer label."""
        self.timer_label = MDLabel(
            text="",
            pos_hint={'top': 1},
            size_hint_y=None,
            height=50,
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="Subtitle1"
        )
        self.add_widget(self.timer_label)

    def on_exit(self) -> None:
        """Handle exit events."""
        self.scene_ended = True
        if self.audio:
            self.audio.unbind(on_stop=self.on_audio_stop)
            self.audio.stop()

        self.unschedule_events()

    def unschedule_events(self) -> None:
        """Unschedule events."""
        if hasattr(self, 'audio_repeat_scheduler'):
            Clock.unschedule(self.audio_repeat_scheduler)
        if hasattr(self, 'fallback_event_scheduler'):
            Clock.unschedule(self.fallback_event_scheduler)
        if hasattr(self, 'timer_event_interval'):
            Clock.unschedule(self.timer_event_interval)
        if hasattr(self, 'audio_player_scheduler'):
            Clock.unschedule(self.audio_player_scheduler)


    def on_audio_stop(self, _) -> None:
        """Handle audio stop events."""
        if not self.scene_ended:
            self.audio.seek(0)
            self.audio_play_count += 1

            if self.audio_play_count < self.audio_repeat_count:
                self.audio.seek(0)
                self.audio_repeat_scheduler = Clock.schedule_once(
                    self.play_audio_after_buffer, self.backoff_rate
                )
            else:
                self.audio.unbind(on_stop=self.on_audio_stop)
                self.audio.stop()
                self.fallback_event_scheduler = Clock.schedule_once(self.go_to_fallback, self.backoff_rate)

    def play_audio_after_buffer(self, _) -> None:
        """Play audio after buffer time."""
        if self.audio:
            self.audio.play()
            self.audio.seek(0)

    def go_to_fallback(self, _) -> None:
        """Go to fallback scene."""
        self.timer_label.text = f"Idle. Game terminating in {self.timer_duration} seconds"
        self.timer_event_interval = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, _) -> None:
        """Update the timer."""
        self.timer_duration -= 1
        self.timer_label.text = f"Idle. Game terminating in {self.timer_duration} seconds"

        if self.timer_duration <= 0:
            self.app.stop()
