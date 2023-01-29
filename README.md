# msfs_keybindings
A small python script to read Microsoft Flight Simulator 2020 input profiles (your controller settings for keyboards, flightsticks,...) and produce nice formatted Overviews.
- export csv files
- export excel xls files
- create latex tex-files to make pdf documents

Dieses kurze Skript liest einzelne oder alle Inputprofile des Microsoft Flugsimulators 2020.
Aus den eingelesenen Kontrollerzuordnungen und Hotkeys können neben csv- und excel-Dateien insbesondere latex-Quelldatein prodiziert werden, die später in eine pdf-Datei umgerehnet werden können.

Zur besseren Übersichtlichkeit können bestimmte Topics gefiltert werden.

# Usage:
usage: msfs_keybindings.py [-h] [-l LANGUAGE] [-c] [-x] [-t] [-k KEEP | -d DROP] [-o OUTPUT] [-p PATH] [-i IMAGESPATH] [-u USERCFGPATH]
                           [-v {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                           filename

Read msfs2020 input device configurations and create readable documents

positional arguments:
  filename

options:
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        Select language for descriptions, i.e. en-US, de-DE,...
  -c, --csv             Save as CSV.
  -x, --xls             Save as Excel xls.
  -t, --tex             Save as Latex-Template
  -k KEEP, --keep KEEP  keep these CONTEXT entrys
  -d DROP, --drop DROP  drop these CONTEXT entrys
  -o OUTPUT, --output OUTPUT
                        Name for output file
  -p PATH, --path PATH  Path for output image
  -i IMAGESPATH, --imagespath IMAGESPATH
                        Path for device images
  -u USERCFGPATH, --usercfgpath USERCFGPATH
                        Path for user config
  -v {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --verbose {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level


