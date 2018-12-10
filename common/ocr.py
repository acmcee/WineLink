# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 19:34
# @desc    :

from PIL import Image
import pytesseract
from PIL import ImageFilter
from aip import AipOcr
import io
import base64
from colorama import init,Fore


# 二值化算法
def binarizing(img, threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


def ocr_img_tess(image, config):
    """只运行一次 Tesseract"""

    combine_region = config.get("region", "combine_region").replace(' ','').split(',')
    combine_region = list(map(int, combine_region))

    # 切割题目+选项区域，左上角坐标和右下角坐标,自行测试分辨率
    region_im = image.crop((combine_region[0], combine_region[1], combine_region[2], combine_region[3]))

    # 转化为灰度图
    region_im = region_im.convert('L')

    # 把图片变成二值图像
    region_im = binarizing(region_im, 190)

    region_im.show()

    # win环境
    # tesseract 路径

    pytesseract.pytesseract.tesseract_cmd = config.get("tesseract", "tesseract_cmd")

    # 语言包目录和参数
    tessdata_dir_config = config.get("tesseract", "tessdata_dir_config")

    # lang 指定中文简体
    region_text = pytesseract.image_to_string(region_im, lang='chi_sim', config=tessdata_dir_config)
    region_text = region_text.replace("_", "一").split("\n")
    texts = [x for x in region_text if x != '']
    #print(texts)
    if len(texts) > 2:
        question = ''.join(texts[0].split())
        choices0 = ''.join(texts[1].split())
        choices1 = ''.join(texts[2].split())
        return question, choices0, choices1

    else:
        print(Fore.RED + '截图区域设置错误，请重新设置' + Fore.RESET)
        exit(0)


def ocr_img_baidu(image, config):
    # 百度OCR API  ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可
    """ 你的 APPID AK SK """
    APP_ID = config.get('baidu_api','APP_ID')
    API_KEY = config.get('baidu_api','API_KEY')
    SECRET_KEY = config.get('baidu_api','SECRET_KEY')

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # global combine_region
    # 切割题目+选项区域，左上角坐标和右下角坐标,自行测试分辨率
    combine_region = config.get("region", "combine_region").replace(' ','').split(',')
    combine_region = list(map(int, combine_region))
    region_im = image.crop((combine_region[0], combine_region[1], combine_region[2], combine_region[3]))

    img_byte_arr = io.BytesIO()
    region_im.save(img_byte_arr, format='PNG')
    image_data = img_byte_arr.getvalue()

    options = {"language_type":"CHN_ENG"}

    response = client.basicAccurate(image_data,options)
    words_result = response['words_result']

    texts = [x['words'] for x in words_result]
    # print(texts)
    if len(texts) == 3:
        question = ''.join(texts[0].split())
        choices0 = ''.join(texts[1].split())
        choices1 = ''.join(texts[2].split())
    elif len(texts) == 4:
        if len(texts[1]) == len(texts[2])+len(texts[3]):
            question = ''.join(texts[0].split())
            choices0 = ''.join(texts[1].split())
            choices1 = ''.join(texts[2].split()) + ''.join(texts[3].split())
        elif len(texts[3]) == len(texts[1])+len(texts[2]):
            question = ''.join(texts[0].split())
            choices0 = ''.join(texts[1].split())+ ''.join(texts[2].split())
            choices1 = ''.join(texts[3].split())

    else:
        print(Fore.RED + '截图区域设置错误，跳过本次' + Fore.RESET)
        return 0, 0, 0
    return question, choices0, choices1
