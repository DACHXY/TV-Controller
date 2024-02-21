from fastapi import APIRouter, Depends
from typing import List
from dbcontext import Database
from src.repositories import Repository
from src.model import Command


router = APIRouter()


@router.get("/")
def get_commands(
    command_repo: Repository[Command] = Depends(Repository),
) -> List[Command]:
    result = command_repo.get_all()
    if result is None:
        return []

    return result
