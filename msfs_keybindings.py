# -*- coding: utf8 -*-
# msfs inputprofile import script
# by dc6jn
#
import os, sys
from pathlib import Path
import argparse
import re
import json

import pandas
from natsort import natsort_keygen

# supress FutureWarning: iteritems is deprecated and will be removed in a future version. Use .items instead.
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

process_all_files = False

parser = argparse.ArgumentParser(
    description='Read msfs2020 input device configurations and create readable documents')
parser.add_argument('filename')
parser.add_argument('-l', '--language', help='Select which language for descriptions, i.e. en-US, de-DE,...',
                    action='store', type=str, default='en-US')
parser.add_argument('-f', '--fill', help='fill areas of differences.', action='store_true')
parser.add_argument('-c', '--csv', help='Save as CSV.', action='store_true')
parser.add_argument('-x', '--xls', help='Save as Excel xls.', action='store_true')
parser.add_argument('-t', '--tex', help='Save as Latex-Template', action='store_true')
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('-k', '--keep', help='keep these CONTEXT entrys', type=str.upper)
group.add_argument('-d', '--drop', help='drop these CONTEXT entrys', type=str.upper)
parser.add_argument('-o', '--output', help='Name for output file')
parser.add_argument('-p', '--path', help='Path for output image')
parser.add_argument('-i', '--imagespath', help='Path for device images')
parser.add_argument('-u', '--usercfgpath', help='Path for user config')
parser.add_argument("-v", "--verbose", dest="logLevel", type=str.upper, default="WARNING",
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set the logging level")

args = parser.parse_args()

try:
    from loguru import logger as log

    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<light-blue>{file}:<bold>{line: >4}</bold></light-blue> <cyan>{name}</cyan>:<cyan>{function}</cyan> | "
        "<level>{message}</level>")

    log.remove()
    log.add(sys.stderr, level=args.logLevel, format=logger_format)
    log.add(__file__ + ".log", rotation="1 day", level=args.logLevel, format=logger_format)

except:
    import logging

    log = logging.getLogger(__name__)
    log.setLevel(logging.getLevelName(args.logLevel))
    fmt = "%(asctime)s %(name)s %(levelname)s %(message)s"
    logformatter = logging.Formatter(fmt)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(logging.Formatter(fmt))
    floghandler = logging.FileHandler(f"{__name__}.log", mode='w')
    floghandler.setFormatter(logging.Formatter(fmt))
    log.addHandler(floghandler)
    log.addHandler(stdout_handler)

log.debug(f"command line parameters: {args}")
# log.debug("debug")
# log.info("info")
# log.warning("warning")
# log.error("error")
# log.critical("critical")

ctx_to_keep = []
ctx_to_drop = []
if args.keep:
    ctx_to_keep = [args.keep]
    log.info(f"Topics to keep: {ctx_to_keep}")
if args.drop:
    ctx_to_drop = [args.drop]
    log.info(f"Topics to drop: {ctx_to_drop}")

# Create Filenames

currentpath = Path.cwd()
if args.path:
    outputpath = Path(args.path)
    if not outputpath.exists:
        log.error("OutputPath does not exist, exiting...")
        exit(0)
else:
    outputpath = currentpath
    log.info(f"Using outputpath {outputpath}")
filename_path = Path(args.filename).absolute()

usercfg_path = None
appdata = os.getenv('APPDATA')
localappdata = os.getenv('LOCALAPPDATA')

# set UserCfgMS=%LOCALAPPDATA%\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\UserCfg.opt
# set UserCfgSteam=%APPDATA%\Microsoft Flight Simulator\UserCfg.opt
usercfg_ms = Path(localappdata + "\\Packages\\Microsoft.FlightSimulator_8wekyb3d8bbwe\\LocalCache\\UserCfg.opt")
usercfg_steam = Path(appdata + "\\Microsoft Flight Simulator\\UserCfg.opt")
if usercfg_ms.is_file():
    log.info("autodetected  MS-Version of flight simulator")
    usercfg_path = usercfg_ms
elif usercfg_steam.is_file():
    log.info("autodetected  steam version of flight simulator")
    usercfg_path = usercfg_steam

if 'usercfgpath' in args:
    usercfg_manual = Path(args.usercfgpath + "\\UserCfg.opt").absolute()
    if usercfg_manual.is_file():
        usercfg_path = usercfg_manual
        log.info(f"manual override for config path, using {usercfg_path}")

