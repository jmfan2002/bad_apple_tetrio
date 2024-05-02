import cv2
import pyautogui
import pyperclip
from pynput import keyboard
import time

X_BLOCKS = 36 # + 4 = 40, height
Y_BLOCKS = 48 # + 4 = 52, width
BLOCK_X_SIZE = 360 // X_BLOCKS
BLOCK_Y_SIZE = 480 // Y_BLOCKS

WAIT = 0.1

def generate_map_strs():
  vidcap = cv2.VideoCapture('bad_apple.mp4')
  success,img = vidcap.read()
  count = 0
  maps = []
  while success:
    # progress indicator
    if count % 1000 == 0:
      print(f"count: {count}")
    # sets FPS, where 30 / x is the FPS
    if count % 2 == 0:
      map_str = "________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________"
      # process in blocks
      for i in range(0, len(img), BLOCK_X_SIZE):
        map_str += "__"
        for j in range(0, len(img[i]), BLOCK_Y_SIZE):
          block = [1 if any(img[i+x][j+y]) else 0 for x in range(BLOCK_X_SIZE) for y in range(BLOCK_Y_SIZE)]
          map_str += "_" if sum(block) >= len(block) // 2 else "#"
        map_str += "__"
      map_str += "________________________________________________________________________________________________________??"
      maps.append(map_str)
    success,img = vidcap.read()
    count += 1
  cv2.destroyAllWindows()
  with open("map_strs.txt", "w+") as f:
    s = "\n".join(maps)
    f.write(s)

def get_sc(map_str, cnt):
  # click solo
  pyautogui.click(1519, 510)
  time.sleep(WAIT)
  # click custom
  pyautogui.click(1519, 897)
  time.sleep(WAIT * 2)
  # click meta
  pyautogui.click(2736, 590)
  time.sleep(WAIT / 10)
  # click map string box
  pyautogui.click(1791, 755)
  time.sleep(WAIT)
  # delete current string
  pyautogui.hotkey("ctrl", "a")
  pyautogui.press("backspace")
  # paste string
  pyperclip.copy(map_str)
  pyautogui.hotkey("ctrl", "v")
  # click start
  pyautogui.click(3153, 469)
  time.sleep(WAIT * 2)
  # take screenshot
  pyautogui.screenshot(f"screenshots/frame{cnt:04}.png", (1235, 664, 1426, 887))
  # reset
  with pyautogui.hold("esc"):
      time.sleep(1)
  time.sleep(WAIT)
  
def run(key):
  try:
    if key.char == "a":
      with open("map_strs.txt", "r") as f:
        for i, s in enumerate(f):
          get_sc(s, i)
  except AttributeError:
    if key == keyboard.Key.enter:
      exit()

if __name__ == '__main__':
  # generate_map_strs()
  
  listener = keyboard.Listener(on_release=run)
  listener.start()
  listener.join()

  # ffmpeg -framerate 20 -i 'frame%04d.png' out.mp4