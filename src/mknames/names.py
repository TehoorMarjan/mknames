from pathlib import Path

import hishel
from platformdirs import user_cache_dir

from .providers import get_provider

CACHEAPPNAME = "mknames"
CACHEAPPAUTHOR = "TehoorMarjan"
CACHETTL = 259200  # 3 days


def mknames(
    boys: int,
    girls: int,
    country: str = "fra",
    seed: int | None = None,
    no_cache: bool = True,
    firstname_duplicates: bool = False,
    lastname_duplicates: bool = False,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """
    Generate firstnames and lastnames picked randomly from the French INSEE
    database or USA's SSA database.
    The firstnames and lastnames are generated based on the number of
    occurrences in the database.
    """
    NameGenerator, LastNameGenerator = get_provider(country)
    storage = hishel.FileStorage(
        base_path=Path(user_cache_dir(CACHEAPPNAME, CACHEAPPAUTHOR)),
        ttl=0 if no_cache else CACHETTL,
    )
    controller = hishel.Controller(force_cache=(not no_cache))
    with hishel.CacheClient(controller=controller, storage=storage) as client:
        names = NameGenerator(seed=seed, client=client)
        last_names = LastNameGenerator(seed=seed, client=client)

    boysnames = list(
        zip(
            names.get_boys(boys, replace=firstname_duplicates),
            last_names.get_names(boys, replace=lastname_duplicates),
        )
    )
    girlsnames = list(
        zip(
            names.get_girls(girls, replace=firstname_duplicates),
            last_names.get_names(girls, replace=lastname_duplicates),
        )
    )

    return boysnames, girlsnames
