import numpy as np
import cv2
import kociemba


class CaptureCube:
    #to determine the position of each colour
    _positions = {
        (0, 0): (220, 140),
        (0, 1): (320, 140),
        (0, 2): (420, 140),
        (1, 0): (220, 240),
        (1, 1): (320, 240),
        (1, 2): (420, 240),
        (2, 0): (220, 340),
        (2, 1): (320, 340),
        (2, 2): (420, 340)
    }

     # to change the face that you are working on the screen
    _trans = {
        'F': 'L',
        'L': 'B',
        'B': 'R',
        'R': 'U',
        'U': 'D',
        'D': 'N'
    }
    #define colour
    _colors = ['w', 'y', 'r', 'g', 'o', 'b']

    _cor_map = {
        'w': 'y',
        'y': 'r',
        'r': 'g',
        'g': 'o',
        'o': 'b',
        'b': 'w',
        'n': 'w'
    }

    _filename = 'frame.png'

    def __init__(self):

        self._state = {}
        self._set = {}

        for pos in self._positions:
            self._state[pos] = 'n'
            self._set[pos] = False

        self._frame = None

        self._cube = {
            'U': None,
            'D': None,
            'F': None,
            'L': None,
            'B': None,
            'R': None
        }

        self._cur_face = 'F'
        self._set_flag = False

    def callback(self, event, x, y, flags, param):
        # Set button on screen to take pics
        if event == cv2.EVENT_RBUTTONDOWN:
            print('saved image to ' + self._filename)
            cv2.imwrite(self._filename, self._frame)

            return
        # button to change the face that you are working on
        elif event == cv2.EVENT_LBUTTONDOWN:
            if 0 < x < 70 and 0 < y < 50:
                self._cube[self._cur_face] = self._state.copy()
                self._cur_face = self._trans[self._cur_face]
                self._set_flag = False

                for pos in self._positions:
                    self._set[pos] = False

                if self._cur_face == 'N':
                    x = self._cube
                    y = translate_solve(x)
                    restults = tranlate_3d(y)
                    print(restults)
                    s = '-'.join(restults)
                    with open('solution_steps.txt', 'w') as file:
                        file.write(s)
                    with open('solution_steps.txt', 'a') as file:
                        file.write("#")
                        file.write(y)

                return

            if 540 < x < 640 and 0 < y < 50:
                if self._set_flag:
                    for pos in self._positions:
                        self._set[pos] = False
                    self._set_flag = False
                else:
                    for pos in self._positions:
                        self._set[pos] = True
                    self._set_flag = True

                return

            if 90 < y < 190:
                i = 0
            elif 190 < y < 290:
                i = 1
            elif 290 < y < 390:
                i = 2
            else:
                return

            if 170 < x < 270:
                j = 0
            elif 270 < x < 370:
                j = 1
            elif 370 < x < 470:
                j = 2
            else:
                return

            self._state[(i, j)] = self._cor_map[self._state[(i, j)]]
            self._set[(i, j)] = True

    def sense_color(self, ind_1, ind_2):

        b_samples = []
        g_samples = []
        r_samples = []

        for i in [-1, 1]:
            for j in [-1, 1]:
                for dev in np.linspace(0, 30, 10):
                    b, g, r = self._frame[ind_1 + int(dev * i), ind_2 + int(dev * j)]
                    b_samples.append(b)
                    g_samples.append(g)
                    r_samples.append(r)

        b, g, r = self._frame[ind_1, ind_2]
        b_samples.append(b)
        g_samples.append(g)
        r_samples.append(r)

        del b_samples[b_samples.index(max(b_samples))]
        del b_samples[b_samples.index(min(b_samples))]

        del g_samples[g_samples.index(max(g_samples))]
        del g_samples[g_samples.index(min(g_samples))]

        del r_samples[r_samples.index(max(r_samples))]
        del r_samples[r_samples.index(min(r_samples))]

        b = np.sum(np.array(b_samples)) / len(b_samples)
        g = np.sum(np.array(g_samples)) / len(g_samples)
        r = np.sum(np.array(r_samples)) / len(r_samples)

        if r > 70 + g and r > 100 + b and g < 60 and b < 60:
            return 'r'
        elif r > 160 + b and r > 80 + g:
            return 'o'
        elif r > 90 + b and g < 30 + r and r < 30 + g:
            return 'y'
        elif b == max(r, g, b) and b > 200 and b > r + 70:
            return 'b'
        elif r > 160 and g > 160 and b > 160:
            return 'w'
        elif g == max(r, g, b) and r < 70 and b < 70:
            return 'g'
        else:
            return 'n'

    def capture_cube(self):
        #  to turn on the camera and end it
        cap = cv2.VideoCapture(0)
        cv2.namedWindow('CaptureCube')
        font = cv2.FONT_HERSHEY_SIMPLEX

        while (True):
            # Capture frame-by-frame
            ret, self._frame = cap.read()

            cv2.setMouseCallback('CaptureCube', self.callback)

            cv2.rectangle(self._frame, (170, 90), (470, 390), (0, 0, 0), 2)

            cv2.line(self._frame, (270, 90), (270, 390), (0, 0, 0), 2)
            cv2.line(self._frame, (370, 90), (370, 390), (0, 0, 0), 2)

            cv2.line(self._frame, (170, 190), (470, 190), (0, 0, 0), 2)
            cv2.line(self._frame, (170, 290), (470, 290), (0, 0, 0), 2)

            cv2.rectangle(self._frame, (0, 0), (100, 50), (255, 255, 255), -1)
            cv2.putText(self._frame, self._cur_face, (40, 35), font, 1, (0, 0, 0), 3)

            cv2.rectangle(self._frame, (540, 0), (640, 50), (255, 255, 255), -1)
            cv2.putText(self._frame, 'SET', (560, 35), font, 1, (0, 0, 0), 3)

            for pos in self._positions:
                # b, g, r = self._frame[self._positions[pos][1], self._positions[pos][0]]
                color = self.sense_color(self._positions[pos][1], self._positions[pos][0])
                if not self._set[pos]:
                    self._state[pos] = color
                cv2.putText(self._frame, self._state[pos], (self._positions[pos][0] - 10, self._positions[pos][1] + 10),
                            font, 1, (0, 0, 0), 1)

            # Display the resulting frame
            cv2.imshow('CaptureCube', self._frame)

            if cv2.waitKey(1) == 27 or self._cur_face == 'N':
                break

        cap.release()
        cv2.destroyAllWindows()


