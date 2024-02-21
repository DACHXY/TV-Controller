from abc import ABC, abstractmethod


class IAudioManager(ABC):
    @abstractmethod
    def volume_set(self, value: int) -> None:
        pass

    @abstractmethod
    def volume_up(self, value: int) -> None:
        pass

    @abstractmethod
    def volume_down(self, value: int) -> None:
        pass

    @abstractmethod
    def volume_off(self) -> None:
        pass

    @abstractmethod
    def volume_on(self) -> None:
        pass

    @abstractmethod
    def toggle_volume_mute(self) -> None:
        pass

    @abstractmethod
    def get_volume(self) -> int:
        pass

    @abstractmethod
    def is_muted(self) -> bool:
        pass
