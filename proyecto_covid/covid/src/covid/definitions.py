from pathlib import Path

from dagster import definitions, load_from_defs_folder
from dagster import Definitions, load_assets_from_modules
from .defs import assets as covid_assets


@definitions
def defs():
    return load_from_defs_folder(project_root=Path(__file__).parent.parent.parent)

defs = Definitions(
    assets=load_assets_from_modules([covid_assets]),
)
