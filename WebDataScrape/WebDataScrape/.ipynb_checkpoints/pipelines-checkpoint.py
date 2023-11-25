# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2

class WebdatascrapePipeline:
    def __init__(self):
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres'  # your password
        database = 'cs699_pdb'
        # port = '5432'

        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS courses_mit(
                    id serial PRIMARY KEY, 
                    title text,
                    des text,
                    inst_name text,
                    url text,
                    tags text[]
                )
                """)

    def process_item(self, item, spider):
        
        self.cur.execute("select * from courses_mit where title = %s", (item['title'],))
        result = self.cur.fetchone()
        if result:
            spider.logger.warn("Item already in database: %s" % item['title'])
        else:
            self.cur.execute(""" insert into courses_mit (title, des, inst_name, url, tags) values (%s,%s,%s,%s,%s)""", (
                item["title"],
                item["des"],
                item["inst_name"],
                item["url"],
                item['tags']
            ))
        self.connection.commit()
        return item

    
    def close_spider(self, spider):
        try:
            self.connection.commit()
        except Exception as e:
            print(f"Error during commit: {e}")
            self.connection.rollback()
        finally:
            self.cur.close()
            self.connection.close()