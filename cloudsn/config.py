import ConfigParser
import xdg.BaseDirectory as bd

class SettingsController:

    CONFIG_HOME = bd.xdg_config_home + '/cloud-services-notifications'
    CONFIG_PREFERENCES = CONFIG_HOME + '/preferences'
    CONFIG_ACCOUNTS = CONFIG_HOME + '/accounts'
    
    def __init__(self):
        self.config_pref = ConfigParser.ConfigParser()
        self.config_pref.read (self.CONFIG_PREFERENCES)
        self.config_acc = ConfigParser.ConfigParser()
        self.config_acc.read (self.CONFIG_ACCOUNTS)

    def get_account_list (self):
        return self.config_acc.sections ()
        
    def get_account_items (self, account):
        return self.config_acc.items (account)
        
    def get_account_value (self, account, key):
        return self.config_acc.get (account, key)

_settings_controller = None

def GetSettingsController():
        global _settings_controller
        if _settings_controller is None:
                _settings_controller = SettingsController()
        return _settings_controller