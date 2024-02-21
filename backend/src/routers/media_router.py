from fastapi import APIRouter, Depends
from src.managers.audio_manager import AudioManager

router = APIRouter()


@router.get("/volume/up")
async def volume_up(audio_manager: AudioManager = Depends(AudioManager)):
    audio_manager.volume_up(5)
    return "ok"


@router.get("/volume/down")
async def volume_down(audio_manager: AudioManager = Depends(AudioManager)):
    audio_manager.volume_down(5)
    return "ok"


@router.get("/volume/set")
async def volume_set(value: int, audio_manager: AudioManager = Depends(AudioManager)):
    audio_manager.volume_set(value)
    return "ok"


@router.get("/volume/mute")
async def volume_mute(audio_manager: AudioManager = Depends(AudioManager)):
    audio_manager.volume_off()
    return "ok"


@router.get("/volume/unmute")
async def volume_unmute(audio_manager: AudioManager = Depends(AudioManager)):
    audio_manager.volume_on()
    return "ok"


@router.get("/volume/togglemute")
async def volume_toggle_mute(audio_manager: AudioManager = Depends(AudioManager)):
    audio_manager.toggle_volume_mute()
    return "ok"


@router.get("/volume")
async def get_volume(audio_manager: AudioManager = Depends(AudioManager)) -> int:
    current_value: int = audio_manager.get_volume()
    return current_value
