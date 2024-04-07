from pathlib import Path
import ctypes
import qrcode
from PIL import Image, ImageTk

from HogwartsPark import *

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk
import tkinter as tk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../assets/frame_menuvisitor")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def deleteEntrysAndLabels():
    for widget in window.winfo_children():
        widget.destroy()

def changeAssetsPath(path):
    global ASSETS_PATH, OUTPUT_PATH
    ASSETS_PATH = OUTPUT_PATH / Path(r"../assets/" + path)

def changeMenuOption(option, assets):
    deleteEntrysAndLabels()
    changeAssetsPath(assets)
    option()

''' UI '''

def printMenu():
    canvas = Canvas(
        window,
        bg = "#17172A",
        height = 700,
        width = 950,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        474.0,
        125.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        475.0,
        434.0,
        image=image_image_5
    )

    amusementInfoBtn_image = PhotoImage(
        file=relative_to_assets("button_1.png"))
    amusementInfoBtn = Button(
        image=amusementInfoBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printAmusementInfo, "frame_amusementinfo"),
        relief="flat"
    )
    amusementInfoBtn.place(
        x=327.0,
        y=269.0,
        width=299.0,
        height=84.0
    )

    accommodationListBtn_image = PhotoImage(
        file=relative_to_assets("button_2.png"))
    accommodationListBtn = Button(
        image=accommodationListBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printAccommodationList, "frame_accommodationlist"),
        relief="flat"
    )
    accommodationListBtn.place(
        x=628.0,
        y=269.0,
        width=299.0,
        height=84.0
    )

    amusementListBtn_image = PhotoImage(
        file=relative_to_assets("button_3.png"))
    amusementListBtn = Button(
        image=amusementListBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printAmusementList, "frame_amusementList"),
        relief="flat"
    )
    amusementListBtn.place(
        x=26.0,
        y=269.0,
        width=299.0,
        height=84.0
    )

    trainRouteListBtn_image = PhotoImage(
        file=relative_to_assets("button_4.png"))
    trainRouteListBtn = Button(
        image=trainRouteListBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printTrainRouteList, "frame_trainroutelist"),
        relief="flat"
    )
    trainRouteListBtn.place(
        x=26.0,
        y=365.0,
        width=299.0,
        height=85.0
    )

    ticketQRCodeBtn_image = PhotoImage(
        file=relative_to_assets("button_5.png"))
    ticketQRCodeBtn = Button(
        image=ticketQRCodeBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printTicketQRCode, "frame_ticketqrcode"),
        relief="flat"
    )
    ticketQRCodeBtn.place(
        x=26.0,
        y=462.0,
        width=299.0,
        height=85.0
    )

    zoneListBtn_image = PhotoImage(
        file=relative_to_assets("button_6.png"))
    zoneListBtn = Button(
        image=zoneListBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printZoneList, "frame_zonelist"),
        relief="flat"
    )
    zoneListBtn.place(
        x=328.0,
        y=365.0,
        width=299.0,
        height=85.0
    )

    zoneInfoBtn_image = PhotoImage(
        file=relative_to_assets("button_7.png"))
    zoneInfoBtn = Button(
        image=zoneInfoBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printZoneInfo, "frame_zoneinfo"),
        relief="flat"
    )
    zoneInfoBtn.place(
        x=628.0,
        y=365.0,
        width=299.0,
        height=85.0
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        78.0,
        223.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        476.0,
        252.0,
        image=image_image_7
    )
    window.resizable(False, False)
    window.mainloop()

