from email import message
from tokenize import group
from turtle import pos
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Bot
from nonebot.log import logger
from pathlib import Path
from typing import Tuple, Union, Dict
import nonebot
import numpy as np
import os
import random
from .config import Config
try:
    import ujson as json
except ModuleNotFoundError:
    import json

scheduler = nonebot.require("nonebot_plugin_apscheduler").scheduler

global_config = nonebot.get_driver().config
godden_config = Config.parse_obj(global_config.dict())
golden_confg = Config.parse_obj(nonebot.get_driver().config.dict())
cards_power = godden_config.cards_power
cat_gold = godden_config.cat_gold
cat_text = godden_config.cat_text
goal_gold = godden_config.goal_gold
golden_path = godden_config.golden_path
max_beg_times = godden_config.max_beg_times
pack_name = godden_config.pack_name
pack_type = godden_config.pack_type
sign_gold = godden_config.sign_gold
user_data_type = godden_config.user_data_type

async def rank(player_data: dict, group_id: int, type_: str) -> str:
    """
    排行榜数据统计
    :param player_data: 玩家数据
    :param group_id: 群号
    :param type_: 排行榜类型
    """
    group_id = str(group_id)
    all_user = list(player_data[group_id].keys())
    if type_ == "gold_rank":
        rank_name = "\t金碟币余额排行榜\n"
        all_user_data = [player_data[group_id][x]["gold"] for x in all_user]
    elif type_ == "cactpot_rec":
        rank_name = "\t仙人彩奖金排行榜\n"
        tmp = [player_data[group_id][x]["cactpot_rec"] for x in all_user]
        for x in range(len(tmp)):
            tmp_sum = 0
            for s in range(1,len(tmp[x])):
                tmp_sum += tmp[x][s]*cat_gold[s]
            tmp[x] = tmp_sum
        all_user_data = tmp
    elif type_ == "cards_power":
        rank_name = "\t幻卡战斗力排行榜\n"
        all_user_data = [player_data[group_id][x]["cards_power"] for x in all_user]
    elif type_ == "make_gold":
        rank_name = "\t赢取的金碟币排行榜\n"
        all_user_data = [player_data[group_id][x]["make_gold"] for x in all_user]
    elif type_ == "lose_gold":
        rank_name = "\t花掉的金碟币排行榜\n"
        all_user_data = [player_data[group_id][x]["lose_gold"] for x in all_user]
    else:
        rank_name = "\t签到天数排行榜\n"
        all_user_data = [player_data[group_id][x]["sign_days"] for x in all_user]
    rst = ""
    if all_user:
        for _ in range(len(all_user) if len(all_user) < 10 else 10):
            _max = max(all_user_data)
            _max_id = all_user[all_user_data.index(_max)]
            name = player_data[group_id][_max_id]["nickname"]
            rst += f"{name}：{_max}\n"
            all_user_data.remove(_max)
            all_user.remove(_max_id)
        rst = rst[:-1]
    return rank_name + rst

