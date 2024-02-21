from typing import Generic, List, Sequence, Type
from src.model import DBModel
from src.dbcontext import Database


class Repository(Generic[DBModel]):
    def __init__(self, db: Database, model: Type[DBModel]) -> None:
        self.db: Database = db
        self.cursor = self.db.cursor
        self.conn = self.db.conn

        # Get Scheme Information
        self.model = model
        self.table_name = self.model.__name__
        self.fields = self.model.model_json_schema()["properties"]
        del self.fields["id"]
        self.properties: List[str] = list(self.fields.keys())

        # Create Table if not exists
        self._create_table()

    def _create_table(self) -> None:
        properties = ", ".join(
            [
                f"{x} INTEGER" if self.fields[x]["type"] == "integer" else f"{x} TEXT"
                for x in self.fields
            ]
        )

        sql_create_command = f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {properties});"
        self.cursor.execute(sql_create_command)
        self.conn.commit()

    def _parse(self, row: Sequence[None | int | str]) -> DBModel:
        model_obj = {
            self.properties[index - 1] if index > 0 else "id": value
            for index, value in enumerate(row)
        }

        new_model = self.model.model_validate(model_obj)
        return new_model

    def _parse_model_value(self, model: DBModel, remove_id: bool = True) -> list[str]:
        model_properties = model.model_dump()
        if remove_id:
            del model_properties["id"]

        values = []
        for property in self.properties:
            value = model_properties[property]
            values.append(self._parse_value(value))

        return values

    def _parse_value(self, value: int | None | str) -> str:
        # null
        if value is None:
            return "NULL"

        # string
        if isinstance(value, str):
            return f"'{value}'"

        # int or else
        return str(value)

    def get_by_id(self, id: int) -> DBModel | None:
        properties_str = ", ".join(self.properties)
        sql_select_command = (
            f"SELECT id, {properties_str} FROM {self.table_name} WHERE id = ?;"
        )
        self.cursor.execute(sql_select_command, (id,))
        row = self.cursor.fetchone()
        if row is None:
            return None

        new_model = self._parse(row)
        return new_model

    def get_all(self) -> List[DBModel] | None:
        properties_str = ", ".join(self.properties)
        sql_select_command = f"SELECT id, {properties_str} FROM {self.table_name};"
        self.cursor.execute(sql_select_command)
        rows = self.cursor.fetchall()

        if rows is None:
            return None

        new_models = [self._parse(row) for row in rows]
        return new_models

    def add(self, model: DBModel) -> None:
        values = self._parse_model_value(model)
        values = ", ".join(values)
        properties = ", ".join(self.properties)

        sql_add_command = (
            f"INSERT INTO {self.table_name} ({properties}) VALUES ({values});"
        )
        print(sql_add_command)
        self.cursor.execute(sql_add_command)
        # update id
        model.id = self.cursor.lastrowid

    def remove(self, model: DBModel) -> None:
        sql_remove_command = f"DELETE FROM {self.table_name} WHERE id = {model.id};"
        self.cursor.execute(sql_remove_command)

    def update(self, model: DBModel) -> None:
        values = self._parse_model_value(model)
        properties_value = ", ".join(
            f"{x} = {values[index]}" for index, x in enumerate(self.properties)
        )
        sql_update_command = (
            f"UPDATE {self.table_name} SET {properties_value} WHERE id = {model.id};"
        )
        self.cursor.execute(sql_update_command)

    def save_changes(self) -> None:
        self.conn.commit()
