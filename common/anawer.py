# coding:utf8

from common import screenshot, ocr, methods, find_ico_pos
from PIL import Image
import configparser

map_list = {'萼': '尊'}
# 读取配置文件
config = configparser.ConfigParser()
config.read('./config/configure.conf', encoding='utf-8')


def answer_j():
    print('进入答题页面')
    screenshot.check_screenshot()
    img = Image.open("./screenshot.png")
    old_question, old_choices0, old_choices1 = ocr.ocr_img_baidu(img, config)
    if old_question == 0:
        screenshot.tap_screen(500, 150)
        return
    print('题目:' + old_question)
    print('第一行选项:' + old_choices0)
    print('第二行选项:' + old_choices1)
    question = []
    choices0 = []
    choices1 = []
    for i in range(len(old_question)):
        question.append(old_question[i])
    for i in range(len(old_choices0)):
        choices0.append(map_list.get(old_choices0[i], old_choices0[i]))
    for i in range(len(old_choices1)):
        choices1.append(map_list.get(old_choices1[i], old_choices1[i]))

    choices0_len = len(choices0)
    every_len = 1080/choices0_len/2
    already_choice_list = []
    for c in question:
        tap_flag = False
        for i, a in enumerate(choices0):
            a_pos = str(0)+str(i)
            if a == c and a_pos not in already_choice_list:
                already_choice_list.append(a_pos)
                screenshot.tap_screen((i*2+1) * every_len, 1480)
                tap_flag = True
                break
        if not tap_flag:
            for j, b in enumerate(choices1):
                b_pos = str(1) + str(j)
                if b == c and b_pos not in already_choice_list:
                    already_choice_list.append(b_pos)
                    screenshot.tap_screen((j * 2 + 1) * every_len, 1670)
                    tap_flag = True
                    break

        if tap_flag is False:
            print('存在找不到的字跳过题目' + old_question)
            screenshot.tap_screen(500, 150)
            break

