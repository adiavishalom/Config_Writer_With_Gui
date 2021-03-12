#RunConfigWriter.py
#This file will create a page with 2 options
#One to generate EBCS Commend Board configs and one for IR829

import PySimpleGUI as sg
import os

# All the stuff inside your window.
layoutMain = [ [sg.Button('Generate EBCS Configs'), sg.Button('Generate IR829 Configs'), sg.Exit()]
]

# Create the Window
window = sg.Window('Config Writer', layoutMain).Finalize()

while True:             # Event Loop
    event, values = window.Read()
    if event in (None, 'Exit'):
        break
    elif event == 'Generate EBCS Configs':
        os.system('py EBCS.py')
    elif event == 'Generate IR829 Configs':
        os.system('py IR829.py')

window.Close()
