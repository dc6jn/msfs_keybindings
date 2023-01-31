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


<pre><font color="#55FF55"><b></b></font>:<font color="#5555FF"><b>~/Dokumente/msfs_keybindings</b></font>$ python ./msfs_keybindings.py data/inputprofile_0306217088 
<font color="#00AA00">2023-01-31 07:46:51.950</font> | <b>INFO    </b> | <font color="#5555FF">msfs_keybindings.py:</font><font color="#5555FF"><b>  94</b></font> <font color="#00AAAA">__main__</font>:<font color="#00AAAA">&lt;module&gt;</font> | <b>Using outputpath ***/Dokumente/msfs_keybindings</b>
<font color="#00AA00">2023-01-31 07:46:51.954</font> | <b>INFO    </b> | <font color="#5555FF">msfs_keybindings.py:</font><font color="#5555FF"><b> 212</b></font> <font color="#00AAAA">__main__</font>:<font color="#00AAAA">&lt;module&gt;</font> | <b>I found these inputprofiles:[PosixPath(&apos;data/inputprofile_0306217088&apos;)]</b>
<font color="#00AA00">2023-01-31 07:46:51.956</font> | <b>INFO    </b> | <font color="#5555FF">msfs_keybindings.py:</font><font color="#5555FF"><b> 278</b></font> <font color="#00AAAA">__main__</font>:<font color="#00AAAA">read_inputprofile</font> | <b>handling inputprofile data/inputprofile_0306217088</b>
<font color="#00AA00">2023-01-31 07:46:51.959</font> | <b>INFO    </b> | <font color="#5555FF">msfs_keybindings.py:</font><font color="#5555FF"><b> 326</b></font> <font color="#00AAAA">__main__</font>:<font color="#00AAAA">read_inputprofile</font> | <b>COCKPIT_CAMERA - KEY_COCKPIT_QUICKVIEW3 : Joystick Pov Right</b>
<font color="#00AA00">2023-01-31 07:46:51.961</font> | <b>INFO    </b> | <font color="#5555FF">msfs_keybindings.py:</font><font color="#5555FF"><b> 326</b></font> <font color="#00AAAA">__main__</font>:<font color="#00AAAA">read_inputprofile</font> | <b>COCKPIT_CAMERA - KEY_COCKPIT_QUICKVIEW4 : JoystickPov Left</b>
<font color="#00AA00">2023-01-31 07:46:51.962</font> | <b>INFO    </b> | <font color="#5555FF">msfs_keybindings.py:</font><font color="#5555FF"><b> 326</b></font> <font color="#00AAAA">__main__</font>:<font color="#00AAAA">read_inputprofile</font> | <b>EXTERNAL_CAMERA - KEY_CHASE_QUICKVIEW1 : Joystick Pov Right</b>
</pre>
