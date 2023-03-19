# hello_guy.py Adding button and Text

import PySimpleGUI as sg


layout = [
    [sg.Text("Hello from PySimpleGUI")],
    [sg.Button("OK")]
]

# create the window
window = sg.Window("Demo", layout)

# create an event loop
while True:
    event, values = window.read()
    # End if user closes window or 
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break
        
window.close()
