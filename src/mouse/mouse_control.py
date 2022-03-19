import cv2
import time
import autopy
import numpy as np
import hand_tracking as ht
from pynput.mouse import Controller as Controller

capture = cv2.VideoCapture(-1)

WIDTH = 480
HEIGHT = 640

capture.set(3, WIDTH)
capture.set(4, HEIGHT)

frame_reduction = 50
smoothening = 10

detector = ht.HandDetector(max_hands=1)

screen_width, screen_height = autopy.screen.size()

mouse = Controller()


class ASCIIColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = "\033[97m"


def mouse_control():

    prev_time = 0

    ploc_x, ploc_y = 0, 0
    cloc_x, cloc_y = 0, 0

    while True:
        success, img = capture.read()

        img = detector.find_hands(img)

        lm_list, bbox = detector.find_position(img, draw=False)

        cv2.rectangle(img, (frame_reduction, frame_reduction), (WIDTH -
                      frame_reduction, HEIGHT - frame_reduction), (255, 0, 255), 2)

        if len(lm_list) != 0:
            x1, y1 = lm_list[8][1:]
            x2, y2 = lm_list[12][1:]

            fingers = detector.fingers_up()

            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frame_reduction, WIDTH -
                               frame_reduction), (0, screen_width))
                y3 = np.interp(y1, (frame_reduction, HEIGHT -
                               frame_reduction), (0, screen_height))

                cloc_x = ploc_x + (x3 - ploc_x) / smoothening
                cloc_y = ploc_y + (y3 - ploc_y) / smoothening

                autopy.mouse.move(screen_width - cloc_x, cloc_y)

                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

                ploc_x, ploc_y = cloc_x, cloc_y

            if fingers[1] == 1 and fingers[2] == 1:
                line_length, img, line_info = detector.find_distance(
                    8, 12, img)

                print(ASCIIColors.GREEN +
                      f"LINE_LENGTH: {str(int(line_length))}")

                if line_length < 50:
                    cv2.circle(img, (line_info[4], line_info[5]),
                               15, (0, 255, 0), cv2.FILLED)

                    autopy.mouse.click()

            if fingers[0] == 1 and fingers[1] == 1:
                mouse.scroll(0, -2)

            if fingers[1] == 1 and fingers[4] == 1:
                mouse.scroll(0, 2)

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        '''cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (255, 0, 0), 3)

        cv2.imshow("MOUSE_DEBUG", img)'''

        if cv2.waitKey(25) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    print('''
███╗░░░███╗░█████╗░██╗░░░██╗░██████╗███████╗░░░░░░░█████╗░░█████╗░███╗░░██╗████████╗██████╗░░█████╗░██╗░░░░░░██████╗
████╗░████║██╔══██╗██║░░░██║██╔════╝██╔════╝░░░░░░██╔══██╗██╔══██╗████╗░██║╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░██╔════╝
██╔████╔██║██║░░██║██║░░░██║╚█████╗░█████╗░░█████╗██║░░╚═╝██║░░██║██╔██╗██║░░░██║░░░██████╔╝██║░░██║██║░░░░░╚█████╗░
██║╚██╔╝██║██║░░██║██║░░░██║░╚═══██╗██╔══╝░░╚════╝██║░░██╗██║░░██║██║╚████║░░░██║░░░██╔══██╗██║░░██║██║░░░░░░╚═══██╗
██║░╚═╝░██║╚█████╔╝╚██████╔╝██████╔╝███████╗░░░░░░╚█████╔╝╚█████╔╝██║░╚███║░░░██║░░░██║░░██║╚█████╔╝███████╗██████╔╝
╚═╝░░░░░╚═╝░╚════╝░░╚═════╝░╚═════╝░╚══════╝░░░░░░░╚════╝░░╚════╝░╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚══════╝╚═════╝░
          \n''')
    mouse_control()