if usercfg_path is None:
    log.error(f"no valid config path provided or found")
    exit()

# hier liegen die Verzeichnisse mit den Bildern: c:\msfs\fs-base-ui\html_ui\Textures\Menu\Control\
# InstalledPackagesPath

with open(usercfg_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        if line.startswith('InstalledPackagesPath'):
            line = str(line)
            log.info(f'found installation path {line}')
            ipath = str(line)
            ipath = ipath.split(' ')[1]
            ipath = ipath.replace('"', '')
            ipath = ipath.replace("'", '')
            ipath = ipath.replace("\n", '')
            imagepath = Path(ipath + r'\fs-base-ui\html_ui\Textures\Menu\Control')
            log.info(imagepath.absolute())

if imagepath.is_dir():
    log.info(f"found directory with images {imagepath}")

#    32-bit: HKEY_LOCAL_MACHINE\SOFTWARE\Valve\Steam
#    64-bit: HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Valve\Steam

# import winreg
# steampath=None
# try:
#     steampath = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Valve\Steam")
# except Exception as ex:
#     log.warning(f"Could not find steam key ; Grund:{ex}")
#     try:
#         steampath = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Wow6432Node\Valve\Steam")
#     except Exception as ex:
#         log.error(f"Could not find steam key ; Grund:{ex}")
#         #exit()
#
# if steampath is None:
#     log.error("Please provide path to steam userprofiles!")
#     exit()
# else:
#     log.info(f"using steam installation path {steampath}")

# if not args.output:
#    output_filename = os.path.join(outputpath, args.output)

# Create Filenames## # currentpath = Path.cwd()
# if args.path:
#     outputpath = Path(args.path)
#     if not outputpath.exists:
#         print("Outputpath does not exist, exiting...")
#         exit(0)
# else:
#     outputpath = currentpath
filename = Path(args.filename).absolute()
# workingpath = Path.cwd()
# mainname = filename.stem
# mainextension = filename.suffixes
basepath = Path(filename.parent.absolute())
basename = filename.name.removesuffix("".join(filename.suffixes))

if not (filename.is_file()):
    log.info(f"Try to find all inputprofiles in path {filename.parent}")
    all_files = list(Path(filename).parent.glob("inputprofile_*"))
    latex_filename = 'msfs_input_definitions.tex'
else:
    all_files = [filename]
    latex_filename = basepath.joinpath(basename + '_input_definitions.tex')

log.info(f"found these inputprofiles:{all_files}")
for filename in all_files:
    log.info(f"{filename}")


def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
        taken from https://stackoverflow.com/a/25875504
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }

    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: - len(item))))
    try:
        res = regex.sub(lambda match: conv[match.group()], text)
    except:
        log.debug(text)
        res = text
    return res


import locale
default_lang = locale.getdefaultlocale()[0]
if args.language:
    default_lang = args.language
# c:\msfs\Official\Steam\fs-base\en-US.locPak für englische Beschreibungen
# c:\msfs\Official\Steam\fs-base\de-DE.locPak für deutsche Beschreibungen

# always load en-US as default:
cmt = ''
cmt_loc = ''
try:
    with open('data//en-US.locPak', encoding='utf-8') as f:
        d = json.load(f)
    cmt = d['LocalisationPackage']['Strings']
except:
    log.warning("Error loading default en-US language pack, no action descriptions available!")
try:
    with open('data//{}.locPak'.format(default_lang), encoding='utf-8') as f:
        d = json.load(f)
    cmt_loc = d['LocalisationPackage']['Strings']
except:
    log.warning(f"Error loading localized language pack {default_lang}, no action descriptions available!")

# Bilder der Controller sind unter c:\msfs\fs-base-ui\html_ui\Textures\Menu\Control\ gespeichert


import xml.etree.ElementTree as ET
import typing


