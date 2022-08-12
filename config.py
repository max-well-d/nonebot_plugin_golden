from pydantic import BaseModel, Extra
from pathlib import Path


class Config(BaseModel, extra=Extra.ignore):
	sign_gold = {6:10000,7:36,8:720,9:60,
				10:80,11:252,12:108,13:72,
				14:540,15:180,16:72,17:1800,
				18:119,19:36,20:306,21:1080,
				22:144,23:1800,24:3600}

	cat_gold = [0,166,888,1666,2888,6666,66666,3000000]
	cat_text =[
				["啥也没有，","空空如也，"],
				["运气平平，","运气一般，"],
	    		["运气稍好，","运气还行，"],
	    		["运气不差，","运气不错，"],
	    		["运气极佳，","运气很好，"],
	    		["人品爆发，","运气爆棚，"],
	    		["万中无一，","运气逆天，"],
	    		["用中500万的运气换取","拿30年寿命换取"]]
	golden_path: Path = Path()
	pack_type = [0,100,300,500,1500]
	pack_name = ['' ,'铜包', '银包', '金包', '白金包']
	cards_power = [1,5,10,50,100,500,10000]

	__plugin_usage__ = """金碟模拟器帮助：
	    仙人微彩(金碟签到，微彩)：每日签到，随机获得金碟币，11点刷新。
	    仙人彩(抽奖，仙人彩抽奖)：随机抽奖，大概率会赚？
	    仙人彩十连(十连仙人彩, 十连抽奖)：十连仙人彩，很有可能赚？
	    仙人彩百连(百连仙人彩, 百连抽奖)：百连仙人彩，很有可能赚？
	    仙人彩记录(仙人彩数据，仙人彩战绩)：仙人彩的数据，欧皇和非酋的记录
	    转账(v你，转账给)?[at对象，可为多个目标][金碟币数量]：给一个或多个人转账
	    买幻卡包(买包，买幻卡)?[卡包种类]?[购买个数]：购买幻卡包，有1：铜包(100金碟币)、2：银包(300金碟币)、3：金包(500金碟币)、4：白金包(1500金碟币)四种
	    开幻卡包(开包，开幻卡)?[卡包种类]?[开启个数]：开启幻卡包，随机获得1~5星幻卡
	    开卡记录(开包记录,幻卡记录)：显示已开的卡包数和获得的幻卡张数
	    金碟帮助(/help)：显示帮助
	    我的金碟币(金碟币)：显示剩余金碟币数量
	    生涯数据(我的数据，我的战绩)：显示金碟币使用获得，幻卡战力，幻卡对战数据，仙人彩购买情况
	    排行榜(金碟币排行，仙人彩排行，[幻卡战力排行，战力排行]，赚币排行，花币排行)：各种排行榜"""