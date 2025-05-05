from typing import Protocol

import httpx


class PClient(Protocol):
    def get(
        self, url: str, *, headers: None|dict[str, str] = None, follow_redirects: bool = False
    ) -> httpx.Response: ...


class PNameGenerator(Protocol):
    def __init__(
        self, seed: int | None = None, client: PClient = httpx
    ) -> None: ...

    def get_boys(self, size: int, replace: bool = False) -> list[str]: ...

    def get_girls(self, size: int, replace: bool = False) -> list[str]: ...


class PLastNameGenerator(Protocol):
    URL = "https://www.data.gouv.fr/fr/datasets/r/9ae80de2-a41e-4282-b9f8-61e6850ef449"
    MINOCC = 50

    def __init__(
        self, seed: int | None = None, client: PClient = httpx
    ) -> None: ...

    def get_names(self, size: int, replace: bool = False) -> list[str]: ...
