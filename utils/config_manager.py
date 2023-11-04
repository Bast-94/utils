
from src.yaml_io import read_yaml, save_config
def assign_value_to_nested_dict(dictionnary, keys, value):
    if len(keys) == 1:
        dictionnary[keys[0]] = value
    else:
        key = keys[0]
        if key not in dictionnary:
            dictionnary[key] = {}
        assign_value_to_nested_dict(dictionnary[key], keys[1:], value)

class ConfigManager():
    def __init__(self, file_name):
        config_dict = read_yaml(file_name)
        self.config_dict = config_dict
        self.file_name = file_name
        self.short_cut_dict = {}
    def save_config(self, file_name=None):
        if file_name is None:
            save_config(self.config_dict, self.file_name)
        else:
            save_config(self.config_dict, file_name)
        
    def make_shortcut(self, shortcut_name, *keys_path):
        self.short_cut_dict[shortcut_name] = keys_path
    
    def get_by_shortcut(self, shortcut_name):
        keys_path = self.short_cut_dict.get(shortcut_name)
        if keys_path is None:
            raise KeyError(f"Shortcut {shortcut_name} not found")
        return self.get_config(*keys_path)
    
    def set_file_name(self, file_name):
        self.file_name = file_name
    
    def get_config(self, *keys_path):
        cur_val = self.config_dict
        for current_key in keys_path:
            cur_val = cur_val.get(current_key)
            # throw an error if the key is not found
            if cur_val is None:
                raise KeyError(f"Config path {keys_path} not found at {current_key}")
            
        return cur_val
    
    def set_config(self, keys_path:str | list[str], value):
        if isinstance(keys_path, str):
            keys_path = [keys_path]
        assign_value_to_nested_dict(self.config_dict, keys_path, value)