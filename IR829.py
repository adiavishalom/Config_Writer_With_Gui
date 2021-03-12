# IR829.py

import PySimpleGUI as sg
import pandas as pd
import os


def openFile():
    with open('/Users/adiav/Desktop/Boyce_Technologies_Work/Config_Writer_With_Gui/IR829Default.cfg') as file:
        content = file.readlines()

    content = [x.strip('\n') for x in content]

    return content

def printConfigFile(path, savePath):
    df = pd.read_csv(path)
    
    for station in df['Station Index']:
        mrnumber = station
        ip = df.loc[df['Station Index']==station]['IP'].values[0]
        ipgw = df.loc[df['Station Index']==station]['IPGW'].values[0]
        content = openFile()
        uniqueinput, filename=inputValues(mrnumber, ip, ipgw)
        content.extend(uniqueinput)

        with open(savePath+'/'+filename, 'w') as file:
            for line in content:
                file.write(line+'\n')

    return

def inputValues(mrnumber, ip, ipgw):
    outputList=[]

    mrnumber=str(mrnumber)
    ip=str(ip)
    ipgw=str(ipgw)
    
    inppwd = '5' + mrnumber + '0'
        
    outputList.extend(['inppwd="'+ inppwd +'"',
                       'inppwd_secondary="'+ inppwd +'"',
                       'inpdisplayname="'+ inppwd +'"',
                       'inpuser="'+ inppwd +'"',
                       'inpuser_secondary="'+ inppwd +'"',
                       'inpauth="'+ inppwd +'"',
                       'inpauth_secondary="'+ inppwd +'"',
                       'prov_file="MR'+ mrnumber +'-EBCSU'+ inppwd +'.cfg"',
                       'Phonebook="MR'+ mrnumber +'-EBCSU'+ inppwd +'.csv"',
                       #'snmp_location="'+ boothnumber +'"',
                       'ipaddr="'+ ip +'"',
                       'ipgw="'+ ipgw +'"'])

    filename = 'MR'+ mrnumber +'-EBCSU'+ inppwd +'.cfg'
    return outputList, filename



# All the stuff inside your window.
layout = [ [sg.Text("Choose a csv file:\t\t"), sg.Input(key="-IN2-" ,change_submits=True), sg.FileBrowse(key="-IN-", file_types=(("CSV Files", "*.csv"),))],
           [sg.Text("Choose a where to save:\t"), sg.Input(key="-IN4-" ,change_submits=True), sg.FolderBrowse(key="-IN3-")],
            [sg.Button('Generate Config'), sg.Exit()]
]

# Create the Window
window = sg.Window('IR829 Config Writer', layout).Finalize()

while True:             # Event Loop
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    elif event == 'Generate Config':
        printConfigFile(values['-IN2-'], values['-IN4-'])

window.Close()