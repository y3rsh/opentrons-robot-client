"""Commands as dictionaries."""

from typing import Any, Dict


def load_module(model: str, location: str) -> Dict[str, Any]:
    return {
        "data": {
            "commandType": "loadModule",
            "params": {"model": model, "location": {"slotName": location}},
        }
    }


def set_rail_lights(on: bool) -> Dict[str, Any]:
    return {"data": {"commandType": "setRailLights", "params": {"on": on}}}


def magdeck_engage(id: str, engage_height: int) -> Dict[str, Any]:
    return {
        "data": {
            "commandType": "magneticModule/engageMagnet",
            "params": {"moduleId": id, "engageHeight": engage_height},
        }
    }


def home() -> Dict[str, Any]:
    return {"data": {"commandType": "home", "params": {}}}
