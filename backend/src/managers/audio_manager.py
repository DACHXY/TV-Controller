import platform
from src.interfaces import IAudioManager


class AudioManager(IAudioManager):
    def __init__(self) -> None:
        os_name = platform.system()
        if os_name == "Windows":
            from src.managers.windows_audio_manager import WindowsAudioManager

            self.audio_manager = WindowsAudioManager()
        elif os_name == "Linux":
            from src.managers.linux_audio_manager import LinuxAudioManager

            self.audio_manager = LinuxAudioManager()
        else:
            raise Exception(f"OS not found: {os_name}")

    def volume_set(self, value: int) -> None:
        self.volume_on()
        self.audio_manager.volume_set(value)

    def volume_up(self, value: int) -> None:
        self.volume_on()
        self.audio_manager.volume_up(value)

    def volume_down(self, value: int) -> None:
        self.audio_manager.volume_down(value)

    def volume_on(self) -> None:
        self.audio_manager.volume_on()

    def volume_off(self) -> None:
        self.audio_manager.volume_off()

    def toggle_volume_mute(self) -> None:
        self.audio_manager.toggle_volume_mute()

    def get_volume(self) -> int:
        return self.audio_manager.get_volume()

    def is_muted(self) -> bool:
        return self.audio_manager.is_muted()
