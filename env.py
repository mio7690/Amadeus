import yaml
import os

def get_yaml_data(yaml_file):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    data = yaml.load(file_data, Loader=yaml.SafeLoader)
    return data

current_path = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.join(current_path, "env.yaml")
config = get_yaml_data(yaml_path)
for k,v in config.items():
    print(f"export {k}={v}")