def read_inputprofile(filename):
    log.info(f"handling inputprofile {filename}")
    with open(filename, 'r') as f:
        xml = f.read()
    # MSFS does not provide valid xml, so we have to patch:
    # https://stackoverflow.com/a/38854127
    xml = re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>"
    root = ET.fromstring(xml)
    DeviceName = root.find('Device').attrib['DeviceName']
    FriendlyName = root.find('FriendlyName').text
    GUID = root.find('Device').attrib['GUID']
    ProductID = root.find('Device').attrib['ProductID']
    CompositeID = root.find('Device').attrib['CompositeID']
    df = pd.DataFrame(
        columns=['DeviceName', 'FriendlyName', 'Context', 'Action', 'Primary', 'Secondary', 'PrimaryKeyCode',
                 'SecondaryKeyCode', 'Description'])
    for ctx in root.iter('Context'):
        currctx = ctx.attrib['ContextName']
        log.debug(f'Actions defined in {currctx}')
        for a in ctx.iter('Action'):
            curraction = a.attrib['ActionName']
            log.debug(curraction)
            keystroke = []
            keycodes = []
            pk = ''
            pkk = ''
            spk = ''
            skk = ''
            for op in a.iter('Primary'):
                log.debug(f'  {op.tag}')
                for key in op.iter('KEY'):
                    currkey = key.attrib['Information']
                    keystroke.append(currkey)
                    keycodes.append(key.text)
                    log.debug(f'    {key.tag}-Key:{key.text} : {currkey}')
            pk = ' - '.join(keystroke)
            pkk = ', '.join(keycodes)
            log.debug("  primary key sequence: " + f"{'-'.join(keystroke)}")
            keystroke = []
            for op in a.iter('Secondary'):
                log.debug(f'  {op.tag}')
                for key in op.iter('KEY'):
                    currkey = key.attrib['Information']
                    keystroke.append(currkey)
                    log.debug(f'    {key.tag}-Key:{key.text} : {keystroke}')
            if keystroke:
                spk = ' - '.join(keystroke)
                skk = ', '.join(keycodes)
                log.debug("\t  secondary key sequence: " + f"{'-'.join(keystroke)}")
            log.info(f"{currctx} - {curraction} : {pk}" + (f" | {spk}" if spk else ""))
            cmtkey = 'INPUT.{}'.format(curraction)
            rcmt = ''
            if cmtkey in cmt_loc:
                rcmt = cmt_loc[cmtkey]
            else:
                if cmtkey in cmt:
                    rcmt = cmt[cmtkey]

            row = {'DeviceName': DeviceName, 'FriendlyName': FriendlyName, 'GUID': GUID, 'ProductID': ProductID,
                   'COmpositeID': CompositeID, 'Context': currctx, 'Action': curraction,
                   'Primary': pk, 'Secondary': spk, 'PrimaryKeyCode': pkk, 'SecondaryKeyCode': skk, 'Description': rcmt}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
            # df = pd.concat([df, new_df])
    return df


def prepare_field(field):
    if isinstance(field, (list, tuple, pandas.Series)):
        res = [tex_escape(text) for text in field]
    else:
        res = tex_escape(field)
    return res


