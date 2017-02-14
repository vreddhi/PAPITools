from papitools import papitools
import configparser
import requests, logging, json, sys
from akamai.edgegrid import EdgeGridAuth
import urllib
import json
import argparse
#Program start here

parser = argparse.ArgumentParser()
parser.add_argument("-act","--activate", help="Activate configuration specified in property_name in .config.txt", action="store_true")
parser.add_argument("-copy","--copyConfig", help="Used to copy source configuration to destination configuration", action="store_true")
parser.add_argument("-config","--Configuration", help="Name of Configuration/Property")
parser.add_argument("-ver","--Version", help="Version of Configuration/Property")
parser.add_argument("-net","--network", help="Network to be activated on")
parser.add_argument("-fconfig","--fromConfiguration", help="Name of fromConfiguration")
parser.add_argument("-tconfig","--toConfiguration", help="Name of toConfiguration")
parser.add_argument("-fver","--fromVersion", help="Config version of fromConfiguration")
parser.add_argument("-tver","--toVersion", help="Config version of toConfiguration")
parser.add_argument("-d","--download", help="Download configuration and display JSON in console", action="store_true")
parser.add_argument("-ar","--addredirects", help="Append Redirect Rules from a csv File", action="store_true")
parser.add_argument("-pc","--propertyCount", help="Count properties", action="store_true")
parser.add_argument("-fmp","--ForwardPath", help="Add FMP Rules from a csv File", action="store_true")
args = parser.parse_args()



try:
    config = configparser.ConfigParser()
    config.read('.config.txt')
    client_token = config['CREDENTIALS']['client_token']
    client_secret = config['CREDENTIALS']['client_secret']
    access_token = config['CREDENTIALS']['access_token']
    access_hostname = config['CREDENTIALS']['access_hostname']
    session = requests.Session()
    session.auth = EdgeGridAuth(
    			client_token = client_token,
    			client_secret = client_secret,
    			access_token = access_token
                )
except (NameError,AttributeError):
    print("\nUse -h to know the options to run program\n")
    exit()

if not args.copyConfig and not args.download and not args.activate and not args.addredirects and not \
    args.propertyCount and not args.ForwardPath and not args.fromConfiguration and not args.toConfiguration and not \
    args.fromVersion and not args.toVersion and not args.Configuration and not args.Version and not args.network:
    print("\nUse -h to know the options to run program\n")
    exit()


if args.activate:
    print("\nHang on... while we activate configuration.. This will take time..\n")
    print("\nSetting up the pre-requisites...\n")
    PapiToolsObject = papitools.Papitools(access_hostname=access_hostname)
    print("\nTrying to activate configuration..\n")
    property_name = args.Configuration
    version = args.Version
    network = args.network
    activationResponseObj = PapiToolsObject.activateConfiguration(session, property_name, version, network, emails, notes)


if args.copyConfig:
    #Initialise Source Property Information
    print("\nHang on... while we copy rules.. This will take time..")
    fromVersion = args.fromVersion
    toVersion = args.toVersion
    fromConfiguration = args.fromConfiguration
    toConfiguration = args.toConfiguration
    if fromVersion is None or toVersion is None or fromConfiguration is None or toConfiguration is None:
        print('\nMandatory arguments missing\n')
        exit()
    PapiToolsObject = papitools.Papitools(access_hostname=access_hostname)
    fromRulesObject = PapiToolsObject.getPropertyRules(session, fromConfiguration, fromVersion)
    if fromRulesObject.status_code != 200:
        print(fromRulesObject.json())
        exit()
    fromPropertyRules = fromRulesObject.json()['rules']
    #Initialise destination Property Information
    toPropertyDetails = PapiToolsObject.getPropertyRules(session, toConfiguration, toVersion).json()
    toPropertyDetails['rules'] = fromPropertyRules
    PapiToolsObject.uploadRules(session, toPropertyDetails, toConfiguration, toVersion)

