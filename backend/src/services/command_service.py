from dbcontext import Database
from src.repositories import Repository
from fastapi import Depends
from typing import List
from model import Command


class CommandService:
    def __init__(self, db: Database) -> None:
        self._command_repo: Repository[Command] = Repository(db, model=Command)

    def get_all(self) -> List[Command]:
        result = self._command_repo.get_all()
        if result is None:
            return []
        return result

    def get_by_id(self) -> None:
        pass
