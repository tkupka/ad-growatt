import hassapi as hass
import growattServer
import time

class AD_Growatt(hass.Hass):

    def initialize(self):
        self.listen_state(self.get_charge_settings, "input_button.adgw_get_charge_settings_button")
        self.listen_state(self.set_charge_settings_export_handler, "input_button.adgw_set_charge_settings_button_export")
        self.listen_state(self.set_charge_settings_battery_handler, "input_button.adgw_set_charge_settings_button_battery_first")
        self.listen_state(self.set_charge_settings_grid_handler, "input_button.adgw_set_charge_settings_button_grid_first")
        #call get_charge_settings by pressing Get charge settings button
        self.call_service("input_button/press", entity_id="input_button.adgw_get_charge_settings_button")

    def get_charge_settings(self, entity, attribute, old, new, kwargs):
        #It's good practice to have those values stored in the secrets file
        un = self.args["growatt_username"]
        pwd = self.args["growatt_password"]
        device_sn = self.args["growatt_device"]
        #Query the server using the api
        api = growattServer.GrowattApi(True) #get an instance of the api, using a random string as the ID
        session = api.login(un, pwd) #login and return a session
        if session['success'] == True: #Handle error message
            self.set_state("sensor.template_adgw_api_state", state = "Initialized")
        else:
            if session["msg"] == "507":
                self.set_state("sensor.template_adgw_api_state", state = "Locked " + session["lockDuration"] + " hours")
            else:
                self.set_state("sensor.template_adgw_api_state", state = "Error Msg " + session["msg"])
            return False
        response = api.get_mix_inverter_settings(device_sn)

        # Populate Export
        if (response['obj']['mixBean']['exportLimit']) == "1":
            self.set_state ("input_boolean.adgw_export_limit_on", state = "on")
        else:
            self.set_state ("input_boolean.adgw_export_limit_on", state = "off")

        # Populate Battery First
        self.set_state("input_select.adgw_battery_charge_max_soc", state = response['obj']['mixBean']['wchargeSOCLowLimit2'])
        self.set_state("input_select.adgw_grid_charge_power", state = response['obj']['mixBean']['chargePowerCommand'])
        
        if (response['obj']['mixBean']['acChargeEnable']) == "1":
            self.set_state ("input_boolean.adgw_ac_charge_on", state = "on")
        else:
            self.set_state ("input_boolean.adgw_ac_charge_on", state = "off")
        self.set_state("input_datetime.adgw_battery_first_time_slot_1_start", state = response['obj']['mixBean']['forcedChargeTimeStart1'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_1_end", state = response['obj']['mixBean']['forcedChargeTimeStop1'])
        if (response['obj']['mixBean']['forcedChargeStopSwitch1']) == "1":
            self.set_state ("input_boolean.adgw_battery_first_time_slot_1_enabled", state = "on")
        else:
            self.set_state ("input_boolean.adgw_battery_first_time_slot_1_enabled", state = "off")

        # Populate Grid First
        self.set_state("input_select.adgw_grid_discharge_stopped_soc", state = response['obj']['mixBean']['wdisChargeSOCLowLimit2'])
        self.set_state("input_select.adgw_grid_discharge_power", state = response['obj']['mixBean']['wdisChargeSOCLowLimit1'])
        self.set_state("input_datetime.adgw_grid_first_time_slot_1_start", state = response['obj']['mixBean']['forcedDischargeTimeStart1'])
        self.set_state("input_datetime.adgw_grid_first_time_slot_1_end", state = response['obj']['mixBean']['forcedDischargeTimeStop1'])
        if (response['obj']['mixBean']['forcedDischargeStopSwitch1']) == "1":
            self.set_state ("input_boolean.adgw_grid_first_time_slot_1_enabled", state = "on")
        else:
            self.set_state ("input_boolean.adgw_grid_first_time_slot_1_enabled", state = "off")

        #List all key pairs from response to log. Comment out before going into production
        for key, value in response['obj']['mixBean'].items():
            self.log(f"{key}: {value}")
        self.log (response)

        if (response['result']) == 1: # Set status in UI
            self.set_state("sensor.template_adgw_api_state", state = "Get success")
        else:
            self.set_state("sensor.template_adgw_api_state", state = "Error getting")

    def set_charge_settings_export(self):
        #It's good practice to have those values stored in the secrets file
        un = self.args["growatt_username"]
        pwd = self.args["growatt_password"]
        device_sn = self.args["growatt_device"]
        #Query the server using the api
        api = growattServer.GrowattApi(True) #get an instance of the api, using a random string as the ID
        session = api.login(un, pwd) #login and return a session
        if session['success'] == True: #Handle error message
            self.set_state("sensor.template_adgw_api_state", state = "Initialized")
        else:
            if session["msg"] == "507":
                self.set_state("sensor.template_adgw_api_state", state = "Locked " + session["lockDuration"] + " hours")
            else:
                self.set_state("sensor.template_adgw_api_state", state = "Error Msg " + session["msg"])
            return False
        # Export limit save
        export_limit_on = convert_on_off(self.get_state("input_boolean.adgw_export_limit_on"))
        schedule_settings = [export_limit_on,   #Export limit - Eabled/Disabled (0/1)
                                "0"] #0% export limit means all export is stopped
        response = api.update_mix_inverter_setting(device_sn, 'backflow_setting', schedule_settings)
        if response['success'] == True:
            self.set_state("sensor.template_adgw_api_state", state = "Export saved")
            return True
        else:
            self.set_state("sensor.template_adgw_api_state", state = "Error saving Export limit: "  + response['msg'])
            return False

    def set_charge_settings_export_handler(self, entity, attribute, old, new, kwargs):
        for attempt in range(5):
            if self.set_charge_settings_export() == True:
                break

    def set_charge_settings_battery(self):
        #It's good practice to have those values stored in the secrets file
        un = self.args["growatt_username"]
        pwd = self.args["growatt_password"]
        device_sn = self.args["growatt_device"]
        #Query the server using the api
        api = growattServer.GrowattApi(True) #get an instance of the api, using a random string as the ID
        session = api.login(un, pwd) #login and return a session
        if session['success'] == True: #Handle error message
            self.set_state("sensor.template_adgw_api_state", state = "Initialized")
        else:
            if session["msg"] == "507":
                self.set_state("sensor.template_adgw_api_state", state = "Locked " + session["lockDuration"] + " hours")
            else:
                self.set_state("sensor.template_adgw_api_state", state = "Error Msg " + session["msg"])
            return False
        #Battery first save
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_1_start").split(":")
        start_time = [s.zfill(2) for s in strings]
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_1_end").split(":")
        end_time = [s.zfill(2) for s in strings]
        charge_final_soc = self.get_state("input_select.adgw_battery_charge_max_soc")
        ac_charge_on = convert_on_off(self.get_state("input_boolean.adgw_ac_charge_on"))
        charge_power = self.get_state("input_select.adgw_grid_charge_power")
        time_slot_1_enabled = convert_on_off(self.get_state("input_boolean.adgw_battery_first_time_slot_1_enabled"))
        # Create dictionary of settings to apply through the api call. The order of these elements is important.
        schedule_settings = [charge_power, #Charging power %
                                charge_final_soc.replace("%", ""), #Stop charging SoC %
                                ac_charge_on,   #Allow AC charging (1 = Enabled)
                                start_time[0], start_time[1], #Schedule 1 - Start time
                                end_time[0], end_time[1], #Schedule 1 - End time
                                time_slot_1_enabled,        #Schedule 1 - Enabled/Disabled (1 = Enabled)
                                "00", "00", #Schedule 2 - Start time
                                "00", "00", #Schedule 2 - End time
                                "0",        #Schedule 2 - Enabled/Disabled (0 = Disabled)
                                "00", "00", #Schedule 3 - Start time
                                "00", "00", #Schedule 3 - End time
                                "0"]        #Schedule 3 - Enabled/Disabled (0 = Disabled)
        # The api call - specifically for the mix inverter. Some other op will need to be applied if you dont have a mix inverter (replace 'mix_ac_charge_time_period')
        response = api.update_mix_inverter_setting(device_sn, 'mix_ac_charge_time_period', schedule_settings)
        if response['success'] == True:
            self.set_state("sensor.template_adgw_api_state", state = "Battery first saved")
            return True
        else:
            self.set_state("sensor.template_adgw_api_state", state = "Error saving Battery first: "  + response['msg'])
            return False

    def set_charge_settings_battery_handler(self, entity, attribute, old, new, kwargs):
        for attempt in range(5):
            if self.set_charge_settings_battery() == True:
                break

    def set_charge_settings_grid(self):
        #It's good practice to have those values stored in the secrets file
        un = self.args["growatt_username"]
        pwd = self.args["growatt_password"]
        device_sn = self.args["growatt_device"]
        #Query the server using the api
        api = growattServer.GrowattApi(True) #get an instance of the api, using a random string as the ID
        session = api.login(un, pwd) #login and return a session
        if session['success'] == True: #Handle error message
            self.set_state("sensor.template_adgw_api_state", state = "Initialized")
        else:
            if session["msg"] == "507":
                self.set_state("sensor.template_adgw_api_state", state = "Locked " + session["lockDuration"] + " hours")
            else:
                self.set_state("sensor.template_adgw_api_state", state = "Error Msg " + session["msg"])
            return False

        #Grid first save
        strings = self.get_state("input_datetime.adgw_grid_first_time_slot_1_start").split(":")
        start_time = [s.zfill(2) for s in strings]
        strings = self.get_state("input_datetime.adgw_grid_first_time_slot_1_end").split(":")
        end_time = [s.zfill(2) for s in strings]
        discharge_stopped_soc = self.get_state("input_select.adgw_grid_discharge_stopped_soc")
        discharge_power = self.get_state("input_select.adgw_grid_discharge_power")
        time_slot_1_enabled = convert_on_off(self.get_state("input_boolean.adgw_grid_first_time_slot_1_enabled"))
        # Create dictionary of settings to apply through the api call. The order of these elements is important.
        schedule_settings = [discharge_power, #Discharging power %
                                discharge_stopped_soc, #Stop charging SoC %
                                start_time[0], start_time[1], #Schedule 1 - Start time
                                end_time[0], end_time[1], #Schedule 1 - End time
                                time_slot_1_enabled,        #Schedule 1 - Enabled/Disabled (1 = Enabled)
                                "00", "00", #Schedule 2 - Start time
                                "00", "00", #Schedule 2 - End time
                                "0",        #Schedule 2 - Enabled/Disabled (0 = Disabled)
                                "00", "00", #Schedule 3 - Start time
                                "00", "00", #Schedule 3 - End time
                                "0"]        #Schedule 3 - Enabled/Disabled (0 = Disabled)
        # The api call - specifically for the mix inverter. Some other op will need to be applied if you dont have a mix inverter (replace 'mix_ac_charge_time_period')
        response = api.update_mix_inverter_setting(device_sn, 'mix_ac_discharge_time_period', schedule_settings)
        if response['success'] == True:
            self.set_state("sensor.template_adgw_api_state", state = "Grid first saved")
            return True
        else:
            self.set_state("sensor.template_adgw_api_state", state = "Error saving Grid first: " + response['msg'])
            return False

    def set_charge_settings_grid_handler(self, entity, attribute, old, new, kwargs):
        for attempt in range(5):
            if self.set_charge_settings_grid() == True:
                break


def convert_on_off(value):
    # Function to convert on/off to 1/0
    if value == "on":
        return "1"
    else:
        return "0"
