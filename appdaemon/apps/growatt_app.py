import hassapi as hass
import growattServer
import stateLogger
import time

class AD_Growatt(hass.Hass):

    api = 'undefined'
    ui_logger = 'undefined'

    def initialize(self):
        un = self.args["growatt_username"]
        pwd = self.args["growatt_password"]
        device_sn = self.args["growatt_device"]
        settings_action = self.args["settings_action"]
        self.ui_logger = stateLogger.StateLogger(self) #loghger instatnce for UI
        #Obtain the server using the api
        self.api = growattServer.GrowattApi(un, pwd, device_sn, self, self.ui_logger, settings_action) #get an instance of the api, using a random string as the ID
        
        
        self.listen_state(self.get_charge_settings, "input_button.adgw_get_charge_settings_button")
        self.listen_state(self.set_charge_settings_export_handler, "input_button.adgw_set_charge_settings_button_export")
        self.listen_state(self.set_charge_settings_battery_handler, "input_button.adgw_set_charge_settings_button_battery_first")
        self.listen_state(self.set_charge_settings_battery_1_handler, "input_button.adgw_set_charge_settings_button_battery_1_first")
        self.listen_state(self.set_charge_settings_grid_handler, "input_button.adgw_set_charge_settings_button_grid_first")
        self.listen_state(self.set_settings_battery_series_number_handler, "input_button.adgw_set_settings_battery_series")
        self.listen_state(self.set_settings_lv_voltage_handler, "input_button.adgw_set_settings_lv_voltage")
        self.listen_state(self.set_settings_cv_voltage_handler, "input_button.adgw_set_settings_cv_voltage")
        self.listen_state(self.set_active_power_rate_handler, "input_button.adgw_set_active_power_rate")
        #call get_charge_settings by pressing Get charge settings button
        self.call_service("input_button/press", entity_id="input_button.adgw_get_charge_settings_button")

    def get_charge_settings(self, entity, attribute, old, new, kwargs):
        response = self.api.get_mix_inverter_settings()

        #If not hybrind inverter no data
        if (response['obj']) == "":
            return True
                
        # Populate Export
        if (response['obj']['mixBean']['exportLimit']) == "1":
            self.set_state ("input_boolean.adgw_export_limit_on", state = "on")
        else:
            self.set_state ("input_boolean.adgw_export_limit_on", state = "off")
        
        self.set_state ("input_number.adgw_export_limit_power_rate", state = response['obj']['mixBean']['exportLimitPowerRate'])

        # Populate Battery First
        self.set_state("input_select.adgw_battery_charge_max_soc", state = response['obj']['mixBean']['wchargeSOCLowLimit2'])
        self.set_state("input_select.adgw_battery_charge_power", state = response['obj']['mixBean']['wchargeSOCLowLimit1'])

        
        
        if (response['obj']['mixBean']['acChargeEnable']) == "1":
            self.set_state ("input_boolean.adgw_ac_charge_on", state = "on")
        else:
            self.set_state ("input_boolean.adgw_ac_charge_on", state = "off")
        self.set_state("input_datetime.adgw_battery_first_time_slot_1_start", state = response['obj']['mixBean']['forcedChargeTimeStart1'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_1_end", state = response['obj']['mixBean']['forcedChargeTimeStop1'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_2_start", state = response['obj']['mixBean']['forcedChargeTimeStart2'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_2_end", state = response['obj']['mixBean']['forcedChargeTimeStop2'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_3_start", state = response['obj']['mixBean']['forcedChargeTimeStart3'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_3_end", state = response['obj']['mixBean']['forcedChargeTimeStop3'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_4_start", state = response['obj']['mixBean']['forcedChargeTimeStart4'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_4_end", state = response['obj']['mixBean']['forcedChargeTimeStop4'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_5_start", state = response['obj']['mixBean']['forcedChargeTimeStart5'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_5_end", state = response['obj']['mixBean']['forcedChargeTimeStop5'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_6_start", state = response['obj']['mixBean']['forcedChargeTimeStart6'])
        self.set_state("input_datetime.adgw_battery_first_time_slot_6_end", state = response['obj']['mixBean']['forcedChargeTimeStop6'])
        
        
        
        if (response['obj']['mixBean']['forcedChargeStopSwitch1']) == "1":
            self.set_state ("input_boolean.adgw_battery_first_time_slot_1_enabled", state = "on")
        else:
            self.set_state ("input_boolean.adgw_battery_first_time_slot_2_enabled", state = "off")
        if (response['obj']['mixBean']['forcedChargeStopSwitch2']) == "1":
            self.set_state ("input_boolean.adgw_battery_first_time_slot_2_enabled", state = "on")
        else:
            self.set_state ("input_boolean.adgw_battery_first_time_slot_2_enabled", state = "off")
        if (response['obj']['mixBean']['forcedChargeStopSwitch3']) == "1":
            self.set_state ("input_boolean.adgw_battery_first_time_slot_3_enabled", state = "on")
        else:
            self.set_state ("input_boolean.adgw_battery_first_time_slot_3_enabled", state = "off")
        if (response['obj']['mixBean']['forcedChargeStopSwitch4']) == "1":
            self.set_state ("input_boolean.adgw_battery_first_time_slot_4_enabled", state = "on")
        else:
            self.set_state ("input_boolean.adgw_battery_first_time_slot_4_enabled", state = "off")
        if (response['obj']['mixBean']['forcedChargeStopSwitch5']) == "1":
            self.set_state ("input_boolean.adgw_battery_first_time_slot_5_enabled", state = "on")
        else:
            self.set_state ("input_boolean.adgw_battery_first_time_slot_5_enabled", state = "off")
        if (response['obj']['mixBean']['forcedChargeStopSwitch6']) == "1":
            self.set_state ("input_boolean.adgw_battery_first_time_slot_6_enabled", state = "on")
        else:
            self.set_state ("input_boolean.adgw_battery_first_time_slot_6_enabled", state = "off")
            
            

        # Populate Grid First
        self.set_state("input_select.adgw_grid_discharge_stopped_soc", state = response['obj']['mixBean']['wdisChargeSOCLowLimit2'])
        self.set_state("input_select.adgw_grid_discharge_power", state = response['obj']['mixBean']['wdisChargeSOCLowLimit1'])
        self.set_state("input_datetime.adgw_grid_first_time_slot_1_start", state = response['obj']['mixBean']['forcedDischargeTimeStart1'])
        self.set_state("input_datetime.adgw_grid_first_time_slot_1_end", state = response['obj']['mixBean']['forcedDischargeTimeStop1'])
        if (response['obj']['mixBean']['forcedDischargeStopSwitch1']) == "1":
            self.set_state ("input_boolean.adgw_grid_first_time_slot_1_enabled", state = "on")
        else:
            self.set_state ("input_boolean.adgw_grid_first_time_slot_1_enabled", state = "off")

        self.set_state("input_datetime.adgw_grid_first_time_slot_2_start", state = response['obj']['mixBean']['forcedDischargeTimeStart2'])
        self.set_state("input_datetime.adgw_grid_first_time_slot_2_end", state = response['obj']['mixBean']['forcedDischargeTimeStop2'])
        if (response['obj']['mixBean']['forcedDischargeStopSwitch2']) == "1":
            self.set_state ("input_boolean.adgw_grid_first_time_slot_2_enabled", state = "on")
        else:
            self.set_state ("input_boolean.adgw_grid_first_time_slot_2_enabled", state = "off")

        self.set_state("input_datetime.adgw_grid_first_time_slot_3_start", state = response['obj']['mixBean']['forcedDischargeTimeStart3'])
        self.set_state("input_datetime.adgw_grid_first_time_slot_3_end", state = response['obj']['mixBean']['forcedDischargeTimeStop3'])
        if (response['obj']['mixBean']['forcedDischargeStopSwitch3']) == "1":
            self.set_state ("input_boolean.adgw_grid_first_time_slot_3_enabled", state = "on")
        else:
            self.set_state ("input_boolean.adgw_grid_first_time_slot_3_enabled", state = "off")
            
        # Populate Battery Series
        self.set_state("input_select.adgw_battery_series_number", state = response['obj']['mixBean']['batSeriesNum'])
        #populate voltage
        self.set_state("input_number.adgw_cv_voltage", state = response['obj']['mixBean']['cvVoltage'])
        self.set_state("input_number.adgw_lv_voltage", state = response['obj']['mixBean']['lvVoltage'])
        
        self.set_state("input_number.adgw_active_power_rate", state = response['obj']['mixBean']['activeRate'])
        

        
        #List all key pairs from response to log. Comment out before going into production
        #for key, value in response['obj']['mixBean'].items():
        #    self.log(f"{key}: {value}")
        #self.log (response)

        if (response['result']) == 1: # Set status in UI
            self.ui_logger.info("Data Load Success")
        else:
            self.ui_logger.error("Data load failed")

    def set_charge_settings_export(self):

        # Export limit save
        export_limit_on = convert_on_off(self.get_state("input_boolean.adgw_export_limit_on"))
        export_limit_power_rate = self.get_state("input_number.adgw_export_limit_power_rate")
        schedule_settings = [export_limit_on,   #Export limit - Eabled/Disabled (0/1)
                                export_limit_power_rate] #0% export limit means all export is stopped
        response = self.api.update_mix_inverter_setting('backflow_setting', schedule_settings)
        return self.log_response(response, "Export saved")


    def set_charge_settings_export_handler(self, entity, attribute, old, new, kwargs):
        for attempt in range(5):
            if self.set_charge_settings_export() == True:
                break
                
    def set_active_power_rate(self):

        # Export limit save
        active_power_rate = round(float(self.get_state("input_number.adgw_active_power_rate")))
        rate_settings = [active_power_rate] #0% export limit means all export is stopped
        response = self.api.update_mix_inverter_setting('pv_active_p_rate', rate_settings)
        return self.log_response(response, "Power Rate Saved")


    def set_active_power_rate_handler(self, entity, attribute, old, new, kwargs):
        for attempt in range(5):
            if self.set_active_power_rate() == True:
                break

    def set_charge_settings_battery(self):
        #It's good practice to have those values stored in the secrets file
        device_sn = self.args["growatt_device"]

        #Battery first save
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_1_start").split(":")
        start_time = [s.zfill(2) for s in strings]
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_1_end").split(":")
        end_time = [s.zfill(2) for s in strings]
        time_slot_1_enabled = convert_on_off(self.get_state("input_boolean.adgw_battery_first_time_slot_1_enabled"))
        
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_2_start").split(":")
        start_time_2 = [s.zfill(2) for s in strings]
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_2_end").split(":")
        end_time_2 = [s.zfill(2) for s in strings]
        time_slot_2_enabled = convert_on_off(self.get_state("input_boolean.adgw_battery_first_time_slot_2_enabled"))
        
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_3_start").split(":")
        start_time_3 = [s.zfill(2) for s in strings]
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_3_end").split(":")
        end_time_3 = [s.zfill(2) for s in strings]
        time_slot_3_enabled = convert_on_off(self.get_state("input_boolean.adgw_battery_first_time_slot_3_enabled"))
        
        
        charge_final_soc = self.get_state("input_select.adgw_battery_charge_max_soc")
        battery_charge_power = self.get_state("input_select.adgw_battery_charge_power")
        ac_charge_on = convert_on_off(self.get_state("input_boolean.adgw_ac_charge_on"))
        
        
        # Create dictionary of settings to apply through the api call. The order of these elements is important.
        schedule_settings = [battery_charge_power, #Charging power %
                                charge_final_soc.replace("%", ""), #Stop charging SoC %
                                ac_charge_on,   #Allow AC charging (1 = Enabled)
                                start_time[0], start_time[1], #Schedule 1 - Start time
                                end_time[0], end_time[1], #Schedule 1 - End time
                                time_slot_1_enabled,        #Schedule 1 - Enabled/Disabled (1 = Enabled)
                                start_time_2[0], start_time_2[1], #Schedule 2 - Start time
                                end_time_2[0], end_time_2[1], #Schedule 2 - End time
                                time_slot_2_enabled,        #Schedule 2 - Enabled/Disabled (0 = Disabled)
                                start_time_3[0], start_time_3[1], #Schedule 3 - Start time
                                end_time_3[0], end_time_3[1], #Schedule 3 - End time
                                time_slot_3_enabled]        #Schedule 3 - Enabled/Disabled (0 = Disabled)
        # The api call - specifically for the mix inverter. Some other op will need to be applied if you dont have a mix inverter (replace 'mix_ac_charge_time_period')
        response = self.api.update_mix_inverter_setting('mix_ac_charge_time_period', schedule_settings)
        return  self.log_response(response, "Battery first saved (slot: 1-3)")

    def set_charge_settings_battery_1(self):
        #It's good practice to have those values stored in the secrets file
        device_sn = self.args["growatt_device"]

        #Battery first save
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_4_start").split(":")
        start_time_4 = [s.zfill(2) for s in strings]
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_4_end").split(":")
        end_time_4 = [s.zfill(2) for s in strings]
        time_slot_4_enabled = convert_on_off(self.get_state("input_boolean.adgw_battery_first_time_slot_4_enabled"))
        
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_5_start").split(":")
        start_time_5 = [s.zfill(2) for s in strings]
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_5_end").split(":")
        end_time_5 = [s.zfill(2) for s in strings]
        time_slot_5_enabled = convert_on_off(self.get_state("input_boolean.adgw_battery_first_time_slot_5_enabled"))
        
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_6_start").split(":")
        start_time_6 = [s.zfill(2) for s in strings]
        strings = self.get_state("input_datetime.adgw_battery_first_time_slot_6_end").split(":")
        end_time_6 = [s.zfill(2) for s in strings]
        time_slot_6_enabled = convert_on_off(self.get_state("input_boolean.adgw_battery_first_time_slot_6_enabled"))
        
        
        
       
        # Create dictionary of settings to apply through the api call. The order of these elements is important.
        schedule_settings = [start_time_4[0], start_time_4[1], #Schedule 4 - Start time
                                end_time_4[0], end_time_4[1], #Schedule 4 - End time
                                time_slot_4_enabled,        #Schedule 4 - Enabled/Disabled (1 = Enabled)
                                start_time_5[0], start_time_5[1], #Schedule 5 - Start time
                                end_time_5[0], end_time_5[1], #Schedule 5 - End time
                                time_slot_5_enabled,        #Schedule 5 - Enabled/Disabled (0 = Disabled)
                                start_time_6[0], start_time_6[1], #Schedule 6 - Start time
                                end_time_6[0], end_time_6[1], #Schedule 6 - End time
                                time_slot_6_enabled]        #Schedule 6 - Enabled/Disabled (0 = Disabled)
        # The api call - specifically for the mix inverter. Another slots in mix_ac_charge_time_multi_1
        response = self.api.update_mix_inverter_setting('mix_ac_charge_time_multi_1', schedule_settings, True)
        return self.log_response(response, "Battery first 1 saved (slot: 4-6)")


    def set_charge_settings_battery_handler(self, entity, attribute, old, new, kwargs):
        for attempt in range(5):
            if self.set_charge_settings_battery() == True:
                break
                
    def set_charge_settings_battery_1_handler(self, entity, attribute, old, new, kwargs):
        for attempt in range(5):
            if self.set_charge_settings_battery_1() == True:
                break

    def set_charge_settings_grid(self):

        #Grid first save
        #Slot 1
        strings = self.get_state("input_datetime.adgw_grid_first_time_slot_1_start").split(":")
        start_time_1 = [s.zfill(2) for s in strings]
        strings = self.get_state("input_datetime.adgw_grid_first_time_slot_1_end").split(":")
        end_time_1 = [s.zfill(2) for s in strings]
        time_slot_1_enabled = convert_on_off(self.get_state("input_boolean.adgw_grid_first_time_slot_1_enabled"))
        #slot 2
        strings = self.get_state("input_datetime.adgw_grid_first_time_slot_2_start").split(":")
        start_time_2 = [s.zfill(2) for s in strings]
        strings = self.get_state("input_datetime.adgw_grid_first_time_slot_2_end").split(":")
        end_time_2 = [s.zfill(2) for s in strings]
        time_slot_2_enabled = convert_on_off(self.get_state("input_boolean.adgw_grid_first_time_slot_2_enabled"))
        #slot 3
        strings = self.get_state("input_datetime.adgw_grid_first_time_slot_3_start").split(":")
        start_time_3 = [s.zfill(2) for s in strings]
        strings = self.get_state("input_datetime.adgw_grid_first_time_slot_3_end").split(":")
        end_time_3 = [s.zfill(2) for s in strings]
        time_slot_3_enabled = convert_on_off(self.get_state("input_boolean.adgw_grid_first_time_slot_3_enabled"))
        discharge_stopped_soc = self.get_state("input_select.adgw_grid_discharge_stopped_soc")
        discharge_power = self.get_state("input_select.adgw_grid_discharge_power")
        
        # Create dictionary of settings to apply through the api call. The order of these elements is important.
        schedule_settings = [discharge_power, #Discharging power %
                                discharge_stopped_soc, #Stop charging SoC %
                                start_time_1[0], start_time_1[1], #Schedule 1 - Start time
                                end_time_1[0], end_time_1[1], #Schedule 1 - End time
                                time_slot_1_enabled,        #Schedule 1 - Enabled/Disabled (1 = Enabled)
                                start_time_2[0], start_time_2[1], #Schedule 2 - Start time
                                end_time_2[0], end_time_2[1], #Schedule 2 - End time
                                time_slot_2_enabled,        #Schedule 2 - Enabled/Disabled (0 = Disabled)
                                start_time_3[0], start_time_3[1], #Schedule 3 - Start time
                                end_time_3[0], end_time_3[1], #Schedule 3 - End time
                                time_slot_3_enabled]        #Schedule 3 - Enabled/Disabled (0 = Disabled)
        # The api call - specifically for the mix inverter. Some other op will need to be applied if you dont have a mix inverter (replace 'mix_ac_charge_time_period')
        response = self.api.update_mix_inverter_setting('mix_ac_discharge_time_period', schedule_settings)
        return self.log_response(response, "Grid first saved")

    def set_charge_settings_grid_handler(self, entity, attribute, old, new, kwargs):
        for attempt in range(5):
            if self.set_charge_settings_grid() == True:
                break

    def set_settings_battery_series_number(self):

        # Battery series settings
        series_number = self.get_state("input_select.adgw_battery_series_number")
        battery_settings = [series_number] 
        # The api call - specifically for the mix inverter. Some other op will need to be applied if you dont have a mix inverter (replace 'mix_ac_charge_time_period')
        response = self.api.update_mix_inverter_setting('mix_bat_series_num', battery_settings, True)
        return self.log_response(response, "Battery Series Num Saved")

    def set_settings_battery_series_number_handler(self, entity, attribute, old, new, kwargs):
        for attempt in range(5):
            if self.set_settings_battery_series_number() == True:
                break

    def set_settings_cv_voltage(self):

        # CV voltage
        cv_voltage = self.get_state("input_number.adgw_cv_voltage")
        voltage_settings = [cv_voltage] 
        # The api call - specifically for the mix inverter. Some other op will need to be applied if you dont have a mix inverter (replace 'mix_ac_charge_time_period')
        response = self.api.update_mix_inverter_setting('mix_cv_voltage', voltage_settings, True)
        return self.log_response(response, "CV Voltage Saved")

    def set_settings_cv_voltage_handler(self, entity, attribute, old, new, kwargs):
        for attempt in range(5):
            if self.set_settings_cv_voltage() == True:
                break                

    def set_settings_lv_voltage(self):

        # Battery series settings
        lv_voltage = self.get_state("input_number.adgw_lv_voltage")
        voltage_settings = [lv_voltage] 
        # The api call - specifically for the mix inverter. Some other op will need to be applied if you dont have a mix inverter (replace 'mix_ac_charge_time_period')
        response = self.api.update_mix_inverter_setting('mix_lv_voltage', voltage_settings, True)
        return self.log_response(response, "LV Voltage Saved")

    def set_settings_lv_voltage_handler(self, entity, attribute, old, new, kwargs):
        for attempt in range(5):
            if self.set_settings_lv_voltage() == True:
                break                
                                

    def log_response(self, response, message):
        self.log("Response for action [%s] from growat:%s"%(message, response))
        if response['success'] == True:
            self.ui_logger.info(message)
            return True
        else:
            self.ui_logger.error(message + " " + response['msg'])
            return False

def convert_on_off(value):
    # Function to convert on/off to 1/0
    if value == "on":
        return "1"
    else:
        return "0"