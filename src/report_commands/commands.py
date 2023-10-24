from click import Command, Option, echo

from src.report_commands.ndt_report_services import NDTReportService


class NDTReportCommand(Command):
    
    def __init__(self) -> None:
        name = 'ndt-report'

        limit_option = Option(['--limit'], type=int)
        search_date_option = Option(["--search_date"], type=str)
        save_mode_option = Option(['--save_mode'], type=str, help="modes: 'excel', 'pdf'")

        super().__init__(name=name, params=[save_mode_option, limit_option, search_date_option], callback=self.execute)


    def execute(self, save_mode: str, limit: int | None = None, search_date: str | None = None) -> None:
        service = NDTReportService()

        service.report(search_date=search_date, save_mode=save_mode, limit=limit)
