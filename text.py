import subprocess, sys, time, os,json

# --- 1. SETUP & DEPENDENCIES ---
# Added 'opencv-python' (Required for confidence parameter in locateCenterOnScreen)
pkgs = ['pywinauto', 'pywin32', 'comtypes', 'pyautogui', 'Pillow', 'opencv-python','pydirectinput']
try:
    print("Checking dependencies...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + pkgs)
    import pyautogui,pydirectinput
except Exception as e:
    sys.exit(f"Setup failed: {e}")

SCREEN_DIR = "screenshots"
os.makedirs(SCREEN_DIR, exist_ok=True)

# --- 2. HELPER FUNCTIONS ---
def run_action(action, val, wait=0, shot=None, **kwargs):
    """Handles key presses, writing text, and screenshots."""
    if action == 'press': pyautogui.press(val, **kwargs)
    elif action == 'write': 
        if val=="@":  # Special case for '@' key
            pydirectinput.keyDown('shift')
            pydirectinput.press('2')
            pydirectinput.keyUp('shift')
        elif val=="enter":
            pydirectinput.press('enter')
        else:   
            pyautogui.write(val)
    elif action == 'hotkey': pyautogui.hotkey(*val)
    
    if wait > 0: time.sleep(wait)
    
    if shot:
        path = os.path.join(SCREEN_DIR, shot)
        pyautogui.screenshot(path)
        print(f"Screenshot: {path}")

def find_and_click(image, wait=0, clicks=1):
    """Locates an image and clicks it. Returns True if found."""
    for confi in [0.8,0.5]:
        try:
            loc = pyautogui.locateCenterOnScreen(image, confidence=confi)
            if loc:
                print(f"Clicked {image} at {loc}")
                # interval=1 ensures 1 second pause between double clicks if clicks=2
                pyautogui.click(loc, clicks=clicks, interval=1) 
                time.sleep(wait)
                return True
        except Exception as e:
            print(f"Exception in finding image {image}: {e} ")
    return False

def launch_app(name):
    """Launches an exe and waits."""
    path = os.path.abspath(name)
    if os.path.exists(path):
        subprocess.Popen(path, shell=True)
        time.sleep(10)
    else:
        print(f"Error: not found.")

# --- 3. AUTOMATION SEQUENCE ---

def install_3(payload):
    try:
        launch_app("install-3.exe")
        run_action(None, None, wait=0, shot="1.png")
        first_steps = [
            ('press', 'tab', 1, None),
            ('press', 'up', 1, None),
            ('press', 'enter', 1, None),
            ('press', 'enter', 1, None),
            ('press', 'enter', 10, "1a.png"),
            ('press', 'tab', 1, None),
            ('press', 'space', 1, None),
            ('press', 'enter', 10, None),
            ('press', 'right', 1, "1b.png"),
            ('press', 'right', 1, "1c.png"),
            ('press', 'tab', 1, "1d.png"),
            ('press', 'space', 1, "1e.png"),
            ('press', 'tab', 1, "1f.png"),
            ('write', payload, 1, None),
            ('press', 'tab', 1, "1g.png")
        ]

        # Run the sequence
        for step in first_steps: run_action(*step)
    except Exception as e:
        print(f"Error in 3: {e}")

def install_1(a,b):
    try:
        a1=a.split("@")
        launch_app("install-1.exe")

        third_steps = [
            ('press', 'enter', 10, None, {'presses': 3, 'interval': 0.5}),
            ('press', 'enter', 1, None, {}),
            ('press', 'tab', 1, None, {}),
            ('press', 'enter', 1, None, {}),
            ('press', 'tab', 0, None, {'presses': 3, 'interval': 0.5}),
            ('write', a1[0], 0, None, {}),
            ('write', "@", 0, None, {}),  
            ('write', a1[1], 1, None, {}),
            ('press', 'tab', 0, None, {}),
            ('write', b, 1, None, {}),
            ('press', 'tab', 1, None, {}),
            ('press', 'enter', 10, "3.png", {}),
        ]

        for action, val, wait, shot, kwargs in third_steps:
            run_action(action, val, wait, shot, **kwargs)
            
        pyautogui.click(501, 419)
        run_action(None, None, wait=0, shot="3b.png")
        pyautogui.click(791, 154)
        run_action(None, None, wait=0, shot="3c.png")
    except Exception as e:
        print(f"Error in 1: {e}")

def install_2(payload):
    try:
        launch_app("install-2.exe")
        second_steps = [
            ('press', 'tab', 1, None),
            ('write', payload, 0, "2a.png")
        ]

        for step in second_steps: run_action(*step)

        # Image Check for Second App
        if find_and_click("install-21.png", wait=10):
            pass 
        run_action(None, None, wait=0, shot="2b.png")
    except Exception as e:
        print(f"Error in 2: {e}")

if __name__ == "__main__":
    payload = json.loads(sys.argv[1])
    install_3(payload['install-3'])
    install_1(payload['install-1a'], payload['install-1b'])
    install_2(payload['install-2'])
    time.sleep(21300)