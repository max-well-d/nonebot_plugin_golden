from .data_source import golden_manager
from .utils import is_number, get_message_at
from .config import Config
from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import (
    Bot,
    GROUP,
    GroupMessageEvent,
    Message,
    MessageSegment,
    helpers 
)
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from nonebot.params import Depends, CommandArg, State, Arg, ArgPlainText
from nonebot.typing import T_State
from typing import List

__zx_plugin_name__ = "金碟模拟器"

__plugin_usage__ = Config.__plugin_usage__
cat_gold = Config.__cat_gold__
scheduler = require("nonebot_plugin_apscheduler").scheduler

sign = on_command("仙人微彩", aliases={"金碟签到", "微彩"}, permission=GROUP, priority=5, block=True)

#battle = on_command("幻卡对决", aliases={"比赛", "幻卡比赛"}, permission=GROUP, priority=5, block=True)
###贷款命令
loan_in = on_command("借贷款", aliases={"借贷"}, permission=GROUP, priority=5, block=True)
accept = on_command("同意贷款", aliases={"同意借贷"}, permission=GROUP, priority=5, block=True)
refuse = on_command("拒绝贷款", aliases={"拒绝借贷"}, permission=GROUP, priority=5, block=True)
my_loan = on_command("我的贷款", aliases={"我的债务", "我的借贷"}, permission=GROUP, priority=5, block=True)
###仙人彩命令
cactpot = on_command("仙人彩", aliases={"仙人彩抽奖", "抽奖"}, permission=GROUP, priority=5, block=True)
cactpot_all = on_command("仙人彩梭哈", aliases={"梭哈仙人彩"}, permission=GROUP, priority=5, block=True)
cactpot_hun = on_command("仙人彩百连", aliases={"百连仙人彩", "百连抽奖"}, permission=GROUP, priority=5, block=True)
cactpot_rate = on_command("仙人彩概率",aliases={"仙人彩记录","仙人彩战绩"},permission=GROUP, priority=5, block=True)
cactpot_ten = on_command("仙人彩十连", aliases={"十连仙人彩", "十连抽奖"}, permission=GROUP, priority=5, block=True)
###幻卡命令
get_cards = on_command("买幻卡包", aliases={"买包","买幻卡"}, permission=GROUP, priority=5, block=True)
open_cards = on_command("开包", aliases={"开幻卡","开幻卡包"}, permission=GROUP, priority=5, block=True)
### SU命令
reload_data = on_command("_reload_data", permission=SUPERUSER, priority=5, block=True)
change_gold = on_command("_change_gold", permission=SUPERUSER, priority=5, block=True)
###杂项命令
beg_plz = on_command("低保", aliases={"领低保"},permission=GROUP, priority=5, block=True) 
vni50 = on_command("转账", aliases={"v你", "转账给"}, permission=GROUP, priority=5, block=True)
game_help = on_command("金碟帮助", aliases={"/help", "help"}, permission=GROUP, priority=5, block=True)
###数据命令
card_rate = on_command("开卡记录", aliases={"开包记录","幻卡记录"}, permission=GROUP, priority=5, block=True)
my_gold = on_command("我的金碟币", aliases={"金碟币"}, permission=GROUP, priority=5, block=True)
record = on_command("生涯数据", aliases={"我的数据","我的记录"}, permission=GROUP, priority=5, block=True)
golden_rank = on_command("排行榜",aliases={"金碟币排行", "仙人彩排行", "战力排行","幻卡战力排行", "赚币排行", "花币排行","签到排行"},permission=GROUP,priority=5,block=True,)

@reload_data.handle()
async def _():
    golden_manager.reload_data()
    await reload_data.send('重载数据完成！')

@game_help.handle()
async def _():
    await game_help.send(__plugin_usage__)

@sign.handle()
async def _(event: GroupMessageEvent):
    msg, gold = golden_manager.sign(event)
    await sign.send(msg, at_sender=True)
    if gold != -1:
        logger.info(f"USER {event.user_id} | GROUP {event.group_id} 获取 {gold} 金碟币")