# U R F D L B

# U D F L B R
def translate_solve(result_obj):
    resu = list(result_obj.values())
    result = [list(x.values()) for x in list(resu)]
    string = ""
    for i in result:
        for x in i:
            x = str(x)
            if x == "r":
                x = "F"
            elif x == "b":
                x = "U"
            elif x == "y":
                x = "R"
            elif x == "w":
                x = "L"
            elif x == "g":
                x = "D"
            elif x == "o":
                x = "B"
            string += x
    U = string[:9]
    D = string[9:18]
    F = string[18:27]
    L = string[27:36]
    B = string[36:45]
    R = string[45:55]

    print(U + R + F + D + L + B)
    print(tranlate_3d(kociemba.solve(U + R + F + D + L + B)))
    return kociemba.solve(U + R + F + D + L + B)


def tranlate_3d(kociemba_str):
    list1 = kociemba_str.split(" ")
    cur_list = []
    final_list = []
    for x in list1:
        a = x[0]

        if a == "U":
            cur_list.append("TOP")
        elif a == "D":
            cur_list.append("BOTTOM")
        elif a == "L":
            cur_list.append("LEFT")
        elif a == "R":
            cur_list.append("RIGHT")
        elif a == "F":
            cur_list.append("FACE")
        elif a == "B":
            cur_list.append("BACK")

        if len(x) == 2:
            b = x[1]
            if b == "'":
                cur_list[0] += "S"
            else:
                cur_list.append(cur_list[0])
        for y in cur_list:
            final_list.append(y)
        cur_list = []
    return final_list


def kosimba_mirror(result):
    list1 = result.split(" ")
    cur_list = []
    final_list = []
    for x in list1:
        a = x[0]

        if a == "U":
            cur_list.append("U'")
        elif a == "D":
            cur_list.append("D'")
        elif a == "L":
            cur_list.append("L'")
        elif a == "R":
            cur_list.append("R'")
        elif a == "F":
            cur_list.append("F'")
        elif a == "B":
            cur_list.append("B'")

        if len(x) == 2:
            b = x[1]
            if b == "'":
                cur_list[0] = cur_list[0][0]
            else:
                if len(cur_list[0]) < 2 :
                    cur_list[0] += "2"
                else:
                    cur_list[0] = cur_list[0][0] + "2"
        for y in cur_list:
            final_list.append(y)
        cur_list = []
    final = final_list[::-1]
    final = " ".join(final)
    return final


if __name__ == '__main__':
    cube = CaptureCube()
    cube.capture_cube()
