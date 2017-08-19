# coding=utf-8

# auto chapter explorer
# 仅适配标准窗口大小

from PIL import ImageGrab
import time
import numpy
import aircv as ac
import pyautogui

# 特殊按钮 标题 标记 文件路径
# chapter_mark_path = "pictures\mark\original_ui\explore\chapters\mark"
chapter_mark_path = "pictures\\mark\\original_ui\\explore\\chapters\\mark\\chapter\\"
select_monster_mark_path = "pictures\\mark\\original_ui\\explore\\chapters\\mark\\monster\\"


def get_mark_pos(img_mark, single=True, confidence=0.94):
    # 查找标记图片在当前界面坐标
    # single=True 查找单个

    current_menu_ui = ImageGrab.grab()
    open_cv_image = numpy.array(current_menu_ui)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    img_main = open_cv_image
    img_sub = ac.imread(img_mark)

    if single:

        template_pos = ac.find_template(img_main, img_sub, threshold=0.5)
        if template_pos is not None and template_pos['confidence'] >= confidence:
            return template_pos
        else:
            return None
    else:

        template_pos = ac.find_all_template(img_main, img_sub)

        return template_pos


def get_multiple_mark_pos():
    pass


def mark_button_click(_mark_pos, x_offset=0, y_offset=0):
    if _mark_pos is not None:
        print "clicking"
        pyautogui.click(int(_mark_pos['result'][0]) + x_offset,
                        int(_mark_pos['result'][1]) + y_offset)
        return 1
    else:
        print "could not find a button or mark to click!"
        return 0


def get_mark_and_click(mark_img, confidence=0.94, x_offset=0, y_offset=0):
    test_mark_pos = get_mark_pos(mark_img, confidence=confidence)
    if mark_button_click(test_mark_pos):
        time.sleep(0.2)
        return 1
    else:
        return 0


def get_chapter_mark_pos(_chapter_mark_img):
    pos_list = get_mark_pos(_chapter_mark_img, single=False)
    temp_item = None
    max_confidence = 0
    if pos_list is not None:
        for item in pos_list:
            if item['confidence'] >= 0.94 and item['confidence'] >= max_confidence:
                max_confidence = item['confidence']
                temp_item = item

        if temp_item is not None:
            return temp_item

    return None


def chapter_button_drag_down(_mark_pos):
    y_offset = 40
    y_h = 420
    pyautogui.moveTo( int(_mark_pos['result'][0]), int(_mark_pos['result'][1]) + y_offset )
    pyautogui.dragTo( int(_mark_pos['result'][0]), int(_mark_pos['result'][1]) + y_h, duration=1, button='left' )
    time.sleep(0.5) # 拖动后等待响应 防止误触


def find_chapter_and_click(chapter_mark_img):
    mark_find_monster_title = chapter_mark_path + "mark_find_monster_title.jpg"

    find_monster_title_pos = None
    wait_times = 0
    while (find_monster_title_pos is None) and (wait_times <= 3):
        # 进入探索界面时 设定尝试并等待客户端反应
        find_monster_title_pos = get_mark_pos(mark_find_monster_title)
        time.sleep(1)
        wait_times += 1

    if find_monster_title_pos is not None:
        chapter_pos = None
        chapter_pos = get_chapter_mark_pos(chapter_mark_img)
        drag_times = 0
        while (chapter_pos is None) and drag_times <= 6:
            chapter_button_drag_down(find_monster_title_pos)
            drag_times += 1
            chapter_pos = get_chapter_mark_pos(chapter_mark_img)
            print "drag times " + str(drag_times)
        if chapter_pos is not None:
            mark_button_click(chapter_pos)
            print chapter_pos
            return 1
        else:
            return 0

def select_chapter_mode(hard_mode):
    # normal or hard

    button_hard_mode_selected = chapter_mark_path + "button_hard_chapter_selected.jpg"
    hard_mode_selected_pos = get_mark_pos(button_hard_mode_selected)
    # 检测困难模式是否已经选中
    if hard_mode_selected_pos is not None and hard_mode_selected_pos['confidence'] >= 0.94:
        if hard_mode:
            return 1
        else:
            button_normal_mode_unselected = chapter_mark_path + "button_normal_chapter_unselected.jpg"
            get_mark_and_click(button_normal_mode_unselected)
            return 1
    else:
        if hard_mode:
            button_hard_mode_unselected = chapter_mark_path + "button_hard_chapter_unselected.jpg"
            get_mark_and_click(button_hard_mode_unselected)
            return 1
        else:
            return 1


