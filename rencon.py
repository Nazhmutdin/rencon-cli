import click

from src.manage_db.commands import ManageWelderTableCommand
from src.report_commands.commands import NDTReportCommand


@click.group()
def cli(): ...


cli.add_command(ManageWelderTableCommand())
cli.add_command(NDTReportCommand())


if __name__ == "__main__":
    cli()
