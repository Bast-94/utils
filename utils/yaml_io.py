import os
import yaml
def read_yaml(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            contenu = yaml.safe_load(file)
    else:
        contenu = {}
    return contenu

def save_config(dictionnaire, file_path="config.yml"):
    with open(file_path, "w") as fichier:
        yaml.dump(dictionnaire, fichier)
    print("Yaml file saved")