# Locally disable rules incompatible with Pandas
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false

import io
from typing import cast

import httpx
import numpy as np
import pandas as pd

from .types import PClient


class NameGenerator:
    URL = (
        "https://www.insee.fr/fr/statistiques/fichier/7633685/nat2022_csv.zip"
    )
    YEAR = 2000
    MINOCC = 1000

    def __init__(
        self, seed: int | None = None, client: PClient = httpx
    ) -> None:
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
        self, dataset: pd.DataFrame, size: int, replace: bool = False
    ) -> list[str]:
        result = self.rng.choice(
            dataset["preusuel"].str.title(),
            size=size,
            replace=replace,
            p=dataset["nombre"] / dataset["nombre"].sum(),
        )
        return cast(list[str], result.tolist())


class LastNameGenerator:
    URL = "https://www.data.gouv.fr/fr/datasets/r/9ae80de2-a41e-4282-b9f8-61e6850ef449"
    MINOCC = 50

    def __init__(
        self, seed: int | None = None, client: PClient = httpx
    ) -> None:
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
            .set_index("patronyme")["count"]
            .loc[lambda x: x  > self.MINOCC]
            .sort_values(ascending=False)
            .reset_index()
            .assign(patronyme=lambda df: df["patronyme"].str.title())
        )
        self.nameset = nameset
        self.rng = np.random.default_rng(seed)

    def get_names(self, size: int, replace: bool = False) -> list[str]:
        return self._get_choice(self.nameset, size, replace)

    def _get_choice(
        self, dataset: pd.DataFrame, size: int, replace: bool = False
    ) -> list[str]:
        result = self.rng.choice(
            dataset["patronyme"],
            size=size,
            replace=replace,
            p=dataset["count"] / dataset["count"].sum(),
        )
        return cast(list[str], result.tolist())
