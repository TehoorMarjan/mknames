from . import fra, usa
from .types import PLastNameGenerator, PNameGenerator

PROVIDER_REGISTRY: dict[
    str, tuple[type[PNameGenerator], type[PLastNameGenerator]]
] = {
    "fra": (fra.NameGenerator, fra.LastNameGenerator),
    "usa": (usa.NameGenerator, fra.LastNameGenerator),  # Placeholder
}


def get_provider(
    country: str,
) -> tuple[type[PNameGenerator], type[PLastNameGenerator]]:
    """
    Get the name generators for the specified country.
    """

    return PROVIDER_REGISTRY[country.lower()]


def list_providers() -> list[str]:
    """
    List all available countries.
    """

    return list(PROVIDER_REGISTRY.keys())
