from itemadapter import ItemAdapter
import psycopg2

class WebdatascrapePipeline:
    def __init__(self):
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres' 
        database = 'cs699_pdb'
        # port = '5432'

        # Establishing connection to pgsql
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

        # Create table if it does not exist
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
        # If course already in Database, then do not add else add.
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