# This collection of projects is a practical demonstration of ability.
## Comments, feedback, & professional inquiries are welcome.

"NVDAPILog.py" & "NVDAPILog_NoSQLite.py" perform similar functions.  Both programs use the National Vulnerability Database's free API to retrieve Common Vulnerability & Exposure (CVE) records in JSON format.  The API retrieves any CVE record created or modified within _n_ hours of the current time, where _n_ is a variable that can be set in an accompanying config.yaml file.  The CVE records are parsed & reformatted as lists, and if any record has a CVSS score greater than _x_ (another configurable variable), a log file with records is generated.  The default values for _n_ & _x_ are "2" & "9.0," respectively.

"NVDAPILog.py" creates a SQLite database, “CVEdatabase.db,” and records reformatted CVE records before checking their CVSS score.  The SQLite database serves no purpose beyond recordkeeping, though it may prove useful in future iterations of the program.

"NVDAPILog_NoSQLite.py" does not create a database, and checks each CVE’s CVSS score _before_ parsing it.  A record is only reformatted if the score triggers a log entry.

"CoPy_v100.py" is a mini-RPG with GUI.  It was written in June of 2022.
