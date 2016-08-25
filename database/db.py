import sqlite3 as sql
from os import path
import time

# UPDATE datarecord  SET temp_1 = 1 WHERE id=1;
# =(datetime('now','localtime'))

def create():
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ] Tabellen anlegen...")

	command_create_1 = """
	CREATE TABLE datarecord (timestamp DATETIME DEFAULT (datetime('now','localtime'))); """
	
	
	command_create_2 = """
	CREATE TABLE `settings` (
	`name`	TEXT,
	`value`	REAL,
	`text`	TEXT,
	PRIMARY KEY(name)); """
	


	
	db_cursor.execute(command_create_1)
	db_cursor.execute(command_create_2)
	db_connection.commit()
	

def write_all (arr):
	if len(arr) > 0:
		columns = arr[0][0]
		values = arr[0][1]
		
		for s in range(1, len(arr)):
			columns = "{}, {}".format(columns, arr[s][0])
			values = "{}, {}".format(values, arr[s][1])
			
		command_add = "INSERT INTO datarecord ({}) VALUES ({});".format(columns, values)
		
		db_cursor.execute(command_add)
		db_connection.commit()
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ] Werte in Datenbank geschrieben.")

def add_write(arr, name, value):
	try:
		command_checkcolumn = "SELECT COUNT({}) FROM datarecord;".format(name)
		db_cursor.execute(command_checkcolumn)
		
		arr.append([name, value])
		
	except Exception as e:
		try:
			print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ][WARN] Spalte \"{}\" existiert nicht".format(name))
			print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ][WARN] Spalte wird angelegt...")
			
			command_createcolumn = "ALTER TABLE datarecord ADD COLUMN {} REAL;".format(name)
			db_cursor.execute(command_createcolumn)
			command_checkcolumn = "SELECT COUNT({}) FROM datarecord;".format(name)
			db_cursor.execute(command_checkcolumn)
			
			arr.append([name, value])
		except Exception as ee:
			print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ][ERROR]", e)
			print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ][ERROR]", ee)

	return (arr)
	
def write_setting(setting, value):

	if type(value) == str:
		datatype = "text" 
	else: 
		datatype = "value"
		
	command_set = """
UPDATE settings
SET {datatype}="{value}"
WHERE name="{setting}"; """.format(datatype=datatype,value=value,setting=setting)
	
	try:
		db_cursor.execute(command_set)
		db_connection.commit()
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ] Wert in Datenbank geschrieben: ", setting, ": ", value)
	except Exception as e :
		
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ][ERROR]", e)
		command_add = "INSERT INTO settings (\"name\") VALUES ({});".format(setting)
		
		db_cursor.execute(command_add)
		db_connection.commit()
		
		db_cursor.execute(command_set)
		db_connection.commit()
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ] Wert in Datenbank geschrieben: ", setting, ": ", value)
		
		return 0
	
def read_setting(setting, type="value"):

	try: 
		command_read = "SELECT {type} FROM settings	WHERE name=\"{setting}\"; ".format(type=type, setting=setting)
		db_cursor.execute(command_read)
		value = db_cursor.fetchone()

		return value[0]
	except Exception as e :
		
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ][ERROR]", e)
		command_add = "INSERT INTO settings (\"name\") VALUES (\"{}\"); ".format(setting)
		
		db_cursor.execute(command_add)
		db_connection.commit()
		
		return 0
	
def read_last(cat):
	command_rl = """
SELECT {cat} from datarecord
ORDER BY timestamp DESC LIMIT 1; """.format(cat=cat)
	
	try: 
		db_cursor.execute(command_rl)
		value = db_cursor.fetchone()
	
		return value[0]
	except Exception as e :
		print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ][ERROR]", e)
		
		return 0
		
def delete_old():
	command_del = """
	DELETE FROM datarecord 
	WHERE timestamp <= date('now','-7 day'); """
	db_cursor.execute(command_del)
	db_connection.commit()
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ] Alte Eintraege geloescht.")
	
def close():
	db_connection.close()
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ] Verbindung getrennt.")
#create()

path = path.dirname(path.realpath(__file__))

print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ] Verbinde zu Datenbank: ", path + "/aquarium.db")
db_connection = sql.connect(path + "/aquarium.db", check_same_thread=False)
db_cursor = db_connection.cursor()

#Ueberpruefen, ob Table existiert (sonst erstellen)
command_checktable = """
SELECT count(*) FROM sqlite_master WHERE type='table' AND name='datarecord';"""
db_cursor.execute(command_checktable)
value = db_cursor.fetchone()
if value[0] == 0:
	create()	


