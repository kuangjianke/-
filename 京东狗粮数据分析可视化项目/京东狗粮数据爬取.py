import requests
import re
from fake_useragent import UserAgent
import time
import random
import pymysql

class DOG_FOOD_DATA():
    def __init__(self, headers, url, total_id, total_title):  # 获取网络数据
        html_data = requests.get(url, headers=headers, timeout=5)
        if html_data.status_code == 200:  # 判断是否连接成功
            print('网页数据获取成功')
            self.html_data = html_data.text
            self.Re_id_data()  # 商品id
        else:
            print("请求失败")

    def Re_id_data(self):  # 获取商品id
        id_datas = re.findall('"sku_id":"(.*?)",', self.html_data)  # id
        price_data = re.findall('"sku_price":"(.*?)"', self.html_data)  # 价格
        title_data = re.findall('"ad_title":"(.*?)"', self.html_data)  # 标题


        self.brand_name_list = []  # 品牌
        self.GoodCount_list = []  # 好评论
        self.GeneralCount_list = []  # 中评论
        self.PoorCount_list = []  # 差评论
        self.com_name_list = []  # 商品名称
        self.rough_weight_list = []  # 商品毛重
        self.effect_list = []  # 功效
        self.the_dog_list = []  # 适用犬型
        self.net_content_list = []  # 净含量
        self.kilogram_list = []  # 每斤单价
        self.breed_list = []  # 适用犬种
        self.stage_list = []  # 适用阶段
        self.taste_list = []  # 口味
        self.recipe_list = []  # 配方
        self.domestic_list = []  # 国产/进口
        self.id_datas = id_datas  # id
        self.price_data = price_data  # 价格
        self.title_data = title_data  # 标题
        self.ID_url_data()  # 网页def

    def ID_url_data(self):  # 获取id的网页
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
        for errot, url_id in enumerate(self.id_datas):  # 循环每一个id并获取商品信息
            # time.sleep(random.random())  # 缓存时间
            urls = 'https://item.jd.com/' + str(url_id) + '.html'
            try:
                html_id_data = requests.get(urls, headers=header, timeout=15)
                if html_id_data.status_code == 200:
                    # print(html_id_data.text)
                    self.url_id = url_id
                    self.urls = urls
                    self.header = header
                    self.html_id_data = html_id_data.text
                    self.Name_Brand()  # 进入商品爬取商品品牌
                    self.commentnum_data_html()  # 评论数爬取
                    # break
                else:
                    print("请求失败")
            except:
                print('id未能获取网页或响应过时')
                print('删除错误数据中:', end=' ')
                print(self.id_datas[errot], self.price_data[errot], self.title_data[errot])
                print(self.id_datas)
                del self.id_datas[errot]
                del self.price_data[errot]
                del self.title_data[errot]
                print(self.id_datas)
        # self.mysql_data_input()

    def mysql_data_input(self):
        db = pymysql.connect('localhost', 'root', '000000', 'python_data')  # 连接数据库
        cusor = db.cursor()  # 获取游标对象
        print('------------------------------写入数据库中---------------------------------------')
        print('===============================数据去重中========================================')
        for lens in range(len(self.id_datas)):  # 判断id是否重复
            if self.id_datas[lens] in total_id and self.title_data[lens] in total_title:
                print(self.id_datas[lens])
                self.id_datas[lens] = 'kjk000000'  # 如果重复改id为kjk000000
                total_id.append(self.id_datas[lens])
            else:
                total_id.append(self.id_datas[lens])
                total_title.append(self.title_data)
            if self.id_datas[lens] != 'kjk000000':
                try:
                    sql = 'insert into data_input values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    cusor.execute(sql, [self.id_datas[lens], self.price_data[lens], self.title_data[lens],
                                        self.brand_name_list[lens], self.GoodCount_list[lens],
                                        self.GeneralCount_list[lens], self.PoorCount_list[lens],
                                        self.com_name_list[lens],
                                        self.rough_weight_list[lens], self.effect_list[lens],
                                        self.the_dog_list[lens], self.net_content_list[lens], self.kilogram_list[lens],
                                        self.breed_list[lens], self.stage_list[lens], self.taste_list[lens],
                                        self.recipe_list[lens], self.domestic_list[lens]])
                    db.commit()
                except:
                    print('----------------------------------错误------------------------------------------'+str(self.id_datas[lens]))
            else:
                print('-----------------------------数据重复，跳过写入-----------------------------------')
        print('--------------------------------写入完成-----------------------------------------')
        db.close()



    def data_none(self, data_none):
        if data_none == []:
            data_none = ['none']
        return data_none[0]

    def Name_Brand(self):  # 商品品牌
        # id_no = re.findall('data-sku="(.*?)"', self.html_id_data)  # id
        # print(id_no, '------------------------------------------------------------------------------')

        brand_name_data = re.findall("<li title='(.*?)'>品牌", self.html_id_data)  # 品牌
        self.brand_name_list.append(self.data_none(brand_name_data))

        com_name = re.findall("商品名称：(.*?)</li>", self.html_id_data)  # 商品名称
        self.com_name_list.append(self.data_none(com_name))

        rough_weight = re.findall("商品毛重：(.*?)</li>", self.html_id_data)  # 商品毛重
        self.rough_weight_list.append(self.data_none(rough_weight))

        effect = re.findall("功效：(.*?)</li>", self.html_id_data)  # 功效
        self.effect_list.append(self.data_none(effect))

        the_dog = re.findall("适用犬型：(.*?)</li>", self.html_id_data)  # 适用犬型
        self.the_dog_list.append(self.data_none(the_dog))

        net_content = re.findall("净含量：(.*?)</li>", self.html_id_data)  # 净含量
        self.net_content_list.append(self.data_none(net_content))

        kilogram = re.findall("每斤单价：(.*?)</li>", self.html_id_data)  # 每斤单价
        self.kilogram_list.append(self.data_none(kilogram))

        breed = re.findall("适用犬种：(.*?)</li>", self.html_id_data)  # 适用犬种
        self.breed_list.append(self.data_none(breed))

        stage = re.findall("适用阶段：(.*?)</li>", self.html_id_data)  # 适用阶段
        self.stage_list.append(self.data_none(stage))

        taste = re.findall("口味：(.*?)</li>", self.html_id_data)  # 口味
        self.taste_list.append(self.data_none(taste))

        recipe = re.findall("配方：(.*?)</li>", self.html_id_data)  # 配方
        self.recipe_list.append(self.data_none(recipe))

        domestic = re.findall("国产/进口：(.*?)</li>", self.html_id_data)  # 国产/进口
        self.domestic_list.append(self.data_none(domestic))

    def commentnum_data_html(self):  # 获取评论数量网页
        url_data = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + str(self.url_id)
        html_commentnum_data = requests.get(url_data, headers=self.header, timeout=5)
        if html_commentnum_data.status_code == 200:

            self.html_commentnum_data = html_commentnum_data.text
            self.commentnum_values()
        else:
            print('评论数据网页获取失败')

    def commentnum_values(self):  # 获取评论数据
        try:
            GoodCount = re.findall('"GoodCount":(.*?),"', self.html_commentnum_data)  # 好评论
            self.GoodCount_list.append(GoodCount[0])
            GeneralCount = re.findall('"GeneralCount":(.*?),"', self.html_commentnum_data)  # 中评论
            self.GeneralCount_list.append(GeneralCount[0])
            PoorCount = re.findall('"PoorCount":(.*?),"', self.html_commentnum_data)  # 差评论
            self.PoorCount_list.append(PoorCount[0])
        except:
            print('评论次数有空值，error：')


if __name__ == '__main__':
    headers = {'UserAgent': UserAgent().random}
    total_id = []
    total_title = []
    for page in range(1, 120):#循环
        url = 'https://re.jd.com/search?keyword=%E7%8B%97%E7%B2%AE&page=' + str(page) + '&enc=utf-8'
        print(url)#打印网页
        DOG_FOOD_DATA(headers, url, total_id, total_title)

'''https://search.jd.com/Search?keyword=%E7%8A%AC%E7%B2%AE&page=126&enc=utf-8#select'''
''''        url = 'https://re.jd.com/search?keyword=%E7%8B%97%E7%B2%AE&page=' + str(page) + '&enc=utf-8' '''
