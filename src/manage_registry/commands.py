from typing import TypeAlias

from click import Command, Option, echo


class ManageRegistryCommand(Command):
    def __init__(self) -> None:

        name = ''

        mode_option = Option(['--mode', '-m'], type=str, help='w')

        super().__init__(name=name, params=[mode_option], callback=self.execute)

    
    def execute(self, mode: str) -> None:
        mode = mode.lower()
        
        match mode:
            case 'w':
                self._ndt_analyze_mode_execution()
            case _:
                echo("Invalid mode")