import configparser
import os

class access_conf:
    
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.config = configparser.ConfigParser()
        self.section = 'DEFAULT'
        if os.path.isfile(filepath):
            self.read(filepath)
        else:
            self.new_conf()
            self.read(filepath)

    def read(self, filepath: str):
        self.config.read(filepath)

    def change_section(self, section: str):
        self.section = section

    def read_all(self):
        list_of_value = []
        for key in self.config[self.section]:
            list_of_value.append(self.config[self.section][key])
        return list_of_value
    
    def update_conf(self):
        f = open(self.filepath, "w")
        self.config.write(f)
        f.close()

    def new_conf(self):
        f = open(self.filepath, "x")

        self.config[self.section]['enable debug mode'] = 'False'
        self.config[self.section]['enable animations'] = 'True'
        self.config[self.section]['port'] = '0818'
        self.config[self.section]['show console'] = 'False'
        self.config[self.section]['cursor color'] = '(255,255,255)'
        self.config[self.section]['chip move animation speed'] = '0.5'
        self.config[self.section]['enable debug mode'] = 'True'
        self.config.write(f)

    def get(self, key_input:str):
        for key in self.config[self.section]:
            if key_input == key:
                return self.config[self.section][key]
    
    def set(self, key_input:str, value_input: str):
        for key in self.config[self.section]:
            if key_input == key:
                self.config[self.section][key] = value_input
        self.update_conf()
        

if __name__ == "__main__":
    confTest = access_conf("option.conf")
    print(confTest.read_all())
    print(confTest.get('port', ))
    print(confTest.set('enable debug mode', 'True'))
    

