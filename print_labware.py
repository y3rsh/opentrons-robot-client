"""Pause counter example."""
import os
from pathlib import Path

from opentrons.protocols.labware import get_all_labware_definitions

labware_dir = Path(
    ".venv/lib/python3.7/site-packages/opentrons_shared_data/data/labware/definitions/2"
)
list_of_labware = [x[0] for x in os.walk(labware_dir)]
print(list_of_labware)


print(get_all_labware_definitions())
