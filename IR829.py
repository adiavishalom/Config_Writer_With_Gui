# IR829.py

import PySimpleGUI as sg
import pandas as pd
import os


def openFile():
    with open('/Users/adiav/Desktop/Boyce_Technologies_Work/Config_Writer_With_Gui/IR829Default.txt') as file:
        content = file.readlines()

    content = [x.strip('\n') for x in content]

    return content

def printConfigFile(path, savePath, yml_check):
    df = pd.read_csv(path)
    
    for station in df['Station Index']:
        mrnumber = station
        ip = df.loc[df['Station Index']==station]['IR829IP'].values[0]
        subnet = df.loc[df['Station Index']==station]['Subnet Mask'].values[0]
        content = []
        if yml_check == False:
            content = openFile()
            uniqueinput, filename=inputValuesRegular(mrnumber, ip, subnet)
        else:
            content = ['- host: pegasus-rtrs',
                        '',
                        '  vars:',
                        '    command_list:',
                        '     - conf t']
            uniqueinput, filename=inputValuesYML(mrnumber, ip, subnet)
        
        content.extend(uniqueinput)

        with open(savePath+'/'+filename, 'w') as file:
            for line in content:
                file.write(line+'\n')

    return

def inputValuesRegular(mrnumber, ip, subnet):
    outputList=[]

    mrnumber=str(mrnumber)
    ip=str(ip)
    subnet=str(subnet)
    
    secondaryip = ip[:-2] + str(int(ip[-2:])+4)
    routeip = ip[:-2] + str(int(ip[-2:])-1)
    permitip = ip[:-2] + str(int(ip[-2:])-2)
        
    outputList.extend(['hostname MR' + mrnumber +'-IR829',
                        'interface Vlan73',
                        ' description EBCS-Vlan',
                        ' ip address ' + secondaryip + ' ' + subnet + ' secondary',
                        ' ip address ' + ip + ' ' + subnet,
                        ' no ip redirects',
                        'snmp-server trap-source Vlan73',
                        '',
                        'ip route 10.228.8.0 255.255.255.248 ' + routeip + ' name RCC-EBCSP2P track 3',
                        'ip route 10.228.8.0 255.255.255.192 ' + routeip + ' name RCC-EBCSP2P track 3',
                        'ip route 10.228.8.64 255.255.255.192 ' + routeip + ' name RCC-EBCSSERVERVLAN track 3',
                        'ip route 10.228.8.128 255.255.255.224 ' + routeip + ' name RCC-EBCSMGMTVLAN track 3',
                        'ip route 10.228.8.160 255.255.255.224 ' + routeip + ' name RCC-EBCSWSAVLAN track 3',
                        'ip route 10.228.8.192 255.255.255.224 ' + routeip + ' name RCC-EBCSWSBVLAN track 3',
                        'ip route 10.228.9.0 255.255.255.248 ' + routeip + ' name BRCC-EBCSP2P track 3',
                        'ip route 10.228.9.0 255.255.255.192 ' + routeip + ' name BRCC-EBCSP2P track 3',
                        'ip route 10.228.9.64 255.255.255.192 ' + routeip + ' name BRCC-EBCSSERVERVLAN track 3',
                        'ip route 10.228.9.128 255.255.255.224 ' + routeip + ' name BRCC-EBCSMGMTVLAN track 3',
                        'ip route 10.228.9.160 255.255.255.224 ' + routeip + ' name BRCC-EBCSWSAVLAN track 3',
                        'ip route 0.0.0.0 0.0.0.0 ' + routeip + ' name DEFAULT-ROUTE',
                        'ip route 10.0.75.0 255.255.255.0 ' + routeip + ' name TEMP-CONNECTION-TO-EBCS-LAB',
                        'ip route 10.228.8.32 255.255.255.252 ' + routeip + ' name RCC-EBCSCOREIPSLA',
                        'ip route 10.228.8.224 255.255.255.248 ' + routeip + ' name RCCEBCSDISTRIBUTION-IPSLA',
                        'ip route 10.228.9.32 255.255.255.252 ' + routeip + ' name BRCC-EBCSCOREIPSLA',
                        'ip route 10.228.9.224 255.255.255.248 ' + routeip + ' name BRCCEBCSDISTRIBUTION-IPSLA'
                        '!',
                        'ip access-list extended rcc_brcc_acl',
                        ' remark PERMIT VLAN73 Network to VLAN73 Network',
                        ' permit ip ' + permitip + ' 0.0.0.7 ' + permitip + ' 0.0.0.7',
                        ' remark PERMIT RCC Network to VLAN73 Network',
                        ' permit ip 10.228.8.0 0.0.0.255 ' + permitip + ' 0.0.0.7',
                        ' remark PERMIT BRCC Network to VLAN73 Network',
                        ' permit ip 10.228.9.0 0.0.0.225 ' + permitip + ' 0.0.0.7',
                        ' remark DENY ANYTHING ELSE',
                        ' deny   ip any any',
                        '!',
                        'ip sla 1',
                        ' icmp-echo 10.228.8.225 source-ip ' + secondaryip + '',
                        ' tag RCC-DISTRIBUTION-IPSLA-VLAN',
                        ' timeout 10000',
                        ' frequency 30',
                        'ip sla schedule 1 life forever start-time now',
                        '!',
                        'exit',
                        '!',
                        'ip sla 2',
                        ' icmp-echo 10.228.9.225 source-ip ' + secondaryip,
                        ' tag BRCC-DISTRIBUTION-IPSLA-VLAN',
                        ' timeout 10000',
                        ' frequency 30',
                        'ip sla schedule 2 life forever start-time now',
                        '!',
                        'exit',
                        '!',
                        'wr'])


    filename = mrnumber +'-IR829.txt'
    
    return outputList, filename