def select_chapter(chapter_num, hard_mode=False):
    chapter_mark_img = chapter_mark_path + str(chapter_num) + ".jpg"
    if find_chapter_and_click(chapter_mark_img):
        time.sleep(3)
        print "chapter " + str(chapter_num) + " selected"
        # 进入怪物选择界面 -> 选择困难模式 -> 选择'探索'
        mode_selected = select_chapter_mode(hard_mode)
        time.sleep(0.5)
        if mode_selected:
            # 模式选择完毕 开始进入探索
            button_chapter_start_mark = chapter_mark_path + "button_chapter_start.jpg"
            get_mark_and_click(button_chapter_start_mark)
            return 1

    else:
        print "cant not find chapter " + str(chapter_num)
        return 0

def click_ready_button():
    button_wait_for_ready = select_monster_mark_path + "button_wait_for_ready.jpg"
    bwfr_pos = get_mark_pos(button_wait_for_ready)
    while bwfr_pos is not None:
        print "Wait for ready..."
        print "Clicking ready button..."
        mark_button_click(bwfr_pos, y_offset=-54)
        time.sleep(0.5)
        bwfr_pos = get_mark_pos(button_wait_for_ready)

    return 1


def in_battle_process(is_boss=False):
    # 等待战斗载入
    time.sleep(0.5)

    # 战斗时间限制
    battle_time_out = 60 * 10
    battle_time = 0

    battle_start_time = time.time()
    in_battle_mark_2 = select_monster_mark_path + "mark_in_battle_2.jpg"
    in_battle_mark_3 = select_monster_mark_path + "mark_in_battle_3.jpg"
    r2_pos = get_mark_pos(in_battle_mark_2)
    r3_pos = get_mark_pos(in_battle_mark_3)

    temp_pos = r2_pos
    while r2_pos is None:
        r2_pos = get_mark_pos(in_battle_mark_2)
        # 备用坐标
        temp_pos = r2_pos

    all_ready = 0
    # 任何一个标记存在 战斗还在进行中
    while r2_pos is not None and battle_time <= battle_time_out:
        print "in battle..."

        # Todo: need improve
        #if all_ready():
        click_ready_button()

        time.sleep(1)
        current_battle_time = time.time()
        battle_time = current_battle_time - battle_start_time

        r2_pos = get_mark_pos(in_battle_mark_2)
        r3_pos = get_mark_pos(in_battle_mark_3)

    if battle_time > battle_time_out:
        return -1 # 超时处理
    else:
        # 战斗正常结束 进入领取奖励确认
        time.sleep(5)  # 等待界面加载
        print "battle end, checking rewards..."
        drag_base = select_monster_mark_path + "monster_select_drag_base.jpg"
        drag_base_pos = get_mark_pos(drag_base)
        while drag_base_pos is None:
            print "battle end, checking rewards..."
            print "pos"
            print temp_pos
            mark_button_click(temp_pos, x_offset=0, y_offset=50)
            time.sleep(0.5)
            drag_base_pos = get_mark_pos(drag_base)

        print "battle end, check rewards Done!"

    if is_boss:
        # 查找是否有章节完成特别奖励
        return sp_reward_picker()
    else:
        time.sleep(0.5)
        return 0


def sp_reward_picker():
    # 已经退出章节的标记

    print "check if chapter is all done and quit successfuly..."
    mark_find_monster_title = chapter_mark_path + "mark_find_monster_title.jpg"
    mark_find_monster_title_pos = get_mark_pos(mark_find_monster_title)

    button_end_chapter_sp_reward = select_monster_mark_path + "button_end_chapter_sp_reward.jpg"
    button_end_chapter_sp_reward_check = select_monster_mark_path + "button_end_chapter_sp_reward_check.jpg"

    drag_base = select_monster_mark_path + "monster_select_drag_base.jpg"
    drag_base_pos = get_mark_pos(drag_base)
    while drag_base_pos is not None:
        print "Chapter end, checking sp rewards..."

        print "Searching sp reward..."
        button_end_chapter_sp_reward_pos = get_mark_pos(button_end_chapter_sp_reward)

        while button_end_chapter_sp_reward_pos is not None:
            print "sp rewards found!"

            print "Clicking sp reward box..."
            mark_button_click(button_end_chapter_sp_reward_pos)

            # 等待响应
            time.sleep(1)
            print "Checking sp reward..."
            mark_button_click(drag_base_pos, y_offset=40)
            # get_mark_and_click(button_end_chapter_sp_reward_check, y_offset=310)

            time.sleep(0.5)
            print "sp rewards gets!"

            # 检测已经完全退出章节挑战
            button_end_chapter_sp_reward_pos = get_mark_pos(button_end_chapter_sp_reward)

        drag_base_pos = get_mark_pos(drag_base)


    return 1

