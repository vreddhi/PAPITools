# PAPITools
This is a wrapper to PAPI framework at akamai

import the module using pip install papitools
 
**Module has below methods or functionalities:**
 

 - getContracts  -- Get all contract related details  ·
 - getPropertyInfo -- Get Sepcific property related details 
 - getGroups -- Get all group related info
 - getAllProperties -- Get all the properties under a contract
 - getPropertyRulesfromPropertyId -- Get rules data of a property
 - getPropertyRules  -- Downloads the configuration in JSON   
 - createVersion  -- Creates a new version of  configuration from base version
 - getVersion – returns property reference of LATEST/STAGING/PRODUCITON version
 - uploadRules – Upload rules to a property/configuration 
 - activateConfiguration  - Activate a configuration in STAGING or PRODUCTION
 - cloneConfig -- clone a configuration 
 - deleteProperty -- delete a configuration
 - listProducts -- list all products under account
 

 
**How to use it (PAPITools Wrapper):**

 - Create an instance/object of Akamai EdgeGrid Session class. 
 - Create an instance/object of papitools class 
 - Call the above methods on papitools object, in desired order to achieve the functionality.

 

**Example command to copy configurations:**
Python3 CustomPAPIActions.py -copy -fconfig="source_config" -tconfig="destination_config" -fver=2 -tver=2


----------


 **NOTE:** 
 CustomPAPIActions.py is a script caller which i have been updating to cover various use-cases
 It is is a script that leverages papiTools.py
   and invokes funtions in them in certain order to achieve below
  
 - activate  -- Activate a configuration     
 - copyConfig -- Copy the configuration     
 - addredirects  -- Add redirect rules from a csv file to a confguration  
 - ForwardPath  -- Add FMP rules from a csv file to configuration   
 - propertyCount -- Count the number of properties in an account    
 - cloneConfig -- CLONE a configuration 
 - deleteProperty  --  Delete the property     
 - advancedCheck  -- Check all the properties in account for the presence of advanced Match
 - listproducts -- Lists all products available in contract
 - cloneConfigList -- clones a list of configurations and updates the productType to Ion
 - cloneAllConfig -- clones all configurations under account and updates the productType to Ion
 - updateSRTO -- updates the STRO object path