def printAmusementList():

    amusementTypes, zones, amusementList = getAmusementListInitialData()

    canvas = Canvas(
        window,
        bg = "#17172A",
        height = 700,
        width = 950,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        475.0,
        439.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        52.0,
        384.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        130.0,
        384.0,
        image=image_image_3
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        260.0,
        384.0,
        image=image_image_8
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        380.0,
        384.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        520.0,
        384.0,
        image=image_image_7
    )


    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        620.0,
        384.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        730.0,
        384.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        850.0,
        384.0,
        image=image_image_11
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        66.0,
        275.0,
        image=image_image_12
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_13
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_14
    )

    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_15
    )

    image_image_16 = PhotoImage(
        file=relative_to_assets("image_16.png"))
    image_16 = canvas.create_image(
        183.0,
        124.0,
        image=image_image_16
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menuVisitor"),
        relief="flat"
    )
    button_1.place(
        x=708.0,
        y=89.0,
        width=217.0,
        height=71.0
    )

    image_image_17 = PhotoImage(
        file=relative_to_assets("image_17.png"))
    image_17 = canvas.create_image(
        120.0,
        222.0,
        image=image_image_17
    )

    image_image_18 = PhotoImage(
        file=relative_to_assets("image_18.png"))
    image_18 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_18
    )

    image_image_19 = PhotoImage(
        file=relative_to_assets("image_19.png"))
    image_19 = canvas.create_image(
        255.0,
        275.0,
        image=image_image_19
    )

    image_image_20 = PhotoImage(
        file=relative_to_assets("image_20.png"))
    image_20 = canvas.create_image(
        467.0,
        275.0,
        image=image_image_20
    )

    image_image_21 = PhotoImage(
        file=relative_to_assets("image_21.png"))
    image_21 = canvas.create_image(
        651.0,
        275.0,
        image=image_image_21
    )

    canvasForAmusements = Canvas(
        window,
        bg = "#354C80",
        #bg = "red",
        height = 200,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        
    )
    canvasForAmusements.place(x=30, y=405)

    previousBtn = ""
    nextBtn = ""

    previousBtn_image = PhotoImage(
        file=relative_to_assets("button_4.png"))
    previousBtn = Button(
        image=previousBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printElementPrevious(amusementList, canvasForAmusements, nextBtn, previousBtn, 7, 1),
        relief="flat"
        )
    previousBtn.place(
        x=500.0,
        y=612.0,
        width=207.0,
        height=74.0
        )

    nextBtn_image = PhotoImage(
        file=relative_to_assets("button_3.png"))
    nextBtn = Button(
        image=nextBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printElementNext(amusementList, canvasForAmusements, nextBtn, previousBtn, 7, 1),
        relief="flat"
        )
    nextBtn.place(
        x=716.0,
        y=612.0,
        width=207.0,
        height=74.0
        )
    
    printElementNext(amusementList, canvasForAmusements, nextBtn, previousBtn, 7, 1)

    #Current Status
    currentStateComboBox = ttk.Combobox(window, values=list(currentStateDic.values()), state="readonly")
    currentStateComboBox.place(
        x=620.0,
        y=300.0,
        width=170.0,
        height=42.0
    )
    currentStateComboBox.set("Select an option")

    #Amusement Type
    amusementTypeComboBox = ttk.Combobox(window, values=list(amusementTypes.values()), state="readonly")
    amusementTypeComboBox.place(
        x=235.0,
        y=300.0,
        width=170.0,
        height=42.0
    )
    amusementTypeComboBox.set("Select an option")

    #Zones
    zonesComboBox = ttk.Combobox(window, values=list(zones.values()), state="readonly")
    zonesComboBox.place(
        x=43.0,
        y=300.0,
        width=170.0,
        height=42.0
    )
    zonesComboBox.set("Select an option")

    #Intensity
    intensityComboBox = ttk.Combobox(window, values=list(intensityDic.values()), state="readonly")
    intensityComboBox.place(
        x=430.0,
        y=300.0,
        width=170.0,
        height=42.0
    )
    intensityComboBox.set("Select an option")

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (amusementList.clear(), amusementList.extend(searchAmusementList(zonesComboBox.get(), amusementTypeComboBox.get(), intensityComboBox.get(), currentStateComboBox.get(), zones, amusementTypes)), printElementNext(amusementList, canvasForAmusements, nextBtn, previousBtn, 7, 1), resetFields(currentStateComboBox, amusementTypeComboBox, zonesComboBox, intensityComboBox)),
        relief="flat"
    )
    button_2.place(
        x=803.0,
        y=294.0,
        width=122.0,
        height=58.0
    )

    window.resizable(False, False)
    window.mainloop()

