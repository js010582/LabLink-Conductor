# img_viewer.py

import PySimpleGUI as sg
import os.path

# window layout of two columns

file_list_column = [
    [
        sg.Text("Image Foldter"),
        sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40,20),
            key="-FILE LIST-"
        )
    ],
]
# for now will only show the name of the chosen file

image_viewer_column = [
    [sg.Text("Choose an image from the list on the left:")],
    [sg.Text(size=(40,1), key="-TOUT")],
    [sg.Image(key="-IMAGE-")],
]

# ----- full layout -----

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Viewer", layout)

# event loop
while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
                break

window.close()