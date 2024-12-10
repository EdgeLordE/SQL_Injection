from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.js.window

class Form1(Form1Template):
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      
      self.sql_injection_possible = True
      

    def outlined_button_Login_click(self, **event_args):
      """This method is called when the button is clicked"""
      if self.sql_injection_possible is True:
        result_state, result_text = anvil.server.call('get_User', self.text_Username.text, self.text_Password.text)
        url = anvil.js.window.location.href
        query = anvil.server.call('get_query_params', url)
        print(query)
      if self.sql_injection_possible is False:
        result_state, result_text = anvil.server.call('get_User_safe', self.text_Username.text, self.text_Password.text)
      open_form('Form2', result_text, result_state)
      print(anvil.js.window.location.href)

    def check_box_1_change(self, **event_args):
      """This method is called when this checkbox is checked or unchecked"""
      if self.check_box_1.checked is True:
        self.sql_injection_possible = False
      else:
        self.sql_injection_possible = True
      

    