def printAmusementInfo():
    canvas = Canvas(
        window,
        bg = "#17172A",
        height = 700,
        width = 950,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        475.0,
        439.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: searchAndPrintAmusementInfo(entryCodeToSearch.get(), entryName, entryLatitude, entryLongitude, entryMinAge, entryMinHeight, entryAmusementType, entryZone, entryIntensity, entryCurrentState, entryDescription),
        relief="flat"
    )
    button_1.place(
        x=258.0,
        y=278.0,
        width=128.0,
        height=49.0
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        70.0,
        347.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        300.0,
        347.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        530.0,
        347.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        94.0,
        593.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        151.0,
        222.0,
        image=image_image_8
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        480.0,
        649.0,
        image=image_image_10
    )

    #Entry Description
    entryDescription = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        state='disabled'
    )
    entryDescription.place(
        x=58.0,
        y=628.0,
        width=845.0,
        height=45.0
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        367.0,
        385.0,
        image=image_image_11
    )

    #Entry Latitude
    entryLatitude = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,       
        state='disabled',
        disabledbackground="white"
    )
    entryLatitude.place(
        x=269.0,
        y=374.0,
        width=198.0,
        height=21.0
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        589.0,
        385.0,
        image=image_image_12
    )

    #Longitude
    entryLongitude = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,       
        state='disabled',
        disabledbackground="white"
    )
    entryLongitude.place(
        x=492.0,
        y=374.0,
        width=196.0,
        height=21.0
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        147.0,
        385.0,
        image=image_image_13
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        284.0,
        429.0,
        image=image_image_14
    )

    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        555.0,
        429.0,
        image=image_image_15
    )

    image_image_16 = PhotoImage(
        file=relative_to_assets("image_16.png"))
    image_16 = canvas.create_image(
        768.0,
        347.0,
        image=image_image_16
    )

    image_image_17 = PhotoImage(
        file=relative_to_assets("image_17.png"))
    image_17 = canvas.create_image(
        117.0,
        427.0,
        image=image_image_17
    )

    image_image_18 = PhotoImage(
        file=relative_to_assets("image_18.png"))
    image_18 = canvas.create_image(
        747.0,
        429.0,
        image=image_image_18
    )

    image_image_19 = PhotoImage(
        file=relative_to_assets("image_19.png"))
    image_19 = canvas.create_image(
        811.0,
        385.0,
        image=image_image_19
    )

    #Entry Minimum Age
    entryMinAge = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,       
        state='disabled',
        disabledbackground="white"
    )
    entryMinAge.place(
        x=713.0,
        y=374.0,
        width=198.0,
        height=21.0
    )

    image_image_20 = PhotoImage(
        file=relative_to_assets("image_20.png"))
    image_20 = canvas.create_image(
        146.0,
        466.0,
        image=image_image_20
    )

    #Entry Minimum Height
    entryMinHeight = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,       
        state='disabled',
        disabledbackground="white"
    )
    entryMinHeight.place(
        x=49.0,
        y=455.0,
        width=196.0,
        height=21.0
    )

    image_image_21 = PhotoImage(
        file=relative_to_assets("image_21.png"))
    image_21 = canvas.create_image(
        146.0,
        546.0,
        image=image_image_21
    )

    #Entry Current Status
    entryCurrentState = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,       
        state='disabled',
        disabledbackground="white"
    )
    entryCurrentState.place(
        x=49.0,
        y=535.0,
        width=196.0,
        height=21.0
    )

    image_image_22 = PhotoImage(
        file=relative_to_assets("image_22.png"))
    image_22 = canvas.create_image(
        368.0,
        466.0,
        image=image_image_22
    )

    #Entry Amusement Type
    entryAmusementType = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,       
        state='disabled',
        disabledbackground="white"
    )
    entryAmusementType.place(
        x=271.0,
        y=455.0,
        width=196.0,
        height=21.0
    )

    image_image_23 = PhotoImage(
        file=relative_to_assets("image_23.png"))
    image_23 = canvas.create_image(
        589.0,
        466.0,
        image=image_image_23
    )

    #Entry Zone
    entryZone = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,       
        state='disabled',
        disabledbackground="white"
    )
    entryZone.place(
        x=492.0,
        y=455.0,
        width=196.0,
        height=21.0
    )

    image_image_24 = PhotoImage(
        file=relative_to_assets("image_24.png"))
    image_24 = canvas.create_image(
        812.0,
        466.0,
        image=image_image_24
    )

    #Entry Intensity
    entryIntensity = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,       
        state='disabled',
        disabledbackground="white"
    )
    entryIntensity.place(
        x=715.0,
        y=455.0,
        width=196.0,
        height=21.0
    )

    image_image_25 = PhotoImage(
        file=relative_to_assets("image_25.png"))
    image_25 = canvas.create_image(
        103.0,
        509.0,
        image=image_image_25
    )

    #Entry Name
    entryName = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,      
        state='disabled',
        disabledbackground="white"
    )
    entryName.place(
        x=48.0,
        y=374.0,
        width=198.0,
        height=21.0
    )

    image_image_26 = PhotoImage(
        file=relative_to_assets("image_26.png"))
    image_26 = canvas.create_image(
        62.0,
        263.0,
        image=image_image_26
    )

    image_image_27 = PhotoImage(
        file=relative_to_assets("image_27.png"))
    image_27 = canvas.create_image(
        147.0,
        301.0,
        image=image_image_27
    )

    #Entry Code To Seach
    entryCodeToSearch = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entryCodeToSearch.place(
        x=48.0,
        y=290.0,
        width=198.0,
        height=21.0
    )

    image_image_28 = PhotoImage(
        file=relative_to_assets("image_28.png"))
    image_28 = canvas.create_image(
        475.0,
        127.0,
        image=image_image_28
    )

    image_image_29 = PhotoImage(
        file=relative_to_assets("image_29.png"))
    image_29 = canvas.create_image(
        183.0,
        126.0,
        image=image_image_29
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menuVisitor"),
        relief="flat"
    )
    button_2.place(
        x=708.0,
        y=91.0,
        width=217.0,
        height=71.0
    )
    window.resizable(False, False)
    window.mainloop()

