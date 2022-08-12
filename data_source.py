from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment, Bot
from typing import Optional, Tuple, Union, List, Dict
from datetime import datetime
from nonebot.log import logger
from pathlib import Path
import numpy as np
import nonebot
import asyncio
import random
import time
import os
from .config import Config

try:
    import ujson as json
except ModuleNotFoundError:
    import json


global_config = nonebot.get_driver().config
godden_config = Config.parse_obj(global_config.dict())
golden_confg = Config.parse_obj(nonebot.get_driver().config.dict())
cards_power = godden_config.cards_power
cat_gold = godden_config.cat_gold
cat_text = godden_config.cat_text
golden_path = godden_config.golden_path
pack_name = godden_config.pack_name
pack_type = godden_config.pack_type
sign_gold = godden_config.sign_gold


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
                tmp_sum+=tmp[x][s]*cat_gold[s]
            tmp[x] = tmp_sum
        all_user_data = tmp
    elif type_ == "cards_power":
        rank_name = "\t幻卡战斗力排行榜\n"
        all_user_data = [player_data[group_id][x]["cards_power"] for x in all_user]
    elif type_ == "make_gold":
        rank_name = "\t赢取的金碟币排行榜\n"
        all_user_data = [player_data[group_id][x]["make_gold"] for x in all_user]
    else:
        rank_name = "\t花掉的金碟币排行榜\n"
        all_user_data = [player_data[group_id][x]["lose_gold"] for x in all_user]
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
        self._current_player = {}
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

    def sign(self, event: GroupMessageEvent) -> Tuple[str, int]:
        """
        签到
        :param event: event
        """
        self._init_player_data(event)
        if self._player_data[str(event.group_id)][str(event.user_id)]["is_sign"]:
            return "你已经刮过仙人微彩了！\n", -1
        backtext = "\n"
        gold = 0
        for ele in range(3):
            gain_num = 0
            num_tmps = random.sample(range(1, 10),3)
            for num_tmp in num_tmps:
                backtext+=str(num_tmp)+'  '
                gain_num+=num_tmp
            gold += sign_gold[gain_num]
            backtext+=f',获得{sign_gold[gain_num]}金碟币\n'
        self._player_data[str(event.group_id)][str(event.user_id)]["sign_days"] += 1
        self._player_data[str(event.group_id)][str(event.user_id)]["gold"] += gold
        self._player_data[str(event.group_id)][str(event.user_id)]["make_gold"] += gold
        self._player_data[str(event.group_id)][str(event.user_id)]["is_sign"] = True
        self.save()
        return (
            backtext + f"共获得了 {gold} 金碟币",
            gold,
        )
    def cactpot(self, event: GroupMessageEvent, times: int, use_all: bool) ->Tuple[str,int]:
        """
        仙人彩
        """
        self._init_player_data(event)
        now_gold = self._player_data[str(event.group_id)][str(event.user_id)]["gold"]
        backtext = f'\n'
        if now_gold - times*10 < 0:
            if not use_all or now_gold < 10:
                return (f'金碟币不足！',-1)
            else :
                backtext +=f'！！有位勇士开始梭哈！！\n'
                times = int(now_gold/10)
        gold = 0
        gold_tab = [0,0,0,0,0,0,0,0]
        num_tmps = np.random.randn(times)
        for num_tmp in num_tmps :
            if num_tmp>5:
                gold_tmp = 7
            elif num_tmp>4:
                gold_tmp = 6
            elif num_tmp>3.6:
                gold_tmp = 5
            elif num_tmp>3.35:
                gold_tmp = 4
            elif num_tmp>3.1:
                gold_tmp = 3
            elif num_tmp>2.75:
                gold_tmp = 2
            elif num_tmp>2.4:
                gold_tmp = 1
            else:
                gold_tmp= 0
            text = cat_text[gold_tmp]
            self._player_data[str(event.group_id)][str(event.user_id)]["cactpot_rec"][gold_tmp]+=1
            gold_num = cat_gold[gold_tmp]

            gold_tab[gold_tmp]+=1
            if times <= 10:
                backtext += random.choice(text) + f"获得了 {gold_num} 金碟币\n"
            elif gold_num != 0 and times <= 100:
                backtext += random.choice(text) + f"获得了 {gold_num} 金碟币\n"
            gold+=gold_num-10
        if times > 100 and use_all:
            backtext +=(
                f'0　　　　　：　{gold_tab[0]}\n'+
                f'166　　　　：　{gold_tab[1]}\n'+
                f'888　　　　：　{gold_tab[2]}\n'+
                f'1666　 　　：　{gold_tab[3]}\n'+
                f'2888　　 　：　{gold_tab[4]}\n'+
                f'6666　　 　：　{gold_tab[5]}\n'+
                f'66666　  　：　{gold_tab[6]}\n'+
                f'3000000  　：　{gold_tab[7]}\n'
            )
        elif times > 10:
            backtext += f"一共没中奖{gold_tab[0]}次，安慰你一下\n"
        backtext += f'消耗了{times*10}金碟币'
        self._player_data[str(event.group_id)][str(event.user_id)]["gold"] += gold
        self._player_data[str(event.group_id)][str(event.user_id)]["make_gold"] += gold
        self._player_data[str(event.group_id)][str(event.user_id)]["lose_gold"] += times*10
        self.save()
        return (
            backtext,
            gold
        )

    def get_cards(self, event: GroupMessageEvent, buy_pack_type: int, nums: int) -> Tuple[str,int]:
        """
        买卡包
        """
        self._init_player_data(event)
        cost = pack_type[buy_pack_type]
        allcost = cost * nums
        gold = self._player_data[str(event.group_id)][str(event.user_id)]["gold"]
        if gold < allcost:
            print (allcost,'------',gold)
            return ("金碟币不足，无法购买",
            -1,
            )
        else:
            self._player_data[str(event.group_id)][str(event.user_id)]["gold"] -= allcost
            self._player_data[str(event.group_id)][str(event.user_id)]["lose_gold"] += allcost
            self._player_data[str(event.group_id)][str(event.user_id)]["pack_store"][buy_pack_type] += nums
            self.save()
            return (
                f"购买成功,消耗{allcost}金碟币,剩余{gold-allcost}金碟币",
                allcost
            )
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
        cards_open = [0,0,0,0,0,0]
        power = 0
        cardstmps = np.random.randn(nums)
        for ele in cardstmps:
            gain_cards = open_pack_type + ele
            if gain_cards >= 8:
                cards_open[5] += 1
                power+=cards_power[5]
            elif gain_cards >=6.5:
                cards_open[4] += 1
                power+=cards_power[4]
            elif gain_cards >=4:
                cards_open[3] += 1
                power+=cards_power[3]
            elif gain_cards >=3:
                cards_open[2] += 1
                power+=cards_power[2]
            elif gain_cards >=1:
                cards_open[1] += 1
                power+=cards_power[1]
            else:
                cards_open[0] += 1
                power+=cards_power[0]
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

    def _change_gold(self, event: GroupMessageEvent,raw_cmd: str, id_give: list[int], nums: int=50):
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
                    if event.user_id == uid:
                        pass
                    self._player_data[str(event.group_id)][str(uid)]["gold"] += nums
                    self._player_data[str(event.group_id)][str(uid)]["make_gold"] += nums

                self._player_data[str(event.group_id)][str(event.user_id)]["gold"] -= count*nums
                self._player_data[str(event.group_id)][str(event.user_id)]["lose_gold"] -= count*nums
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
            self._player_data[group_id][user_id] = {
                "user_id": user_id,
                "group_id": group_id,
                "nickname": nickname,
                "gold": 0,
                "sign_days": 0,
                "make_gold": 0,
                "lose_gold": 0,
                "cactpot_rec":[0,0,0,0,0,0,0,0],
                "win_count": 0,
                "lose_count": 0,
                "cards_opend": [0,0,0,0,0,0],
                "pack_store": [0,0,0,0,0],
                "pack_opend": [0,0,0,0,0],
                "cards_power": 0,
                "is_sign": False
            }

    def _end_data_handle(
        self,
        win_user_id: int,
        lose_user_id,
        group_id: int,
        gold: int,
    ):
        """
        结算数据处理保存
        :param win_user_id: 胜利玩家id
        :param lose_user_id: 失败玩家id
        :param group_id: 群聊
        :param gold: 赌注金币
        """
        win_user_id = str(win_user_id)
        lose_user_id = str(lose_user_id)
        group_id = str(group_id)
        self._player_data[group_id][win_user_id]["gold"] += gold
        self._player_data[group_id][win_user_id]["make_gold"] += gold
        self._player_data[group_id][win_user_id]["win_count"] += 1

        self._player_data[group_id][lose_user_id]["gold"] -= gold
        self._player_data[group_id][lose_user_id]["lose_gold"] += gold
        self._player_data[group_id][lose_user_id]["lose_count"] += 1

        self.save()

    def get_user_data(self, event: GroupMessageEvent) -> Dict[str, Union[str, int]]:
        """
        获取用户数据
        :param event:
        :return:
        """
        self._init_player_data(event)
        return self._player_data[str(event.group_id)][str(event.user_id)]

    def reset_gold(self):
        """
        重置签到
        """
        for group in self._player_data.keys():
            for user_id in self._player_data[group].keys():
                self._player_data[group][user_id]["is_sign"] = False
        self.save()

golden_manager = GoldenManager()