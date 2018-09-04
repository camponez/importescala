class Dir:
    def __init__(self, userdata_dir):
        self.data_dir = userdata_dir

    def get_data_dir(self):
        return self.data_dir

    def get_data_file(self, file):
        return self.get_data_dir() + file

class DevelDir(Dir):
    def __init__(self):
        self.data_dir = "./"

class TestDir(Dir):
    def __init__(self):
        self.data_dir = "./test/"

default_dir = None

def set_default_dir(dir):
    default_dir = dir

def get_default_dir():
    global default_dir
    if default_dir == None:
        default_dir = DevelDir()
    return default_dir

# vim:tabstop=4:expandtab:smartindent
