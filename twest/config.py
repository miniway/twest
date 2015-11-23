import sys
import ConfigParser

class Config(object):

    def __init__(self):
        self.config = ConfigParser.ConfigParser() 
        pass

    def init(self, path, **additionals):
        self.config.read(path)
        
        for section, options in additionals.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            
            for k,v in options.items():
                self.config.set(section, k, str(v))

        self.config.write(sys.stdout)

    def get_list_confs(self, section, defaults = {}):
        if not self.config.has_section(section):
            return [defaults]

        result = []
        for k, v in self.config.items(section):
            sp = k.split('.')
            idx = int(sp[1])
            while idx >= len(result):
                result.append(dict(defaults))

            result[idx][sp[0]] = v

        return result

    def get_confs(self, section, defaults = {}):

        result = dict(defaults)
        if not self.config.has_section(section):
            return result

        for k, v in self.config.items(section):
            result[k] = v

        return result

    def get_conf(self, section, option, default = None):

        value = self.config.get(section, option, True)
        if value is None:
            value = default
        return value

    def sections(self):
        return self.config.sections()

    def has_section(self, section):
        return self.config.has_section(section)

    get = get_conf
    get_config = get_conf
    get_configs = get_confs
    get_list_configs = get_list_confs


instances = {}

def new_config(name, path, **kw):
    config = Config()
    config.init(path, **kw)
    instances[name] = config

def get_config(name):
    return instances.get(name, Config())

