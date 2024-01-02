import keyboard
import mss
import cv2
import numpy as np
from time import time, sleep
import pyautogui

pyautogui.PAUSE = 0
#r for change capture area
#q forr quit
#p for recorogize 
#n for delete last recogonation
print("Press 's' to start playing.")
print("Once started press 'q' to quit.")
keyboard.wait('s')

sct = mss.mss()
screen_width, screen_height = pyautogui.size()
reference_images = []  # List to store multiple reference images
dimensions2 = sct.monitors[0]
while True:
    if keyboard.is_pressed('q'):
        break
    if keyboard.is_pressed('r'):
        mouse_x, mouse_y = pyautogui.position()

        # Get screen size

        # Calculate the area to capture based on mouse position (adjust as needed)
        capture_width = 400
        capture_height = 300
        left = max(0, mouse_x - capture_width // 2)
        top = max(0, mouse_y - capture_height // 2)
        right = min(screen_width, left + capture_width)
        bottom = min(screen_height, top + capture_height)

        # Set dimensions for screen capture
        dimensions2 = {
            'left': left,
            'top': top,
            'width': right - left,
            'height': bottom - top
        }
    if keyboard.is_pressed('n'):
        if reference_images:
            reference_images.pop()  # Remove the last saved reference image
            print("Last saved reference image removed!")

    if keyboard.is_pressed('p'):
        mouse_x, mouse_y = pyautogui.position()

        screen_width, screen_height = pyautogui.size()

        capture_width = 100  # Adjust the capture area size as needed
        capture_height = 100

        left = max(0, mouse_x - capture_width // 2)
        top = max(0, mouse_y - capture_height // 2)
        right = min(screen_width, left + capture_width)
        bottom = min(screen_height, top + capture_height)

        dimensions = {
            'left': left,
            'top': top,
            'width': right - left,
            'height': bottom - top
        }

        scr = np.array(sct.grab(dimensions))
        scr_remove = scr[:, :, :3]

        reference_images.append(scr_remove.copy())  # Store the captured obstacle image as a reference
        print("Reference obstacle image saved!")
        sleep(0.2)  # Add a small delay to prevent multiple presses

    #if not dimensions2:
    #    scr = np.array(sct.grab(sct.monitors[0]))  # Capture the entire screen (adjust monitor index as needed)
   
    scr = np.array(sct.grab(dimensions2))

    scr_remove = scr[:, :, :3]

    try:
        for reference_img in reference_images:
            result = cv2.matchTemplate(scr_remove, reference_img, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > .55:
                pyautogui.press('space')
                cv2.rectangle(scr, max_loc, (max_loc[0] + reference_img.shape[1], max_loc[1] + reference_img.shape[0]), (0, 255, 255), 2)

    except Exception as e:
        print(f"Error: {e}")

    cv2.imshow('Screen Shot', scr)
    cv2.waitKey(1)
    #sleep(.10)

    if keyboard.is_pressed('q'):
        break
