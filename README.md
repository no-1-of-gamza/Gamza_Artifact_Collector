----
# Digital Fornsic Windows Artifact Collector
### Window 10, 8, 7

Digital forensic artifacts are evidence or information collected from a digital device.

Digital forensics is the process by which law enforcement agencies, companies, and individuals collect and analyze legally important information in a digital environment. 

It is used in various fields such as criminal investigation, in-house investigation, and data infringement investigation.

Gamza_Artifact_Collector is that Collectng digital forensic artifact <systeminformation, registry files, event log, browser history, trash bin data>

and Collecting specific extnsion files <.pdf, .txt, .xlsx > that usually is used mailcious code 

You can also checked summary.txt each modules that give each artifact infomation
files of summary.txt help summarize data and analysis data

----
## How to Use
### 1. Gamza_Artifact_Collector.exe
```python
      1. Check your Window version (can run Window10, Window8, Window7)
      2. Download this repository matched your Window version
      3. Check files on same folder Gamza_Artifact_Collector.exe and RawCopy.exe, RawCopy64.exe
      4. Run Gamza_Artifact_Collector.exe
      *** Window 7 version can run Window10, Window8 but suggest use this program matched your Window version      
```

### 2. Gamza_Artifact_Collector.py
```python
      1. Check your Python version (can run Python 3.x, 2.x)
      2. Download this repository matched your Python version ->
            if your Python version is 3.x -> Download Window10 ,8 Version (build on Python 3.11.4)
            else if Python version is 2.x -> Download Window7 (build on python 2.7.14)
      3. Check files on same folder Gamza_Artifact_Collector.exe and RawCopy.exe, RawCopy64.exe
         and Check files of modules,
         python 3.x version has subfolder named "Artifact",
         python 2.x version must be same folder with files of moudules
      4. Run Gamza_Artifact_Collector.py
```
```python
python Gamza_Artifact_Collector.py
``` 
---
## Using Option
Default Run is Collecting all of Artifacts data and save Artifacts file

Choose the artifact section you want to collect -a option : all is default and system informatin is collected default all of option

-a t : t is trash bin data
-a r : r is registry data
-a e : e is event log
-a b : b is browser history
```python
python Gamza_Artifact_Collector.py -a t
``` 
```python
python Gamza_Artifact_Collector.py -a r e
``` 

If you want to collect specific extension files, set -s <.extension>
Choose the -s option is Collecting specific extnsion files <".txt", ".pdf", ".doc", ".xlsx", ".zip", ".exe", ".lnk">
```python
python Gamza_Artifact_Collector.py -s .pdf
``` 
```python
python Gamza_Artifact_Collector.py -s txt .zip
```
*this option takes a lot of time, please wait and don't stop this program*

