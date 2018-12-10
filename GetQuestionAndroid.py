# -*- coding: utf-8 -*-


from common import screenshot, ocr, methods, find_ico_pos
import time
import sys
from common.anawer import answer_j


# current_step = 0  # 0 首页品酒， 1 全民品酒

if __name__ == '__main__':
    current_step = 0
    # 截图
    while True:
        if current_step == 0:
            while True:
                screenshot.tap_screen(952, 256)  #进入全民品酒图标，右上角 自行修改位置
                print("从全民品酒页切换一次，调整首页待品酒的位置")
                time.sleep(0.5)
                screenshot.tap_screen(64, 132)  #返回到首页，左上角 自行修改位置
                time.sleep(1)
                screenshot.check_screenshot()
                pos = find_ico_pos.find_ico_pos("./screenshot.png", "./resources/WinePoint_ico.png", current_step)
                if pos:
                    print('找到首页可以品的酒')
                    screenshot.tap_screen(pos[0], pos[1])

                    time.sleep(1)
                    answer_j()
                    time.sleep(3)
                else:
                    print('首页酒已经品完了，开始全民品酒')
                    current_step = 1
                    break
        elif current_step == 1:
            screenshot.tap_screen(952, 256)  #进入全民品酒图标，右上角 自行修改位置
            time.sleep(1)
            qmpj_times = 0
            while True:
                qmpj_times += 1
                if qmpj_times % 10 == 3:
                    screenshot.swipe_screen(516, 1780, 516, 760)   #往下滑动到底部，自行修改位置
                if qmpj_times % 10 == 0:
                    screenshot.swipe_screen(516, 360, 516, 1780)    #滑动到顶部，自行修改位置
                    time.sleep(1)
                    screenshot.tap_screen(920, 1392)        #点击刷新按钮 自行修改位置
                    time.sleep(1)
                if qmpj_times >= 50:
                    print('总次数达到50次，退出')
                    exit(0)
                screenshot.check_screenshot()
                pos = find_ico_pos.find_ico_pos("./screenshot.png", "./resources/jlsj_point.png", current_step)
                if pos:
                    print('找到全民品酒页面可以品的酒')
                    screenshot.tap_screen(pos[0], pos[1])
                    time.sleep(1.5)
                    answer_j()
                    time.sleep(1)
                else:
                    print('找不到全民品酒页面酒的图标..')
                    current_step = 1
                    continue


