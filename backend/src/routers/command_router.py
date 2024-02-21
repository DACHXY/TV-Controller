from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.dbcontext import Database
from src.repositories import Repository
from src.model import Command


router = APIRouter()


def get_repo(db=Depends(Database)):
    return Repository(db, Command)


@router.get("/")
def get_commands(
    command_repo: Repository[Command] = Depends(get_repo),
):
    result = command_repo.get_all()
    if result is None:
        return []

    return result


@router.post("/")
def post_commands(
    command: Command,
    command_repo: Repository[Command] = Depends(get_repo),
):
    if command.id is None:
        command_repo.add(command)
        command_repo.save_changes()
        return command

    entity = command_repo.get_by_id(command.id)
    if entity is None:
        raise HTTPException(status_code=301, detail=f"Id: {command.id} not found")

    entity.command = command.command
    entity.name = command.name
    entity.sequence = command.sequence

    command_repo.update(entity)
    command_repo.save_changes()
    return entity


@router.delete("/{id}")
def delete_command(id: int, command_repo: Repository[Command] = Depends(get_repo)):
    command = command_repo.get_by_id(id)
    if command is None:
        raise HTTPException(status_code=301, detail=f"Id: {id} not found.")

    command_repo.remove(command)
    command_repo.save_changes()
    return "ok"
