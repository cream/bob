import os
from lxml.etree import parse as parse_xml

class ConfigurationFile(object):
    
    def __init__(self, path):
        
        self.pools = {}
        self.repositories = {}
        self.options = {}
        
        self.path = path
        self.tree = parse_xml(path)
        
        root = self.tree.getroot()

        for elm in root.xpath('//configuration/pool'):
            self.pools[elm.get('id')] = {
                'path': elm.get('path')
            }

        for elm in root.xpath('//configuration/repository'):
            self.repositories[elm.get('id')] = {
                'remote': elm.get('remote'),
                'pool': elm.get('pool'),
            }

        for elm in root.xpath('//configuration/option'):
            self.options[elm.get('key')] = elm.get('value')


class Configuration(object):
    
    def __init__(self):
        
        self.pools = {}
        self.repositories = {}
        self.options = {}

        self.read_configuration(os.path.expanduser('~/.config/bob.xml'))
        self.read_configuration('/etc/bob.xml')
        
        
    def read_configuration(self, path):
        
        try:
            config_file = ConfigurationFile(path)
            
            self.pools.update(config_file.pools)
            self.repositories.update(config_file.repositories)
            self.options.update(config_file.options)
            return True
        except:
            return False
