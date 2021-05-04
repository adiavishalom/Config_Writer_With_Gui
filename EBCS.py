# EBCS.py

import PySimpleGUI as sg
import pandas as pd
import os


def writeFile(savePath, content, filename):
    with open(savePath+'/'+filename, 'w') as file:
                for line in content:
                    file.write(line+'\n')
    return


def openFile():
    with open('/Users/adiav/Desktop/Boyce_Technologies_Work/Config_Writer_With_Gui/EBCSDefault.cfg') as file:
        content = file.readlines()

    content = [x.strip('\n') for x in content]

    return content

def printConfigFile(path, savePath):
    df = pd.read_csv(path)
    
    for mrnumber in df['Station Index']:
        iplist = list(df.loc[df['Station Index']==mrnumber]['EBCSIP'])
        if len(iplist) == 1:
            ip = df.loc[df['Station Index']==mrnumber]['EBCSIP'].values[0]
            ipgw = df.loc[df['Station Index']==mrnumber]['IR829IP'].values[0]
            subnet = df.loc[df['Station Index']==mrnumber]['Subnet Mask'].values[0]
            lastdigit = 0
            content = openFile()
            uniqueinput, filename=inputValues(mrnumber, ip, ipgw, subnet, lastdigit)
            content.extend(uniqueinput)

            testSavePath = savePath + '/ToTestAgainst'
            writeFile(testSavePath, uniqueinput, filename)
            writeFile(savePath, content, filename)


        elif len(iplist) > 1:
            if checkIfDuplicates(iplist) == True:
                print('There is a duplicate IP')
                break

            for ip in iplist:
                index = iplist.index(ip)
                ipdf = df.loc[df['Station Index']==mrnumber].loc[df['EBCSIP']==ip]
                ipgw = ipdf['IR829IP'].values[0]
                subnet = ipdf['Subnet Mask'].values[0]
                content = openFile()
                uniqueinput, filename=inputValues(mrnumber, ip, ipgw, subnet, index)
                content.extend(uniqueinput)

                testSavePath = savePath + '/ToTestAgainst'
                writeFile(testSavePath, uniqueinput, filename)
                writeFile(savePath, content, filename) 

    return

def inputValues(mrnumber, ip, ipgw, subnet, lastdigit):
    outputList=[]

    mrnumber=str(mrnumber)
    ip=str(ip)
    ipgw=str(ipgw)
    subnet=str(subnet)
    lastdigit=str(lastdigit)
    
    inppwd = '5' + mrnumber + lastdigit
        
    outputList.extend(['inppwd="'+ inppwd +'"',
                       'inppwd_secondary="MR'+ mrnumber +'EBCSVOIP"',
                       'inpdisplayname="'+ inppwd +'"',
                       'inpuser="'+ inppwd +'"',
                       'inpuser_secondary="'+ inppwd +'"',
                       'inpauth="'+ inppwd +'"',
                       'inpauth_secondary="'+ inppwd +'"',
                       'prov_file="MR'+ mrnumber +'-EBCSU'+ inppwd +'.cfg"',
                       'Phonebook="MR'+ mrnumber +'-EBCSU'+ inppwd +'.csv"',
                       #'snmp_location="'+ boothnumber +'"',
                       'ipaddr="'+ ip +'"',
                       'ipgw="'+ ipgw +'"',
                       'ipsubnet="' + subnet +'"'])

    filename = 'MR'+ mrnumber +'-EBCSU'+ inppwd +'.cfg'
    return outputList, filename


def checkIfDuplicates(listOfElems):
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True


# All the stuff inside your window.
layout = [ [sg.Text("Choose a csv file:\t\t"), sg.Input(key="-IN2-" ,change_submits=True), sg.FileBrowse(key="-IN-", file_types=(("CSV Files", "*.csv"),))],
           [sg.Text("Choose a where to save:\t"), sg.Input(key="-IN4-" ,change_submits=True), sg.FolderBrowse(key="-IN3-")],
            [sg.Button('Generate Config'), sg.Exit()]
]

# Create the Window
window = sg.Window('EBCS Config Writer', layout).Finalize()

while True:             # Event Loop
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    elif event == 'Generate Config':
        printConfigFile(values['-IN2-'], values['-IN4-'])

window.Close()
