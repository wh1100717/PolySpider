import sqlite3
con = sqlite3.connect('app.db')
cur = con.cursor()
cur.execute('select * from app_info')
apps = cur.fetchall()
for app in apps:
	print ('id: %d | pakage_name: %s\napk_url: %s' %(app[0],app[2],app[1]))