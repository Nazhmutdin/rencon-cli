from typing import TypeAlias
from pathlib import Path
from re import match
import os

from .act_registry_services import ActRegistryService

from click import Command, Option, echo



class ManageActsRegistryCommand(Command):
    def __init__(self) -> None:

        name = 'manage-act-registry'

        folder_option = Option(['--folder', '-f'], type=str, help='w')

        super().__init__(name=name, params=[folder_option], callback=self.execute)


    def execute(self, folder: str | Path) -> None:
        service = ActRegistryService()

        service.update_registry(folder)
        