from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from src.interfaces import IAudioManager


class WindowsAudioManager(IAudioManager):
    def __init__(self) -> None:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)

    def volume_set(self, value: int) -> None:
        if value > 100:
            value = 100
        if value < 0:
            value = 0
        db_value = value / 100
        self.volume.SetMasterVolumeLevelScalar(db_value, None)

    def volume_up(self, value: int) -> None:
        current_value = self.get_volume()
        new_value = current_value + value
        self.volume_set(new_value)

    def volume_down(self, value: int) -> None:
        current_value = self.get_volume()
        new_value = current_value - value
        self.volume_set(new_value)

    def volume_off(self) -> None:
        self.volume.SetMute(1, None)

    def volume_on(self) -> None:
        self.volume.SetMute(0, None)

    def is_muted(self) -> bool:
        return True if self.volume.GetMute() == 1 else False

    def toggle_volume_mute(self) -> None:
        if self.is_muted():
            self.volume_on()
        else:
            self.volume_off()

    def get_volume(self) -> int:
        db_value = self.volume.GetMasterVolumeLevelScalar() * 100
        return db_value