class GoldenManager:
    def __init__(self):
        self._player_data = {}
        self._current_player = {"battles":{}}
        file = golden_path / "data" / "golden" / "golden_data.json"
        self.file = file
        file.parent.mkdir(exist_ok=True, parents=True)
        if not file.exists():
            old_file = Path(os.path.dirname(__file__)) / "golden_data.json"
            if old_file.exists():
                os.rename(old_file, file)
        if file.exists():
            with open(file, "r", encoding="utf8") as f:
                self._player_data = json.load(f)
        #检查数据项
        data_change = 0
        for key_name in user_data_type.keys():
            for group_id in self._player_data.keys():
                for user_id in self._player_data[group_id].keys():
                    if not key_name in self._player_data[str(group_id)][str(user_id)]:
                        data_change += 1
                        self._player_data[str(group_id)][str(user_id)][key_name] = user_data_type[key_name]
        if data_change > 0:
            self.save()
            logger.info(f'添加{data_change}条缺失数据')

    def change_gold_self(self, group_id: str, user_id: str, nums: int):
        group_id = str(group_id)
        user_id = str(user_id)
        player_datas = self._player_data[group_id]
        loan_in = player_datas[user_id]["loan_in"]
        if nums > 0:
            if len(loan_in) > 0:
                del_out_list = []
                del_in_list = []
                for loan_out_id in loan_in:
                    player_datas[loan_out_id]["gold"] += int(nums/10)
                    player_datas[loan_out_id]["loan_out"][user_id] -= int(nums/10)
                    player_datas[user_id]["loan_in"][loan_out_id] -= int(nums/10)
                    if player_datas[loan_out_id]["loan_out"][user_id] < 0:
                        del_out_list.append(loan_out_id)
                    if player_datas[user_id]["loan_in"][loan_out_id] <= 0:
                        del_in_list.append(loan_out_id)
                for del_user_id in del_out_list:
                    del player_datas[del_user_id]["loan_out"][user_id]
                for del_user_id in del_in_list:
                    del player_datas[user_id]["loan_in"][del_user_id]

                player_datas[user_id]["gold"] += nums-int(nums/10*len(loan_in))
                player_datas[user_id]["make_gold"] += nums-int(nums/10*len(loan_in))
            else:
                player_datas[user_id]["gold"] += nums
                player_datas[user_id]["make_gold"] += nums
            return nums - int(nums/10*len(loan_in))
        elif nums < 0:
            player_datas[user_id]["gold"] += nums
            player_datas[user_id]["lose_gold"] -= nums
            return nums
        else:
            return 0

    def sign(self, event: GroupMessageEvent) -> Tuple[str, int]:
        """
        签到
        :param event: event
        """
        self._init_player_data(event)
        if self._player_data[str(event.group_id)][str(event.user_id)]["is_sign"]:
            return "你已经刮过仙人微彩了！", -1
        backtext = "\n"
        gold = 0
        for ele in range(3):
            gain_num = 0
            num_tmps = random.sample(range(1, 10),3)
            for num_tmp in num_tmps:
                backtext += str(num_tmp)+'  '
                gain_num += num_tmp
            gold += sign_gold[gain_num]
            backtext += f',获得{sign_gold[gain_num]}金碟币\n'
        left_gold = self.change_gold_self(event.group_id, event.user_id, gold)
        self._player_data[str(event.group_id)][str(event.user_id)]["sign_days"] += 1
        self._player_data[str(event.group_id)][str(event.user_id)]["is_sign"] = True
        self.save()
        return (
            backtext + f"共获得了 {gold} 金碟币",
            left_gold,)

    def cactpot(self, event: GroupMessageEvent, times: int, use_all: bool) -> Tuple[str, int]:
        """
        仙人彩
        """
        self._init_player_data(event)
        now_gold = self._player_data[str(event.group_id)][str(event.user_id)]["gold"]
        backtext = f'\n'
        if now_gold - times*10 < 0:
            if not use_all or now_gold < 10:
                return (f'金碟币不足！',-1)
            else:
                backtext +=f'！！有位勇士开始梭哈！！\n'
                times = int(now_gold/10)
        gold = 0
        gold_tab = [0, 0, 0, 0, 0, 0, 0, 0]
        num_list = range(1,10000001)
        adjust = 0
        for x in range(0,times):
            num_tmp = random.choice(num_list)
            if num_tmp > 100000 and num_tmp <= 100001:
                gold_tmp = 7#0.3
            elif num_tmp > 2000000 and num_tmp <= 2000174:
                gold_tmp = 6#1.16
            elif num_tmp > 3000000 and num_tmp <= 3001740:
                gold_tmp = 5#1.16
            elif num_tmp > 1000000 and num_tmp <= 1004016:
                gold_tmp = 4#1.16
            elif num_tmp > 4000000 and num_tmp <= 4022523:
                gold_tmp = 3#1.16
            elif num_tmp > 5000000 and num_tmp <= 5130120:
                gold_tmp = 2#2.16
            elif num_tmp > 6000000 and num_tmp <= 9160000:
                gold_tmp = 1#3.16
            else:
                gold_tmp = 0
            text = cat_text[gold_tmp]
            self._player_data[str(event.group_id)][str(event.user_id)]["cactpot_rec"][gold_tmp]+=1
            gold_num = cat_gold[gold_tmp]

            gold_tab[gold_tmp] += 1
            if times <= 10 or gold_num > 10 and times <= 100:
                backtext += random.choice(text) + f"获得了 {gold_num} 金碟币\n"
            gold+=gold_num
        if times > 10 and times <= 100:
            backtext += f'获得了  {cat_gold[1]}  金碟币  {gold_tab[1]}  次\n'
        if times > 100 and use_all:
            backtext +=(
                f'{cat_gold[0]}金碟币            ：{gold_tab[0]}\n'+
                f'{cat_gold[1]}金碟币          ：{gold_tab[1]}\n'+
                f'{cat_gold[2]}金碟币        ：{gold_tab[2]}\n'+
                f'{cat_gold[3]}金碟币        ：{gold_tab[3]}\n'+
                f'{cat_gold[4]}金碟币      ：{gold_tab[4]}\n'+
                f'{cat_gold[5]}金碟币      ：{gold_tab[5]}\n'+
                f'{cat_gold[6]}金碟币    ：{gold_tab[6]}\n'+
                f'{cat_gold[7]}金碟币：{gold_tab[7]}\n'
            )
        elif times > 10:
            backtext += f"一共{gold_tab[0]}次没中奖，安慰你一下\n"
        backtext += f'消耗了{times*10}金碟币'
        left_gold = self.change_gold_self(event.group_id, event.user_id, gold)
        self.change_gold_self(event.group_id, event.user_id, times*-10)
        self.save()
        return (
            backtext,
            left_gold - times*10
        )

    def get_cards(self, event: GroupMessageEvent, buy_pack_type: int, nums: int) -> str:
        """
        买卡包
        """
        self._init_player_data(event)
        cost = pack_type[buy_pack_type]
        allcost = cost * nums
        gold = self._player_data[str(event.group_id)][str(event.user_id)]["gold"]
        if gold < allcost:
            return ("金碟币不足，无法购买",
                    -1,)
        else:
            self.change_gold_self(event.group_id, event.user_id, allcost*-1)
            self._player_data[str(event.group_id)][str(event.user_id)]["pack_store"][buy_pack_type] += nums
            self.save()
            return (f"购买成功,消耗{allcost}金碟币,剩余{gold-allcost}金碟币")

    def open_cards(self, event: GroupMessageEvent, open_pack_type: int, nums: int) -> str:
        """
        开卡包
        """
        self._init_player_data(event)
        type_nums = self._player_data[str(event.group_id)][str(event.user_id)]["pack_store"][open_pack_type]
        if type_nums <= 0 :
            return ("卡包不足！")
        if type_nums < nums:
            nums = type_nums
        cards_open = [0, 0, 0, 0, 0, 0]
        power = 0
        cardstmps = np.random.randn(nums)
        for ele in cardstmps:
            gain_cards = open_pack_type + ele
            if gain_cards >= 8:
                cards_open[5] += 1
                power += cards_power[5]
            elif gain_cards >= 6.5:
                cards_open[4] += 1
                power += cards_power[4]
            elif gain_cards >= 4:
                cards_open[3] += 1
                power += cards_power[3]
            elif gain_cards >= 3:
                cards_open[2] += 1
                power += cards_power[2]
            elif gain_cards >= 1:
                cards_open[1] += 1
                power += cards_power[1]
            else:
                cards_open[0] += 1
                power += cards_power[0]
        for gain in range(6):
            self._player_data[str(event.group_id)][str(event.user_id)]["cards_opend"][gain] += cards_open[gain]
        self._player_data[str(event.group_id)][str(event.user_id)]["pack_store"][open_pack_type] -= nums
        self._player_data[str(event.group_id)][str(event.user_id)]["pack_opend"][open_pack_type] += nums
        self._player_data[str(event.group_id)][str(event.user_id)]["cards_power"] += power
        self.save()
        backtext = f'\n一共开了{pack_name[open_pack_type]}{nums}包\n☆：{cards_open[0]}\n☆☆：{cards_open[1]}\n☆☆☆：{cards_open[2]}\n☆☆☆☆：{cards_open[3]}\n☆☆☆☆☆：{cards_open[4]}\n'
        if cards_open[5]:
            backtext+=f'隐藏究极卡！★：{cards_open[5]}\n'
        backtext+=f'幻卡战力增加了{power}'
        return (backtext)
    
    def battle_handle_timer(self, group_id):
        try:
            scheduler.remove_job(self._current_player["battles"][group_id]["scheduler_id"] + '_appl')
            logger.info(f"幻卡对决申请已超时")
        except:
            logger.info(f'幻卡申请定时删除错误')
        if group_id in self._current_player["battles"]:
            del self._current_player["battles"][group_id]

    async def battle_stop_timer(self, bot: Bot, group_id):
        try:
            scheduler.remove_job(self._current_player["battles"][group_id]["scheduler_id"] + '_play')
            logger.info(f"幻卡对决已超时")
        except:
            logger.info(f'幻卡对决定时删除错误')
        if group_id in self._current_player["battles"]:
            del self._current_player["battles"][group_id]
        await bot.send(MessageSegment.text(f'对决结束，没有分出胜负！'))
        
    def battle_check(self, event: GroupMessageEvent, at_id: int, nums: int=50):
        self._init_player_data(event)
        if not str(at_id) in self._player_data[str(event.group_id)]:
            return f'该用户还没有签过到！'
        if str(event.group_id) in self._current_player["battles"]:
            return f'已经有正在开始的对决了！'
        if nums <= 0:
            return f'赌注是不是有点奇怪？再输入一次吧！'
        a_nickname = self._player_data[str(event.group_id)][str(event.user_id)]["nickname"]
        a_gold = self._player_data[str(event.group_id)][str(event.user_id)]["gold"]
        a_opend = self._player_data[str(event.group_id)][str(event.user_id)]["cards_opend"]
        a_power = 0
        a_cards = 0
        b_nickname = self._player_data[str(event.group_id)][str(at_id)]["nickname"]
        b_gold = self._player_data[str(event.group_id)][str(at_id)]["gold"]
        b_opend = self._player_data[str(event.group_id)][str(at_id)]["cards_opend"]
        b_power = 0
        b_cards = 0

        if a_gold < nums or b_gold < nums:
            return f'对决一方余额不足，无法开始对决！'

        for x in range(0,6):
            if a_cards < 6:
                if a_cards+a_opend[5-x] > 6:
                    add_cards = 6 - a_cards
                else:
                    add_cards = a_opend[5-x]
                a_power += add_cards * cards_power[5-x]
                a_cards += add_cards
            if b_cards < 6:
                if b_cards+b_opend[5-x] > 6:
                    add_cards = 6 - b_cards
                else:
                    add_cards = b_opend[5-x]
                b_power += add_cards * cards_power[5-x]
                b_cards += add_cards
        if a_cards<6 or b_cards<6:
            return f'对决一方幻卡数少于6张，无法开始对决！'

        self._current_player["battles"][str(event.group_id)] = {
            str(event.user_id):{"power":a_power, "id":event.user_id, "nickname":a_nickname, "side": 0},
            str(at_id):{"power":b_power, "id":at_id, "nickname":b_nickname, "side": 1},
            "scheduler_id": str(event.group_id),
            "turn_id":"",
            "playground": 0b0001000,
            "nums": nums,
        }
        group_id = str(event.group_id)
        try:
            scheduler.add_job(func=self.battle_handle_timer,
                            args=[group_id],
                            trigger='interval',
                            seconds=60,
                            id=self._current_player["battles"][str(event.group_id)]["scheduler_id"]+ '_appl')
            logger.info(f'{self._current_player["battles"][str(event.group_id)]["scheduler_id"]}任务生成')
        except:
            logger.info(f'定时任务生成失败！')

        msg = (MessageSegment.at(at_id)
               + MessageSegment.text(f'\n{a_nickname}向您申请幻卡决斗'
                                     f'请在60秒内输入“同意决斗”，或“拒绝决斗”，超时将自动帮您拒绝。'))
        return msg

    def accetp_battle(self, bot: Bot, event:GroupMessageEvent) -> str:
        battle_info = self._current_player["battles"][str(event.group_id)]
        try:
            scheduler.remove_job(battle_info["scheduler_id"]+ '_appl')
            logger.info(f"幻卡对决申请已结束")
        except:
            logger.info(f'幻卡申请定时删除错误')
        try:
            scheduler.add_job(func=self.battle_stop_timer,
                            args=[bot, str(event.group_id)],
                            trigger='interval',
                            seconds=300,
                            id=battle_info["scheduler_id"] + '_play')
            logger.info(f'{battle_info["scheduler_id"]}任务生成')
        except:
            logger.info(f"定时任务生成失败！")
        name = []
        abid = []
        for ab in battle_info:
            if isinstance(battle_info[ab],dict):
                name.append(battle_info[ab]["nickname"])
                abid.append(battle_info[ab]["id"])
        start_player = random.choice([0,1])
        
        battle_info["turn_id"] = abid[start_player]
        msg = f'{name[0]}与{name[1]}的对决开始，限时5分钟，由{name[start_player]}开始！\n初始化棋盘\n0001000'
        return msg

    def check_battle(self, event: GroupMessageEvent) -> int:
        battles_info = self._current_player["battles"]
        if str(event.group_id) in battles_info:
            if str(event.user_id) in battles_info[str(event.group_id)]:
                return 0
            else:
                return 1
        else:
            return 2

    def refuse_battle(self, event: GroupMessageEvent) -> str:
        match self.check_battle(event):
            case 0:
                scheduler.remove_job(self._current_player["battles"][str(event.group_id)]["scheduler_id"]+ '_appl')
                return f'已成功拒绝'
            case 1:
                return f'您不在对决申请之中'
            case 2:
                return f'当前没有对决正在被申请'

    def battle_chose(self, event: GroupMessageEvent, chose) -> str:
        match self.check_battle(event):
            case 1:
                return f'您不在对决之中'
            case 2:
                return f'当前没有对决正在进行'
        battle_info = self._current_player["battles"][str(event.group_id)]
        if event.user_id != battle_info["turn_id"]:
            return f'不在你的回合！'
        power = battle_info[str(event.user_id)]["power"]
        abpower = []
        now_pg = battle_info["playground"]
        if chose == "幻卡出牌":
            chose_step = 1
        elif chose == "幻卡梭哈":
            chose_step = 2
        for ab in battle_info:
            if isinstance(battle_info[ab],dict):
                abpower.append(battle_info[ab]["power"])
                if battle_info[ab]["id"] != event.user_id:
                    pos_id = battle_info[ab]["id"]
        rate = power/(chose_step*chose_step)/(abpower[0]+abpower[1])
        ans = random.random()
        if ans < rate:
            msg = f"\n成功，向前推进{chose_step}格！\n"
            if battle_info[str(event.user_id)]["side"] == 0:
                now_pg = now_pg<<chose_step
                if now_pg > 0b1000000:
                    msg = self.battle_win(event, pos_id)
                else:
                    msg += str(bin(now_pg))[2:].zfill(7)
            elif battle_info[str(event.user_id)]["side"] == 1:
                now_pg = now_pg>>chose_step
                if now_pg < 0b0000001:
                    msg = self.battle_win(event, pos_id)
                else:
                    msg += str(bin(now_pg))[2:].zfill(7)
        else:
            msg = f"\n失败了，没有推进\n{self.battle_win(event, pos_id)}"
        battle_info["playground"] = now_pg
        battle_info["turn_id"] = pos_id
        return msg
    
    def battle_win(self, event: GroupMessageEvent, pos_id: int):
        battle_info = self._current_player["battles"][str(event.group_id)]

        try:
            scheduler.remove_job(battle_info["scheduler_id"] + '_play')
            logger.info(f"幻卡对决已结束")
        except:
            logger.info(f'幻卡定时删除错误')
        self.change_gold_self(str(event.group_id), str(event.user_id), battle_info["nums"])
        self.change_gold_self(str(event.group_id), str(pos_id), battle_info["nums"]*-1)
        self._player_data[str(event.group_id)][str(event.user_id)]["win_count"]+=1
        self._player_data[str(event.group_id)][str(pos_id)]["lose_count"]+=1
        self.save()
        del self._current_player["battles"][str(event.group_id)]
        return f'{battle_info[str(event.user_id)]["nickname"]}胜利，奖励已结算！'

    async def rank(self, msg: str, group_id: int) -> str:
        """
        获取排行榜
        :param msg: 排行榜类型
        :param group_id: 群号
        """
        if msg in ["排行榜","金碟币排行"]:
            return await rank(self._player_data, group_id, "gold_rank")
        if msg == "仙人彩排行":
            return await rank(self._player_data, group_id, "cactpot_rec")
        if msg in ["战力排行","幻卡战力排行"]:
            return await rank(self._player_data, group_id, "cards_power")
        if msg == "赚币排行":
            return await rank(self._player_data, group_id, "make_gold")
        if msg == "花币排行":
            return await rank(self._player_data, group_id, "lose_gold")
        if msg == "签到排行":
            return await rank(self._player_data, group_id, "sign_days")

    def _change_gold(self, event: GroupMessageEvent, raw_cmd: str, id_give: list[int], nums: int=50):
        """
        转账 | SU命令
        """
        self._init_player_data(event)
        count = len(id_give)
        if raw_cmd == '_change_gold':
            for uid in id_give:
                self._player_data[str(event.group_id)][str(uid)]["gold"] += nums
            self.save()
            return 'SU命令完成！'
        else:
            if nums <= 0:
                return f'你好歹V 1块钱吧'
            elif self._player_data[str(event.group_id)][str(event.user_id)]["gold"] - count*nums < 0:
                    return f'余额不足，V不了了'
            else:
                for uid in id_give:
                    if not event.user_id == uid:
                        self.change_gold_self(event.group_id, uid, nums)
                self.change_gold_self(event.group_id, event.user_id, count*nums*-1)
                self.save()
                return f'已到账，还剩{self._player_data[str(event.group_id)][str(event.user_id)]["gold"]}金碟币'

    def reload_data(self):
        self.__init__()
        self.save()

    def reset_sign(self):
        """
        重置签到
        """
        for group in self._player_data.keys():
            for user_id in self._player_data[group].keys():
                self._player_data[group][user_id]["is_sign"] = False
        self.save()

    def save(self):
        """
        保存数据
        """
        with open(self.file, "w", encoding="utf8") as f:
            json.dump(self._player_data, f, ensure_ascii=False, indent=4)
        logger.info(f"--数据已保存--")

    def beg(self,event: GroupMessageEvent):
        """
        领低保
        """
        self._init_player_data(event)
        beg_times = self._player_data[str(event.group_id)][str(event.user_id)]["beg_times"]
        gold = self._player_data[str(event.group_id)][str(event.user_id)]["gold"]
        if beg_times >= max_beg_times:
            return f"你已经领过{max_beg_times}次低保了，明天再来吧！"
        if gold<500:
            self.change_gold_self(event.group_id, event.user_id, 500)
            self._player_data[str(event.group_id)][str(event.user_id)]["beg_times"] += 1
            self.save()
            return f"低保领取成功，省着花吧，今天还剩{max_beg_times - beg_times - 1}次低保！"
        elif gold<100000:
            return f"你还有{gold}金碟币，领什么低保"
        else:
            return f"存款{gold}的狗大户，来骗低保是么？"

    def _init_player_data(self, event: GroupMessageEvent):
        """
        初始化用户数据
        :param event: event
        """
        user_id = str(event.user_id)
        group_id = str(event.group_id)
        nickname = event.sender.card if event.sender.card else event.sender.nickname
        if group_id not in self._player_data.keys():
            self._player_data[group_id] = {}
        if user_id not in self._player_data[group_id].keys():
            self._player_data[group_id][user_id] = user_data_type
            self._player_data[group_id][user_id]["user_id"] = user_id
            self._player_data[group_id][user_id]["group_id"] = group_id
            self._player_data[group_id][user_id]["nickname"] = nickname
        if not self._player_data[str(event.group_id)][str(event.user_id)]["nickname"] == nickname:
            self._player_data[str(event.group_id)][str(event.user_id)]["nickname"] = nickname
            logger.info(f"{event.group_id}群:qq{event.user_id}已改名为:{nickname}")
            self.save()

