import time
from pathlib import Path
from turtle import clear

import run_comands
from http_robot import HttpRobot, RunActions

my_robot = "http://192.168.50.89:31950"


def test_run_commands():
    robot = HttpRobot(base=my_robot)
    response = robot.post_runs()
    run_id = response.json()["data"]["id"]
    command = robot.post_runs_commands(run_id, run_comands.set_rail_lights(True))
    command_id = command.json()["data"]["id"]
    robot.wait_until_command_status("succeeded", 5, 0.5, run_id, command_id)
    # robot.post_runs_commands(run_id, run_comands.set_rail_lights(False))
    modules = robot.get_modules().json()["modules"]
    # magdeck = next(item for item in modules if item["name"] == "magdeck")
    # response = robot.post_runs_commands(
    #    run_id, run_comands.load_module(magdeck["moduleModel"], "3"))
    # mag_deck_id = response.json()["data"]["id"]
    # robot.post_runs_commands(run_id, run_comands.magdeck_engage(mag_deck_id, 1))
    robot.post_runs_commands(run_id, run_comands.set_rail_lights(False))
    robot.get_runs_commands(run_id)
    robot.get_runs()
    robot.post_runs_actions(run_id, "play")


def test_get_run():
    robot = HttpRobot()
    robot.get_runs()


def test_post_protocol():
    robot = HttpRobot(my_robot)
    protocol = robot.post_protocol([Path("logo.py")])
    protocol_id = protocol.json()["data"]["id"]
    robot.post_runs({"data": {"protocolId": protocol_id}})
    runs = robot.get_runs().json()
    current_link = runs["links"]["current"]["href"]
    robot.get_link(current_link)


def test_any():
    robot = HttpRobot(my_robot)
    robot.get_link("/runs/66bee1b4-8f2a-4c77-a6bc-40504a3c0cee/commands")


def test_home():
    robot = HttpRobot(base=my_robot)
    response = robot.post_runs()
    run_id = response.json()["data"]["id"]
    command = robot.post_runs_commands(run_id, run_comands.home())
    command_id = command.json()["data"]["id"]
    robot.wait_until_command_status("succeeded", 20, 3, run_id, command_id)


def test_home_wait():
    robot = HttpRobot(base=my_robot)
    response = robot.post_runs()
    run_id = response.json()["data"]["id"]
    robot.post_runs_commands(
        run_id, run_comands.home(), True, 20000
    )  # takes  ~18 seconds if already at home


def test_home_wait_timeout():
    robot = HttpRobot(base=my_robot)
    response = robot.post_runs()
    run_id = response.json()["data"]["id"]
    robot.post_runs_commands(
        run_id, run_comands.home(), True, 1000
    )  # takes  ~18 seconds if already at home
