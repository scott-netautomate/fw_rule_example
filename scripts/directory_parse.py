'''
Functions for parsing the rule example directory
'''

from functools import reduce
import json
import os
import yaml

class ParserError(Exception):
    pass

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    :param rootdir: str -> of directory to search can be with or without
    trailing '/'
    """
    dir = {}
    if not rootdir.endswith('/'):
        rootdir = rootdir + '/'
    start = rootdir.rfind(os.sep) + 1
    walk = os.walk(rootdir)
    exclude = set(['.git']) #this will exclude directories we don't want
    for path, dirs, files in walk:
        if path.__len__() >= start:
            folders = path[start:].split(os.sep)
            subdir = {}
            if files:
                for file in files:
                    if file.endswith('.yml') or file.endswith('.yaml'):
                        subdir.update(**process_files(path, file))
            if folders != ['']:
                parent = reduce(dict.get, folders[:-1], dir)
                parent[folders[-1]] = subdir
            else:
                dir = subdir
    return dir

def process_files(path, file):
    '''
    Processes yaml files and returns them as a dictionary
    :param path: str -> current file path
    :param file: str -> filename
    :return:
    '''
    out_dict = {}
    name = os.path.splitext(os.path.basename(file))
    with open(path+os.sep+file, 'r') as infile:
        data = yaml.load(infile, Loader=yaml.FullLoader)
    if name:
        out_dict[name[0]] = data
        return out_dict
    else:
        return data

def config_getter(in_dict):
    '''
    Only returns the config section of a level if it exists and is not empty
    :param in_dict:
    :return:
    '''
    if in_dict:
        if 'config' in in_dict.keys():
            if in_dict['config']:
                return in_dict.pop('config')
        else:
            return {}
    return {}

def process_fw_rules(path):
    rawdict = get_directory_structure(path)
    config = config_getter(dir)
    if 'unique_prefix' in config.keys():
        if config['unique_prefix']:
            pdict = prepend_names(rawdict)

class DirParser:
    '''
    Class to process a rule directory
    '''
    def __init__(self, rootpath):
        '''
        Initialisation
        :param rootpath: str -> path to folder
        '''
        self.rootpath = rootpath
        self.pdict = get_directory_structure(self.rootpath)
        if 'config' in self.pdict.keys():
            self.config = self.pdict['config']


    def get_dict(self):
        '''
        Returns a dict representation of the folder data
        :return: dict
        '''
        return self.pdict

    def save_json(self, save_path):
        '''
        Saves the data as a json file in the specified path
        :param save_path: str -> path to save file
        :return: boolean
        '''
        try:
            with open(save_path, 'w') as outfile:
                json.dump(self.pdict, outfile, indent=4)
            return True
        except OSError:
            return False


