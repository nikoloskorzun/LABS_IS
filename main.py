import math

import cv2
import imutils
from PIL import Image, ImageDraw
import os
from random import randint
from math import pi, sqrt


class App:
    __info_for_lab3_str = "1042: Korzun Nikolay Vadimovich; counts = {}"
    __min_count_rect = 2
    __max_count_rect = 10
    __min_count_ellipse = 2
    __max_count_ellipse = 10
    __min_color_param = 10

    __input_image_filename = "img.png"
    __output_image_filename = "o.png"

    __counters_color = (0, 0, 0)
    __text_color = (255, 0, 255)
    def __get_random_color(self):
        return (randint(self.__min_color_param, 255), randint(self.__min_color_param, 255), randint(self.__min_color_param, 255))

    def __get_random_xy_in_area(self, maxw, maxh):

        def get_min_in_n_repeat(min_, max_, n):
            a=[]
            for i in range(n):
                a.append(randint(min_, max_))
            return min(a)

        w = get_min_in_n_repeat(1, maxw-10, 1)
        h = get_min_in_n_repeat(1, maxh-10, 1)
        ww = get_min_in_n_repeat(w+1, maxw - 10, 10)
        hh = get_min_in_n_repeat(h + 1, maxh - 10, 10)

        return (w, h, ww, hh)

    def __init__(self, file_name="img.jpg"):
        pass

    def print_creator(self):
        print("this simply app developed by Korzun Nikolay.")

    def __show_image(self, fn, additionaly_info=""):
        if os.path.isfile(fn):
            image = cv2.imread(fn)
            if len(additionaly_info) != 0:
                cv2.putText(image, additionaly_info, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.__text_color, 2)

            cv2.imshow(fn, image)
            cv2.waitKey(0)
        else:
            print("unavailable filename {}".format(fn))

    def __lab3(self, fn_input, fn_output):
        image = cv2.imread(fn_input)
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_img, 255 - self.__min_color_param, 255, cv2.THRESH_BINARY_INV)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        output = image.copy()
        for c in cnts:
            cv2.drawContours(output, [c], -1, self.__counters_color, 1)
        cv2.imwrite(fn_output, output)
        return len(cnts)

    def __lab4(self, fn_input, fn_output):
        def classify(c):
            def comp(a, b, eps=0.05):
                return (a >= b*(1-eps) and a <= b*(1+eps))

            #approximation? But why? It is performed during the search.

            shape = "unidentified" #this value not using in original code. wtf?
            peri = cv2.arcLength(c, True)
            area = cv2.contourArea(c)
            approx = cv2.approxPolyDP(c, 0.01 * peri, True)
            #count_vertexes = len(c)
            count_vertexes = len(approx)

            if count_vertexes == 2:
                shape = "line"
            elif count_vertexes == 3:
                shape = "triangle"
            elif count_vertexes == 4:
                (x, y, w, h) = cv2.boundingRect(c)
                ar = w / float(h)
                shape = "square" if comp(ar, 1) else "rectangle"
            elif count_vertexes == 5:
                shape = "pentagon"
            else:
                if comp(peri/(2*pi), sqrt(area/pi), 0.06):
                    shape = "circle"
                else:
                    shape = "ellipse"
            return shape

        image = cv2.imread(fn_input)
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_img, 255 - self.__min_color_param, 255, cv2.THRESH_BINARY_INV)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        output = image.copy()
        shapes = {}


        for c in cnts:
            M = cv2.moments(c)
            cX = int((M["m10"] / M["m00"]))
            cY = int((M["m01"] / M["m00"]))
            shape = classify(c)
            if shape not in shapes:
                shapes[shape] = 1
            else:
                shapes[shape] += 1
            cv2.drawContours(output, [c], -1, self.__counters_color, 1)
            #cv2.circle(output, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(output, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.__text_color, 2)
        cv2.imwrite(fn_output, output)
        return shapes

    def __print_info(self, info):
        print(info)

    def menu(self):
        c = input("choice option number?\n\t[1] - generate new image\n\t[2] - display image\n\t[3] - create image with"
                  " counters\n\t[4] - classify figures on image\n\t[0] - exit\n >>")
        if c == "1":
            self.__generate_new_image(self.__input_image_filename, 800, 600)
        elif c == "2":
            fn = input("input image fn: ")
            self.__show_image(fn)

        elif c == "3":
            count = self.__lab3(self.__input_image_filename, self.__output_image_filename)
            self.__show_image(self.__output_image_filename, self.__info_for_lab3_str.format(count))
        elif c == "4":
            info = self.__lab4(self.__input_image_filename, self.__output_image_filename)
            self.__print_info(info)
        else:
            return False
        return True

    def __generate_new_image(self, filename:str, width, height):
        img = Image.new('RGBA', (width, height), 'white')
        idraw = ImageDraw.Draw(img)
        count_rect = randint(self.__min_count_rect, self.__max_count_rect)
        count_ellipse = randint(self.__min_count_ellipse, self.__max_count_ellipse)

        for i in range(count_rect):
            idraw.rectangle(self.__get_random_xy_in_area(width, height), fill = self.__get_random_color())
        for i in range(count_ellipse):
            idraw.ellipse(self.__get_random_xy_in_area(width, height), fill = self.__get_random_color())
        img.save(filename)


if __name__ == "__main__":
    app = App()
    while(app.menu()):
        pass

