from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form2(Form2Template):
  def __init__(self, result_text, result_state, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.result_text = result_text
    self.result_state = result_state
  
    if self.result_state is False:
      self.label_Output.text = f"Login failed\n{self.result_text}"
    if self.result_state is True:
      self.label_Output.text = "Login successful"
    
    # Any code you write here will run before the form opens.

  def outlined_button_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Form1")
