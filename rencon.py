import click

from src.manage_db.commands import ManageWelderTableCommand
from src.report_commands.commands import NDTReportCommand
from src.parse_naks import ParsePersonalCommand
from src.manage_registry.commands import ManageActsRegistryCommand


@click.group()
def cli(): ...


cli.add_command(ManageWelderTableCommand())
cli.add_command(NDTReportCommand())
cli.add_command(ParsePersonalCommand())
cli.add_command(ManageActsRegistryCommand())


if __name__ == "__main__":
    cli()
