from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.js
from anvil.tables import app_tables

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.injection_possible = True
    
    # Any code you write here will run before the form opens.
    state = anvil.server.call('get_login_state')[0]
    if state is True:
      open_form('Form2')


  def outlined_button_Login_click(self, **event_args):
    username = self.text_Username.text
    passwort = self.text_Password.text
    Resultpage = open_form('Form2')
    if self.injection_possible:
      Resultpage.label_Output.text =  anvil.server.call("get_user",username, passwort)
    else:
      Resultpage.label_Output.text = anvil.server.call('get_user_safe', username, passwort)


  def check_box_safe_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.injection_possible = not self.injection_possible
      
    
      
      

    

    

    
