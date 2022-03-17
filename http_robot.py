"""."""
import inspect
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import requests
from requests import Response
from requests.sessions import Session
from rich import inspect as rich_inspect
from rich.console import Console
from typing_extensions import Literal

from wait import wait_until

RunActions = Literal["play", "pause", "stop"]
CommandStatus = Literal["queued", "succeeded"]


class HttpRobot:
    """."""

    def __init__(
        self,
        base: str = "http://host.docker.internal:31950",
        version: str = "*",
        debug: bool = True,
    ) -> None:
        """."""
        self.session: Session = requests.Session()
        self.session.headers = {"Opentrons-Version": version}
        self.base: str = base
        self.debug: bool = debug
        self.console: Console = Console()
        self.console.print("\n")
        self.console.print(rich_inspect(self))

    def debug_print(self, response: Response) -> None:
        """."""
        self.console.print(f"Response for {inspect.currentframe().f_back.f_code.co_name}")
        self.console.print(rich_inspect(response))
        json = None
        try:
            json = response.json()
        except Exception as e:
            self.console.print("JSON parse Exception =")
            self.console.print_exception(e)
        if json:
            self.console.print("JSON response is parseable:")
            self.console.print_json(response.content.decode(response.encoding))

    def set_lights(self, on: bool) -> Response:
        """."""
        endpoint = f"{self.base}/robot/lights"
        response: Response = self.session.post(endpoint, json={"on": on})
        if self.debug:
            self.debug_print(response)
        return response

    def spooky_lights(self) -> None:
        """."""
        for _ in range(0, 10):
            self.set_lights(True)
            time.sleep(random.random())
            self.set_lights(False)
            time.sleep(random.random())

    def get_health(self) -> Response:
        """."""
        endpoint = f"{self.base}/health"
        response: Response = self.session.get(endpoint)
        if self.debug:
            self.debug_print(response)
        return response

    def get_runs(self) -> Response:
        """."""
        endpoint = f"{self.base}/runs"
        response: Response = self.session.get(endpoint)
        if self.debug:
            self.debug_print(response)
        return response

    def post_runs(self, run: Dict = {}) -> Response:
        """."""
        endpoint = f"{self.base}/runs"
        response: Response = self.session.post(endpoint, json={"data": run})
        if self.debug:
            self.debug_print(response)
        return response

    def get_runs_commands(self, run_id: str) -> Response:
        """."""
        endpoint = f"{self.base}/runs/{run_id}/commands"
        response: Response = self.session.get(endpoint)
        if self.debug:
            self.debug_print(response)
        return response

    def post_runs_commands(
        self, run_id: str, command: dict, wait_until_complete: bool = False, timeout_ms: int = 10
    ) -> Response:
        """."""
        endpoint = f"{self.base}/runs/{run_id}/commands"
        response: Response = self.session.post(
            endpoint,
            json=command,
            params={"waitUntilComplete": wait_until_complete, "timeout": timeout_ms},
        )
        if self.debug:
            self.debug_print(response)
        return response

    def get_modules(self) -> Response:
        """."""
        endpoint = f"{self.base}/modules"
        response: Response = self.session.get(endpoint)
        if self.debug:
            self.debug_print(response)
        return response

    def post_runs_actions(self, run_id: str, action_type: RunActions) -> Response:
        """."""
        endpoint = f"{self.base}/runs/{run_id}/actions"
        response: Response = self.session.post(endpoint, json={"data": {"actionType": action_type}})
        if self.debug:
            self.debug_print(response)
        return response

    def post_protocol(self, files: List[Path]) -> Response:
        """."""
        file_payload = []
        for file in files:
            file_payload.append(("files", open(file, "rb")))
        endpoint = f"{self.base}/protocols"
        response: Response = self.session.post(endpoint, files=file_payload)
        if self.debug:
            self.debug_print(response)
        return response

    def get_link(self, link: str) -> Response:
        """."""
        endpoint = f"{self.base}{link}"
        response: Response = self.session.get(endpoint)
        if self.debug:
            self.debug_print(response)
        return response

    def wait_until_command_status(
        self,
        status: CommandStatus,
        timout_seconds: 5,
        poll_wait_period: float,
        run_id: str,
        command_id: str,
    ):
        wait_until(
            self.command_status_equals_target,
            timout_seconds,
            poll_wait_period,
            run_id=run_id,
            command_id=command_id,
            command_status_target=status,
        )

    def command_status_equals_target(
        self, run_id: str, command_id: str, command_status_target: CommandStatus
    ) -> str:
        endpoint = f"{self.base}/runs/{run_id}/commands/{command_id}"
        response: Response = self.session.get(endpoint)
        if self.debug:
            self.debug_print(response)
        return response.json()["data"]["status"] == command_status_target
