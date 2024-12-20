import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3
import urllib.parse

@anvil.server.callable
def get_login_state():
  if "login" not in anvil.server.session:
    anvil.server.session["login"] = False
  if "injection_possible" not in anvil.server.session:
    anvil.server.session["injection_possible"] = True
  return anvil.server.session["login"], anvil.server.session['injection_possible']
  
@anvil.server.callable
def get_user(username, passwort):
  conn = sqlite3.connect(data_files["database.db"])
  cursor =  conn.cursor()
  try:
    res = cursor.execute(f"SELECT username FROM Users WHERE username = '{username}' AND password = '{passwort}'")
    result = cursor.fetchone()
    res1 = cursor.execute("Select AccountNo from Users Where username = ? AND password = ?", (username, passwort))
    result1 = cursor.fetchone()
    if result1:
      balance = cursor.execute("SELECT Balances.balance FROM Users JOIN Balances ON Users.AccountNo = Balances.AccountNo WHERE Users.username = ? AND Users.password = ?",(username, passwort))
      result_balance = cursor.fetchone()[0]
      res = f"Welcome {username}. Your Balance is {result_balance}"
      anvil.server.session['login'] = True
      anvil.server.session["injection_possible"] = True
    elif result:
      res = "Login successful but 'AccountNo' was not passed."
      anvil.server.session['login'] = True
      anvil.server.session["injection_possible"] = True
    else:
      raise ValueError("Empty Data")
  except Exception:
    res = f"Login not successful: \nSELECT username FROM Users WHERE username = '{username}' AND password = '{passwort}'"
  return res

@anvil.server.callable
def get_query_params(url):
  query = url.split('?')[-1] if '?' in url else ''
  query = urllib.parse.parse_qs(query)
  return query
  
@anvil.server.callable
def get_data_accountno(accountno):
  conn = sqlite3.connect(data_files["database.db"])
  cursor = conn.cursor()
  querybalance = f"SELECT balance FROM Balances WHERE AccountNo = {accountno}"
  queryusername = f"SELECT username FROM Users WHERE AccountNo = {accountno}"
  try:
    if len(list(cursor.execute(querybalance))) == 0:
      return f"User not found.\n{querybalance}\n{queryusername}"
    else:
      return list(cursor.execute(queryusername)) + list(cursor.execute(querybalance))
  except:
    return ""
    
@anvil.server.callable
def logout():
  anvil.server.session["login"] = False


@anvil.server.callable
def get_user_safe(username, passwort):
  conn = sqlite3.connect(data_files["database.db"])
  cursor =  conn.cursor()
  try:
    res = cursor.execute("SELECT username FROM Users WHERE username = ? AND password = ?", (username, passwort))
    result = cursor.fetchone()
    if result:
      balance = cursor.execute("SELECT Balances.balance FROM Users JOIN Balances ON Users.AccountNo = Balances.AccountNo WHERE Users.username = ? AND Users.password = ?",(username, passwort))
      result_balance = cursor.fetchone()[0]
      res = f"Welcome {username}. Your Balance is {result_balance}"
      anvil.server.session["login"] = True
      anvil.server.session["injection_possible"] = False
    else:
      raise ValueError("Empty Data")
  except Exception:
    res = f"Login not successful: \nSELECT username FROM Users WHERE username = '{username}' AND password = '{passwort}'"
  return res

@anvil.server.callable
def get_data_accountno_safe(accountno):
  conn = sqlite3.connect(data_files["database.db"])
  cursor = conn.cursor()
  querybalance = "SELECT balance FROM Balances WHERE AccountNo = ?", (accountno)
  queryusername = "SELECT username FROM Users WHERE AccountNo = ?", (accountno)
  try:
    if len(list(cursor.execute(querybalance))) == 0:
      return f"User not found.\n{querybalance}\n{queryusername}"
    else:
      return list(cursor.execute(queryusername)) + list(cursor.execute(querybalance))
  except:
    return f"User not found.\n{querybalance}\n{queryusername}"


    
