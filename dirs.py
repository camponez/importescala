class Dir:
    def __init__(self, userdata_dir):
        self.data_dir = userdata_dir

    def get_data_dir(self):
        return self.data_dir

    def get_data_file(self, _file):
        return self.get_data_dir() + _file

class DevelDir(Dir):
    def __init__(self):
        self.data_dir = "./"

class TestDir(Dir):
    def __init__(self):
        self.data_dir = "./test/"

DEFAULT_DIR = None

def set_default_dir(_dir):
    DEFAULT_DIR = _dir

def get_default_dir():
    global DEFAULT_DIR
    if DEFAULT_DIR == None:
        DEFAULT_DIR = DevelDir()
    return DEFAULT_DIR

# vim:tabstop=4:expandtab:smartindent
