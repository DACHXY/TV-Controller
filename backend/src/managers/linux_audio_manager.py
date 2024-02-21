from src.interfaces import IAudioManager
import alsaaudio


class LinuxAudioManager(IAudioManager):
    def __init__(self) -> None:
        self.mixer = alsaaudio.Mixer()

    def get_volume(self) -> int:
        vol = self.mixer.getvolume()
        return int(vol[0])

    def volume_set(self, value: int) -> None:
        if value < 0:
            value = 0
        if value > 100:
            value = 100
        self.mixer.setvolume(value)

    def volume_up(self, value: int) -> None:
        current_value = self.get_volume()
        new_value = current_value + value
        self.volume_set(new_value)

    def volume_down(self, value: int) -> None:
        current_value = self.get_volume()
        new_value = current_value - value
        self.volume_set(new_value)

    def volume_off(self) -> None:
        self.mixer.setmute(1)

    def volume_on(self) -> None:
        self.mixer.setmute(0)

    def toggle_volume_mute(self) -> None:
        if self.is_muted():
            self.volume_on()
        else:
            self.volume_off()

    def is_muted(self) -> bool:
        value = self.mixer.getmute()
        return True if int(value[0]) == 1 else False
