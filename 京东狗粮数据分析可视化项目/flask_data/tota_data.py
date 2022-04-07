from flask import Flask, render_template
import pymysql
import pandas
import numpy as np

app = Flask(__name__)

@app.route('/散点图.html')
def mysql1():
    db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
    cusor = db.cursor()  # 通过获取到的数据库连接db下的cursor()方法来创建游标
    cusor.execute("SELECT price_data,GoodCount,taste_list FROM data_input;")  # 查询相对应都数据表
    data = pandas.DataFrame(list(cusor.fetchall()))  # 转换为DataFrame
    lists = ['鱼肉', '鸭肉', '鸡肉', '牛肉', '其它',  '羊肉', ]
    list_data = []
    for i in lists:
        datas = data.loc[data[2].str.contains(i)]
        list_data.append([float('%.1f' % datas[0].mean()), float('%.1f' % datas[1].mean()), datas[2].count(), i + '味'])

    return render_template('散点图.html',list_data=list_data)

@app.route('/柱状图.html')
def mysql2():
    db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
    cusor = db.cursor()  # 通过获取到的数据库连接db下的cursor()方法来创建游标
    cusor.execute("SELECT com_name,GoodCount,GeneralCount,PoorCount,price_data FROM data_input;")  # 查询相对应都数据表
    data = pandas.DataFrame(list(cusor.fetchall()))  # 转换为DataFrame
    lists = ['麦富迪', '皇家', '疯狂的小狗', '耐威克', '伯纳天纯', '宝路', '冠能', '力狼', '海洋之星', '渴望', '好主人', '纽顿', '比乐', '爱肯拿', '雷米高', '醇粹',
             '奥丁']
    list_a = []
    list_b = []
    for i in lists:
        datas = data.loc[data[0].str.contains(i)]
        list_a.append('%.1f' % (datas[1].mean()+datas[2].mean()+datas[3].mean()))
        list_b.append('%.1f' % datas[4].mean())

    return render_template('柱状图.html',list_a=list_a,list_b=list_b,lists=lists)

@app.route('/雷达图.html')
def mysql3():
    db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
    cusor = db.cursor()  # 通过获取到的数据库连接db下的cursor()方法来创建游标
    cusor.execute("select recipe,price_data,GoodCount from data_input;")  # 查询相对应都数据表
    data = pandas.DataFrame(list(cusor.fetchall()))  # 转换为DataFrame
    # data=data[True^(data[0].isin(['none']))]
    # 取下面几个字段的数据进行统计
    data = data[
        (data[0].isin(['冻干粮'])) | (data[0].isin(['处方粮'])) | (data[0].isin(['天然粮'])) | (data[0].isin(['无谷粮'])) | (
            data[0].isin(['通用粮'])) | (data[0].isin(['鲜肉粮']))]

    data = data.groupby(0)
    data = data[1, 2].agg([np.mean])

    list1 = data[1]['mean'].tolist()
    list2 = data[2]['mean'].tolist()
    list1 = list(map(lambda x: '%.1f' % x, list1))
    list2 = list(map(lambda x: '%.1f' % x, list2))


    return render_template('雷达图.html', list1=list1, list2=list2)

@app.route('/玫瑰图.html')
def mysql4():
    db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
    cusor = db.cursor()  # 通过获取到的数据库连接db下的cursor()方法来创建游标
    cusor.execute(
        "SELECT stage,count(stage),sum(GoodCount+GeneralCount+PoorCount) FROM data_input GROUP BY stage")  # 查询相对应都数据表
    data = pandas.DataFrame(list(cusor.fetchall()))  # 转换为DataFrame
    count = data[1].sum()
    # print(data)
    lists = ['成犬', '幼犬', '全阶段', '离乳期', '老龄犬', '哺乳期/孕期']
    data_coun = []
    count_data = []
    for i in lists:
        datas = data.loc[data[0].str.contains(i)]
        data_coun.append("{value: " + '%.1f' % (datas[1].sum() / count * 100) + ", name: '" + i + "'}")
        count_data.append("{value: %s, name: '%s'}" % (('%.1f' % datas[2].sum()), i))
    data_coun = str(data_coun).replace('"', '')
    count_data = str(count_data).replace('"', '')
    return render_template('玫瑰图.html',lists=lists,data_coun=data_coun,count_data=count_data)

@app.route('/漏斗图.html')
def mysql5():
    db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
    cusor = db.cursor()  # 通过获取到的数据库连接db下的cursor()方法来创建游标
    cusor.execute("SELECT the_dog,count(the_dog) FROM data_input WHERE the_dog!='none' GROUP BY the_dog;")  # 查询相对应都数据表
    data = pandas.DataFrame(list(cusor.fetchall()))  # 转换为DataFrame
    total = data[1].sum()  # 总数
    lists = ['通用', '巨型犬', '大型犬', '中型犬', '小型犬', '迷你犬']
    the_dog = []
    for i in lists:
        datas = data.loc[data[0].str.contains(i)]
        the_dog.append(int((datas[1].sum() / total * 100)))
    lists[0] = '通用犬型'
    the = 33.19  # 预期值
    the_data = sum(the_dog) + the
    the_dog1 = list(map(lambda x: int((x / the_data * 100) + x), the_dog))
    for j, i in enumerate(the_dog):
        the_dog[j] = "{value: " + str(i) + ",name:'" + lists[j] + "'}"
    the_dog = (str(the_dog).replace('"', ''))
    for j, i in enumerate(the_dog1):
        the_dog1[j] = "{value: " + str(i) + ",name:'" + lists[j] + "'}"
    the_dog1 = (str(the_dog1).replace('"', ''))
    return render_template('漏斗图.html',lists=lists,the_dog=the_dog,the_dog1=the_dog1)

