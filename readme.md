# Introduction
evtx-hunter helps to quickly spot interesting activity in Windows Event Viewer (EVTX) files.

# What is evtx-hunter

evtx-hunter is a Python tool that generates a web report of interesting activity observed
in EVTX files. The tool comes with a few predefined rules to help you get going. This includes
rules to spot for example:
- The first time a certain DNS domain is queried;
- The first time a process is launched;
- New service installations;
- User account lockouts;
- ...

New use cases can easily be added to support your use case:
- ``rules/first_occurence.json``: monitor the first time something happens that matches the rule, such as a certain service being
installed or a compromised user account being used.

  
- ``rules/interesting_events.json``: monitor each time something happens that matches the rule, such as the audit
log being cleared or a new service being instakked.


# Why evtx-hunter?
We developed evtx-hunter to quickly process a large volume of events stored in EVTX dump files during
incident response activities. 
We love tools like [Event Log Explorer](https://eventlogxp.com/) 
and [Evtx Explorer](https://isc.sans.edu/forums/diary/Introduction+to+EvtxEcmd+Evtx+Explorer/25858/) but found them
most suited to deep dive into a specific EVTX file - quickly spotted interesting activity across a large number
of EVTX events is something we were missing - this was the reason to develop and release evtx-hunter.

# Requirements

evtx-hunter only runs on Windows due to its dependency on 
[EVTX Parsing](https://github.com/omerbenamram/EVTX) library, which is included in the tool. 

It requires Python (tested in ``python 3.9`` but any version ``>=python 3.0`` will most likely work).

# Installation
```
pip install -r requirements.txt
```

# Usage
```
python evtx_hunter.py <evtx_folder>
```
Once the EVTX files have been processed, a link on the command line will be printed to view the
generated report in your browser (typically http://127.0.0.1:8050/).

# Roadmap
We plan to continuously improve this tool in a few different ways, based on our experience
using it during incidents where EVTX files require investigation:
- Add new rules to spot new interesting activity in EVTX files;
- Improve how the information is presented in the resulting report;
- Make the reports interactive (live filtering & searching for example).

# Screenshots

![Report header](/documentation/screenshots/report_header.PNG)
![Example of a first time detection](/documentation/screenshots/first_time_example.PNG)

# Contributions
Everyone is invited to contribute! 

If you are a user of the tool and  have a suggestion for a new feature or a bug to report,
please do so through the issue tracker.

# Acknowledgements
Developed by Daan Raman, [@NVISO_labs](https://twitter.com/nviso_labs)

## External libraries
- EVTX Parsing: https://github.com/omerbenamram/EVTX

