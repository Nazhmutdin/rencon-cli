import click

from src.manage_db.commands import ManageWelderTableCommand


@click.group()
def cli(): ...


cli.add_command(ManageWelderTableCommand())


if __name__ == "__main__":
    cli()
