from click import Command, Option, echo

from .services import NDTReportService


class NDTReportCommand(Command):
    
    def __init__(self) -> None:
        name = 'ndt-report'

        limit_option = Option(['--limit'], type=int)
        save_mode_option = Option(['--save_mode'], type=str, help="modes: 'excel', 'pdf'")

        super().__init__(name=name, params=[save_mode_option, limit_option], callback=self.execute)

    
    def execute(self, save_mode: str, limit: int | None = None) -> None:
        service = NDTReportService()

        service.report(save_mode, limit)
