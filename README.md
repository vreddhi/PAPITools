# PAPITools
This is a wrapper to PAPI framework at akamai

import the module using pip install papitools
 
**Module has below methods or functionalities:**
 

·getPropertyRules  -- Downloads the configuration in JSON format

·createVersion  -- Creates a new version of  configuration from base version 

·getVersion – returns       property reference of LATEST/STAGING/PRODUCITON version

·uploadRules – Upload rules to a property/configuration

·activateConfiguration  - Activate a configuration in STAGING or PRODUCTION


 
**How to use it:**
· Create an instance/object of Akamai EdgeGrid Session class.
· Create an instance/object of papitools class
· Call the above methods on papitools object, in desired order to achieve the functionality.
 
 
**Example command to copy configurations:**
Python3 CustomPAPIActions.py -copy -fconfig="source_config" -tconfig="destination_config" -fver=2 -tver=2
