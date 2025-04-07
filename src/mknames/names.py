import io

import hishel
import httpx
import numpy as np
import pandas as pd
from appdirs import user_cache_dir

CACHEAPPNAME = "mknames"
CACHEAPPVENDOR = "TehoorMarjan"
CACHETTL = 259200  # 3 days


class NameGenerator:
    URL = (
        "https://www.insee.fr/fr/statistiques/fichier/7633685/nat2022_csv.zip"
    )
    YEAR = 2000
    MINOCC = 1000

    def __init__(self, seed: int | None = None, client=httpx) -> None:
        nameset = pd.read_csv(
            io.BytesIO(client.get(self.URL, follow_redirects=True).content),
            compression="zip",
            sep=";",
            dtype={
                "sexe": "category",
                "nombre": "Int32",
                "annais": "Int32",
            },
            na_values=["XXXX", "_PRENOMS_RARES"],
            keep_default_na=False,
        ).dropna()
        statset = (
            nameset[nameset["annais"] >= self.YEAR]
            .groupby(["sexe", "preusuel"], observed=True)["nombre"]
            .sum()
        )
        statset = statset[statset >= self.MINOCC]
        self.boysset = statset["1"].reset_index()
        self.girlsset = statset["2"].reset_index()
        self.rng = np.random.default_rng(seed)

    def get_boys(self, size: int, replace: bool = False) -> list[str]:
        return self._get_choice(self.boysset, size, replace)

    def get_girls(self, size: int, replace: bool = False) -> list[str]:
        return self._get_choice(self.girlsset, size, replace)

    def _get_choice(
        self, dataset, size: int, replace: bool = False
    ) -> list[str]:
        return self.rng.choice(
            dataset["preusuel"].str.title(),
            size=size,
            replace=replace,
            p=dataset["nombre"] / dataset["nombre"].sum(),
        )


class LastNameGenerator:
    URL = "https://www.data.gouv.fr/fr/datasets/r/9ae80de2-a41e-4282-b9f8-61e6850ef449"
    MINOCC = 50

    def __init__(self, seed: int | None = None, client=httpx) -> None:
        nameset = (
            pd.read_csv(
                io.BytesIO(
                    client.get(self.URL, follow_redirects=True).content
                ),
                sep=",",
                dtype={"count": "Int32"},
                keep_default_na=False,
            )
            .dropna()
            .query(f"count > {self.MINOCC}")
            .sort_values("count", ascending=False)
            .reset_index(drop=True)
        )
        self.nameset = nameset
        self.rng = np.random.default_rng(seed)

    def get_names(self, size: int, replace: bool = False) -> list[str]:
        return self._get_choice(self.nameset, size, replace)

    def _get_choice(
        self, dataset, size: int, replace: bool = False
    ) -> list[str]:
        return self.rng.choice(
            dataset["patronyme"].str.title(),
            size=size,
            replace=replace,
            p=dataset["count"] / dataset["count"].sum(),
        )


def mknames(
    boys: int,
    girls: int,
    seed: int | None = None,
    no_cache: bool = True,
    firstname_duplicates: bool = False,
    lastname_duplicates: bool = False,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """
    Generate firstnames and lastnames picked randomly from the French INSEE
    database.
    The firstnames and lastnames are generated based on the number of
    occurrences in the database.
    """
    storage = hishel.FileStorage(
        base_path=user_cache_dir(CACHEAPPNAME, CACHEAPPVENDOR),
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
