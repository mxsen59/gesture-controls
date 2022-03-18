import cv2
import time
import math
import numpy as np
import alsaaudio as alsa
import hand_tracking as ht

_WIDTH = 480
_HEIGHT = 640

capture = cv2.VideoCapture(-1)

capture.set(3, _WIDTH)
capture.set(4, _HEIGHT)

detector = ht.HandDetector(detection_con=0.7)

mixer = alsa.Mixer()

min_vol = 0
max_vol = 100


class ASCIIColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = "\033[97m"


def volume_control():

    prev_time = 0

    while True:
        success, img = capture.read()

        img = detector.find_hands(img)

        lm_list = detector.find_position(img)

        if len(lm_list) != 0:
            # print(lm_list[4], lm_list[8])

            x1, y1 = lm_list[4][1], lm_list[4][2]
            x2, y2 = lm_list[8][1], lm_list[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            line_length = math.hypot(x2 - x1, y2 - y1)

            # print(line_length)

            if line_length < 50:
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

            volume = np.interp(line_length, [35, 200], [min_vol, max_vol])

            mixer.setvolume(int(volume))

            print(ASCIIColors.GREEN + f"VOLUME: {str(int(volume))}")

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        '''cv2.putText(img, f"FPS: {int(fps)}", (40, 50),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        
        cv2.imshow("DEBUG", img)'''

        if cv2.waitKey(25) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    print('''
██╗░░░██╗░█████╗░██╗░░░░░██╗░░░██╗███╗░░░███╗███████╗░░░░░░░█████╗░░█████╗░███╗░░██╗████████╗██████╗░░█████╗░██╗░░░░░░██████╗
██║░░░██║██╔══██╗██║░░░░░██║░░░██║████╗░████║██╔════╝░░░░░░██╔══██╗██╔══██╗████╗░██║╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░██╔════╝
╚██╗░██╔╝██║░░██║██║░░░░░██║░░░██║██╔████╔██║█████╗░░█████╗██║░░╚═╝██║░░██║██╔██╗██║░░░██║░░░██████╔╝██║░░██║██║░░░░░╚█████╗░
░╚████╔╝░██║░░██║██║░░░░░██║░░░██║██║╚██╔╝██║██╔══╝░░╚════╝██║░░██╗██║░░██║██║╚████║░░░██║░░░██╔══██╗██║░░██║██║░░░░░░╚═══██╗
░░╚██╔╝░░╚█████╔╝███████╗╚██████╔╝██║░╚═╝░██║███████╗░░░░░░╚█████╔╝╚█████╔╝██║░╚███║░░░██║░░░██║░░██║╚█████╔╝███████╗██████╔╝
░░░╚═╝░░░░╚════╝░╚══════╝░╚═════╝░╚═╝░░░░░╚═╝╚══════╝░░░░░░░╚════╝░░╚════╝░╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚══════╝╚═════╝░
          \n''')
    volume_control()
