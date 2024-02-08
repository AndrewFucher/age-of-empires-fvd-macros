# Fast Villager Defense (FVD) macros utils

## Running

1. Install Python v. 3.11+ (pip and python in PATH must be)
1. Install packages (libraries) via requirements: `pip install -r requirements.txt`
1. Install library from 3rdParty `pynput`. Go to `3rdParty\pynput` and run in terminal `pip install .`
1. Replace in `main.py` values with your own (on MacOS it may be not pixels but some virtual value, on Windows it is pixels) on line 37-38. Calculate values on your own (size of diamond from corner to opposite corner), with maximum zoom-OUT (smallest map can get). But it depends on your choice of playing e.g. if u play full zoom-in u can calculate distance that way.
1. Run the program with `python main.py`

## Usage

1. Zoom-in or out as u have calculated sizes of squares
1. Unselect villager (no focus on him)
1. Villager must be set on 1 e.g. when he is not active if u press 1 he will be active
1. `ctrl + alt + shift-left + d` - activate logic to build towers.
1. Press wanted tower (hot key) e.g. `d` for siege, `f` for usual towers, `t` for trebuchet etc.
1. Click with mouse 2 points from which to which build and enjoy the show

## Notes

1. Program is not ready for production. Use on your own accord
1. Do not scroll while executing commands. Program is not clever to move to correct point on it's own
1. If u have troubles with building, try on some skimirish or custom scenario map to get to know the technique better