def printAccommodationList():

    zones, accommodationList = getAccommodationListInitialData()

    canvas = Canvas(
        window,
        bg = "#17172A",
        height = 700,
        width = 950,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        475.0,
        439.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        52.0,
        385.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        146.0,
        384.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        464.0,
        384.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        644.0,
        384.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        303.0,
        384.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        861.0,
        384.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        66.0,
        275.0,
        image=image_image_8
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_11
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        183.0,
        124.0,
        image=image_image_12
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menuvisitor"),
        relief="flat"
    )
    button_1.place(
        x=708.0,
        y=89.0,
        width=217.0,
        height=71.0
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        150.0,
        222.0,
        image=image_image_13
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_14
    )

    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        361.0,
        275.0,
        image=image_image_15
    )

    canvasForAccommodations = Canvas(
        window,
        bg = "#354C80",
        #bg = "red",
        height = 200,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        
    )
    canvasForAccommodations.place(x=30, y=405)

    previousBtn = ""
    nextBtn = ""

    previousBtn_image = PhotoImage(
        file=relative_to_assets("button_4.png"))
    previousBtn = Button(
        image=previousBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printElementPrevious(accommodationList, canvasForAccommodations, nextBtn, previousBtn, 7, 2),
        relief="flat"
        )
    previousBtn.place(
        x=500.0,
        y=612.0,
        width=207.0,
        height=74.0
        )

    nextBtn_image = PhotoImage(
        file=relative_to_assets("button_3.png"))
    nextBtn = Button(
        image=nextBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printElementNext(accommodationList, canvasForAccommodations, nextBtn, previousBtn, 7, 2),
        relief="flat"
        )
    nextBtn.place(
        x=716.0,
        y=612.0,
        width=207.0,
        height=74.0
        )
    
    printElementNext(accommodationList, canvasForAccommodations, nextBtn, previousBtn, 7, 2)

    #Current Status
    currentStateComboBox = ttk.Combobox(window, values=list(currentStateDic.values()), state="readonly")
    currentStateComboBox.place(
        x=333.0,
        y=300.0,
        width=250.0,
        height=42.0
    )
    currentStateComboBox.set("Select an option")

    #Zones
    zonesComboBox = ttk.Combobox(window, values=list(zones.values()), state="readonly")
    zonesComboBox.place(
        x=43.0,
        y=300.0,
        width=250.0,
        height=42.0
    )
    zonesComboBox.set("Select an option")

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (accommodationList.clear(), accommodationList.extend(searchAccommodationList(zonesComboBox.get(), currentStateComboBox.get(), zones)), printElementNext(accommodationList, canvasForAccommodations, nextBtn, previousBtn, 7, 2), currentStateComboBox.set("Select an option"), zonesComboBox.set("Select an option")),
        relief="flat"
    )
    button_2.place(
        x=600.0,
        y=294.0,
        width=122.0,
        height=58.0
    )

    window.resizable(False, False)
    window.mainloop()

