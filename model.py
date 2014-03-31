import sae
import sae.const
import MySQLdb
from datetime import *



def get_posts():
	conn = MySQLdb.connect("localhost", "root", "", "webblog", 3306)
	cur = conn.cursor()
	cur.execute('select * from blogs order by id')
	results = cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()
	return results


def new_post(title, content, date):
	conn = MySQLdb.connect("localhost", "root", "", "webblog", 3306)
	cur = conn.cursor()
	replace = [title, content, date]
	cur.execute('insert into blogs values(NULL, %s, %s, %s)', replace)
	conn.commit()
	cur.close()
	conn.close()

def del_post(id):
	conn = MySQLdb.connect("localhost", "root", "", "webblog", 3306)
	cur = conn.cursor()
	cur.execute('delete from blogs where id=%d'%id)	
	conn.commit()
	cur.close()
	conn.close()


