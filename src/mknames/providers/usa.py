# Locally disable rules incompatible with Pandas
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false

import io
import re
import zipfile
from typing import cast

import httpx
import numpy as np
import pandas as pd

from .types import PClient


class NameGenerator:
    URL = "https://www.ssa.gov/oact/babynames/names.zip"
    YEAR = 2000
    MINOCC = 1000

    def __init__(
        self, seed: int | None = None, client: PClient = httpx
    ) -> None:
        def extract_content(content: bytes) -> pd.DataFrame:
            columns = ["name", "gender", "count"]
            df = pd.DataFrame(columns=columns)
            _re_file = re.compile(r"yob(?P<year>\d{4}).txt")
            with zipfile.ZipFile(io.BytesIO(content), "r") as zf:
                for name in zf.namelist():
                    if m := _re_file.match(name):
                        year = int(m.group("year"))
                        if year >= self.YEAR:
                            with zf.open(name) as f:
                                ndf = pd.read_csv(f, names=columns)
                                df = pd.concat([df, ndf], ignore_index=True)
            return df

        usazip = client.get(self.URL)
        usazip.raise_for_status()
        statset = (
            extract_content(usazip.content)
            .dropna()
            .groupby(["gender", "name"])["count"]
            .sum()
            .loc[lambda x: x >= self.MINOCC]
            .sort_values(ascending=False)
        )
        self.boysset = statset["M"].reset_index()
        self.girlsset = statset["F"].reset_index()
        self.rng = np.random.default_rng(seed)

    def get_boys(self, size: int, replace: bool = False) -> list[str]:
        return self._get_choice(self.boysset, size, replace)

    def get_girls(self, size: int, replace: bool = False) -> list[str]:
        return self._get_choice(self.girlsset, size, replace)

    def _get_choice(
        self, dataset: pd.DataFrame, size: int, replace: bool = False
    ) -> list[str]:
        result = self.rng.choice(
            dataset["name"].str.title(),
            size=size,
            replace=replace,
            p=dataset["count"] / dataset["count"].sum(),
        )
        return cast(list[str], result.tolist())