def printTrainRouteList():

    zones, trainStops, trainRouteList = getTrainRouteListInitialData()

    canvas = Canvas(
        window,
        bg = "#17172A",
        height = 700,
        width = 950,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        475.0,
        439.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        52.0,
        385.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        146.0,
        384.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        520.0,
        384.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        690.0,
        384.0,
        image=image_image_5
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        330.0,
        384.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        861.0,
        384.0,
        image=image_image_8
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        93.0,
        275.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_11
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_12
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        183.0,
        124.0,
        image=image_image_13
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menuvisitor"),
        relief="flat"
    )
    button_1.place(
        x=708.0,
        y=89.0,
        width=217.0,
        height=71.0
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        114.0,
        222.0,
        image=image_image_14
    )

    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_15
    )

    canvasForTrainRoutes = Canvas(
        window,
        bg = "#354C80",
        #bg = "red",
        height = 200,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        
    )
    canvasForTrainRoutes.place(x=30, y=405)

    previousBtn = ""
    nextBtn = ""

    previousBtn_image = PhotoImage(
        file=relative_to_assets("button_4.png"))
    previousBtn = Button(
        image=previousBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printElementPrevious(trainRouteList, canvasForTrainRoutes, nextBtn, previousBtn, 7, 3),
        relief="flat"
        )
    previousBtn.place(
        x=500.0,
        y=612.0,
        width=207.0,
        height=74.0
        )

    nextBtn_image = PhotoImage(
        file=relative_to_assets("button_3.png"))
    nextBtn = Button(
        image=nextBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printElementNext(trainRouteList, canvasForTrainRoutes, nextBtn, previousBtn, 7, 3),
        relief="flat"
        )
    nextBtn.place(
        x=716.0,
        y=612.0,
        width=207.0,
        height=74.0
        )
    
    printElementNext(trainRouteList, canvasForTrainRoutes, nextBtn, previousBtn, 7, 3)

    #Zones
    zonesComboBox = ttk.Combobox(window, values=list(zones.values()), state="readonly")
    zonesComboBox.place(
        x=43.0,
        y=300.0,
        width=250.0,
        height=42.0
    )
    zonesComboBox.set("Select an option")

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (trainRouteList.clear(), trainRouteList.extend(searchTrainRouteList(zonesComboBox.get(), zones, trainStops)), printElementNext(trainRouteList, canvasForTrainRoutes, nextBtn, previousBtn, 7, 3),  zonesComboBox.set("Select an option")),
        relief="flat"
    )
    button_2.place(
        x=310.0,
        y=294.0,
        width=122.0,
        height=58.0
    )

    window.resizable(False, False)
    window.mainloop()