if args.download:
    print("\nSetting up the pre-requisites...\n")
    PapiToolsObject = papitools.Papitools(access_hostname=access_hostname)
    print("\nHang on... while we download the json data.. ")
    print("\nHang on... We are almost set, fetching the rules now.. This will take time..\n")
    rulesObject = PapiToolsObject.getPropertyRules(session,property_name,version)
    print(json.dumps(rulesObject.json()['rules']))

if args.addredirects:
    csvTojsonObj = csvTojsonParser.optionSelector()
    print("\nConvert csv to Json is finished.. ")
    print("\nSetting up the pre-requisites...\n")
    redirectJsonData = csvTojsonObj.parseCSVFile()
    destPropertyObject = PropertyDetails.Property(dest_access_hostname, dest_property_name, dest_version, dest_notes, dest_emails)
    PAPIWrapperObject = PAPIWrapper.PAPIWrapper()
    print("\nWe are now fetching the property details like ID, contractId and GroupID\n")
    destGroupsInfo = PAPIWrapperObject.getGroups(destSession, destPropertyObject)
    PAPIWrapperObject.getPropertyInfo(destSession, destPropertyObject, destGroupsInfo)
    print("\nHang on... Fetching property rules now.. This will take time..\n")
    destPropertyRules = PAPIWrapperObject.getPropertyRules(destSession, destPropertyObject).json()
    destPropertyRules['rules']['children'].append(redirectJsonData)
    print("\nHang on... We are almost set, Updating with the rules now.. This will again take time..\n")
    updateObjectResponse = PAPIWrapperObject.uploadRules(destSession, destPropertyObject, destPropertyRules)

if args.ForwardPath:
    csvTojsonObj = csvTojsonParser.optionSelector()
    print("\nConvert csv to Json is finished.. ")
    print("\nSetting up the pre-requisites...\n")
    FMPJsonData = csvTojsonObj.parseCSVFile()
    PapiToolsObject = papitools.Papitools(access_hostname=access_hostname)
    print("\nHang on... while we download the json data.. ")
    print("\nHang on... We are almost set, fetching the rules now.. This will take time..\n")
    propertyRules = PapiToolsObject.getPropertyRules(session,property_name,version).json()
    print(json.dumps(propertyRules))
    propertyRules['rules']['children'].append(FMPJsonData)
    print("\nHang on... We are almost set, Updating with the rules now.. This will again take time..\n")
    updateObjectResponse = PapiToolsObject.uploadRules(session, propertyRules,property_name, version)
    print(updateObjectResponse.json())


if args.propertyCount:
    print("\nHang on... while we Count properties.. ")
    propertyObject = PropertyDetails.Property(access_hostname, property_name, version, notes, emails)
    print("\nSetting up the pre-requisites...\n")
    PAPIWrapperObject = PAPIWrapper.PAPIWrapper()
    groupsInfo = PAPIWrapperObject.getGroups(session, propertyObject)
    print("\nWe are now fetching the property details like ID, contractId and GroupID\n")
    count = 1
    for eachDataGroup in groupsInfo.json()['groups']['items']:
        try:
            contractId = [eachDataGroup['contractIds'][0]]
            groupId = [eachDataGroup['groupId']]
            url = 'https://' + propertyObject.access_hostname + '/papi/v0/properties/?contractId=' + contractId[0] +'&groupId=' + groupId[0]
            propertiesResponse = session.get(url)
            if propertiesResponse.status_code == 200:
                propertiesResponseJson = propertiesResponse.json()
                propertiesList = propertiesResponseJson['properties']['items']
                for propertyInfo in propertiesList:
                    propertyName = propertyInfo['propertyName']
                    propertyId = propertyInfo['propertyId']
                    propertyContractId = propertyInfo['contractId']
                    propertyGroupId = propertyInfo['groupId']
                    print(str(count) + ". propertyName: " + propertyName)
                    count += 1
        except KeyError:
            pass