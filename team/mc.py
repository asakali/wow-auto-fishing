from datetime import datetime

revenue = 11600			#全部
other_in = 0			#其他收入

people_nb = 37			#分全G人数
half_people_nb = 0		#分半G人数
tn_bl = 0.1				#TN补助比例
hk_t = 300				#火炕T
dps_3 = 300				#dps前三
n_2 = 200				#治疗前二
qusan = 50				#驱散
zuzhou = 50				#解诅咒
miehuo = 210			#灭火
jiqiren = 0				#机器人
other_out = 0			#其他

tn_nb = 14				#tn人数（应减去火炕T）

i_am_zhiliao = False

def calculate(before = True):
	title = "《极致公允》MC G团开组 2.5小时稳过 TN补助{}% DPS前三100 治疗前二100 驱散诅咒第一50 火炕T{} 灭火30".format(int(tn_bl * 100) , hk_t)
	total = revenue + other_in

	if before == True:
		tn_bz = int(total * tn_bl)
		net_profits = total - (tn_bz + hk_t + dps_3 + n_2 + qusan + zuzhou + miehuo + jiqiren + other_out)
	else:
		net_profits = total - (hk_t + dps_3 + n_2 + qusan + zuzhou + miehuo + jiqiren + other_out)
		tn_bz = int(net_profits * tn_bl)
		net_profits -= tn_bz
	
	tn_single = int(tn_bz / tn_nb)
	half = int(net_profits / (people_nb * 2 + half_people_nb))
	normal = int(half * 2)
	
	print(title)
	print("")

	print("--------- 支出 ---------")
	print("火炕T：{}".format(hk_t))
	print("T/N补助: {}".format(tn_bz))
	print("DPS前三：{}".format(dps_3))
	print("治疗前二：{}".format(n_2))
	print("驱散：{}".format(qusan))
	print("解诅咒：{}".format(zuzhou))
	print("灭火：{}".format(miehuo))
	print("机器人：{}".format(jiqiren))
	print("其他：{}".format(other_out))
	print("支出总计：{}".format(hk_t + tn_bz + dps_3 + n_2 + qusan + zuzhou + miehuo + jiqiren + other_out))
	print("")

	print("--------- 收入 ---------")
	print("拍卖收入：{}".format(revenue))
	print("其他收入: {}".format(other_in))
	print("最终收入: {}".format(total))
	print("净收入：{}".format(net_profits))
	print("")

	half_total = half * half_people_nb
	normal_total = normal * people_nb
	tn_total = tn_single * tn_nb

	print("--------- 结果 ---------")
	print("当前时间: {}".format(datetime.now()))
	print("50%分金: {} 人数：{}".format(half, half_people_nb))
	print("100%分金: {} 人数：{}".format(normal, people_nb))
	print("T/N补助: {} 每人: {} ({} + {})".format(tn_single, tn_single + normal, tn_single, normal))
	print("")

	my_zlbz = tn_single if i_am_zhiliao else 0
	my_left = total - (half_total + normal_total + tn_total + hk_t + dps_3 + n_2 + qusan + zuzhou + miehuo + jiqiren + other_out)

	print("--------- 我的收益 ---------")
	print("分金: {}".format(normal))
	if i_am_zhiliao == True:
		print("治疗补助: {}".format(my_zlbz))
	print("剩余: {}".format(my_left))
	print("总计: {}".format(normal + my_zlbz + my_left))
	print("")

	print("--------- END ---------\n")

	return normal + my_zlbz + my_left

if __name__ == "__main__":
	ret_1 = calculate(True)
	ret_2 = calculate(False)

	print(ret_1, ret_2)
	print("T/N补助 找团长交易，打工找每个队伍第一个玩家交易")


## 战神牛 骷髅
## 戦绅 叉子
## 铃儿叮当响 方快
## 施南野人 月亮
## 抬头望天发呆 倒三角

## 放逐
## 半斤灬	大饼	元素
## 心有余悸	星星	鲁莽