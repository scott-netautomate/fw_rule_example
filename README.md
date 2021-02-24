# Rule Repo Example

This repo provides an example for storing firewall rules and all related data in a structure of folders and yaml files.

It supports the following structures:
* hosts -> individual host or network items
* objects -> object groups, named collections of hosts
* services -> fw service definitions
* service_groups -> collections of service definitions
* rules -> rule definitions

Additionally the repo supports the adding of meta-data at each folder level through the use of config.yml (or other named file)
Directory_parser has a method which can pick out these files as part of the processing. 

## Directory parser

The directory parser is a script which walks through a give folders structure containing folder names and yaml files. 
It turns these files into structured dictionaries, which can then be saved as json data. 

### Set up

Please install the required dependancies on the requirements.txt file
> pip install -r requirements.txt
### Running

To run the directory parse please run the following. 

```python
from scripts.directory_parse import DirParser
dirparser = DirParser('fw_example')
#Print a dictionary representation
print(dirparser.get_dict())
#Save the dictionary to a json file
dirparser.save_json('outputfile.json')
```
