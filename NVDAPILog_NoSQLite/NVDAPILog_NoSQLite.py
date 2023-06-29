"""This program uses the National Vulnerability Database's free API to 
retrieve Common Vulnerability & Exposure (CVE) records in JSON format.
If a CVE record's CVSS score exceeds a certain value, the record is 
parsed & reformatted as a list.  Each list contains the CVE ID, date published,
date modified, vulnerability description, threat vector string, CVSS score, 
and CWE(s), if applicable.  Missing values are replaced with "NULL."
A dated log file with record(s) is generated.  The log files could be piped 
to an analytics platform."""

"""An accompanying "config.yaml" file may be used to set the 
API's retrieval window & CVSS alert threshold.
Default values are 2 hours & CVSS 9.0, respectively."""

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###
### This product uses the NVD API but is not endorsed or certified by the NVD. ###
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

# Imports requisite modules.
import datetime
import logging
import requests # pip install requests
import yaml # pip install pyyaml


# Imports values from config file.
with open("Projects/NVDAPILog_NoSQLite/config.yml","r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    tDelta = config['timeDelta']
    aScore = config['alertScore']


def NVDAPI():
    """Submits API request for any CVE updates within the timedelta value.  
    Checks if a returned CVE record's CVSS score exceeds the alertScore value."""
    url = 'https://services.nvd.nist.gov/rest/json/cves/2.0/?lastModStartDate='
    pasttime = datetime.datetime.now() - datetime.timedelta(hours=tDelta)
    nowtime = datetime.datetime.now()
    url += pasttime.strftime('%Y-%m-%dT%H:%M:%S.000')
    url += nowtime.strftime('&lastModEndDate=%Y-%m-%dT%H:%M:%S.000')
    response = requests.get(url)
    response = response.json()
    total = response['totalResults']
    # Prints total number of CVE results from query.
    print()
    print('Total results =', total)
    print()
    # Sends each CVE record to the parseJSON function for reformatting.
    for element in response['vulnerabilities']:
        # Sets variables to reduce program size.
        isV31 = 'cvssMetricV31' in element['cve']['metrics'] ### Might be redundant?  Only used on line 74.
        isntV31 = 'cvssMetricV31' not in element['cve']['metrics']
        isV30 = 'cvssMetricV30' in element['cve']['metrics']
        isntV30 = 'cvssMetricV30' not in element['cve']['metrics']
        isV2 = 'cvssMetricV2' in element['cve']['metrics']
        isntV2 = 'cvssMetricV2' not in element['cve']['metrics']
        # If no CVSS metrics found.
        if 'metrics' not in element['cve']:
            CVSSScore = [0.0]
        # If no CVSSv3.1 metric found:       
        elif isntV31:
            # If no other CVSS metrics found.
            if isntV30 and isntV2:
                CVSSScore = [0.0]
            # If only CVSSv2 metric found.
            elif isntV30 and isV2:
                CVSSScore = ([element['cve']['metrics']['cvssMetricV2'][0]['cvssData']['baseScore']])
            # If only CVSSv3.0 metric found.
            elif isV30 and isntV2:
                CVSSScore = ([element['cve']['metrics']['cvssMetricV30'][0]['cvssData']['baseScore']])
            # If both CVSSv3.0 & CVSSv2 metrics found.
            elif isV30 and isV2:
                CVSSScore = ([element['cve']['metrics']['cvssMetricV30'][0]['cvssData']['baseScore']])
        # If CVSSv3.1 metric is found.
        elif isV31:  ### Switch to "else:"?
            # If only CVSSv3.1 metric is found.
            if isntV30 and isntV2:
                CVSSScore = ([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
            # If both CVSSv3.1 & CVSSv2 metrics found.
            elif isntV30 and isV2:
                CVSSScore = ([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
            # If both CVSSv3.1 & CVSSv3.0 metrics found.
            elif isV30 and isntV2:
                CVSSScore = ([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
            # If all three CVSS metrics found.     
            else:
                CVSSScore = ([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
        newScore = float(CVSSScore[0])
        if newScore >= aScore:
            CVEdbEntry = parseJSON(element)
            createLog(CVEdbEntry)
            print('Log entry created:', CVEdbEntry[0], '-', CVEdbEntry[5])
            print()


def parseJSON(element):
    """Parses JSON data into a list of values."""
    CVEdbEntry = []
    # Checks if there's a CVE entry in the JSON return.
    if 'cve' not in element:
        pass
    # Adds the CVE name, published date, and lastModified date to CVEdbEntry.
    else:
        CVEdbEntry.append(element['cve']['id'])
        CVEdbEntry.append(element['cve']['published'])
        CVEdbEntry.append(element['cve']['lastModified'])
        # Adds the CVE text description to CVEdbEntry.
        if 'descriptions' not in element['cve']:
            CVEdbEntry.append('NULL')
        elif 'value' not in element['cve']['descriptions'][0]:
            CVEdbEntry.append('NULL')
        else:
            CVEdbEntry.append(element['cve']['descriptions'][0]['value'])       
        # Sets variables to reduce program size.
        isV31 = 'cvssMetricV31' in element['cve']['metrics'] ### Might be redundant?  Only used on line 142.
        isntV31 = 'cvssMetricV31' not in element['cve']['metrics']
        isV30 = 'cvssMetricV30' in element['cve']['metrics']
        isntV30 = 'cvssMetricV30' not in element['cve']['metrics']
        isV2 = 'cvssMetricV2' in element['cve']['metrics']
        isntV2 = 'cvssMetricV2' not in element['cve']['metrics']    
        # Adds the CVSS vectorString & baseScore to CVEdbEntry.  
        # If no CVSS metrics found.
        if 'metrics' not in element['cve']:
            CVEdbEntry.extend(['NULL', 'NULL'])
        # If no CVSSv3.1 metric found:       
        elif isntV31:
            # If no other CVSS metrics found.
            if isntV30 and isntV2:
                CVEdbEntry.extend(['NULL', 'NULL'])
            # If only CVSSv2 metric found.
            elif isntV30 and isV2:
                CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV2'][0]['cvssData']['vectorString'],\
                                   element['cve']['metrics']['cvssMetricV2'][0]['cvssData']['baseScore']])
            # If only CVSSv3.0 metric found.
            elif isV30 and isntV2:
                CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV30'][0]['cvssData']['vectorString'],\
                                element['cve']['metrics']['cvssMetricV30'][0]['cvssData']['baseScore']])
            # If both CVSSv3.0 & CVSSv2 metrics found.
            elif isV30 and isV2:
                CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV30'][0]['cvssData']['vectorString'],\
                                   element['cve']['metrics']['cvssMetricV30'][0]['cvssData']['baseScore']])
        # If CVSSv3.1 metric is found.
        elif isV31:  ### Switch to "else:"?
            # If only CVSSv3.1 metric is found.
            if isntV30 and isntV2:
                CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['vectorString'],\
                                   element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
            # If both CVSSv3.1 & CVSSv2 metrics found.
            elif isntV30 and isV2:
                CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['vectorString'],\
                                   element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
            # If both CVSSv3.1 & CVSSv3.0 metrics found.
            elif isV30 and isntV2:
                CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['vectorString'],\
                                   element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
            # If all three CVSS metrics found.     
            else:
                CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['vectorString'],\
                                   element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
        # Adds CWE name(s) to CVEdbEntry.
        if 'weaknesses' not in element['cve']:
            CVEdbEntry.append('NULL')
        elif len(element['cve']['weaknesses']) == 0:
            CVEdbEntry.append('NULL')
        elif 'description' not in element['cve']['weaknesses'][0]:
            CVEdbEntry.append('NULL')
        elif len(element['cve']['weaknesses'][0]['description']) == 0:
            CVEdbEntry.append('NULL')
        elif 'value' not in element['cve']['weaknesses'][0]['description'][0]:
            CVEdbEntry.append('NULL')
        elif element['cve']['weaknesses'][0]['description'][0]['value'] == 'NVD-CWE-noinfo':
            CVEdbEntry.append('NULL')
        elif element['cve']['weaknesses'][0]['description'][0]['value'] == 'NVD-CWE-Other':
            CVEdbEntry.append('NULL')
        else:
            CWEValues = []
            for i in range(len(element['cve']['weaknesses'])):
                if element['cve']['weaknesses'][i]['description'][0]['value'] == 'NVD-CWE-noinfo':
                    CVEdbEntry.append('NULL')
                elif element['cve']['weaknesses'][i]['description'][0]['value'] == 'NVD-CWE-Other':
                    CVEdbEntry.append('NULL')
                else:
                    CWEValues.append(element['cve']['weaknesses'][i]['description'][0]['value'])
            CWEValues = '; '.join(CWEValues)
            CVEdbEntry.append(CWEValues)
    return CVEdbEntry


def createLog(CVEdbEntry):
    """Generates a log file of selected CVEs."""
    logging.basicConfig(filename=datetime.datetime.now().strftime('CVEAlerts_%Y%m%d_%H%M%S.log'), encoding='utf-8', level=logging.INFO)
    logging.info(CVEdbEntry)


def main():
    """The main function."""
    NVDAPI()
    print('Check complete -', datetime.datetime.now())
    print()


if __name__ == '__main__':
    """Calls the main function."""
    main()