def create_latex(df):
    # iterate over each group
    rows = ''

    for idx, row in df.iterrows():
        log.debug(row)
        s2c = prepare_field(row['Context'])
        s2f = prepare_field(row['FriendlyName'])
        s2d = prepare_field(row['DeviceName'])
        s2z1 = []
        for d in list(zip(s2c, s2d, s2f)):
            s2z1.append(f"{tex_escape(d[0])} ({tex_escape(d[1])} ({tex_escape(d[2])})")

        s2za = ' \\newline '.join(s2z1)
        # s2f = ' \\newline '.join(s2f)
        # s2d=' \\newline '.join(s2d)
        # s2 = "\\textbf{" + f"{row['Primary']}" + " }{ \\tiny " + f"{s2d} ({s2f})    " + "}"
        sP = "\\textbf{" + f"{row['Primary']}" + " }"
        sC = "{" + f"{s2za} " + "}"
        sA = ' \\newline '.join(row['Action'])
        sD = ' \\newline '.join(row['Description'])
        texrow = '{}&{} &{} & {} \\\\\\midrule\n'.format(sP, sC, sA, sD)
        #    texrow = texrow.replace("_", "\_")
        #    texrow = texrow.replace("%", "\%")
        #    texrow = texrow.replace("#", "\#")
        #    if s2 in t320stick:
        #           t320[s2]=' \\'.join(row['Action'])
        # if args.verbose:
        log.debug(texrow)
        rows = rows + texrow
    texheader = r'''
    \documentclass[landscape,pagesize]{scrartcl}
    \usepackage{libertine}
    \usepackage{graphicx}
     \usepackage[table,xcdraw]{xcolor}
    \usepackage{booktabs,tabularx}
    \usepackage{longtable}
    \usepackage{wrapfig}
    \usepackage{blindtext}
    \usepackage[
    %showframe,% Seitenlayout anzeigen
    left=1cm,
    right=1cm,
    top=.5cm,
    bottom=1cm,
    %includeheadfoot
    ]{geometry}
    \begin{document}'''

    texfigure = r'''
        \begin{wrapfigure}[18]{l}{0.4\linewidth}*	
            \includegraphics[width=\linewidth]{"data/T.A320 Pilot/mapping"}
    %		\caption{}
            \label{fig:mapping}

    \end{wrapfigure}'''
    tex_tablehead = r'''
    \begin{longtable}{p{.2\textwidth}p{.18\textwidth}p{.25\textwidth}p{.25\textwidth}}
            \toprule
    Keyname {\tiny located at}  &active context  & action &comment  \\\midrule
    \endfirsthead
    \toprule
    Keyname {\tiny located at}  &active context  & action &comment  \\\midrule
    \endhead	
    \hline\multicolumn{2}{l}{\textit{Fortsetzung auf der nächsten Seite}}\\\hline
    \endfoot
    %\bottomrule
    %\caption{}\label{tab:table1}
    \endlastfoot

    '''
    tex_tablefoot = r'''\end{longtable}'''

    tex_foot = r'''\end{document}'''

    tex = texheader + texfigure + tex_tablehead + rows + tex_tablefoot + tex_foot
    latex_filename = outputpath.joinpath('keybindings.tex')
    log.info(f"writing keybindings as latex-file to {latex_filename}")
    with open(latex_filename, 'w', encoding='utf-8') as f:
        f.write(tex)
        f.close()


def make_t320_chart(df):
    t320def = '''
        1 ;Joystick Button 1;   0; 0
        2 ;Joystick Button 2;   0; 0
        3 ;Joystick Button 3;   0; 0
        4 ;Joystick Button 4;   0; 0
        5 ;Joystick Button 5;   0; 0
        6 ;Joystick Button 6;   0; 0
        7 ;Joystick Button 7;   0; 0
        8 ;Joystick Button 8;   0; 0
        9 ;Joystick Button 9;   0; 0
        10;Joystick Button 10;   0; 0
        11;Joystick Button 11;   0; 0
        12;Joystick Button 12;   0; 0
        13;Joystick Button 13;   0; 0
        14;Joystick Button 14;   0; 0
        15;Joystick Button 15;   0; 0
        16;Joystick Button 16;   0; 0
        17;Joystick Pov Down;   0; 0
        18;Joystick Pov Up;   0; 0
        19;JoystickPov Left;   0; 0
        20;Joystick Pov Right;   0; 0
        21;Joystick L-Axis X;   0; 0
        22;Joystick L-Axis Y;   0; 0
        23;Joystick Slider X;   0; 0
        24;Joystick R-Axis Z;   0; 0'''

    from io import StringIO
    columns = ['Index', 'Primary', 'POSX', 'POSY']
    t320def = pd.read_csv(StringIO(t320def), names=columns, sep=';')
    log.debug(t320def.keys())
    log.debug(t320def)

    rows = ''
    # df.loc[df['col1'].isin([value1, value2, value3, ...])]
    px = t320def['POSX']
    sp = t320def['Primary'].tolist()
    adf = df.loc[df['Primary'].isin(sp)]
    for idx, row in t320def.iterrows():
        log.debug(row)

        action = df.loc[df['Primary'].str.contains(row['Primary'])]
        sP = r"\textbf{" + f"{row['Index']} - {row['Primary']}" + " }"

        if not action.empty:
            s2c = prepare_field(action['Context'])
            s2f = prepare_field(action['FriendlyName'])
            s2d = prepare_field(action['DeviceName'])
            s2z1 = []
            for d in list(zip(s2c, s2d, s2f)):
                # s2z1.append(f"{tex_escape(d[0])} ({tex_escape(d[1])} ({tex_escape(d[2])})")
                s2z1.append(f"{tex_escape(d[0])} ({tex_escape(d[2])})")

            s2za = r' \newline '.join(s2z1)
            sC = "{" + f"{s2za} " + "}"

            sA = r' \newline '.join(prepare_field(action['Action']))
            sD = r' \newline '.join(prepare_field(action['Description']))

            texrow = '{} & {} & {} & {} \\\\\\midrule\n'.format(sP, sC, sA, sD)
        else:
            texrow = '{} & & &  \\\\\\midrule\n'.format(sP)
        rows = rows + texrow
    texheader = r'''
    \documentclass[landscape,pagesize]{scrartcl}
    \usepackage{libertine}
    \usepackage{graphicx}
     \usepackage[table,xcdraw]{xcolor}
    \usepackage{booktabs,tabularx}
    \usepackage{longtable}
    \usepackage{wrapfig}
    \usepackage{blindtext}
    \usepackage[
    %showframe,% Seitenlayout anzeigen
    left=1cm,
    right=1cm,
    top=.5cm,
    bottom=1cm,
    %includeheadfoot
    ]{geometry}
    \begin{document}'''

    texfigure = r'''
        \begin{wrapfigure}[18]{l}{0.4\linewidth}*	
            \includegraphics[width=\linewidth]{"data/T.A320 Pilot/mapping"}
    %		\caption{}
            \label{fig:mapping}

    \end{wrapfigure}'''
    tex_tablehead = r'''
    \begin{longtable}{p{.2\textwidth}p{.18\textwidth}p{.25\textwidth}p{.25\textwidth}}
            \toprule
    Keyname {\tiny located at}  &active context  & action &comment  \\\midrule
    \endfirsthead
    \toprule
    Keyname {\tiny located at}  &active context  & action &comment  \\\midrule
    \endhead	
    \hline\multicolumn{2}{l}{\textit{Fortsetzung auf der nächsten Seite}}\\\hline
    \endfoot
    %\bottomrule
    %\caption{}\label{tab:table1}
    \endlastfoot

    '''
    tex_tablefoot = r'''\end{longtable}'''

    tex_foot = r'''\end{document}'''

    tex = texheader + texfigure + tex_tablehead + rows + tex_tablefoot + tex_foot

    latex_filename = outputpath.joinpath('t320_keybindings.tex')
    log.info(f"writing keybindings as latex-file to {latex_filename}")

    with open(latex_filename, 'w', encoding='utf-8') as f:
        f.write(tex)
        f.close()

