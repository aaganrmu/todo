import yaml

class Config():
    def __init__(self, path):
        self._path = path
        with  open(self._path, "r") as file:
            self._config = yaml.safe_load(file)

    def save(self):
        with open(self._path, "w") as file:
            yaml.dumps(self._config, file)

    @property
    def file_path(self):
        return self._config["file_path"]

    @file_path.setter
    def file_path(self, file_path):
        self._config["file_path"] = file_path
        self.save() 
