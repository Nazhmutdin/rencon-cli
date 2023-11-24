import click

from src.manage_db.commands import ManageWelderDataCommand
from src.report_commands.commands import NDTReportCommand
from src.parse_naks import ParsePersonalCommand
from src.manage_registry import ParseNDTReport, ManageWelderRegistryCommand
from src.notification_module import WelderNotificationCommand
from src.another_commands import RenameFolderCommand


@click.group()
def cli(): ...


cli.add_command(ManageWelderDataCommand())
cli.add_command(NDTReportCommand())
cli.add_command(ParsePersonalCommand())
cli.add_command(ParseNDTReport())
cli.add_command(ManageWelderRegistryCommand())
cli.add_command(WelderNotificationCommand())
cli.add_command(RenameFolderCommand())


if __name__ == "__main__":
    cli()
