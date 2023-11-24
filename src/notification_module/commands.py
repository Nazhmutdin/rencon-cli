import typing as t
from click import Command, Option, echo

from .welder_certificate_expiration_service import WelderCertificationExpirationNotificationService


class WelderNotificationCommand(Command):
    def __init__(self) -> None:
        name = "welder-notifications"

        mode_option = Option(["--mode", "-m"], type = int, help="1 - welder certificate expiration notification\n\n2 - engineer certificate notification")
        super().__init__(name=name, params=[mode_option], callback=self.execute)


    def execute(self, mode: int) -> None:
        match mode:
            case 1:
                WelderCertificationExpirationNotificationService().notificate()

            case 2:
                ...

            case _:
                echo("Invalid mode")
        