def get_monster_pos():
    # boss 优先
    boss = False
    mark_button_boss_select = select_monster_mark_path + "button_boss_select.jpg"
    boss_pos = get_mark_pos(mark_button_boss_select)
    if boss_pos is not None and boss_pos['confidence'] >= 0.94:
        return boss_pos, True
    else:
        mark_button_monster_select = select_monster_mark_path + "button_monster_select.jpg"
        monster_pos = get_mark_pos(mark_button_monster_select)
        if monster_pos is not None and monster_pos['confidence'] >= 0.94:
            return monster_pos, False
        else:
            return None, False


def select_monster():
    monster_pos, boss = get_monster_pos()

    chapter_end = 0
    drag2left_times = 0
    while drag2left_times <= 6:
        if monster_pos is not None:
            mark_button_click(monster_pos)
            chapter_end = in_battle_process(is_boss=boss)
            if chapter_end == 1:
                return 1
        else:
            print "drag2left"
            select_monster_drag()
            drag2left_times += 1

        monster_pos, boss = get_monster_pos()
        # monster_pos = get_mark_pos(mark_button_monster_select)

    drag2right_times = 0
    while drag2right_times <= 3:
        if monster_pos is not None:
            mark_button_click(monster_pos)
            chapter_end = in_battle_process(is_boss=boss)
            if chapter_end == 1:
                return 1
        else:
            print "drag2right"
            select_monster_drag(drag2left=False)
            drag2right_times += 1

        monster_pos, boss = get_monster_pos()
        # monster_pos = get_mark_pos(mark_button_monster_select)


def select_monster_drag(drag2left=True):
    # drag2left=True :Right to left
    # drag2left=False :Left to Right

    # 向下偏移80
    y_offset = 40
    # 横向偏移800
    x_h = 800

    drag_base = select_monster_mark_path + "monster_select_drag_base.jpg"
    drag_base_pos = get_mark_pos(drag_base)

    if drag_base_pos is not None:
        if drag2left:
            pyautogui.moveTo(int(drag_base_pos['result'][0]), int(drag_base_pos['result'][1]) + y_offset)
            pyautogui.dragTo(int(drag_base_pos['result'][0]) - x_h, int(drag_base_pos['result'][1]) + y_offset,
                             duration=1, button='left')
            # time.sleep(0.5)
        else:
            pyautogui.moveTo(int(drag_base_pos['result'][0]) - x_h, int(drag_base_pos['result'][1]) + y_offset)
            pyautogui.dragTo(int(drag_base_pos['result'][0]), int(drag_base_pos['result'][1]) + y_offset,
                             duration=1, button='left')
            # time.sleep(0.5)
        return 1
    else:
        return 0


def enter_explorer():
    # 由主界面进入探索
    button_main_menu_explorer = "pictures\\mark\\original_ui\\explore\\button_main_menu_explorer.jpg"
    button_main_menu_explorer_pos = get_mark_pos(button_main_menu_explorer, confidence=60)

    try_times = 0
    while button_main_menu_explorer_pos is None and try_times < 20:
        print "Searching 'Explorer' button..."
        time.sleep(0.2)
        button_main_menu_explorer_pos = get_mark_pos(button_main_menu_explorer)
        try_times += 1

    if button_main_menu_explorer_pos is None:
        print "Error, Please retry..."
        return 0
    else:
        print "'Explorer' button found!"
        mark_button_click(button_main_menu_explorer_pos)
        return 1


def back_home():
    print "Back home..."
    general_mark_path = "pictures\\mark\\original_ui\\explore\\chapters\\mark\\general_mark\\"
    # 回到主界面

    mark_button_confirm = general_mark_path + "button_confirm.jpg"

    mark_back_button = general_mark_path + "button_back.jpg"
    mark_back_button_pos = get_mark_pos(mark_back_button)
    while mark_back_button_pos is not None:
        print "Found back button, clicking..."
        mark_button_click(mark_back_button_pos)
        time.sleep(0.5)

        button_confirm_pos = get_mark_pos(mark_button_confirm)
        if button_confirm_pos is not None:
            print "Found confirm button, clicking..."
            mark_button_click(button_confirm_pos)
            time.sleep(1)

        mark_back_button_pos = get_mark_pos(mark_back_button)

    return 1


# back_home()

# 探索副本测试
if enter_explorer():
    if select_chapter(13, hard_mode=True):
        chapter_done = select_monster()
        if chapter_done:
            # Todo check_treasure_box()
            back_home()

