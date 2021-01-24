from threading import Thread
from time import sleep
from timeit import default_timer as timer
from importlib import import_module
import os, sys, inspect, json, errno

               
class Config:

    DEFAULT_CONFIG = { 'module_list': [
                           'BigWorld'
                       ],
                       'show_magic_methods': False
                     }
                     
    DEFAULT_FILEPATH = 'mods/configs/builtins_dump/builtins_dump.json'

    def __init__(self):
        self.module_list = Config.DEFAULT_CONFIG['module_list']
        self.show_magic_methods = Config.DEFAULT_CONFIG['show_magic_methods']
        
        
    def to_dict(self):
        return { 'module_list': self.module_list,
                 'show_magic_methods': self.show_magic_methods
               }
        
    def save_config(self):
        if not os.path.exists(os.path.dirname(Config.DEFAULT_FILEPATH)):
            try:
                os.makedirs(os.path.dirname(Config.DEFAULT_FILEPATH))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        try:
            with open(Config.DEFAULT_FILEPATH, 'w+') as json_file:
                json.dump(self.to_dict(), json_file, indent=4)
        except IOError as e:
            print '[BUILTINS DUMP] Failed to save config file! Falling back to default config...'    
    
    @classmethod
    def from_file(cls):
        config = cls()
        try:
            with open(Config.DEFAULT_FILEPATH) as json_file:
                try:
                    config_json = json.load(json_file)
                    config.module_list = config_json['module_list']
                    config.show_magic_methods = config_json['show_magic_methods']
                    return config
                except (ValueError, KeyError) as jsonerror:
                    print '[BUILTINS DUMP] Invalid config file! Falling back to default config...'
                    return config
        except IOError as ioerror:
            print '[BUILTINS DUMP] Config file missing! Creating a new one...'
            config.save_config()
            return config
            
        
                 
def dump_module(module_name, show_magic_methods):
    start = timer()
    try:
        module = import_module(module_name)
    except ImportError as e:
        print '[BUILTINS DUMP] Module \"{}\" not found. Skipping'.format(module_name)
        return
    
    with open('dumps/{}.dump'.format(module_name), 'w+') as f:
        #print >>f, sys.builtin_module_names
        print >>f, 'Dumping {} module...'.format(module_name)
        for name, data in inspect.getmembers(module):
            print >>f, '{} : {!r}'.format(name, data)
            
            if inspect.isclass(data) or inspect.ismethod(data) or inspect.isfunction(data) or inspect.isbuiltin(data):
                for name2, data2 in inspect.getmembers(data):
                    if not show_magic_methods and name2 != '__init__' and name2.startswith('__') and name2.endswith('__'):
                        continue
                    print >>f, '    {} : {!r}'.format(name2, data2)
                       
                print >>f, '\n'
        end = timer()
        print >>f, 'End of {} dump ({:.4f} sec)'.format(module_name, (end - start))

def dump_modules(config):
    if not os.path.exists('dumps'):
        os.makedirs('dumps')
        
    for module_name in config.module_list:
        dump_module(module_name, config.show_magic_methods)


thread = Thread(target = dump_modules, args=(Config.from_file(),))
thread.start()