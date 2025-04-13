import click

from .names import mknames
from .providers import list_providers

BOYCOLOR = "blue"
GIRLCOLOR = "magenta"


@click.command()
@click.option(
    "-b",
    "--boys",
    default=0,
    help="Number of boy names to generate.",
    type=click.IntRange(0, None),
    metavar="<int>",
)
@click.option(
    "-g",
    "--girls",
    default=0,
    help="Number of girl names to generate.",
    type=click.IntRange(0, None),
    metavar="<int>",
)
@click.option(
    "-c",
    "--country",
    default="fra",
    help="Country code",
    type=click.Choice(list_providers(), case_sensitive=False),
    show_default=True,
)
@click.option(
    "-d",
    "--firstname-duplicates",
    is_flag=True,
    help="Allow duplicates on firstnames.",
)
@click.option(
    "-D",
    "--lastname-duplicates",
    is_flag=True,
    help="Allow duplicates on lastnames.",
)
@click.option(
    "-s",
    "--seed",
    default=None,
    help="Custom seed.",
    type=int,
    metavar="<int>",
)
@click.option(
    "-N",
    "--no-cache",
    is_flag=True,
    help="Clear cache.",
)
@click.version_option()
@click.help_option("-h", "--help")
def main(
    boys: int,
    girls: int,
    country: str,
    seed: int | None,
    no_cache: bool,
    firstname_duplicates: bool,
    lastname_duplicates: bool,
) -> None:
    """
    Generate firstnames and lastnames picked randomly from the French INSEE
    database or USA's SSA database.

    The firstnames and lastnames are generated based on the number of
    occurrences in the database.
    """
    if boys <= 0 and girls <= 0:
        gender = click.prompt(
            "What do you want to generate? b[o]th/[b]oys/[g]irls",
            type=click.Choice(("b", "g", "o"), case_sensitive=False),
            default="o",
            show_choices=False,
        )
        boys = 0
        girls = 0
        if gender in ("o", "b"):
            boys = click.prompt(
                "How many boy names do you want to generate?",
                type=click.IntRange(0, None),
                default=10,
            )
        if gender in ("o", "g"):
            girls = click.prompt(
                "How many girl names do you want to generate?",
                type=click.IntRange(0, None),
                default=10,
            )

    boysnames, girlsnames = mknames(
        boys=boys,
        girls=girls,
        country=country,
        seed=seed,
        no_cache=no_cache,
        firstname_duplicates=firstname_duplicates,
        lastname_duplicates=lastname_duplicates,
    )

    for color, it in ((BOYCOLOR, boysnames), (GIRLCOLOR, girlsnames)):
        for name, last_name in it:
            click.secho(f"{name:<12}", fg=color, nl=False)
            click.echo(f"{last_name}")


if __name__ == "__main__":
    main()
