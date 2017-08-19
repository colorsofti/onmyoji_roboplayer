# coding=utf-8

# auto chapter explorer
# 仅适配标准窗口大小

from PIL import ImageGrab
import time
import numpy
import aircv as ac
import pyautogui

# 特殊按钮 标题 标记 文件路径

soul_mark_path = "pictures\\mark\\original_ui\\explore\\exclusive_soul\\"


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
    test_mark_pos = get_mark_pos(mark_img, confidence)
    if mark_button_click(test_mark_pos):
        time.sleep(0.2)
        return 1
    else:
        return 0


def click_ready_button():
    button_wait_for_ready = soul_mark_path + "button_wait_for_ready.jpg"
    bwfr_pos = get_mark_pos(button_wait_for_ready)
    while bwfr_pos is not None:
        # 持续点击 准备 按钮
        print "Wait for ready..."
        print "Clicking ready button..."
        mark_button_click(bwfr_pos, y_offset=-54)
        time.sleep(0.5)
        bwfr_pos = get_mark_pos(button_wait_for_ready)

    return 1


def in_battle_process(is_boss=False):
    # 等待载入
    time.sleep(2)

    # 战斗时间限制
    battle_time_out = 60 * 30
    battle_time = 0

    battle_start_time = time.time()
    in_battle_mark_2 = soul_mark_path + "mark_in_battle_2.jpg"
    in_battle_mark_3 = soul_mark_path + "mark_in_battle_3.jpg"
    r2_pos = get_mark_pos(in_battle_mark_2)
    r3_pos = get_mark_pos(in_battle_mark_3)


    button_leave_team = soul_mark_path + "button_leave_team.jpg"
    button_leave_team_pos = get_mark_pos(button_leave_team)
    at_team_wait_duration = 0
    # 组队等待时间限制
    at_team_wait_limits = 20
    at_team_wait_start = time.time()
    while get_mark_pos(button_leave_team) is not None and at_team_wait_duration <= at_team_wait_limits:
        time.sleep(1)
        at_team_wait_duration = time.time() - at_team_wait_start

    if at_team_wait_duration > at_team_wait_limits:
        # 等待组队超时

        leave_team_confirm = soul_mark_path + "leave_team_confirm.jpg"
        # 退出组队
        mark_button_click(button_leave_team)
        time.sleep(1)
        while get_mark_pos(leave_team_confirm) is not None:
            # 点击 确定
            mark_button_click(leave_team_confirm, x_offset=100, y_offset=50)
            time.sleep(1)

        teamwork_soul_cross_cancel = soul_mark_path + "teamwork_soul_cross_cancel.jpg"
        while get_mark_pos(teamwork_soul_cross_cancel):
            # 退出组队界面 到主界面
            mark_button_click(teamwork_soul_cross_cancel)
            time.sleep(1)

        return 0
    else:

        temp_pos = r2_pos
        while r2_pos is None:
            # 用固定标记识别是否已经开始战斗
            print "Wait to start..."
            r2_pos = get_mark_pos(in_battle_mark_2)
            time.sleep(0.5)

        # TODO 用于节省时间
        in_battle_start = 0
        # 可以接受的战斗时长
        in_time = 65
        in_battle_duration = 0

        all_ready = 0
        # 任何一个标记存在 战斗还在进行中
        while (r2_pos is not None or r3_pos is not None) \
                and battle_time <= battle_time_out:
            print "in battle..."

            # Todo: need improve
            #if all_ready():
            # 战斗开始时 检测是否有 准备 按钮 以及点击
            click_ready_button()
            in_battle_start = time.time()

            time.sleep(1)
            current_battle_time = time.time()
            battle_time = current_battle_time - battle_start_time

            r2_pos = get_mark_pos(in_battle_mark_2)
            r3_pos = get_mark_pos(in_battle_mark_3)

            # 备用坐标
            if r2_pos is not None:
                temp_pos = r2_pos

        in_battle_duration = time.time() - in_battle_start

        if battle_time > battle_time_out:
            return -1 # 超时处理
        else:
            # 战斗结束查收超时时间限制
            check_rewards_time_limits = 30

            check_rewards_start = time.time()
            check_rewards_duration = 0
            # 战斗正常结束 进入领取奖励确认
            time.sleep(2)  # 等待界面加载
            print "battle end, checking rewards..."

            # todo mark_home.jpg标记有可能出现意外问题
            drag_base = soul_mark_path + "mark_home.jpg"
            drag_base_pos = get_mark_pos(drag_base)
            while drag_base_pos is None and check_rewards_duration <= check_rewards_time_limits:
                # 一直点击 直到回到游戏主界面
                print "battle end, checking rewards..."
                # print "pos"
                # print temp_pos
                mark_button_click(temp_pos, x_offset=0, y_offset=50)

                print "Waiting..."
                time.sleep(1.5)
                # 检测是否回到游戏主界面
                drag_base_pos = get_mark_pos(drag_base)
                check_rewards_duration = time.time() - check_rewards_start

            if check_rewards_duration <= check_rewards_time_limits:
                print "battle end, check rewards Done!"
                return 1
            else:
                print "Checking rewards timeout!"
                # todo
                return 0


