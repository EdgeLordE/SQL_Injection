import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3
import urllib.parse


# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def get_User(username, password):
  conn = sqlite3.connect(data_files['SQL_Injection_database.db'])
  cursor = conn.cursor()
  try:
    res = list(cursor.execute(f"SELECT username FROM Users WHERE username = '{username}' AND password = '{password}'"))
    
    if res:
        return True, f"SELECT username, AccountNo FROM Users WHERE username = '{username}' AND password = '{password}'"
    else:
        return False, f"SELECT username FROM Users WHERE username = '{username}' AND password = '{password}'"
  except Exception as e:
    pass
  finally:
    conn.close()

@anvil.server.callable
def get_User_safe(username, password):
    conn = sqlite3.connect(data_files['SQL_Injection_database.db'])
    cursor = conn.cursor()

    try:
        # Sichere parametrisierte Abfrage
        cursor.execute("SELECT username FROM Users WHERE username = ? AND password = ?", (username, password))
        res = cursor.fetchone()

        if res:
            return True, ""
        else:
            return False, f"SELECT username FROM Users WHERE username = '{username}' AND password = '{password}'"
    except Exception as e:
        pass
    finally:
        conn.close()

@anvil.server.callable
def get_query_params(url):
  query = url.split('?')[-1] if '?' in url else ''
  query = urllib.parse.parse_qs(query)
  return query