def printZoneInfo():
    canvas = Canvas(
        window,
        bg = "#17172A",
        height = 700,
        width = 950,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        475.0,
        439.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        65.0,
        272.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        66.0,
        456.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        175.0,
        456.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        400.0,
        456.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        667.0,
        272.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        81.0,
        355.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        473.0,
        355.0,
        image=image_image_8
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        70.0,
        222.0,
        image=image_image_11
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_12
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        665.0,
        397.0,
        image=image_image_13
    )

    #Entry Description
    entryDescription = Text(
        bd=0,
        bg="#FFFFFF",      
        fg="#000716",
        highlightthickness=0,
        state='disabled',
    )
    entryDescription.place(
        x=429.0,
        y=382.0,
        width=474.0,
        height=31.0
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        770.0,
        314.0,
        image=image_image_14
    )

    #Entry Name
    entryName = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        state='disabled',
        disabledbackground="white"
    )
    entryName.place(
        x=643.0,
        y=302.0,
        width=256.0,
        height=25.0
    )

    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        132.0,
        397.0,
        image=image_image_15
    )

    entryLatitude = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        state='disabled',
        disabledbackground="white"
    )
    entryLatitude.place(
        x=49.0,
        y=385.0,
        width=168.0,
        height=25.0
    )

    image_image_16 = PhotoImage(
        file=relative_to_assets("image_16.png"))
    image_16 = canvas.create_image(
        282.0,
        272.0,
        image=image_image_16
    )

    image_image_17 = PhotoImage(
        file=relative_to_assets("image_17.png"))
    image_17 = canvas.create_image(
        278.0,
        355.0,
        image=image_image_17
    )

    image_image_18 = PhotoImage(
        file=relative_to_assets("image_18.png"))
    image_18 = canvas.create_image(
        322.0,
        397.0,
        image=image_image_18
    )

    entryLongitude = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        state='disabled',
        disabledbackground="white"
    )
    entryLongitude.place(
        x=239.0,
        y=385.0,
        width=168.0,
        height=25.0
    )

    image_image_19 = PhotoImage(
        file=relative_to_assets("image_19.png"))
    image_19 = canvas.create_image(
        131.0,
        311.0,
        image=image_image_19
    )

    #Entry Code
    entryCodeToSearch = Entry(
        bd=0,
        bg="#FFFFFF",        
        fg="#000716",
        highlightthickness=0,
    )
    entryCodeToSearch.place(
        x=46.0,
        y=300.0,
        width=171.0,
        height=21.0
    )

    image_image_20 = PhotoImage(
        file=relative_to_assets("image_20.png"))
    image_20 = canvas.create_image(
        475.0,
        126.0,
        image=image_image_20
    )

    image_image_21 = PhotoImage(
        file=relative_to_assets("image_21.png"))
    image_21 = canvas.create_image(
        183.0,
        125.0,
        image=image_image_21
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menuvisitor"),
        relief="flat"
    )
    button_1.place(
        x=708.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    elementsList = []

    canvasForElements = Canvas(
        window,
        bg = "#354C80",
        #bg = "red",
        height = 140,
        width = 880,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        
    )
    canvasForElements.place(x=40, y=475)

    previousBtn = ""
    nextBtn = ""

    previousBtn_image = PhotoImage(
        file=relative_to_assets("button_4.png"))
    previousBtn = Button(
        image=previousBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printElementPrevious(elementsList, canvasForElements, nextBtn, previousBtn, 5, 4),
        relief="flat"
        )
    previousBtn.place(
        x=500.0,
        y=612.0,
        width=207.0,
        height=74.0
        )

    nextBtn_image = PhotoImage(
        file=relative_to_assets("button_3.png"))
    nextBtn = Button(
        image=nextBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printElementNext(elementsList, canvasForElements, nextBtn, previousBtn, 5, 4),
        relief="flat"
        )
    nextBtn.place(
        x=716.0,
        y=612.0,
        width=207.0,
        height=74.0
        )
    
    printElementNext(elementsList, canvasForElements, nextBtn, previousBtn, 5, 4)

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (elementsList.clear(), elementsList.extend(searchAndPrintZoneInfo(entryCodeToSearch.get(), searchForComboBox.get(), entryName, entryLatitude, entryLongitude, entryDescription, searchFor)), printElementNext(elementsList, canvasForElements, nextBtn, previousBtn, 5, 4)),
        relief="flat"
    )
    button_2.place(
        x=474.0,
        y=284.0,
        width=136.0,
        height=54.0
    )

    searchFor = {0:"Diversões", 1:"Comodidades", 2:"Paragens de Comboio"}

    #Search For
    searchForComboBox = ttk.Combobox(window, values=list(searchFor.values()), state="readonly")
    searchForComboBox.place(
        x=233.0,
        y=290.0,
        width=230.0,
        height=37.0
    )
    searchForComboBox.set("Select an option")


    window.resizable(False, False)
    window.mainloop()