#买卡包-------------
@get_cards.handle()
async def _(event: GroupMessageEvent, state: T_State = State(),arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        msg = msg.split()
        if len(msg) == 2:
            if is_number(msg[0]) and msg[0] > "0" and msg[0] <= "4":
                buy_card_type = int(msg[0])
                state["buy_card_type"] = buy_card_type
                if is_number(msg[1]) and msg[1] > "0":
                    purchase_num = int(msg[1])
                    state["purchase_num"] = purchase_num

                    if buy_card_type and purchase_num:
                        msg, gold = golden_manager.get_cards(event, buy_card_type, purchase_num)
                        await get_cards.finish(msg, at_sender=True)

@get_cards.got("buy_card_type_raw", prompt="要买哪个等级的卡包?1.铜包(100) 2.银包(300) 3.金包(500) 4.白金包(1500)")
async def _(
    event: GroupMessageEvent, 
    state: T_State, 
    buy_card_type_raw: Message = Arg(), 
    buy_card_type: str = ArgPlainText("buy_card_type_raw")):

    if buy_card_type == "取消":
        await get_cards.finish("已取消", at_sender=True)
    if not is_number(buy_card_type):
        await get_cards.reject("请输入1到4的数字!", at_sender=True)
    buy_card_type = int(buy_card_type)
    if buy_card_type < 1 or buy_card_type > 4:
        await get_cards.reject("卡包只能在1到4中选择!", at_sender=True)
    state["buy_card_type"] = buy_card_type

@get_cards.got("purchase_num_raw", prompt="要买多少包?")
async def _(
    event: GroupMessageEvent, 
    state: T_State, 
    purchase_num_raw: Message = Arg(), 
    purchase_num: str = ArgPlainText("purchase_num_raw")):

    if purchase_num == "取消":
        await get_cards.finish("已取消", at_sender=True)
    if not is_number(purchase_num):
        await get_cards.reject("请输入大于0的数字!", at_sender=True)
    purchase_num = int(purchase_num)
    if purchase_num < 1:
        await get_cards.reject("你还想卖卡包给我?想得美!", at_sender=True)
    state["purchase_num"] = purchase_num
    msg, gold = golden_manager.get_cards(event, int(state["buy_card_type"]), int(state["purchase_num"]))
    await get_cards.send(msg, at_sender=True)



#开卡包-------------
@open_cards.handle()
async def _(event: GroupMessageEvent, state: T_State = State(),arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        msg = msg.split()
        if len(msg) == 2:
            if is_number(msg[0]) and msg[0] > "0" and msg[0] <= "4":
                open_card_type = msg[0]
                state["open_card_type"] = open_card_type
                if is_number(msg[1]) and msg[1] > "0":
                    open_num = msg[1]
                    state["open_num"] = open_num
                    if open_card_type and open_num:
                        msg = golden_manager.open_cards(event, int(open_card_type), int(open_num))
                        await open_cards.finish(msg, at_sender=True)


@open_cards.got("open_card_type_raw", prompt="要开哪个等级的卡包?1.铜包 2.银包 3.金包 4.白金包")
async def _(
    event: GroupMessageEvent, 
    state: T_State, 
    open_card_type_raw: Message = Arg(), 
    open_card_type: str = ArgPlainText("open_card_type_raw")):

    if open_card_type == "取消":
        await open_cards.finish("已取消", at_sender=True)
    if not is_number(open_card_type):
        await open_cards.reject("请输入1到4的数字!", at_sender=True)
    open_card_type = int(open_card_type)
    if open_card_type < 1 or open_card_type > 4:
        await golden_manager.reject("卡包只能在1到4中选择!", at_sender=True)
    state["open_card_type"] = open_card_type


@open_cards.got("open_num_raw", prompt="要开多少包?")
async def _(
    event: GroupMessageEvent, 
    state: T_State, 
    open_num_raw: Message = Arg(), 
    open_num: str = ArgPlainText("open_num_raw")):

    if open_num == "取消":
        await open_cards.finish("已取消", at_sender=True)
    if not is_number(open_num):
        await open_cards.reject("请输入大于0的数字!", at_sender=True)
    open_num = int(open_num)
    if open_num < 1:
        await golden_manager.reject("你还想卖卡包给我?想得美!", at_sender=True)
    state["open_num"] = open_num
    msg = golden_manager.open_cards(event,int(state["open_card_type"]), int(state["open_num"]))
    await open_cards.send(msg, at_sender=True)


@my_gold.handle()
async def _(event: GroupMessageEvent):
    gold = golden_manager.get_user_data(event)["gold"]
    await my_gold.send(f"你还有 {gold} 枚金碟币", at_sender=True)


@card_rate.handle()
async def _(event: GroupMessageEvent):
    card = golden_manager.get_user_data(event)["cards_opend"]
    pack = golden_manager.get_user_data(event)["pack_opend"]
    back_text = f'\n铜包{pack[1]}包\n银包{pack[2]}包\n金包{pack[3]}包\n白金包{pack[4]}包\n'
    if card[5] > 0:
        back_text += (f'开出：\n' +
                      f'☆：{card[0]}\n' +
                      f'☆☆：{card[1]}\n' +
                      f'☆☆☆：{card[2]}\n' +
                      f'☆☆☆☆：{card[3]}\n' +
                      f'☆☆☆☆☆：{card[4]}\n' +
                      f'隐藏究极卡！★：{card[5]}')
    else:
        back_text += (f'开出：\n' +
                      f'☆：{card[0]}\n' +
                      f'☆☆：{card[1]}\n' +
                      f'☆☆☆：{card[2]}\n' +
                      f'☆☆☆☆：{card[3]}\n' +
                      f'☆☆☆☆☆：{card[4]}')
    await card_rate.send(back_text, at_sender=True)


@golden_rank.handle()
async def _(event: GroupMessageEvent, state: T_State = State()):
    msg = await golden_manager.rank(state["_prefix"]["raw_command"], event.group_id)
    await golden_rank.send(msg)


@record.handle()
async def _(event: GroupMessageEvent):
    user = golden_manager.get_user_data(event)
    ctp_rec = user["cactpot_rec"]
    await record.send(
        f'\n金碟游乐场记录\n'
        f'幻卡战力  ：{user["cards_power"]}\n'
        f'签到天数  ：{user["sign_days"]}\n'
        f'赚取金碟币：{user["make_gold"]}\n'
        f'花费金碟币：{user["lose_gold"]}',
        at_sender=True,
    )

@cactpot_rate.handle()
async def _(event: GroupMessageEvent):
    user = golden_manager.get_user_data(event)
    ctp_rec = user["cactpot_rec"]
    await cactpot_rate.send(
        f'\n仙人彩记录:\n'
        f'{cat_gold[0]}金碟币            ：{ctp_rec[0]}\n'
        f'{cat_gold[1]}金碟币          ：{ctp_rec[1]}\n'
        f'{cat_gold[2]}金碟币        ：{ctp_rec[2]}\n'
        f'{cat_gold[3]}金碟币        ：{ctp_rec[3]}\n'
        f'{cat_gold[4]}金碟币      ：{ctp_rec[4]}\n'
        f'{cat_gold[5]}金碟币      ：{ctp_rec[5]}\n'
        f'{cat_gold[6]}金碟币    ：{ctp_rec[6]}\n'
        f'{cat_gold[7]}0金碟币：{ctp_rec[7]}',
        at_sender=True,
    )


@cactpot.handle()
async def _(event: GroupMessageEvent):
    msg, gold = golden_manager.cactpot(event, 1, False)
    await cactpot.send(msg, at_sender=True)
    if gold != -1:
        logger.info(f"USER {event.user_id} | GROUP {event.group_id} 获取 {gold} 金碟币")


@cactpot_ten.handle()
async def _(event: GroupMessageEvent):
    msg, gold = golden_manager.cactpot(event, 10, False)
    await cactpot_ten.send(msg, at_sender=True)
    if gold != -1:
        logger.info(f"USER {event.user_id} | GROUP {event.group_id} 获取 {gold} 金碟币")

@cactpot_hun.handle()
async def _(event: GroupMessageEvent):
    msg, gold = golden_manager.cactpot(event, 100, False)
    await cactpot_hun.send(msg, at_sender=True)
    if gold != -1:
        logger.info(f"USER {event.user_id} | GROUP {event.group_id} 获取 {gold} 金碟币")

@cactpot_all.handle(parameterless=[helpers.Cooldown(cooldown=10,prompt="正在10秒CD中")])
async def _(event: GroupMessageEvent):
    msg, gold = golden_manager.cactpot(event, 100000, True)
    await cactpot_all.send(msg, at_sender=True)
    if gold != -1:
        logger.info(f"USER {event.user_id} | GROUP {event.group_id} 获取 {gold} 金碟币")


@vni50.handle()
@change_gold.handle()
async def _(event: GroupMessageEvent, state: T_State = State(), arg: Message = CommandArg()):
    at_id = get_message_at(event.json())
    if not at_id:
        await vni50.finish("没有@收款人，请@想要转账的人，可以为复数", at_sender=True)
    raw_cmd = state["_prefix"]["raw_command"]
    nums = arg.extract_plain_text()
    if is_number(nums):
        msg = golden_manager._change_gold(event, raw_cmd, at_id, int(nums))
    else:
        msg = golden_manager._change_gold(event, raw_cmd, at_id)
    await vni50.send(msg, at_sender=True)

@loan_in.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State(), arg: Message = CommandArg()):
    debate = golden_manager.get_user_data(event)["loan_in"]
    if len(debate) >= 5:
        await loan_in.finish(f"你已经向5个人借贷了，先把钱还清吧！", at_sender=True)
    nums = arg.extract_plain_text()
    at_id = get_message_at(event.json())
    if not at_id or len(at_id) > 1:
        await loan_in.finish("没有@借款人或者@了多个人，请@想要借贷的人", at_sender=True)
    elif at_id[0] == event.user_id:
        await loan_in.finish("不能问自己贷款的啦！")
    loan_user = golden_manager.get_user_data(event, str(at_id[0]))
    if loan_user == "Null":
        await loan_in.finish("该用户没有在金碟游乐场游玩过")
    else:
        state["loan_user_gold"] = loan_user["gold"]
    state["at"] = at_id[0]
    if nums and is_number(nums) and int(nums) > 0:
        if state["at"]:
            msg = golden_manager.loan_in(event, nums, state["at"])
            await loan_in.finish(msg)

@loan_in.got("nums", prompt="你要借多少贷款?")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State, nums_ano: str = ArgPlainText("nums")):
    nums = nums_ano
    if nums:
        nums = nums_ano
    at = state["at"]
    loan_user_gold = state["loan_user_gold"]
    if nums == "取消":
        await loan_in.finish("已取消操作", at_sender=True)
    if is_number(nums):
        if int(nums) <= 0:
            await loan_in.reject("做个人吧！", at_sender=True)
        else:
            if int(loan_user_gold) < int(nums):
                await loan_in.reject("你借太多啦！")
            else:
                msg = golden_manager.loan_in(event, nums, at)
                await loan_in.send(msg)
    else:
        await loan_in.reject("请输入数字！", at_sender=True)

