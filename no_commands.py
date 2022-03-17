"""Pause counter example."""
import itertools
from dataclasses import dataclass

from opentrons import protocol_api

metadata = {
    "protocolName": "Pause Counter",
    "author": "Opentrons <protocols@opentrons.com>",
    "source": "Example",
    "apiLevel": "2.12",
}


@dataclass
class Counter:
    """Count things during a run."""

    pauses: int

    def increment_pauses(self) -> int:
        """Increment pauses."""
        self.pauses += 1
        return self.pauses


def run(ctx: protocol_api.ProtocolContext) -> None:
    """This method is run by the protocol engine."""
    print("nothing")