def printZoneList():

    zoneList = getZoneListInitialData()

    canvas = Canvas(
        window,
        bg = "#17172A",
        height = 700,
        width = 950,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        475.0,
        439.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        65.0,
        282.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        197.0,
        281.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        427.0,
        281.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        680.0,
        281.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_8
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        183.0,
        124.0,
        image=image_image_9
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menuvisitor"),
        relief="flat"
    )
    button_1.place(
        x=708.0,
        y=89.0,
        width=217.0,
        height=71.0
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        75.0,
        222.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_11
    )

    canvasForZones = Canvas(
        window,
        bg = "#354C80",
        #bg = "red",
        height = 300,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        
    )
    canvasForZones.place(x=30, y=305)

    previousBtn = ""
    nextBtn = ""

    previousBtn_image = PhotoImage(
        file=relative_to_assets("button_4.png"))
    previousBtn = Button(
        image=previousBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printElementPrevious(zoneList, canvasForZones, nextBtn, previousBtn, 10, 5),
        relief="flat"
        )
    previousBtn.place(
        x=500.0,
        y=612.0,
        width=207.0,
        height=74.0
        )

    nextBtn_image = PhotoImage(
        file=relative_to_assets("button_3.png"))
    nextBtn = Button(
        image=nextBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printElementNext(zoneList, canvasForZones, nextBtn, previousBtn, 10, 5),
        relief="flat"
        )
    nextBtn.place(
        x=716.0,
        y=612.0,
        width=207.0,
        height=74.0
        )
    
    printElementNext(zoneList, canvasForZones, nextBtn, previousBtn, 10, 5)

    window.resizable(False, False)
    window.mainloop()

def printTicketQRCode():
    canvas = Canvas(
        window,
        bg = "#17172A",
        height = 700,
        width = 950,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        475.0,
        439.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        119.0,
        275.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_4
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: generateTicketQRCode(entryRef.get(), canvasForQRCode),
        relief="flat"
    )
    button_1.place(
        x=331.0,
        y=294.0,
        width=159.0,
        height=60.0
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        141.0,
        222.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_6
    )

    canvas.create_rectangle(
        35.0,
        291.0,
        331.0,
        356.0,
        fill="#354C80",
        outline="")

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        184.0,
        321.0,
        image=image_image_7
    )

    entryRef = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entryRef.place(
        x=52.0,
        y=308.0,
        width=265.0,
        height=26.0
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        474.0,
        126.0,
        image=image_image_8
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        182.0,
        125.0,
        image=image_image_9
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menuvisitor"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    canvasForQRCode = Canvas(
        window,
        bg = "#354C80",
        #bg = "red",
        height = 270,
        width = 270,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        
    )
    canvasForQRCode.place(x=350, y=380)

    window.resizable(False, False)
    window.mainloop()

window = Tk()

window.geometry("950x700")
window.configure(bg = "#ECEEED")
window.title("HogwartsPark")

printMenu()