def inputValuesYML(mrnumber, ip, subnet):
    outputList=[]

    mrnumber=str(mrnumber)
    ip=str(ip)
    subnet=str(subnet)
    
    secondaryip = ip[:-2] + str(int(ip[-2:])+4)
    routeip = ip[:-2] + str(int(ip[-2:])-1)
    permitip = ip[:-2] + str(int(ip[-2:])-2)
        
    outputList.extend(['hostname MR' + mrnumber +'-IR829',
                        'interface Vlan73',
                        'description EBCS-Vlan',
                        'ip address ' + ip + ' ' + subnet + ' secondary',
                        'ip address ' + secondaryip + ' ' + subnet,
                        'no ip redirects',
                        'ip route 10.228.8.0 255.255.255.248 ' + routeip + ' name RCC-EBCSP2P track 3',
                        'ip route 10.228.8.0 255.255.255.192 ' + routeip + ' name RCC-EBCSP2P track 3',
                        'ip route 10.228.8.64 255.255.255.192 ' + routeip + ' name RCC-EBCSSERVERVLAN track 3',
                        'ip route 10.228.8.128 255.255.255.224 ' + routeip + ' name RCC-EBCSMGMTVLAN track 3',
                        'ip route 10.228.8.160 255.255.255.224 ' + routeip + ' name RCC-EBCSWSAVLAN track 3',
                        'ip route 10.228.8.192 255.255.255.224 ' + routeip + ' name RCC-EBCSWSBVLAN track 3',
                        'ip route 10.228.9.0 255.255.255.248 ' + routeip + ' name BRCC-EBCSP2P track 3',
                        'ip route 10.228.9.0 255.255.255.192 ' + routeip + ' name BRCC-EBCSP2P track 3',
                        'ip route 10.228.9.64 255.255.255.192 ' + routeip + ' name BRCC-EBCSSERVERVLAN track 3',
                        'ip route 10.228.9.128 255.255.255.224 ' + routeip + ' name BRCC-EBCSMGMTVLAN track 3',
                        'ip route 10.228.9.160 255.255.255.224 ' + routeip + ' name BRCC-EBCSWSAVLAN track 3',
                        'ip route 0.0.0.0 0.0.0.0 ' + routeip + ' name DEFAULT-ROUTE',
                        'ip route 10.228.8.32 255.255.255.252 ' + routeip + ' name RCC-EBCSCOREIPSLA',
                        'ip route 10.228.8.224 255.255.255.248 ' + routeip + ' name RCCEBCSDISTRIBUTION-IPSLA',
                        'ip route 10.228.9.32 255.255.255.252 ' + routeip + ' name BRCC-EBCSCOREIPSLA',
                        'ip route 10.228.9.224 255.255.255.248 ' + routeip + ' name BRCCEBCSDISTRIBUTION-IPSLA',
                        'ip access-list extended rcc_brcc_acl',
                        'remark PERMIT VLAN73 Network to VLAN73 Network',
                        'permit ip ' + permitip + ' 0.0.0.7 ' + permitip + ' 0.0.0.7',
                        'remark PERMIT RCC Network to VLAN73 Network',
                        'permit ip 10.228.8.0 0.0.0.255 ' + permitip + ' 0.0.0.7',
                        'remark PERMIT BRCC Network to VLAN73 Network',
                        'permit ip 10.228.9.0 0.0.0.225 ' + permitip + ' 0.0.0.7',
                        'remark DENY ANYTHING ELSE',
                        'deny   ip any any',
                        'ip sla 1',
                        'icmp-echo 10.228.8.225 source-ip ' + ip + '',
                        'tag RCC-DISTRIBUTION-IPSLA-VLAN',
                        'timeout 10000',
                        'frequency 30',
                        'ip sla schedule 1 life forever start-time now',
                        'ip sla 2',
                        'icmp-echo 10.228.9.225 source-ip ' + ip + '',
                        'tag BRCC-DISTRIBUTION-IPSLA-VLAN',
                        'timeout 10000',
                        'frequency 30',
                        'ip sla schedule 2 life forever start-time now',
                        'snmp-server trap-source Vlan73'])


                        
    outputList = YML_Format(outputList)
    
    outputList.extend(['',
                        '  tasks:', 
                        '',
                        '   - name: Pushing Unique Config',
                        '     ios_command:',
                        '       commands: "{{ command_list }}"'])



    filename = mrnumber +'-IR829.yml'
    
    return outputList, filename


def YML_Format(givenList):
    outputList = []

    for line in givenList:
        outputList.extend(['     - ' + line])

    return outputList


# All the stuff inside your window.
layout = [ [sg.Text("Choose a csv file:\t\t"), sg.Input(key="-IN2-" ,change_submits=True), sg.FileBrowse(key="-IN-", file_types=(("CSV Files", "*.csv"),))],
           [sg.Text("Choose a where to save:\t"), sg.Input(key="-IN4-" ,change_submits=True), sg.FolderBrowse(key="-IN3-")],
           [sg.Checkbox('YML Config?', default=False, key="-YML-")],
            [sg.Button('Generate Config'), sg.Exit()]
]

# Create the Window
window = sg.Window('IR829 Config Writer', layout).Finalize()

while True:             # Event Loop
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    elif event == 'Generate Config':
        printConfigFile(values['-IN2-'], values['-IN4-'], values['-YML-'])

window.Close()