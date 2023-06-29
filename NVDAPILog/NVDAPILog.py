"""This program uses the National Vulnerability Database's free API to 
retrieve Common Vulnerability & Exposure (CVE) records in JSON format.
Those records are then parsed & reformatted as lists, which are added as 
single entries to a SQLite database.  Each list contains the CVE ID, 
date published, date modified, vulnerability description, threat vector string, 
CVSS score, and CWE(s), if applicable.  Missing values are replaced with "NULL."
If a CVE record's CVSS score exceeds a certain value, a dated log file with 
record(s) is also generated.  The log files can be piped to an analytics platform."""

"""The SQLite database serves no purpose beyond a practical demonstration of coding ability."""

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
import sqlite3
import yaml # pip install pyyaml


# Imports values from config file.
with open("Projects/NVDAPILog/config.yml","r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    tDelta = config['timeDelta']
    aScore = config['alertScore']


def makeCVETable():
    """Creates a SQLite table for CVE records if none exists."""
    connection = sqlite3.connect('CVEdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS NVD_CVEs (CVE_ID STRING PRIMARY KEY NOT NULL,
                                                            published STRING, 
                                                            lastModified STRING, 
                                                            description STRING, 
                                                            vectorString STRING, 
                                                            baseScore FLOAT, 
                                                            CWE_ID STRING)''')
    connection.commit()
    connection.close()


def NVDAPI():
    """Submits API request for any CVE updates within the timedelta value."""
    url = 'https://services.nvd.nist.gov/rest/json/cves/2.0/?lastModStartDate='
    pasttime = datetime.datetime.now() - datetime.timedelta(hours=tDelta)
    nowtime = datetime.datetime.now()
    url += pasttime.strftime('%Y-%m-%dT%H:%M:%S.000')
    url += nowtime.strftime('&lastModEndDate=%Y-%m-%dT%H:%M:%S.000')
    # # Prints the concatinated API URL.
    # print(url)
    response = requests.get(url)
    # # Prints the server HTTP response code.
    # print(response)
    response = response.json()
    # # Prints all unformatted JSON results.
    # print(response)
    total = response['totalResults']
    # Prints total number of CVE results from query.
    print()
    print('Total results =', total)
    print()
    # Sends each CVE record to the parseJSON function for reformatting.
    for element in response['vulnerabilities']:
        CVEdbEntry = parseJSON(element)
        addCVE(CVEdbEntry)
        # Checks each CVE's CVSS score.
        if CVEdbEntry[5] == 'NULL':
            pass
        elif float(CVEdbEntry[5]) >= aScore:
            # # Prints each CVE entry that meets the alert threshold.
            # print(CVEdbEntry)
            # print()
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


def addCVE(CVEdbEntry):
    """Adds a CVE entry to the SQLite table."""
    connection = sqlite3.connect('CVEdatabase.db')
    cursor = connection.cursor()
    cursor.executemany('''INSERT OR REPLACE INTO NVD_CVEs (CVE_ID,
                                                published,
                                                lastModified, 
                                                description,
                                                vectorString,
                                                baseScore,
                                                CWE_ID) VALUES (?, ?, ?, ?, ?, ?, ?)''', (CVEdbEntry,))
    connection.commit()
    connection.close()


def createLog(CVEdbEntry):
    """Generates a log file of selected CVEs."""
    logging.basicConfig(filename=datetime.datetime.now().strftime('CVEAlerts_%Y%m%d_%H%M%S.log'), encoding='utf-8', level=logging.INFO)
    logging.info(CVEdbEntry)


def main():
    """The main function."""
    makeCVETable()
    NVDAPI()
    print('Check complete -', datetime.datetime.now())
    print()


if __name__ == '__main__':
    """Calls the main function."""
    main()
