### This program uses the National Vulnerability Database's free API to 
### retrieve Common Vulnerability & Exposure (CVE) records in JSON format.
### Those records are then parsed & reformatted as lists, which are added as 
### single entries to a SQLite database.  Each list contains the CVE ID, 
### date published, date modified, vulnerability description, threat vector string, 
### CVSS score, and CWE(s), if applicable.  Missing values are replaced with "NULL."
### If a CVE record's CVSS score exceeds a certain value, a dated log file with 
### record(s) is also generated.  The log files can be piped to an analytics platform.

### An accompanying "config.yaml" file may be used to set the
### API's retrieval window & CVSS alert threshold.
### Default values are 2 hours & CVSS 9.0, respectively.

### The SQLite database serves no purpose beyond a practical demonstration of coding ability.

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
with open("config.yml","r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    tDelta = config['timeDelta']
    aScore = config['alertScore']
    # # Prints the current config file values.
    # print(tDelta, aScore)


# Creates a SQLite table for CVE records if none exists.
def makeCVETable():
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


# API request for any CVE updates within the timedelta value.
def NVDAPI():
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


# Parses JSON data into table entries.
def parseJSON(element):
    CVEdbEntry = []
    # Check is there's a CVE entry in the JSON return.
    if 'cve' not in element:
        pass
    # Add the CVE name, published date, and lastModified date to CVEdbEntry.
    else:
        CVEdbEntry.append(element['cve']['id'])
        CVEdbEntry.append(element['cve']['published'])
        CVEdbEntry.append(element['cve']['lastModified'])
        # Add the CVE text description to CVEdbEntry.
        if 'descriptions' not in element['cve']:
            CVEdbEntry.append('NULL')
        elif 'value' not in element['cve']['descriptions'][0]:
            CVEdbEntry.append('NULL')
        else:
            CVEdbEntry.append(element['cve']['descriptions'][0]['value'])
        # Add the CVSS vectorString & baseScore to CVEdbEntry.
        if 'metrics' not in element['cve']:
            CVEdbEntry.extend(['NULL', 'NULL'])
        # If no CVSS metric found.
        elif 'cvssMetricV31' not in element['cve']['metrics'] and 'cvssMetricV30' not in element['cve']['metrics']\
            and 'cvssMetricV2' not in element['cve']['metrics']:
            CVEdbEntry.extend(['NULL', 'NULL'])
        # If only CVSSv2 metric found.
        elif 'cvssMetricV31' not in element['cve']['metrics'] and 'cvssMetricV30' not in element['cve']['metrics']\
            and 'cvssMetricV2' in element['cve']['metrics']:
            CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV2'][0]['cvssData']['vectorString'],\
                               element['cve']['metrics']['cvssMetricV2'][0]['cvssData']['baseScore']])
        # If only CVSSv3.0 metric found.
        elif 'cvssMetricV31' not in element['cve']['metrics'] and 'cvssMetricV30' in element['cve']['metrics']\
            and 'cvssMetricV2' not in element['cve']['metrics']:
            CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV30'][0]['cvssData']['vectorString'],\
                               element['cve']['metrics']['cvssMetricV30'][0]['cvssData']['baseScore']])
        # If only CVSSv3.1 metric found.
        elif 'cvssMetricV31' in element['cve']['metrics'] and 'cvssMetricV30' not in element['cve']['metrics']\
            and 'cvssMetricV2' not in element['cve']['metrics']:
            CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['vectorString'],\
                               element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
        # If both CVSSv3.1 & CVSSv2 metrics found.
        elif 'cvssMetricV31' in element['cve']['metrics'] and 'cvssMetricV30' not in element['cve']['metrics']\
            and 'cvssMetricV2' in element['cve']['metrics']:
            CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['vectorString'],\
                               element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
        # If both CVSSv3.1 & CVSSv3.0 metrics found.
        elif 'cvssMetricV31' in element['cve']['metrics'] and 'cvssMetricV30' in element['cve']['metrics']\
            and 'cvssMetricV2' not in element['cve']['metrics']:
            CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['vectorString'],\
                               element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
        # If both CVSSv3.0 & CVSSv2 metrics found.
        elif 'cvssMetricV31' not in element['cve']['metrics'] and 'cvssMetricV30' in element['cve']['metrics']\
            and 'cvssMetricV2' in element['cve']['metrics']:
            CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV30'][0]['cvssData']['vectorString'],\
                               element['cve']['metrics']['cvssMetricV30'][0]['cvssData']['baseScore']])
        # If all three CVSS metrics found.
        else:
            CVEdbEntry.extend([element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['vectorString'],\
                               element['cve']['metrics']['cvssMetricV31'][0]['cvssData']['baseScore']])
        # Add CWE name(s) to CVEdbEntry.
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
                CWEValues.append(element['cve']['weaknesses'][i]['description'][0]['value'])
            CWEValues = '; '.join(CWEValues)
            CVEdbEntry.append(CWEValues)
    # # Prints each record after it's reformatted.
    # print(CVEdbEntry)
    # print()
    return CVEdbEntry


# Adds a CVE entry to the SQLite table.
def addCVE(CVEdbEntry):
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


# Generates a log file of selected CVEs.
def createLog(CVEdbEntry):
    logging.basicConfig(filename=datetime.datetime.now().strftime('CVEAlerts_%Y%m%d_%H%M%S.log'), encoding='utf-8', level=logging.INFO)
    logging.info(CVEdbEntry)


# The main function.
def main():
    makeCVETable()
    NVDAPI()
    print('Check complete -', datetime.datetime.now())
    print()


# Calls the main function.
if __name__ == '__main__':
    main()
