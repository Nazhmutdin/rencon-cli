from typing import Literal

from click import Command, Option, echo

from .help_messages import welder_table_mode_option_help_message


class ManageWelderTableCommand(Command):
    def __init__(self) -> None:
        name = "manage-welder-table"

        mode_option = Option(["--mode", "-m"], type=str, help=welder_table_mode_option_help_message)

        super().__init__(name=name, params=[mode_option], callback=self.execute)


    def _append_mode_execution(self) -> None: ...


    def _update_mode_execution(self) -> None: ...

    
    def execute(self, mode: Literal["a", "u"]) -> None:
        mode = mode.lower()

        match mode:
            case "a":
                self._append_mode_execution()

            case "u":
                self._update_mode_execution()
            
            case _:
                echo("Invalid mode")
