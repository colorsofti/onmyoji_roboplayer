# coding=utf-8

import aircv as ac


def get_pos():
    # 查找 a图 在 b图是否存在及返回坐标
    img_main = ac.imread('monster_chose.JPG')
    img_sub = ac.imread('mark\original_ui\explore\chapters\mark\mark_double_money.jpg')

    print ac.find_template(img_main, img_sub)
    print ac.find_all_template(img_main, img_sub)


get_pos()
