name = "stateLogger"

import datetime

class StateLogger:
    
    hass = ''
    

    def __init__(self,  hass):
        self.hass = hass


    def info(self, message):
        self.hass.set_state("sensor.template_adgw_api_state", state = self.format_message(message))
        
    def error(self, message):
        self.hass.set_state("sensor.template_adgw_api_state", state = self.format_message("Error: %s"%message))
        
    def format_message(self, message):
        timestamp = datetime.datetime.now().strftime('%H:%M')
        return "%s [%s]" %(message, timestamp)