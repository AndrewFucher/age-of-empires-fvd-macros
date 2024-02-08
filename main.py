from pynput import mouse, keyboard
import time
import asyncio
import threading
import enum
import pyautogui


pyautogui.PAUSE = 0

class ProgramState(enum.Enum):
    TERMINATE = enum.auto()
    WORK = enum.auto()


class BuildingState(enum.Enum):
    CHOOSE_TOWER = enum.auto()
    STOP_BUILDING = enum.auto()
    BUILD = enum.auto()
    PENDING = enum.auto()


mouse_presses = []
mouse_recording = False
program_state = ProgramState.WORK
building_state = BuildingState.PENDING
tower_key: str = None

keyboard_controller = keyboard.Controller()
mouse_controller = mouse.Controller()

allowed_keys = ("s", "d", "z", "h", "t", "f", "v", "g", "x", "c")

# =================================

# blocks width and height in pixels. TO EVALUATE BY USER
block_width_pixels = 72
block_height_pixels = 36

# =================================

# first - move to wanted position. others - move in loop
workflows = {
    "top-right": [
        (0, block_height_pixels),
        (block_width_pixels, -block_height_pixels),
        (-block_width_pixels, 0),
        (int(0.5 * block_width_pixels), int(1.5 * block_height_pixels)),
    ],
    "top-left": [
        (0, block_height_pixels),
        (-block_width_pixels, -block_height_pixels),
        (block_width_pixels, 0),
        (-int(0.5 * block_width_pixels), int(1.5 * block_height_pixels)),
    ],
    "bottom-right": [
        (0, -block_height_pixels),
        (block_width_pixels, block_height_pixels),
        (-block_width_pixels, 0),
        (int(0.5 * block_width_pixels), -int(1.5 * block_height_pixels)),
    ],
    "bottom-left": [
        (0, -block_height_pixels),
        (-block_width_pixels, block_height_pixels),
        (block_width_pixels, 0),
        (-int(0.5 * block_width_pixels), -int(1.5 * block_height_pixels)),
    ],
}


def get_workflow(point_from: tuple[int, int], point_to: tuple[int, int]) -> list:
    result = None
    if point_to[0] > point_from[0]:
        if point_to[1] > point_from[1]:
            result = workflows["top-right"]
        else:
            result = workflows["bottom-right"]
    else:
        if point_to[1] > point_from[1]:
            result = workflows["top-left"]
        else:
            result = workflows["bottom-left"]

    return result


def build_foundations(
    point_from: tuple[int, int], point_to: tuple[int, int], tower_key: str
):
    global stop_building, program_state, building_state

    mouse_controller.position = point_from

    time.sleep(0.2)
    # keyboard_controller.press("1")
    # time.sleep(0.1)
    # keyboard_controller.release("1")
    pyautogui.press("1")
    time.sleep(0.1)

    # keyboard_controller.press("w")
    # time.sleep(0.2)
    # keyboard_controller.release("w")
    pyautogui.press("w")
    time.sleep(0.1)

    # keyboard_controller.press(tower_key)
    # time.sleep(0.1)
    # keyboard_controller.release(tower_key)
    pyautogui.press(tower_key)
    time.sleep(0.1)
    
    workflow = get_workflow(point_from, point_to)
    loops_count = int(abs(point_to[0] - point_from[0]) / (block_width_pixels / 2))

    if loops_count == 0:
        return

    point_from = (point_from[0] + workflow[0][0], point_from[1] + workflow[0][1])
    pyautogui.moveTo(point_from)

    time.sleep(0.3)
    with pyautogui.hold("shift"):
        pyautogui.leftClick()
        time.sleep(0.3)
        for loops_num in range(loops_count):
            for workflow_step in range(1, len(workflow)):
                if program_state == ProgramState.TERMINATE:
                    return
                if building_state != BuildingState.BUILD:
                    building_state == BuildingState.PENDING
                    return
                point_from = (point_from[0] + workflow[workflow_step][0], point_from[1] + workflow[workflow_step][1])
                pyautogui.moveTo(point_from)
                pyautogui.leftClick(_pause = False)
                time.sleep(0.01)
    building_state = BuildingState.PENDING


def on_click(x: int, y: int, button: mouse.Button, pressed: bool):
    global mouse_presses, mouse_recording, program_state
    if building_state != BuildingState.BUILD:
        building_state == BuildingState.PENDING
        return
    if program_state == ProgramState.TERMINATE:
        return False
    if mouse_recording and not pressed:
        if len(mouse_presses) == 2:
            mouse_presses = []
        mouse_presses.append((x, y))
        if len(mouse_presses) == 2:
            mouse_recording = False
            threading.Thread(
                target=build_foundations,
                args=(mouse_presses[0], mouse_presses[1], tower_key),
            ).start()


def on_activate_start_building():
    global building_state
    if building_state == BuildingState.PENDING:
        building_state = BuildingState.CHOOSE_TOWER


def on_activate_stop_building():
    global building_state
    building_state = BuildingState.PENDING


def terminate_program():
    global program_state
    program_state = ProgramState.TERMINATE


def on_key_pressed(key):
    global building_state, mouse_recording, tower_key, allowed_keys
    if isinstance(key, keyboard.KeyCode):
        key = key.char
    if building_state == BuildingState.CHOOSE_TOWER and key in allowed_keys:
        building_state = BuildingState.BUILD
        mouse_recording = True
        tower_key = key


async def main():
    global program_stated
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
    await asyncio.sleep(1)
    keyboard_listener = keyboard.Listener(on_press=on_key_pressed)
    keyboard_listener.start()
    await asyncio.sleep(1)
    keyboard_hot_key_listener = keyboard.GlobalHotKeys(
        {
            "<ctrl>+<alt>+<shift_l>+d": on_activate_start_building,
            "<ctrl>+<alt>+<shift_l>+e": on_activate_stop_building,
            "<ctrl>+<alt>+<shift_l>+<space>": terminate_program,
        }
    )
    keyboard_hot_key_listener.start()
    await asyncio.sleep(1)
    while True:
        if program_state == ProgramState.TERMINATE:
            if mouse_listener.is_alive():
                mouse_listener.stop()
            if keyboard_hot_key_listener.is_alive():
                keyboard_hot_key_listener.stop()
            if keyboard_listener.is_alive():
                keyboard_listener.stop()
            return
        await asyncio.sleep(5000)


if __name__ == "__main__":
    asyncio.run(main())
