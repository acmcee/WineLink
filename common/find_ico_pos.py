# coding:utf8

import aircv as ac
import cv2


def draw_circle(img, pos):
    circle_radius = 50
    color = (255, 255, 255)
    line_width = 10
    cv2.circle(img, pos, 50, color, line_width)
    cv2.imwrite("/tmp/Copy.jpg", img)


def find_ico_pos(back_png_url, obj_png_url, find_step):
    old_imsrc = ac.imread(back_png_url)
    if find_step == 0:
        imsrc = old_imsrc[0:820, 200:1080]
    else:
        imsrc = old_imsrc
    # cv2.imwrite("/tmp/Copy.jpg", imsrc)
    imobj = ac.imread(obj_png_url)

    # find the match position
    pos = ac.find_template(imsrc, imobj, 0.85)
    if not pos:
        return pos
    print('相似度 %s' % pos['confidence'])
    if find_step == 0:
        x = int(pos['result'][0])+200
        y = int(pos['result'][1])
    else:
        x = int(pos['result'][0])
        y = int(pos['result'][1])
    circle_center_pos = (x, y)

    # draw_circle(imsrc, circle_center_pos, circle_radius, color, line_width)

    return circle_center_pos


if __name__ == '__main__':
    find_ico_pos('../resources/mainpage.png', '../resources/WinePoint_ico.png')

