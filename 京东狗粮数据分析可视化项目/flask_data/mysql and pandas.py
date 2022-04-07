import pymysql
import pandas
import pandas as pd

db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
cusor = db.cursor()  # 通过获取到的数据库连接db下的cursor()方法来创建游标
cusor.execute("SELECT frame,avg(counts) FROM pymysql_data WHERE timeto like '%2019%' GROUP BY frame;")  # 查询相对应都数据表
data = pandas.DataFrame(list(cusor.fetchall()))  # 转换为DataFrame
title_data=data[0].to_list()
list1,list2=[],[]
for i in title_data:
    datas = data.loc[data[0].str.contains(i)]
    list1.append('%.1f' % datas[1].mean())
cusor.execute("SELECT frame,avg(counts) FROM pymysql_data WHERE timeto like '%2020%' GROUP BY frame;")  # 查询相对应都数据表
data = pandas.DataFrame(list(cusor.fetchall()))  # 转换为DataFrame
title_data=data[0].to_list()
for i in title_data:
    datas = data.loc[data[0].str.contains(i)]
    list2.append('%.1f' % datas[1].mean())
print(list1)
print(list2)
print(title_data)




'''
[[520, 923, 2305], [44, 205, 164], [91, 205, 117], [116, 296, 65]]
['全框', '半框', '无框', '眉线框']
[520, 44, 91, 116] [923, 205, 205, 296] [2305, 164, 117, 65]
'''
# lists = list(data[0])
# print(data)
# counts = []
# price_list = []
# for i in range(len(lists)):
#     counts.append('%.1f' % data[1].iloc[i])
#     price_list.append('%.1f' % data[2].iloc[i])




'''{value: 10, name: 'rose1'},'''





# lists=['其它','哈士奇','拉布拉多','柯基','阿拉斯加','柴犬','比熊','贵宾','金毛','雪纳瑞','通用']
# counts=[]
# price_data=[]
# for i in lists:
#     datas = data.loc[data[0].str.contains(i)]
#     counts.append('%.1f' % (datas[1].mean() + datas[2].mean() + datas[3].mean()))
#     price_data.append('%.1f' % datas[4].mean())

# lists=['鱼肉','鸭肉','鸡肉','牛肉','其它','奶香','水果','羊肉',]
# list_data=[]
# for i in lists:
#     datas = data.loc[data[2].str.contains(i)]
#     list_data.append(['%.1f' % datas[0].mean(),'%.1f' % datas[1].mean(),datas[2].count(),i+'味'])
# 
# print(list_data)





# lists=['通用','巨型犬','大型犬','中型犬','小型犬','迷你犬']
# the_dog=[]
# for i in lists:
#     datas = data.loc[data[0].str.contains(i)]
#     the_dog.append(int((datas[1].sum()/total*100)))
# print(the_dog)
# the=33.19#预期值
# the_data=sum(the_dog)+the
# the_dog1 = list(map(lambda x: int((x / the_data * 100) + x), the_dog))
# print(the_dog1)
# for j,i in enumerate(the_dog):
#     the_dog[j]="{value: "+str(i)+",name:'"+lists[j]+"'}"
# the_dog=(str(the_dog).replace('"',''))
# print(the_dog)
# for j,i in enumerate(the_dog1):
#     the_dog1[j]="{value: "+str(i)+",name:'"+lists[j]+"'}"
# the_dog1=(str(the_dog1).replace('"',''))
# print(the_dog1)


# {value: 60, name: '访问'},

# lists=['麦富迪','皇家','疯狂的小狗','耐威克','伯纳天纯','宝路','冠能','力狼','海洋之星','渴望','好主人','纽顿','比乐','爱肯拿','雷米高','醇粹','奥丁']
# list_a=[]
# list_b=[]
# for i in lists:
#     datas = data.loc[data[0].str.contains(i)]
#     list_a.append('%.2f' % datas[1].mean())
#     list_b.append(datas[2].mean())
# print(list_b)
# print(list_a)