def repeat_click(img, times_limits=20):
    img_pos =get_mark_pos(img)
    while img_pos is None:
        pass


def click_teamwork():
    button_make_teamwork = soul_mark_path + "button_make_teamwork.jpg"
    mark_scroll_closed = soul_mark_path + "mark_scroll_closed.jpg"
    mark_scroll_opened = soul_mark_path + "mark_scroll_opened.jpg"

    try_times = 0
    mark_scroll_opened_pos = get_mark_pos(mark_scroll_opened)
    while mark_scroll_opened_pos is None and try_times <= 20:
        # 检测界面底下 卷轴 打开 否则尝试点击未打开的卷轴
        print "Opening scroll..."
        get_mark_and_click(mark_scroll_closed)
        try_times += 1
        time.sleep(0.5)
        mark_scroll_opened_pos = get_mark_pos(mark_scroll_opened)

    if mark_scroll_opened_pos is not None:
        # 找到 组队 并点击进入
        print "'Make teamwork' button found! Clicking..."
        button_make_teamwork_pos = get_mark_pos(button_make_teamwork)
        mark_button_click(button_make_teamwork_pos)
        return 1
    else:
        print "can not found 'Make teamwork' button !! Please retry!"
        return 0


def click_button_soul_and_chose_level(level=10):
    button_soul_unclicked = soul_mark_path + "button_soul_unclicked.jpg"
    button_soul_unclicked_pos  = get_mark_pos(button_soul_unclicked)

    while button_soul_unclicked_pos is None:
        # 持续查找 御魂 按钮
        time.sleep(0.5)
        button_soul_unclicked_pos = get_mark_pos(button_soul_unclicked)

    # 找到 御魂 按钮后点击
    mark_button_click(button_soul_unclicked_pos)

    if select_soul_level(level=level):
        # 选择御魂 等级 成功后
        return 1
    else:
        print "Can not found level" + str(level) + "!"
        return 0


def select_soul_level(level=1):
    level_img = soul_mark_path + "button_soul_" + str(level) + ".jpg"
    level_img_pos = get_mark_pos(level_img)

    drag_time_limits = 10
    drag_duration = 0
    drag_time_start = time.time()
    drag2up = True
    while level_img_pos is None and drag_duration <= drag_time_limits:
        # 持续拖动菜单并查找响应的 御魂 等级按钮
        soul_level_menu_drag(drag2up=drag2up)
        drag2up = not drag2up
        time.sleep(0.5)
        level_img_pos = get_mark_pos(level_img)
        drag_duration = time.time() - drag_time_start

    if drag_duration <= drag_time_limits:
        if level_img_pos is not None:
            # 找到 等级 按钮并且未超时
            print "Level " + str(level) + "found!"
            mark_button_click(level_img_pos)
            return 1
        else:
            print "Soul level not found !"
            return 0
    else:
        print "Search soul level timeout!"
        return 0


def soul_level_menu_drag(drag2up=True):
    level_pos_base = soul_mark_path + "button_soul_refresh.jpg"
    level_pos_base_pos = get_mark_pos(level_pos_base)

    while level_pos_base_pos is None:
        # 以 刷新 按钮作为选择等级菜单的基准坐标
        level_pos_base_pos = get_mark_pos(level_pos_base)
        time.sleep(0.5)

    y_offset_t = 330
    y_offset_b = 60

    if drag2up:
        # 菜单向上拖动
        pyautogui.moveTo(int(level_pos_base_pos['result'][0]),
                         int(level_pos_base_pos['result'][1]) - y_offset_b)
        pyautogui.dragTo(int(level_pos_base_pos['result'][0]),
                         int(level_pos_base_pos['result'][1]) - y_offset_t, duration=1, button='left')
    else:
        # 菜单向下拖动
        pyautogui.moveTo(int(level_pos_base_pos['result'][0]),
                         int(level_pos_base_pos['result'][1]) - y_offset_t)
        pyautogui.dragTo(int(level_pos_base_pos['result'][0]),
                         int(level_pos_base_pos['result'][1]) - y_offset_b, duration=1, button='left')


