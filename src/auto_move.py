#Deals with automating movement

import time
import pyautogui as pg
import pydirectinput as pd
import pyautogui as pg


def move_mouse(target_coordinates):
    x=target_coordinates[0]
    y=target_coordinates[1]

    # Move to absolute coords and click multiple times with small delays
    pd.moveTo(x, y, duration=0.25)
    time.sleep(0.05)
    pd.click(x=x, y=y)
    time.sleep(0.08)
    pd.click(x=x, y=y)
    time.sleep(0.08)
    pd.click(x=x, y=y)

def click_run_button(target_coordinates):
    x = int(target_coordinates[0])
    y = int(target_coordinates[1])

    # Clamp to screen bounds to avoid invalid coordinates
    screen_w, screen_h = pg.size()
    x = max(0, min(x, screen_w - 1))
    y = max(0, min(y, screen_h - 1))

    # Focus the Roblox window by clicking near screen center
    center_x, center_y = screen_w // 2, screen_h // 2
    pd.moveTo(center_x, center_y, duration=0.15)
    time.sleep(0.05)
    pd.click(x=center_x, y=center_y)
    time.sleep(0.1)

    # Move to base position and perform multiple targeted clicks with slight jitter
    pd.moveTo(x, y, duration=0.2)
    time.sleep(0.05)
    # Try down/up with small holds; some UIs need this
    for dx, dy in [(0,0),(6,0),(-6,0),(0,6),(0,-6),(8,3),(-8,3)]:
        pd.moveTo(x+dx, y+dy, duration=0.05)
        pd.mouseDown()
        time.sleep(0.06)
        pd.mouseUp()
        time.sleep(0.06)

def idle_game():
    while True:
        x = 100
        y = 100

        pd.move(x,y, duration=2)
        pd.click(x,y, duration=2)
        pd.click()
        time.sleep(8)
        pd.move(x+200,y, duration=2)
        pd.click(x+200,y, duration=2)
        pd.click()
        time.sleep(8)

def press_keys(key_press, hold_time):
    start = time.time()

    while time.time() - start < hold_time:
        pd.press(key_press)

def get_screen_size():
    return pg.size()

def idle_for(duration_seconds):
    end_time = time.time() + duration_seconds
    while time.time() < end_time:
        x = 100
        y = 100
        pd.move(x, y, duration=2)
        pd.click(x, y, duration=2)
        pd.click()
        time.sleep(8)
        pd.move(x + 200, y, duration=2)
        pd.click(x + 200, y, duration=2)
        pd.click()
        time.sleep(8)