#借贷
    def del_loan_timer(self, group_id, at_id):
        """
        删除贷款触发定时器
        """
        try:
            scheduler.remove_job(self._current_player[group_id][at_id]["scheduler_id"])
            logger.info(f"贷款申请已超时")
        except:
            logger.info(f"贷款定时删除错误")
        if at_id in self._current_player[group_id]:
            del self._current_player[group_id][at_id]

    def loan_in(self, event: GroupMessageEvent, nums: str, at_id: str):
        if str(event.group_id) in self._current_player:
            if str(at_id) in self._current_player[str(event.group_id)]:
                return f"该用户正在被申请贷款！"
        else:
            self._current_player[str(event.group_id)] = {}
        self._current_player[str(event.group_id)] = {
            str(at_id): {"loan_in": str(event.user_id),
                         "loan_in_nickname": self._player_data[str(event.group_id)][str(event.user_id)]["nickname"],
                         "loan_out": str(at_id),
                         "loan_out_nickname": self._player_data[str(event.group_id)][str(at_id)]["nickname"],
                         "nums": nums,
                         "scheduler_id": str(event.group_id)+str(at_id), }
            }
        try:
            scheduler.add_job(func=self.del_loan_timer,
                            args=(str(event.group_id), str(at_id)),
                            trigger='interval',
                            seconds=60,
                            id=self._current_player[str(event.group_id)][str(at_id)]["scheduler_id"])
            logger.info(f'{self._current_player[str(event.group_id)][str(at_id)]["scheduler_id"]}任务生成')
        except:
            logger.info(f"定时任务生成失败！")
        msg = (MessageSegment.at(at_id)
               + MessageSegment.text(f'\n{self._player_data[str(event.group_id)][str(event.user_id)]["nickname"]}'
                                     f'向您借贷{nums}金碟币，请在60秒内输入“同意贷款”，或“拒绝贷款”，超时将自动帮您拒绝。'))
        return msg

    def accept_loan(self, event: GroupMessageEvent):

        if str(event.user_id) in self._current_player[str(event.group_id)]:
            loan_in_id = self._current_player[str(event.group_id)][str(event.user_id)]["loan_in"]
            nums = int(self._current_player[str(event.group_id)][str(event.user_id)]["nums"])
            self.del_loan_timer(str(event.group_id), str(event.user_id))

            player_datas = self._player_data[str(event.group_id)]

            player_datas[str(event.user_id)]["gold"] -= nums
            player_datas[loan_in_id]["gold"] += nums
            if not loan_in_id in player_datas[str(event.user_id)]["loan_out"]:
                player_datas[str(event.user_id)]["loan_out"][loan_in_id] = nums
            else:
                player_datas[str(event.user_id)]["loan_out"][loan_in_id] += nums
            if not str(event.user_id) in player_datas[loan_in_id]["loan_in"]:
                player_datas[loan_in_id]["loan_in"][str(event.user_id)] = nums
            else:
                player_datas[loan_in_id]["loan_in"][str(event.user_id)] += nums
            self.save()
            nickname = player_datas[loan_in_id]["nickname"]
            return f"您已成功向{nickname}借贷{nums}金碟币"
        else:
            return f'您没有被申请借贷！'

    def refuse_loan(self, event: GroupMessageEvent):
        if str(event.group_id) in self._current_player and str(event.user_id) in self._current_player[str(event.group_id)]:
            self.del_loan_timer(str(event.group_id), str(event.user_id))
            return f'已成功拒绝！'
        return f'您没有被申请借贷！'

    def get_user_data(self, event: GroupMessageEvent, search_Uid: str="") -> Dict[str, Union[str, int]]:
        """
        获取用户数据
        :param event:
        :return:
        """
        self._init_player_data(event)
        if search_Uid == "":
            return self._player_data[str(event.group_id)][str(event.user_id)]
        elif search_Uid in self._player_data[str(event.group_id)]:
            return self._player_data[str(event.group_id)][search_Uid]
        else:
            return "Null"

    def reset_gold(self):
        """
        重置签到
        """
        for group in self._player_data.keys():
            for user_id in self._player_data[group].keys():
                self._player_data[group][user_id]["is_sign"] = False
                self._player_data[group][user_id]["beg_times"] = 0
        self.save()

golden_manager = GoldenManager()