def click_refresh_and_join():
    button_soul_refresh = soul_mark_path + "button_soul_refresh.jpg"
    button_soul_refresh_pos = get_mark_pos(button_soul_refresh)

    button_soul_join = soul_mark_path + "button_soul_join.jpg"

    while button_soul_refresh_pos is not None:
        # 如果 刷新 按钮未消失 说明未进入组队 重复 刷新 并尝试点击 加入
        print "clicking 'refresh'..."
        mark_button_click(button_soul_refresh_pos)
        time.sleep(1)
        get_mark_and_click(button_soul_join)
        time.sleep(1)
        button_soul_refresh_pos = get_mark_pos(button_soul_refresh)

    if button_soul_refresh_pos is None:
        # 如果 刷新 按钮消失 说明已经进入组队
        # todo
        print "Join team success!"
        return 1


def receive_soul_invite(remaining_times=1, good_team=True):
    wait_start_time = time.time()
    invite_message = soul_mark_path + "receive_invite.jpg"
    invite_message_pos = get_mark_pos(invite_message)

    # 等待邀请超时限制
    wait_time_limits = 15
    delta_time = 0

    while invite_message_pos is None and delta_time <= wait_time_limits and remaining_times >= 1:
        # 等待邀请框的出现
        print "Waiting for next invite..."
        time.sleep(0.5)
        invite_message_pos = get_mark_pos(invite_message)
        delta_time = time.time() - wait_start_time

    if remaining_times >= 1:
        print "Remaining souling teamwork times:" + str(remaining_times)
        if delta_time > wait_time_limits:
            print "Wait for invite time out!"
            print "Receive invite timeout, restart teamwork!"
            # return 0

        x_offset = 40
        if invite_message_pos is not None:
            if good_team:
                print "Accept inviting..."
                # 点击接受邀请
                # TODO 可能发生意外接受其他邀请
                mark_button_click(invite_message_pos, x_offset=40)
                # 点击接受后 进入 等待、开始 战斗
                return in_battle_process()
            else:
                # 拒绝组队
                print "Reject inviting..."
                mark_button_click(invite_message_pos, x_offset=-40)

        # 未收到邀请则 重新开始组队 同时组队次数减1
        rece_invite_timeout_reteam(times_limits=(remaining_times))

    else:
        print "Stop souling, remaining times:" + str(remaining_times)
        return 0


def continue_teamwork(times_limits=10):
    # 接受后续邀请
    # 组队次数
    soul_times_limits = times_limits

    good_team = True
    battle_duration = 0
    battle_start = time.time()
    battle_sussess = in_battle_process()
    battle_duration = time.time() - battle_start

    good_standard = 80
    print "Battle duration: " + str(battle_duration) + " seconds"
    print "Good standard:less then " + str(good_standard) + " seconds"
    if battle_sussess and battle_duration <= good_standard:
        good_team = True
        print "Good teamworking!"
    else:
        print "Bad teamworking!"
        good_team = False

    while battle_sussess and soul_times_limits >= 1:
        soul_times_limits -= 1
        print str(soul_times_limits) + " times to stop souling...."
        battle_sussess = receive_soul_invite(remaining_times=soul_times_limits, good_team=good_team)

    if not battle_sussess and soul_times_limits >= 1:
        start_souling_teamwork(souling_times=soul_times_limits)

    if soul_times_limits < 1:
        # 结束
        print "All Done!"
        return 1

def rece_invite_timeout_reteam(times_limits=1):
    if click_teamwork():
        if click_button_soul_and_chose_level():
            if click_refresh_and_join():
                if continue_teamwork(times_limits=times_limits):



def start_souling_teamwork(join_team=True, souling_times=5):
    if rece_invite_timeout_reteam(times_limits=souling_times):
        return 1

start_souling_teamwork(souling_times=3)