import click

from src.manage_db.commands import ManageWelderTableCommand
from src.report_commands.commands import NDTReportCommand
from src.parse_naks.commands import ParsePersonalCommand


@click.group()
def cli(): ...


cli.add_command(ManageWelderTableCommand())
cli.add_command(NDTReportCommand())
cli.add_command(ParsePersonalCommand())


if __name__ == "__main__":
    cli()