@accept.handle()
async def _(event: GroupMessageEvent):
    msg = golden_manager.accept(event)
    await accept.send(msg, at_sender=True)

@refuse.handle()
async def _(event: GroupMessageEvent):
    msg = golden_manager.refuse(event)
    await refuse.send(msg, at_sender=True)

@my_loan.handle()
async def _(event: GroupMessageEvent):
    data = golden_manager.get_user_data(event)
    loan_in = data["loan_in"]
    print (type(loan_in))
    loan_out = data["loan_out"]
    msg = f"\n债务：\n"
    if not loan_in:
        msg += f"无\n"
    else:
        for uid in loan_in.keys():
            msg += golden_manager.get_user_data(event, uid)["nickname"]
            msg += f':{loan_in[uid]}\n'
    msg += f"借贷：\n"
    if not loan_out:
        msg += f"无"
    else:
        for uid in loan_out.keys():
            msg += golden_manager.get_user_data(event, uid)["nickname"]
            msg += f'：{loan_out[uid]}\n'
        msg += f'将抽取所有赚到的金碟币的10%来偿还债务'
    await my_loan.send(msg, at_sender=True)

@beg_plz.handle()
async def _(event: GroupMessageEvent):
    msg = golden_manager.beg(event)
    await beg_plz.send(msg, at_sender=True)

# 重置每日签到
@scheduler.scheduled_job(
    "cron",
    hour=23,
    minute=0,
)
async def _():
    golden_manager.reset_gold()
    logger.info("每日仙人微彩次数重置成功...")