#################################################################################################

df = None
for filename in all_files:
    dfn = read_inputprofile(filename)
    if df is None:
        df = dfn
    else:
        df = pd.concat([df, dfn], ignore_index=True, sort=False)

# Adjust wich subset should be used:
if ctx_to_keep:
    df = df[df['Context'].isin(ctx_to_keep)]
if ctx_to_drop:
    df = df[~df['Context'].isin(ctx_to_drop)]

# sortiere df nach Context,Primary:
try:
    df = df.sort_values(by=['Primary', 'Context'], key=natsort_keygen(), ignore_index=True)
except:
    try:
        df = df.sort_values(['Primary', 'Context'])
    except:
        log.warning("problems sorting dataframe, try to continue")
        pass
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    log.debug("" + df['Primary'] + "" + df['Action'])


df = df.reset_index(drop=True)
log.info(f"read all inputfiles, got {df.shape[0]} entries")
#### Ab hier sind alle Kombinationen eingelesen und im dataframe hinterlegt
# output requested file format
if args.csv:
    csvpath = outputpath.joinpath('keybindings.csv')
    log.info(f"writing keybindings as csv-file to {csvpath}")
    df.to_csv(csvpath, encoding='utf-8', sep=';')
if args.xls:
    csvpath = outputpath.joinpath('keybindings.xls')
    log.info(f"writing keybindings as Excel-File to {csvpath}")
    df.to_excel(csvpath.as_posix(), encoding='utf-8')

#create grouped dataframes
df_grouped = df.groupby('Primary').agg(list).reset_index()
df_grouped = df_grouped.sort_values(by=['Primary', 'DeviceName', 'Context'], key=natsort_keygen(), ignore_index=True)
df_grouped['CTEX'] = df_grouped['Context'].astype(str) + ' (' + df_grouped['DeviceName'].astype(str) + ', ' + \
                     df_grouped['FriendlyName'].astype(str) + ')'
df_grouped[['DeviceName', 'FriendlyName']] = df_grouped[['DeviceName', 'FriendlyName']].apply(tex_escape)




if args.tex:
    create_latex(df_grouped)
    make_t320_chart(df)

if __name__ == '__main__':
    pass
