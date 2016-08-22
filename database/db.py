import sqlite3 as sql
from os import path
import time



def create():
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ] Tabellen anlegen...")

	command_create_1 = """
	CREATE TABLE datarecord (
	timestamp DATETIME DEFAULT (datetime('now','localtime')),
	temp_1 REAL,
	temp_2 REAL,
	temp_r REAL,
	temp_c REAL,
	ph REAL,
	volt REAL,
	current REAL,
	flow REAL,
	fill REAL ); """
	
	
	command_create_2 = """
	CREATE TABLE `settings` (
	`name`	TEXT,
	`value`	REAL,
	`text`	TEXT,
	PRIMARY KEY(name)); """
	
	db_cursor.execute(command_create_1)
	db_cursor.execute(command_create_2)
	db_connection.commit()
	

def write_all (temp_1 = "NULL", temp_2 = "NULL", temp_r = "NULL", temp_c = "NULL", ph = "NULL", volt = "NULL", current = "NULL", flow = "NULL", fill = "NULL"):
	command_add = """
INSERT INTO datarecord (temp_1, temp_2, temp_r, temp_c, ph, volt, current, flow, fill)
 VALUES ({temp_1}, {temp_2}, {temp_r}, {temp_c}, {ph}, {volt}, {current}, {flow}, {fill}); 
 """.format(temp_1=temp_1, temp_2=temp_2, temp_r=temp_r, temp_c=temp_c, ph=ph, volt=volt, current=current, flow=flow, fill=fill)
	db_cursor.execute(command_add)
	db_connection.commit()
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ] Werte in Datenbank geschrieben.")
	
def write_setting(setting, value):

	if type(value) == str:
		datatype = "text" 
	else: 
		datatype = "value"
		
	command_set = """
UPDATE settings
SET {datatype}="{value}"
WHERE name="{setting}"; """.format(datatype=datatype,value=value,setting=setting)
	db_cursor.execute(command_set)
	db_connection.commit()
	print(time.strftime("[%Y-%m-%d %H:%M]"), "[ DB ] Wert in Datenbank geschrieben: ", setting, ": ", value)
def read_setting(setting, type="value"):
	command_read = """
SELECT {type} FROM settings
WHERE name="{setting}"; """.format(type=type, setting=setting)
	db_cursor.execute(command_read)
	value = db_cursor.fetchone()
	return value[0]
	
def read_last(cat):
	command_rl = """
SELECT {cat} from datarecord
ORDER BY timestamp DESC LIMIT 1; """.format(cat=cat)
	db_cursor.execute(command_rl)
	value = db_cursor.fetchone()
	return value[0]
	
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