@app.route('/折线图.html')
def mysql6():
    db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
    cusor = db.cursor()  # 通过获取到的数据库连接db下的cursor()方法来创建游标
    cusor.execute("SELECT breed,GoodCount,GeneralCount,PoorCount,price_data FROM data_input;")  # 查询相对应都数据表
    data = pandas.DataFrame(list(cusor.fetchall()))  # 转换为DataFrame
    lists = ['比熊', '哈士奇', '拉布拉多', '柯基', '阿拉斯加', '雪纳瑞', '柴犬', '贵宾', '金毛', '通用', '其它']
    counts = []
    price_data = []
    for i in lists:
        datas = data.loc[data[0].str.contains(i)]
        counts.append('%.1f' % (datas[1].mean() + datas[2].mean() + datas[3].mean()))
        price_data.append('%.1f' % datas[4].mean())

    return render_template('折线图.html',lists=lists,counts=counts,price_data=price_data)

@app.route('/饼图.html')
def mysql7():
    db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
    cusor = db.cursor()  # 通过获取到的数据库连接db下的cursor()方法来创建游标
    cusor.execute("SELECT count(domestic),domestic FROM data_input GROUP BY domestic;")  # 查询相对应都数据表
    data = list(cusor.fetchall())  # 转换为DataFrame
    lists=['国产','进口']
    data_coun = []
    for i in data:
        data_coun.append("{value: " + '%.1f' % (i[0] / 2282 * 100) + ", name: '" + i[1] + "'}")
    data_coun = str(data_coun).replace('"', '')
    return render_template('饼图.html',lists=lists,data_coun=data_coun)

@app.route('/金字塔图.html')
def mysql8():
    db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
    cusor = db.cursor()  # 通过获取到的数据库连接db下的cursor()方法来创建游标
    cusor.execute("SELECT com_name,PoorCount FROM data_input;")  # 查询相对应都数据表
    data = pandas.DataFrame(list(cusor.fetchall()))  # 转换为DataFrame
    lists = ['麦富迪', '皇家', '疯狂的小狗', '耐威克', '伯纳天纯', '宝路', '冠能', '力狼', '海洋之星',  '好主人', '雷米高', '醇粹',
             '奥丁']
    list_a = []
    counts=[]
    data_list=[]
    for i in lists:
        datas = data.loc[data[0].str.contains(i)]
        list_a.append('%.1f' % (datas[1].mean()))

    total = data[1].sum()
    for i in lists:
        datas = data.loc[data[0].str.contains(i)]
        counts.append('%.1f' % (datas[1].sum() / total * 100))
    for j, i in enumerate(counts):
        data_list.append("{value: " + str(i) + ",name:'" + lists[j] + "'}")
    data_list = (str(data_list).replace('"', ''))
    print(data_list)
    return render_template('金字塔图.html',lists=lists,data_list=data_list)


@app.route('/条形图.html')
def mysql9():
    db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
    cusor = db.cursor()  # 通过获取到的数据库连接db下的cursor()方法来创建游标
    cusor.execute("SELECT stage,AVG(price_data),AVG(GoodCount+GeneralCount+PoorCount) FROM data_input GROUP BY stage;")  # 查询相对应都数据表
    data = pandas.DataFrame(list(cusor.fetchall()))  # 转换为DataFrame
    lists = ['成犬', '幼犬', '全阶段', '离乳期', '老龄犬', '哺乳期/孕期']
    the_dog = []
    data2=[]
    for i in lists:
        datas = data.loc[data[0].str.contains(i)]
        the_dog.append('%.1f' % (datas[1].mean()))
        data2.append('%.1f' % (datas[2].mean()))
    return render_template('条形图.html',lists=lists,list_b=the_dog,list_a=data2)

@app.route('/折线图1.html')
def mysql10():
    db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
    cusor = db.cursor()  # 通过获取到的数据库连接db下的cursor()方法来创建游标
    cusor.execute("SELECT the_dog,AVG(price_data),AVG(GoodCount+GeneralCount+PoorCount) FROM data_input GROUP BY the_dog;")  # 查询相对应都数据表
    data = pandas.DataFrame(list(cusor.fetchall()))  # 转换为DataFrame
    lists = ['通用', '巨型犬', '大型犬', '中型犬', '小型犬', '迷你犬']
    counts = []
    price_data = []
    for i in lists:
        datas = data.loc[data[0].str.contains(i)]
        price_data.append('%.1f' % (datas[1].mean()))
        counts.append('%.1f' % datas[2].mean())

    return render_template('折线图1.html',lists=lists,price_data=price_data,counts=counts)





if __name__ == '__main__':
    app.run()
