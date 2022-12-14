from pydantic import BaseModel, Extra
from pathlib import Path


class Config(BaseModel, extra=Extra.ignore):
	user_data_type = {
				"user_id": "",
				"group_id": "",
				"nickname": "",
				"gold": 0,
				"sign_days": 0,
				"make_gold": 0,
				"lose_gold": 0,
				"loan_out": {},
				"loan_in": {},
				"cactpot_rec":[0,0,0,0,0,0,0,0],
				"win_count": 0,
				"lose_count": 0,
				"cards_opend": [0,0,0,0,0,0],
				"pack_store": [0,0,0,0,0],
				"pack_opend": [0,0,0,0,0],
				"cards_power": 0,
				"beg_times":0,
				"is_sign": False
            }
	
	max_beg_times = 10

	sign_gold = {6: 10000, 7: 36, 8: 720, 9: 60,
				10: 80, 11: 252, 12: 108, 13: 72,
				14: 540, 15: 180, 16: 72, 17: 1800,
				18: 119, 19: 36, 20: 306, 21: 1080,
				22: 144, 23: 1800, 24: 3600}

	goal_gold = 100000
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
	cards_power = [1,5,10,50,100,500]

	__plugin_usage__ = """金碟模拟器帮助：
	    1、仙人微彩(金碟签到，微彩)：每日签到，随机获得金碟币，11点刷新
	    2、[十连,百连,梭哈]?仙人彩[十连,百连,梭哈]?(抽奖，仙人彩抽奖)：随机抽奖，大概率会赚？
	    3、领低保(低保)：领取低保，500金碟币，每天十次
	    4、仙人彩记录(仙人彩数据，仙人彩战绩)：仙人彩的数据，欧皇和非酋的记录
	    5、转账(v你，转账给)?[at对象，可为多个目标][金碟币数量]：给一个或多个人转账
	    6、借贷(贷款)?[at对象][金碟币数量]：向某个土豪借贷款，
	      将会在之后每次赚金蝶币时扣除10%(每个贷款人)作为偿还
	    7、同意借贷(同意贷款)|拒绝借贷(拒绝贷款)：同意贷款，展示你的仁慈或者无情拒绝
	    8、我的贷款(我的债务, 我的借贷)：看看你的借贷债务情况
		9、水晶争锋(推水晶，水晶比赛)?[at对象][赌注]：开启推水晶比赛
		10、同意决斗|拒绝决斗：同意或拒绝决斗
		11、稳步推进|全力推进：稳步推进前进1格，概率正常，全力推进前进2格，概率不稳定
	    12、买幻卡包(买包，买幻卡)?[卡包种类]?[购买个数]：购买幻卡包，有
	    	1：铜包(100金碟币)、
	    	2：银包(300金碟币)、
	    	3：金包(500金碟币)、
	    	4：白金包(1500金碟币)四种
	    11、开幻卡包(开包，开幻卡)?[卡包种类]?[开启个数]：开启幻卡包，随机获得1~5星幻卡
	    12、开卡记录(开包记录,幻卡记录)：显示已开的卡包数和获得的幻卡张数
	    13、金碟帮助(/help)：显示帮助
	    14、我的金碟币(金碟币)：显示剩余金碟币数量
	    15、生涯数据(我的数据，我的战绩)：显示金碟币使用获得，
	       幻卡战力，幻卡对战数据，仙人彩购买情况
	    16、排行榜(金碟币排行，仙人彩排行，[幻卡战力排行，战力排行]，赚币排行，花币排行，签到排行)：各种排行榜
		17、查房?[大区]?[服务器]+[房型|房区]+[房型|房号]：查空余房子
		18、占卜：FF14今日运势"""
	power_rank_price = [10000,30000,50000]

	__cat_gold__ = [0,10,166,666,2888,6666,66666,3000000]
	cat_gold = __cat_gold__

	main_dict = {
		"server":
		{
			"陆行鸟":{
				"红玉海":1167,
				"神意之地":1081,
				"拉诺西亚":1042,
				"幻影群岛":1044,
				"萌芽池":1060,
				"宇宙和音":1173,
				"沃仙曦染":1174,
				"晨曦王座":1175,
			},
			"莫古力":{
				"白银乡":1172,
				"白金幻象":1076,
				"神拳痕":1171,
				"潮风亭":1170,
				"旅人栈桥":1113,
				"拂晓之间":1121,
				"龙巢神殿":1166,
				"梦羽宝境":1176,
			},
			"猫小胖":{
				"紫水栈桥":1043,
				"延夏":1169,
				"静语庄园":1106,
				"摩杜纳":1045,
				"海猫茶屋":1177,
				"柔风海湾":1178,
				"琥珀原":1179,
			},
			"豆豆柴":{
				"水晶塔":1192,
				"银泪湖":1183,
				"太阳海岸":1180,
				"伊修加德":1186,
				"红茶川":1201,
				}
		},
		"area_requre":
		{
			"所有":-1,
			"海雾村":0,
			"薰衣草苗圃":1,
			"高脚孤丘":2,
			"白银乡":3,
			"穹顶皓天":4,
		},
		"area_read":
		{
			0:"海雾村",
			1:"薰衣草苗圃",
			2:"高脚孤丘",
			3:"白银乡",
			4:"穹顶皓天",
		},
		"size_requre":
		{
			"S/M/L":-1,
			"S":0,
			"M":1,
			"L":2,
		},
		"size_read":
		{
			0:"S",
			1:"M",
			2:"L",
		},
		"Slot":
		{
			"min_value":0,
			"max_value":23,
		},
		"RegionType_requre":
		{
			"个人":2,
			"部队":1,
		},
		"RegionType_read":
		{
			2:"个人购买",
			1:"部队购买",
		}
	}
	comments = [["高级公馆 优美景观 交通便利 设施完善 独特海景",
			"独家别墅 海景相伴 设施便利",
			"海滨小屋 配套完善",
			"顶级公馆 一线海景 城区环绕 设施齐备",
			"顶级别墅 临海美景 城区环绕 设施完善",
			"顶级公馆 一线海景 城区环绕 设施便利",
			"高级公馆 风景独特 ",
			"私家小屋 设施便利 独特海景",
			"私家小屋 设施便利",
			"巅峰住宅 设施便利 开阔广场",
			"私家小屋 独家海景",
			"私家小屋 独家海景",
			"独家小屋 设施便利",
			"高级公馆 独家风景 海城相映",
			"顶级别墅 山巅美景 海城相映 设施完善",
			"城区小屋 轻奢海景",
			"贵族小屋 海城相映 独家花园 设施便利",
			"城区小屋 独家海景 设施便利",
			"海滩小屋 顶级海景 沙滩相伴 设施便利",
			"海滩小屋 顶级海景 沙滩相伴 设施齐备",
			"海滩小屋 独家海景 沙滩相伴",
			"高贵小屋 海城相望 专属保安 设施齐备 社区广场 独家夕阳",
			"海景小屋 美景相伴",
			"城区小屋 设施齐备",
			"城区小屋 海城相映 设施便利",
			"城区小屋 轻奢海景 设施便利",
			"城区小屋 独家城景",
			"城区小屋 独家海景 专享菠萝",
			"贵族公馆 海城相映 独家庄园",
			"高级公馆 海城相望 专属保安 设施齐备 社区广场 独家夕阳",
			"优美景观 交通便利 设施完善 独特海景 夕阳美景 与您相伴",
			"独家别墅 海景相伴 设施便利 纵享夕阳",
			"配套完善",
			"顶级公馆 一线海景 城区环绕 设施齐备 极致夕阳 相伴相随",
			"顶级别墅 临海美景 城区环绕 设施完善 极致夕阳 相伴相随",
			"顶级公馆 一线海景 城区环绕 设施齐备 极致夕阳 相伴相随",
			"高级公馆 风景独特 纵享夕阳",
			"设施便利 海中落日",
			"私家小屋 设施便利",
			"巅峰住宅 设施便利 开阔广场",
			"私家小屋 独家海景 绝美夕阳",
			"私家小屋 独家海景 美丽夕阳",
			"独家小屋 设施便利 纵享夕阳",
			"高级公馆 独家风景 海城相映 绝美夕阳",
			"顶级别墅 山巅美景 海城相映 设施完善 极致夕阳",
			"城区小屋 轻奢海景 纵享夕阳",
			"贵族小屋 海城相映 独家花园 设施便利 纵享夕阳",
			"城区小屋 独家海景 设施便利 绝美夕阳",
			"海滩小屋 顶级海景 沙滩相伴 设施便利 极致夕阳",
			"海滩小屋 顶级海景 沙滩相伴 设施齐备 纵享夕阳",
			"海滩小屋 独家海景 沙滩相伴",
			"高贵小屋 海城相望 专属保安 设施齐备 社区广场",
			"海景小屋 美景相伴",
			"城区小屋 设施齐备",
			"城区小屋 海城相映 设施便利",
			"城区小屋 轻奢海景 设施便利",
			"城区小屋 独家城景",
			"城区小屋 独家海景 专享菠萝",
			"贵族公馆 海城相映 独家庄园",
			"高级公馆 海城相望 专属保安 设施齐备 社区广场"],
		["私家公馆 独门独户 风景优美",
			"私家小屋 独门独户",
			"私家别墅 独门独户",
			"私家小屋 独门独户",
			"高级公馆 设施便利 风景优美",
			"私家别墅 独门独户 瀑布美景",
			"私家小屋 独家瀑布",
			"私家小屋 瀑布美景",
			"尊享小屋 完美瀑布 临湖而居 设施完善",
			"尊享小屋 瀑布美景 临湖而居 设施方便",
			"顶级公馆 绝美湖景 独家花池 独门独户 设施完善 瀑布美景",
			"私家小屋 设施完善",
			"私家小屋 风景优美",
			"私家小屋 风景优美",
			"私家小屋 风景优美 临湖而居",
			"顶级公馆 纵享湖景 设施方便 社区广场",
			"尊享小屋 临湖而居 设施方便 风景优美",
			"私家小屋 独门独户",
			"私家小屋 独家风景",
			"私家小屋 独家风景",
			"私家公馆 风景独特",
			"私家小屋 社区广场 设施方便",
			"私家小屋 设施方便",
			"私家小屋 风景独特 设施齐备",
			"私家小屋 风景独特",
			"私家小屋 高瞻远瞩",
			"高级公馆 设施方便 独家湖景",
			"私家别墅 独门独户 独特瀑布",
			"私家小屋 独门独户 专享瀑布 景色优美",
			"高级公馆 高瞻远瞩 远景瀑布",
			"私家公馆 独门独户 风景优美",
			"私家小屋 独门独户",
			"私家别墅 独门独户",
			"私家小屋 独门独户",
			"高级公馆 设施便利 风景优美 落日余晖",
			"私家别墅 独门独户 瀑布美景",
			"私家小屋 独家瀑布",
			"私家小屋 瀑布美景",
			"尊享小屋 完美瀑布 临湖而居 设施齐备",
			"尊享小屋 瀑布美景 临湖而居 设施方便",
			"顶级公馆 绝美湖景 独家花池 独门独户 设施完善 瀑布美景 极致夕阳",
			"私家小屋 设施完善",
			"私家小屋 风景优美 别致夕阳",
			"私家小屋 风景优美 别致夕阳",
			"私家小屋 风景优美 临湖而居 纵享夕阳",
			"顶级公馆 纵享湖景 设施方便 社区广场",
			"尊享小屋 临湖而居 设施方便 风景优美",
			"私家小屋 独门独户 别致夕阳",
			"私家小屋 独家风景",
			"私家小屋 独家风景",
			"私家公馆 风景独特",
			"私家小屋 社区广场 设施方便",
			"私家小屋 设施方便",
			"私家小屋 风景独特 设施齐备",
			"私家小屋 风景独特",
			"私家小屋 高瞻远瞩",
			"高级公馆 设施方便 独家湖景",
			"私家别墅 独门独户 独特瀑布",
			"私家小屋 独门独户 专享瀑布 景色优美",
			"高级公馆 高瞻远瞩 远景瀑布"],
		["私家小屋 设施便利 旭日初升",
			"私家小屋 旭日初升",
			"城区小屋 设施完善",
			"私家公馆 私人领地",
			"顶级别墅 独特风景 设施便利 社区广场",
			"私家公馆 独门独户 旭日初升",
			"尊享小屋 设施便利 社区广场 独家花池 旭日初升",
			"高级公馆 设施便利 独家花池 旭日初升",
			"私家小屋 独家山景",
			"私家小屋 独家山景",
			"私家公馆 私人领地",
			"私家公馆 私人领地",
			"高级别墅 独家美景 巅峰住宅 俯瞰众生 完美日出",
			"私家小屋 社区广场 别致瀑布",
			"私家小屋 社区广场 别致瀑布",
			"私家小屋 社区广场",
			"私家小屋 社区广场 露天浴场",
			"私家小屋 社区广场",
			"私家公馆 社区广场 别致凉亭 遥望瀑布",
			"私家小屋 社区广场 别致凉亭 独家瀑布",
			"私家小屋 独享瀑布 独门独户 设施便利",
			"私家小屋 旭日初升",
			"私家小屋 旭日初升",
			"顶级小屋 风景优美 设施便利 完美日出",
			"尊享公馆 风景优美 设施便利 完美日出",
			"私家小屋 旭日初升 设施齐备",
			"私家小屋 风景优美 设施便利",
			"私家小屋 风景独特",
			"私家小屋 旭日初升",
			"高级别墅 绝美朝阳 设施便利",
			"私家小屋 设施便利",
			"私家小屋 独家山景",
			"城区小屋 设施完善",
			"私家公馆 私人领地",
			"顶级别墅 独特风景 设施便利 社区广场",
			"私家公馆 独门独户",
			"尊享小屋 设施便利 社区广场 独家花池",
			"高级公馆 设施便利 独家花池",
			"私家小屋 独家山景",
			"私家小屋 独家山景",
			"私家公馆 私人领地 纵享夕阳",
			"私家公馆 私人领地 纵享夕阳",
			"高级别墅 独家美景 巅峰住宅 俯瞰众生",
			"私家小屋 社区广场 别致瀑布",
			"私家小屋 社区广场 别致瀑布",
			"私家小屋 社区广场",
			"私家小屋 社区广场 露天浴场",
			"私家小屋 社区广场",
			"私家公馆 社区广场 别致凉亭 遥望瀑布",
			"私家小屋 社区广场 别致凉亭 独家瀑布",
			"私家小屋 独享瀑布 独门独户 设施便利",
			"私家小屋 落日余晖",
			"私家小屋 落日余晖",
			"顶级小屋 风景优美 设施便利 极致夕阳",
			"尊享公馆 风景优美 设施便利 极致夕阳",
			"私家小屋 设施齐备 纵享夕阳",
			"私家小屋 风景优美 设施便利 绝美夕阳",
			"私家小屋 风景独特",
			"私家小屋 风景独特",
			"高级别墅 设施便利"],
		["高级公馆 设施便利 海滩美景",
			"私家小屋 设施便利",
			"私家小屋 海滩美景",
			"私家小屋 环境优美",
			"私家小屋 环境优美",
			"私家小屋 设施便利",
			"私家别墅 设施便利",
			"顶级公馆 独家海景 私家温泉 设施便利",
			"私家小屋 独门独户",
			"和睦邻里 视野开阔",
			"和睦邻里 视野开阔",
			"私家小屋 环境优美",
			"高级公馆 环境优美 设施便利",
			"尊享小屋 设施便利",
			"顶级公馆 设施便利 高瞻远瞩 海城相映 顶级夕阳",
			"尊贵别墅 高瞻远瞩 独家海景 专属庭院",
			"私家小屋 海滩美景 独特夕阳",
			"私家小屋 尊享海景 设施齐备",
			"私家公馆 海滩美景",
			"私家小屋 设施便利",
			"私家小屋 海滩美景 独特夕阳",
			"私家小屋 海滩美景 独特夕阳",
			"尊享小屋 独享夕阳 私人领地 环境优美",
			"私家公馆 设施便利 城区环绕",
			"私家小屋 设施便利",
			"私家小屋 设施便利",
			"尊享小屋 私人领地 环境优美 独家瀑布",
			"私家公馆 独门独户",
			"私家小屋 设施便利 别致夕阳 独特海景",
			"顶级别墅 设施便利 高瞻远瞩 海城相映 纵享夕阳 私家温泉",
			"高级公馆 设施便利 海滩美景 纵享夕阳",
			"私家小屋 设施便利 纵享夕阳",
			"私家小屋 海滩美景 绝美夕阳",
			"私家小屋 环境优美 别致夕阳",
			"私家小屋 环境优美",
			"私家小屋 设施便利",
			"私家别墅 设施便利",
			"顶级公馆 独家海景 私家温泉 设施便利 纵享夕阳",
			"私家小屋 独门独户",
			"和睦邻里 视野开阔",
			"和睦邻里 视野开阔",
			"私家小屋 环境优美",
			"高级公馆 环境优美 设施便利",
			"尊享小屋 设施便利",
			"顶级公馆 设施便利 高瞻远瞩 海城相映 顶级夕阳",
			"尊贵别墅 高瞻远瞩 独家海景 专属庭院 绝美夕阳",
			"私家小屋 海滩美景",
			"私家小屋 尊享海景 设施齐备 纵享夕阳",
			"私家公馆 海滩美景",
			"私家小屋 设施便利 别致夕阳",
			"私家小屋 海滩美景 独特夕阳",
			"私家小屋 海滩美景 独特夕阳",
			"尊享小屋 私人领地 环境优美",
			"私家公馆 设施便利 城区环绕",
			"私家小屋 设施便利",
			"私家小屋 设施便利",
			"尊享小屋 私人领地 环境优美 独家瀑布",
			"私家公馆 独门独户",
			"私家小屋 设施便利 独特海景",
			"顶级别墅 设施便利 高瞻远瞩 海城相映 纵享夕阳 私家温泉"],
		["私家小屋 设施便利 独门独户 视野开阔",
			"私家公馆 独门独户 运动娱乐",
			"私家小屋 独家雪地",
			"私家小屋 视野开阔",
			"私家小屋 运动娱乐",
			"私家小屋 运动娱乐",
			"私家公馆 尊享山景",
			"私家公馆 视野开阔",
			"私家小屋",
			"私家小屋 社区市场",
			"私家小屋 社区广场 独家城景",
			"尊享公馆 设施便利 视野开阔 山城相映",
			"私家小屋 视野开阔",
			"私家小屋 社区市场 视野开阔",
			"私家小屋",
			"私家小屋",
			"私家公馆 视野开阔 山城相映 社区广场",
			"尊享公馆 视野开阔 山城相映 设施便利",
			"私家小屋 视野开阔",
			"私家小屋",
			"私家公馆 视野开阔 山城相映 独门独户",
			"巅峰别墅 视野开阔 山城相映 独门独户 设施便利",
			"私家小屋 视野开阔 社区广场",
			"私家小屋 和睦邻里 尊享浴池",
			"私家小屋 和睦邻里 尊享浴池",
			"尊贵公馆 视野开阔 独家山景 社区广场",
			"私家小屋 独家山景 尊享浴池",
			"私家小屋 视野开阔 山城相映 社区广场",
			"私家小屋",
			"顶级别墅 视野开阔 山城相映 社区广场 尊享浴池",
			"私家小屋 设施便利 独门独户 视野开阔",
			"私家公馆 独门独户 运动娱乐",
			"私家小屋 独家雪地",
			"私家小屋 视野开阔",
			"私家小屋 运动娱乐",
			"私家小屋 运动娱乐",
			"私家公馆 尊享山景",
			"私家公馆 视野开阔",
			"私家小屋",
			"私家小屋 社区市场",
			"私家小屋 社区广场 独家城景",
			"尊享公馆 设施便利 视野开阔 山城相映",
			"私家小屋 视野开阔",
			"私家小屋 社区市场 视野开阔",
			"私家小屋",
			"私家小屋",
			"私家公馆 视野开阔 山城相映 社区广场",
			"尊享公馆 视野开阔 山城相映 设施便利",
			"私家小屋 视野开阔",
			"私家小屋",
			"私家公馆 视野开阔 山城相映 独门独户",
			"巅峰别墅 视野开阔 山城相映 独门独户 设施便利",
			"私家小屋 视野开阔 社区广场",
			"私家小屋 和睦邻里 尊享浴池",
			"私家小屋 和睦邻里 尊享浴池",
			"尊贵公馆 视野开阔 独家山景 社区广场",
			"私家小屋 独家山景 尊享浴池",
			"私家小屋 视野开阔 山城相映 社区广场",
			"私家小屋",
			"顶级别墅 视野开阔 山城相映 社区广场 尊享浴池"]]
