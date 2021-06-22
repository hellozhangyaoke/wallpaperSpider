# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from pymongo import MongoClient
from pymysql.converters import escape_string
from twisted.enterprise import adbapi

class WallpaperspiderPipeline:

    # def __init__(self):
    #     self.connect = pymysql.connect(
    #         host = "47.115.95.116",
    #         port = 3306,
    #         user = 'root',
    #         password = "jackson1227",
    #         db = "wallpaper",
    #         charset = "utf8mb4"
    #     )
    #     self.cur = self.connect.cursor()
    #     self.cur.execute("SET FOREIGN_KEY_CHECKS=0;")
    def open_spider(self,spider):
        self.client = MongoClient("mongodb://yaoke:jackson1227@47.115.95.116:27017/")
        self.db = self.client["maoyanImg"]
        self.col = self.db["maoyanImg"]

    def process_item(self,item,spider):
        try:
            self.col.insert(dict(item))
        except:
            pass
        return item
    # def process_item(self,item,spider):
    #     result = (
    #         str(item["old_id"]),
    #         item["thumb"],
    #         item["large"],
    #         item["cover"],
    #         item["full"],
    #         item["meta"]
    #     )
    #     insert_sql = "insert into `maoyanImg`(old_id,thumb,large,cover,full,meta) values (%s,%s,%s,%s,%s,%s)"%(result)
    #     self.cur.execute(insert_sql)
    #     self.connect.commit()

    # def close_spider(self,spider):
    #     self.cur.close()
    #     self.connect.close()



# class WallpaperspiderPipeline:

#     def __init__(self,dbpool):
#         self.dbpool = dbpool

#     @classmethod
#     def from_settings(cls,settings):
#         """
#         数据库建立连接
#         :param settings: 配置参数
#         :return: 实例化参数
#         """
#         adbparams = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             password=settings['MYSQL_PASSWORD'],
#             charset="utf8mb4",
#             cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
#         )
#         # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
#         dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
#         # 返回实例化参数
#         return cls(dbpool)

#     def process_item(self, item, spider):
#         """
#         使用twisted将MySQL插入变成异步执行，通过连接池执行具体的sql操作，返回一个对象
#         """
#         # 指定操作方法和操作数据
#         query = self.dbpool.runInteraction(self.insert_maoyan_img, item)  
#         # 添加异常处理
#         query.addCallback(self.handle_error)  # 处理异常

#     # 爬取国外壁纸网站插入动作
#     def do_insert(self, cursor, item):
#         # 对数据库进行插入操作，并不需要commit，twisted会自动commit
#         insert_sql = """
#         insert into `wallpaper`(img_url,targets,img_type) VALUES(%s,%s,%s)
#                     """
#         try:
#             cursor.execute(insert_sql, (item['img_url'],item["targets"],"Mac"))
#         except pymysql.err.IntegrityError:
#             print("【数据重复】：%s"%(item['img_url']))

#     # 爬取猫眼壁纸插入动作
#     def insert_maoyan_img(self, cursor, item):
#         # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        
#         insert_sql = """
#         SET FOREIGN_KEY_CHECKS=0;
#         insert into `maoyanImg`(old_id,thumb,large,cover,full,meta) values (%s,%s,%s,%s,%s,%s)
#                     """
#         insert_cate = """
#                 insert into `maoyan_categorie`(name,description,cover) select (%s,%s,%s)\
#                     from DUAL where not EXISTS (select name from maoyan_categorie where name=%s)
#                 """
#         insert_tag = """
#                 insert into `maoyan_tag`(name,description,cover) select (%s,%s,%s)\
#                     from DUAL where not EXISTS (select name from maoyan_tag where name=%s)
#                 """
        
#         cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
#         cursor.execute(insert_sql,(str(item["old_id"]),item["thumb"].replace("https://","").replace("http://",""),item["large"],item["cover"],item["full"],item["meta"]))
#         img_id = cursor.lastrowid
#         cate_id = []
#         for c in item["categorie"]:
#             cursor.execute(insert_cate,(c["name"],c["description"],escape_string(c["cover"])))
#             cate_id.append(cursor.lastrowid)
#         tag_id = []
#         for t in item["tag"]:
#             cursor.execute(insert_tag,(t["name"],t["description"],escape_string(t["cover"])))
#             tag_id.append(cursor.lastrowid)
        
#         insert_cate_img = """
#                 insert into `img_categorie`(img_id,cate_id) values (%s,%s,%s)
#                 """
#         insert_tag_img = """
#                 insert into `img_tag`(img_id,tag_id) values (%s,%s,%s)
#                 """
#         for _cate in cate_id:
#             cursor.execute(insert_cate_img,(img_id,_cate))
#         for _tag in tag_id:
#             cursor.execute(insert_tag_img,(img_id,_tag))
        

        
        
       

#     def insert_maoyan_cate(self, cursor, item):
#         # 对数据库进行插入操作，并不需要commit，twisted会自动commit
#         insert_cate = """
#                 insert into `maoyan_tag`(name,description,cover) select (%s,%s,%s)\
#                     from DUAL where not EXISTS (select name from maoyan_tag where name=%s)
#                 """
#         insert_sql = """
#         insert into `maoyanImg`(img_url,targets,img_type) VALUES(%s,%s,%s)
#                     """
#         try:
#             # cursor.execute(insert_sql, (item['img_url'],item["targets"],"Mac"))
#             cursor.execute(insert_cate,(item["name"],item["description"],item["cover"],item["name"]))
#         except pymysql.err.IntegrityError:
#             print("【数据重复】：%s"%(item['name']))


#     def handle_error(self, failure):
#         if failure:
#             # 打印错误信息
#             print(failure)