# Simple global configuration system
# Retrieve it with config()
from ConfigParser import SafeConfigParser
from json import dumps, loads


global_config = None


class IiabConfig(SafeConfigParser):
    """Just some conveniences for IIAB configuration"""

    def all_items(self):
        """Return a dictionary of sections with a dictionary of name/value pairs"""
        j = {}
        for section in self.sections():
            js = {}
            for name, value in self.items(section):
                js[name] = self.get(section, name)
            j[section] = js
        return j

    def all_items_to_str(self):
        return dumps(self.all_items(), indent=4)

    def __str__(self):
        return self.all_items_to_str()

    def getjson(self, section, name):
        """Load a configuration value string and interpret
           it as a JSON structure"""
        print "getjson: " + self.get(section, name)
        return loads(self.get(section, name))


def load_config(master_config_file, additional_config_files=[]):
    """First load master_config_file, which is required.
    Then load optional files in the additional_config_files array
    if they exist."""
    global global_config
    config = IiabConfig()
    config.readfp(open(master_config_file, 'r'))
    config.read(additional_config_files)
    global_config = config
    return global_config


def config():
    """Return the global ConfigParser object.
    If the config files have not yet been read, than this
    will load them"""
    global global_config
    if global_config is None:
        raise Exception("config() called before load_config()")
    return global_config
