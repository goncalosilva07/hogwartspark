from pathlib import Path
import random
import ctypes
from country_list import countries_for_language
from datetime import datetime, timedelta
from math import sin, cos, sqrt, atan2, radians
from HogwartsPark import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk
import tkinter as tk
import hashlib

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../assets/frame_login")

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

def haversine(lat1, lon1, lat2, lon2):
    # Raio médio da Terra em metros
    R = 6371000.0

    # Converte as latitudes e longitudes de graus para radianos
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Diferença de latitudes e longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return int(distance)

''' Functions '''

def login(user, password):
    file = open("../Dados/users.txt", "r")

    for linha in file:
        line = linha.strip().split(",")
        hasher = hashlib.sha256()
        # Converte a senha para bytes antes de alimentar o hasher
        password_bytes = password.encode('utf-8')
        # Atualiza o hasher com os bytes da senha
        hasher.update(password_bytes)
        # Obtem o hash resultante como uma string hexadecimal
        hashed_password = hasher.hexdigest()
        if line[0] == user and line[1] == hashed_password:
            global userName, house
            userName = line[0]
            house = line[2]
            deleteEntrysAndLabels()
            changeAssetsPath("frame_menu")
            printMenu()
        
    file.close()

def register(user, password, repeatpassword):
    file = open("../Dados/users.txt", "r")
    erro = 0
    
    for line in file:
        line = line.strip().split(",")
        if line[0] == user:
            erro = 1

    file.close()

    if erro == 0:
        if (user != "" and user != None) and password != "" and password == repeatpassword:
            file = open("../Dados/users.txt", "a")
            house = chooseHouse()

            hasher = hashlib.sha256()
            # Converte a senha para bytes antes de alimentar o hasher
            password_bytes = password.encode('utf-8')
            # Atualiza o hasher com os bytes da senha
            hasher.update(password_bytes)
            # Obtem o hash resultante como uma string hexadecimal
            hashed_password = hasher.hexdigest()

            file.writelines(user + "," + hashed_password + "," + house + "\n")
            file.close()
            changeMenuOption(printLogin, "frame_login")
        else: 
            ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)
    else:
        ctypes.windll.user32.MessageBoxW(0, "Username already exists\nTry a different one", "Error!", 0)

def chooseHouse():
        num = random.randrange(1,4)

        if num == 1:
            return "Gryffindor"
        elif num == 2:
            return "Slytherin"
        elif num == 3:
            return "Ravenclaw"
        elif num == 4:
            return "Hufflepuff"
 
def addZone(zoneName, latitude, longitude, description):
    
    code = generateCode("zones.txt")

    try: 
        latitude = float(latitude)
        longitude = float(longitude)
        description = description.strip()
        zoneName = zoneName.strip()

        if zoneName != "" and (latitude <= 90 and latitude >= -90) and (longitude <= 180 and longitude >= -180) and description != "":
            file = open("../Dados/zones.txt", "a")  
            file.writelines(code + "," + zoneName + "," + str(latitude) + "," + str(longitude) + "," + description + "\n")
            file.close()
            changeMenuOption(printMenu, "frame_menu")
        else:
            ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)
    except:
         ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)
  
def addAmusement(amusementName, latitude, longitude, minAge, minHeight, codAmusementType, codZone, codIntensity, codCurrentState, description, amusementTypes, zones):
   
    codAmusementType = getKeyByValue(amusementTypes, codAmusementType)
    codZone = getKeyByValue(zones, codZone)
    codIntensity = getKeyByValue(intensity, codIntensity)
    #codCurrentState = getKeyByValue(currentState, codCurrentState)

    code = generateCode("amusements.txt")

    try:
        latitude = float(latitude)
        longitude = float(longitude)
        minAge = int(minAge)
        minHeight = int(minHeight)
        description = description.strip()
        amusementName = amusementName.strip()
        
        if amusementName != "" and codAmusementType != "" and codZone != "" and (latitude <= 90 and latitude >= -90) and (longitude <= 180 and longitude >= -180) and description != "" and (minAge > 0 and minAge <= 18) and (minHeight > 0 and minHeight <= 200) and codIntensity != "" and codCurrentState != "":
            file = open("../Dados/amusements.txt", "a")  
            file.writelines(code + "," + amusementName+ "," + codZone + "," + codAmusementType + "," + str(latitude) + "," + str(longitude) + "," + str(minAge) + "," + str(minHeight) + "," + str(codIntensity) + "," + codCurrentState + "," + description + "\n")
            file.close()
            changeMenuOption(printMenu, "frame_menu")
        else:
            ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)

    except: 
        ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)

def getAddAmusementInitialData():
    amusementTypes = {}
    zones = {}

    amusementTypesFile = open("../Dados/amusementType.txt", "r")
    zonesFile = open("../Dados/zones.txt", "r")

    for line in amusementTypesFile:
        line = line.strip().split(",")
        amusementTypes[line[0]] = line[1]

    amusementTypesFile.close()

    for line in zonesFile:
        line = line.strip().split(",")
        zones[line[0]] = line[1]
        
    zonesFile.close()

    return amusementTypes, zones

def generateCode(file):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'.upper()
    code = ""
    exists = False
    i = 1

    file = open("../Dados/" + file, "r")  
    allCodes = []

    for var in file.readlines():
        allCodes.append(var.split(",")[0])
    
    while(i < 4):
        if code in allCodes:
            i = 1
            code = ""

        for var in range(4):
            num = random.randrange(0,25)
            code = code + alphabet[num]
            i = i + 1

    file.close()
    return code

def getKeyByValue(dictionary, value):
    for key in dictionary:
        if dictionary[key] == value:
            value = key
    
    if value == "Select an option":
        value = ""
    
    return value

def getValueByKey(dictionary, value):
    for key in dictionary:
        if key == value:
            value = dictionary[key]
 
    return value

def addAccommodationInitialData():
    zones = {}

    zonesFile = open("../Dados/zones.txt", "r")

    for line in zonesFile:
        line = line.strip().split(",")
        zones[line[0]] = line[1]
        
    zonesFile.close()

    return zones

def addAccommodation(name, latitude, longitude, codZone, codCurrentState, description, zones):
   
    codZone = getKeyByValue(zones, codZone)
    #codCurrentState = getKeyByValue(currentState, codCurrentState)

    code = generateCode("accommodations.txt")

    try:
        latitude = float(latitude)
        longitude = float(longitude)
        description = description.strip()
        name = name.strip()
        
        if name != "" and codZone != "" and (latitude <= 90 and latitude >= -90) and (longitude <= 180 and longitude >= -180) and description != "" and codCurrentState != "":
            file = open("../Dados/accommodations.txt", "a")  
            file.writelines(code + "," + name + "," + codZone + "," + str(latitude) + "," + str(longitude) + "," + codCurrentState + "," + description + "\n")
            file.close()
            changeMenuOption(printMenu, "frame_menu")
        else:
            ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)

    except: 
        ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)

def addTrainStopInitialData():
    zones = {}

    zonesFile = open("../Dados/zones.txt", "r")

    for line in zonesFile:
        line = line.strip().split(",")
        zones[line[0]] = line[1]
        
    zonesFile.close()

    return zones

def addTrainStop(name, latitude, longitude, codZone, description, zones):
   
    codZone = getKeyByValue(zones, codZone)

    code = generateCode("trainStops.txt")

    try:
        latitude = float(latitude)
        longitude = float(longitude)
        description = description.strip()
        name = name.strip()
        
        if name != "" and codZone != "" and (latitude <= 90 and latitude >= -90) and (longitude <= 180 and longitude >= -180) and description != "":
            file = open("../Dados/trainStops.txt", "a")  
            file.writelines(code + "," + name + "," + codZone + "," + str(latitude) + "," + str(longitude) + "," + description + "\n")
            file.close()
            changeMenuOption(printMenu, "frame_menu")
        else:
            ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)

    except: 
        ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)

def getIssueTicketInitialData():
    ticketTypes = {}
    nationalities = {}

    ticketTypesFile = open("../Dados/ticketType.txt", "r")

    for line in ticketTypesFile:
        line = line.strip().split(",")
        ticketTypes[line[0]] = (line[1], line[2])

    ticketTypesFile.close()

    for language in countries_for_language('en'):
        nationalities[language[0]] = language[1]
    
    return ticketTypes, nationalities

def setTicketDate(event, ticketTypes, startDate, startHour, endDate, endHour):
    #park opening hours - 9h to 23h
    ticketType = event.widget.get()

    for var in ticketTypes.values():
        if var[0] == ticketType:
            now = datetime.now()
            insertEntryDate(startDate, (str(now.day) + "/" + str(now.month) + "/" + str(now.year)))
            insertEntryDate(startHour, (str(now.hour) + ":" + (str(now.minute) if now.minute >= 10 else "0" + str(now.minute))))

            aux = now + timedelta(hours=int(var[1]))
            endOfTime = now.replace(hour=23)

            if aux > endOfTime:
                hour = int(var[1]) - (23 - now.hour)
                days = 0

                while(hour >= 14):                    
                    hour = hour - 14
                    days = days + 1

                if hour == 0:
                    now = now.replace(day=now.day + 1 + days, hour=23, minute= (now.minute if now.minute >= 30 else 0))
                else:
                    now = now.replace(day=now.day + 1 + days, hour=9) + timedelta(hours=hour)

                insertEntryDate(endDate, (str(now.day) + "/" + str(now.month) + "/" + str(now.year)))
                insertEntryDate(endHour, (str(now.hour) + ":" + (str(now.minute) if now.minute >= 10 else "0" + str(now.minute))))
            else:
                insertEntryDate(endDate, (str(aux.day) + "/" + str(aux.month) + "/" + str(aux.year)))
                insertEntryDate(endHour, (str(aux.hour) + ":" + (str(aux.minute) if aux.minute >= 10 else "0" + str(aux.minute))))

def insertEntryDate(entry, data):
    entry.configure(state="normal")
    entry.delete(0, "end")
    entry.insert(0, data)
    entry.configure(state="disabled")

def addTicket(personName, nationality, ticketType, startDate, startHour, endDate, endHour, ticketTypes):
    for key in ticketTypes:
        if ticketTypes[key][0] == ticketType:
            ticketType = key
    
    if ticketType == "Select an option":
        ticketType = ""

    if nationality == "Select an option":
        nationality = ""

    code = generateReference("ticket.txt")

    try:       
        personName = personName.strip()
        
        if personName != "" and ticketType != "" and nationality != "" and startDate != "" and startHour != "" and endDate != "" and endHour != "":
            file = open("../Dados/ticket.txt", "a")  
            file.writelines(code + "," + personName + "," + nationality + "," + ticketType + "," + startDate + "," + startHour + "," + endDate + "," + endHour + "\n")
            file.close()
            changeMenuOption(printMenu, "frame_menu")
        else:
            ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)

    except: 
        ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)

def generateReference(file):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'.upper()
    code = "REF-"
    exists = False
    i = 1

    file = open("../Dados/" + file, "r")  
    allCodes = []

    for var in file.readlines():
        allCodes.append(var.split(",")[0])
    
    while(i < 4):
        if code in allCodes:
            i = 1
            code = "REF-"

        for var in range(4):
            num = random.randrange(0,25)
            code = code + alphabet[num]
            i = i + 1

    file.close()
    return code
    
def getTicketListing():
    global ticketPosition
    ticketPosition = 0

    ticketList = []
    ticketTypes = {}

    ticketTypesFile = open("../Dados/ticketType.txt", "r")

    for line in ticketTypesFile:
        line = line.strip().split(",")
        ticketTypes[line[0]] = (line[1], line[2])

    ticketTypesFile.close()

    file = open("../Dados/ticket.txt", "r")   

    for var in file.readlines():
        ticket = {}
        var = var.strip("\n").split(",")

        ticket["ref"] = var[0] 
        ticket["name"] = var[1]
        ticket["nationality"] = var[2]
        ticket["ticketType"] = getValueByKey(ticketTypes, var[3])[0]    
        ticket["startDate"] = var[4]
        ticket["startHour"] = var[5]
        ticket["endDate"] = var[6]
        ticket["endHour"] = var[7]
        
        ticketList.append(ticket)

    file.close()
    return ticketList

def printTicketsNext(tickets, canvasForTickets, nextBtn, previousBtn, numberOfTicketsToShow):
    global ticketPosition
    global actualPosition
    positionY = 1
    objective = 0

    if actualPosition == 0 and (((ticketPosition + numberOfTicketsToShow) - len(tickets)) < numberOfTicketsToShow):
        ticketPosition = ticketPosition + numberOfTicketsToShow

    canvasForTickets.delete('all')

    if ticketPosition <= numberOfTicketsToShow:
        previousBtn.place_forget()

    if ticketPosition + numberOfTicketsToShow <= len(tickets):
        objective = ticketPosition + numberOfTicketsToShow
    else:
        objective = len(tickets)
        
    for var in range(ticketPosition, objective):
        try:
            canvasForTickets.create_text(
            7,
            positionY,
            anchor="nw",
            text=tickets[var]["ref"],
            fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                86,
                positionY,
                anchor="nw",
                text=tickets[var]["name"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                187,
                positionY,
                anchor="nw",
                text=tickets[var]["nationality"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                360,
                positionY,
                anchor="nw",
                text=tickets[var]["ticketType"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                478.0,
                positionY,
                anchor="nw",
                text=tickets[var]["startDate"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                585.0,
                positionY,
                anchor="nw",
                text=tickets[var]["startHour"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                705.0,
                positionY,
                anchor="nw",
                text=tickets[var]["endDate"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                810.0,
                positionY,
                anchor="nw",
                text=tickets[var]["endHour"],
                fill="#FFFFFF"
            )
            positionY = positionY + 30
            ticketPosition = ticketPosition + 1
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

    actualPosition = 1

    if ticketPosition <= numberOfTicketsToShow:
        previousBtn.place_forget() 
    else:
        previousBtn.place(
            x=500.0,
            y=612.0,
            width=207.0,
            height=74.0
            ) 
            
    if len(tickets) - ticketPosition != 0:
        nextBtn.place(
            x=716.0,
            y=612.0,
            width=207.0,
            height=74.0
            ) 
    else:
        nextBtn.place_forget() 

def printTicketsPrevious(tickets, canvasForTickets, nextBtn, previousBtn, numberOfTicketsToShow):
    global ticketPosition
    global actualPosition
    positionY = 1
    objective = 0

    canvasForTickets.delete('all')

    if actualPosition == 1 and (len(tickets) != ticketPosition):
        ticketPosition = ticketPosition - numberOfTicketsToShow

    if (ticketPosition - numberOfTicketsToShow) + 1 <= numberOfTicketsToShow:
        previousBtn.place_forget()

    if len(tickets) == ticketPosition:
        if ticketPosition % numberOfTicketsToShow != 0:
            objective = (len(tickets) - (ticketPosition % numberOfTicketsToShow)) - numberOfTicketsToShow
            ticketPosition = ticketPosition - (ticketPosition % numberOfTicketsToShow)
        else:
            objective = len(tickets) - (numberOfTicketsToShow * 2)
            ticketPosition = ticketPosition - numberOfTicketsToShow
    elif ticketPosition == numberOfTicketsToShow:
        objective = 0
    else:
        #objective = ticketPosition - (numberOfTicketsToShow * 2)
        objective = ticketPosition - numberOfTicketsToShow
        #ticketPosition = ticketPosition - numberOfTicketsToShow

    actualPosition = 0

    for var in range(ticketPosition - 1, objective - 1, -1):
        try:
            canvasForTickets.create_text(
            7,
            positionY,
            anchor="nw",
            text=tickets[var]["ref"],
            fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                86,
                positionY,
                anchor="nw",
                text=tickets[var]["name"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                187,
                positionY,
                anchor="nw",
                text=tickets[var]["nationality"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                360,
                positionY,
                anchor="nw",
                text=tickets[var]["ticketType"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                478.0,
                positionY,
                anchor="nw",
                text=tickets[var]["startDate"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                585.0,
                positionY,
                anchor="nw",
                text=tickets[var]["startHour"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                705.0,
                positionY,
                anchor="nw",
                text=tickets[var]["endDate"],
                fill="#FFFFFF"
            )

            canvasForTickets.create_text(
                810.0,
                positionY,
                anchor="nw",
                text=tickets[var]["endHour"],
                fill="#FFFFFF"
            )
            positionY = positionY + 30

            ticketPosition = ticketPosition - 1
            if ticketPosition == 0:
                ticketPosition = numberOfTicketsToShow
                actualPosition = 1
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

    if len(tickets) - ticketPosition != 0:
        nextBtn.place(
            x=716.0,
            y=612.0,
            width=207.0,
            height=74.0
            ) 
    else:
        nextBtn.place_forget() 

def getTicketByRef(ref, canvasForTicket):
    ticketTypes = {}
    ticket = {}
    positionY = 1

    ticketTypesFile = open("../Dados/ticketType.txt", "r")

    for line in ticketTypesFile:
        line = line.strip().split(",")
        ticketTypes[line[0]] = (line[1], line[2])

    ticketTypesFile.close()

    file = open("../Dados/ticket.txt", "r")   

    for var in file.readlines():
        var = var.strip("\n").split(",")

        if var[0] == ref:
            ticket["ref"] = var[0] 
            ticket["name"] = var[1]
            ticket["nationality"] = var[2]
            ticket["ticketType"] = getValueByKey(ticketTypes, var[3])[0]    
            ticket["startDate"] = var[4]
            ticket["startHour"] = var[5]
            ticket["endDate"] = var[6]
            ticket["endHour"] = var[7]
            break

    file.close()

    if len(ticket) == 0:
         ctypes.windll.user32.MessageBoxW(0, "The reference given does not correspond to any ticket!\nCheck the reference given.", "Error!", 0)
    else:
        canvasForTicket.delete('all')
        canvasForTicket.create_text(
            7,
            positionY,
            anchor="nw",
            text=ticket["ref"],
            fill="#FFFFFF"
        )

        canvasForTicket.create_text(
            86,
            positionY,
            anchor="nw",
            text=ticket["name"],
            fill="#FFFFFF"
        )

        canvasForTicket.create_text(
            187,
            positionY,
            anchor="nw",
            text=ticket["nationality"],
            fill="#FFFFFF"
        )

        canvasForTicket.create_text(
            360,
            positionY,
            anchor="nw",
            text=ticket["ticketType"],
            fill="#FFFFFF"
        )

        canvasForTicket.create_text(
            478.0,
            positionY,
            anchor="nw",
            text=ticket["startDate"],
            fill="#FFFFFF"
        )

        canvasForTicket.create_text(
            585.0,
            positionY,
            anchor="nw",
            text=ticket["startHour"],
            fill="#FFFFFF"
        )

        canvasForTicket.create_text(
            705.0,
            positionY,
            anchor="nw",
            text=ticket["endDate"],
            fill="#FFFFFF"
        )

        canvasForTicket.create_text(
            810.0,
            positionY,
            anchor="nw",
            text=ticket["endHour"],
            fill="#FFFFFF"
        )

def getTicketByDay(startDay, endDay, endDateEntry, canvasForTickets, nextBtn, previousBtn):
    global ticketPosition
    ticketPosition = 0

    ticketList = []
    ticketTypes = {}

    canvasForTickets.delete('all')

    nextBtn.place_forget()
    previousBtn.place_forget()

    if startDay == "DD/MM/YYYY":
        startDay = ""

    if endDay == "DD/MM/YYYY":
        endDay = ""

    try:
        startDayDate = datetime.strptime(startDay, '%d/%m/%Y').date()

        if endDay != "":
            endDayDate = datetime.strptime(endDay, '%d/%m/%Y').date()
        else:
            now = datetime.now()
            endDayDate = datetime.strptime(str(now.day) + "/" + str(now.month) + "/" + str(now.year), '%d/%m/%Y').date()
            endDateEntry.delete(0, "end")
            endDateEntry.insert(0, str(now.day) + "/" + str(now.month) + "/" + str(now.year))
            endDateEntry.config(fg='black')


        ticketTypesFile = open("../Dados/ticketType.txt", "r")

        for line in ticketTypesFile:
            line = line.strip().split(",")
            ticketTypes[line[0]] = (line[1], line[2])

        ticketTypesFile.close()

        file = open("../Dados/ticket.txt", "r")   

        for var in file.readlines():
            ticket = {}
            var = var.strip("\n").split(",")

            fileStartDay = datetime.strptime(var[4], '%d/%m/%Y').date()
            fileEndDay = datetime.strptime(var[6], '%d/%m/%Y').date()

            if (startDayDate <= fileStartDay) and (endDayDate >= fileEndDay):
                ticket["ref"] = var[0] 
                ticket["name"] = var[1]
                ticket["nationality"] = var[2]
                ticket["ticketType"] = getValueByKey(ticketTypes, var[3])[0]    
                ticket["startDate"] = var[4]
                ticket["startHour"] = var[5]
                ticket["endDate"] = var[6]
                ticket["endHour"] = var[7]
                
                ticketList.append(ticket)

        file.close()

        printTicketsNext(ticketList, canvasForTickets, nextBtn, previousBtn, 7)
        return ticketList
    except:
        ctypes.windll.user32.MessageBoxW(0, "Error in the dates entered!\nCheck the dates and try again.", "Error!", 0)  
     
def onEntryClick(event, placeholder):
    if event.widget.get() == placeholder:
        event.widget.delete(0, "end")
        event.widget.config(fg='black') 

def onEntryFocusOut(event, placeholder):
    if event.widget.get() == "":
        event.widget.insert(0, placeholder)
        event.widget.config(fg='grey')

def getAddTrainConnectionInitialData():
    trainStops = {}

    trainStopsFile = open("../Dados/trainStops.txt", "r")

    for line in trainStopsFile:
        line = line.strip().split(",")
        trainStops[line[0]] = (line[1], line[3], line[4])

    trainStopsFile.close()
 
    return trainStops

def calculateDistanceBetweenTrainStops(startTrainStop, endTrainStop, trainStopsDic, entryDistance):

    if (startTrainStop != "Select an option") and (endTrainStop != "Select an option"):
        startTrainStopCoordinates = ()
        endTrainStopCoordinates = ()

        for value in trainStopsDic.values():
            if value[0] == startTrainStop:
                startTrainStopCoordinates = (float(value[1]), float(value[2]))

            if value[0] == endTrainStop:
                endTrainStopCoordinates = (float(value[1]), float(value[2]))
    
        distance = haversine(startTrainStopCoordinates[0], startTrainStopCoordinates[1], endTrainStopCoordinates[0], endTrainStopCoordinates[1])
        insertEntryDate(entryDistance, str(distance) + " m")
        return distance

def addTrainStopConnection(startTrainStop, endTrainStop, trainStopsDic, entryDistance):
    
    if (startTrainStop != "Select an option") and (endTrainStop != "Select an option"):
        
        startTrainStopCode = ""
        endTrainStopCode = ""

        alreadyExists = False   

        for key in trainStopsDic:
            if trainStopsDic[key][0] == startTrainStop:
                startTrainStopCode = key

            if trainStopsDic[key][0] == endTrainStop:
                endTrainStopCode = key

            if (startTrainStopCode != "") and (endTrainStopCode != ""):
                break

        file = open("../Dados/trainStopsConnections.txt", "r")   

        for var in file.readlines():
            var = var.strip("\n").split(",")
            if var[0] == startTrainStopCode + "-" + endTrainStopCode or var[0] == endTrainStopCode+ "-" + startTrainStopCode:
                alreadyExists = True
                
        file.close()

        if alreadyExists == False:
            code = startTrainStopCode + "-" + endTrainStopCode
            distance = calculateDistanceBetweenTrainStops(startTrainStop, endTrainStop, trainStopsDic, entryDistance)

            try:
                if distance > 0:
                    file = open("../Dados/trainStopsConnections.txt", "a")  
                    file.writelines(code + "," + startTrainStopCode + "," + endTrainStopCode + "," + str(distance) + "\n")
                    file.close()
                    changeMenuOption(printMenu, "frame_menu")
                else:
                    ctypes.windll.user32.MessageBoxW(0, "The stops cannot be the same!\nTry again.", "Error!", 0)

            except: 
                ctypes.windll.user32.MessageBoxW(0, "Something went wrong\nTry again.", "Error!", 0)
        else:
            ctypes.windll.user32.MessageBoxW(0, "The introduced connection already exists!", "Error!", 0)
    else:
        ctypes.windll.user32.MessageBoxW(0, "You have to select two train stops!\nTry again.", "Error!", 0)

def getAddTrainRouteInitialData():
    trainStops = {}

    trainStopsFile = open("../Dados/trainStops.txt", "r")

    for line in trainStopsFile:
        line = line.strip().split(",")
        trainStops[line[0]] = (line[1], line[3], line[4])

    trainStopsFile.close()
 
    return trainStops

def addTrainRoute(name, startTrainStop, endTrainStop, periodicity, trainStopsDic):
    
    if (startTrainStop != "Select an option") and (endTrainStop != "Select an option"):
        if startTrainStop != endTrainStop:
            try:
                periodicity = float(periodicity) 
                connections = {}
                
                startTrainStopCode = ""
                endTrainStopCode = ""  

                for key in trainStopsDic:
                    if trainStopsDic[key][0] == startTrainStop:
                        startTrainStopCode = key

                    if trainStopsDic[key][0] == endTrainStop:
                        endTrainStopCode = key

                    connections[key] = []
                    
                file = open("../Dados/trainStopsConnections.txt", "r")

                for line in file:
                    line = line.strip().split(",")
                    connections[line[1]].append(line[2])
                    connections[line[2]].append(line[1])

                file.close()
                
                isPossible = verifyConnection(connections, startTrainStopCode, endTrainStopCode)

                if isPossible:
                    code = generateCode("trainRoute.txt")

                    file = open("../Dados/trainRoute.txt", "a")  
                    file.writelines(code + "," + name + "," + startTrainStopCode + "," + endTrainStopCode + "," + "Aberto" + "," + str(periodicity) + "\n")
                    file.close()
                    changeMenuOption(printMenu, "frame_menu")
                else:        
                    ctypes.windll.user32.MessageBoxW(0, "Impossible to create train route!\nThere are not enough connections between train stops.", "Error!", 0)
            except:
                ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)
        else:
            ctypes.windll.user32.MessageBoxW(0, "Train stops cannot be the same!", "Error!", 0)
    else:
        ctypes.windll.user32.MessageBoxW(0, "You need to choose the starting train stop and the ending train stop!", "Error!", 0)

def verifyConnection(data, start, end):
    visited = set()
    queue = [start]

    while queue:
        currentPoint = queue.pop(0)

        if currentPoint == end:
            return True

        if currentPoint not in visited:
            visited.add(currentPoint)
            queue.extend(data.get(currentPoint, []))

    return False     

def editStatus(code, fileName, state, changeFileDic):
    if fileName != "Select an option":
        #fileName = getKeyByValue(changeFileDic, fileName)
        positionToEdit = -1
        lines = []


        for key in changeFileDic:
            if changeFileDic[key][0] == fileName:
                fileName = key
                positionToEdit = changeFileDic[key][1]


        if state != "Select an option":
            try:         
                if code != "":
                    isCodeValid = False
                    file = open("../Dados/" + fileName, "r") 

                    for line in file:
                        line = line.strip().split(",")
                        if line[0] == code:
                            line[positionToEdit] = state
                            isCodeValid = True
                        lines.append(line)

                    file.close()

                    if isCodeValid:
                        file = open("../Dados/" + fileName, "w") 

                        for line in lines:
                            if fileName == 'amusements.txt':
                                file.writelines(line[0] + "," + line[1] + "," + line[2] + "," + line[3] + "," + line[4] + "," + line[5] + "," + line[6] + "," + line[7] + "," + line[8] + "," + line[9] + "," + line[10] + "\n")
                            elif fileName == "accommodations.txt":
                                file.writelines(line[0] + "," + line[1] + "," + line[2] + "," + line[3] + "," + line[4] + "," + line[5] + "," + line[6] + "\n")
                            elif fileName == "trainRoute.txt":
                                file.writelines(line[0] + "," + line[1] + "," + line[2] + "," + line[3] + "," + line[4] + "," + line[5] + "\n")
                                        
                        file.close()
                        changeMenuOption(printMenu, "frame_menu")
                    else:
                        ctypes.windll.user32.MessageBoxW(0, "Invalid code.\nTry another code.", "Error!", 0)
                else:
                    ctypes.windll.user32.MessageBoxW(0, "A valid code must be entered!\nTry again.", "Error!", 0)
            except: 
                ctypes.windll.user32.MessageBoxW(0, "The data entered is invalid\nTry again", "Error!", 0)
        else:
            ctypes.windll.user32.MessageBoxW(0, "It is necessary to indicate the status!\nChoose an option and try again.", "Error!", 0)
    else:
        ctypes.windll.user32.MessageBoxW(0, "It is necessary to indicate what to change!\nChoose an option and try again.", "Error!", 0)

''' UI '''

def printLogin():
    canvas = Canvas(
        window,
        bg = "#1F1F43",
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
        699.0,
        350.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printRegister, "frame_register"),
        relief="flat"
    )
    button_1.place(
        x=704.0,
        y=556.0,
        width=157.0,
        height=25.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: login(entry_1.get(), entry_2.get()),
        relief="flat"
    )
    button_2.place(
        x=539.0,
        y=478.0,
        width=322.0,
        height=82.0
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        700.0,
        409.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        700.0,
        277.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        600.0,
        361.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        585.0,
        229.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        229.0,
        350.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        700.0,
        138.0,
        image=image_image_7
    )

    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font="Arial, 16"
    )
    entry_1.place(
        x=553.0,
        y=259.0,
        width=294.0,
        height=36.0
    )

    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        show="*",
        font="Arial, 18"
    )
    entry_2.place(
        x=553.0,
        y=391.0,
        width=294.0,
        height=36.0
    )
    window.resizable(False, False)
    window.mainloop()

def printRegister():
    canvas = Canvas(
        window,
        bg = "#1F1F43",
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
        699.0,
        350.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_1.place(
        x=687.0,
        y=588.0,
        width=172.0,
        height=23.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: register(entry_1.get(), entry_2.get(), entry_3.get()),
        relief="flat"
    )
    button_2.place(
        x=539.0,
        y=509.0,
        width=322.0,
        height=82.0
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        700.0,
        456.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        700.0,
        221.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        641.0,
        408.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        600.0,
        289.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        585.0,
        172.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        229.0,
        350.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        700.0,
        110.0,
        image=image_image_8
    )

    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        font="Arial, 16"
    )
    entry_1.place(
        x=553.0,
        y=203.0,
        width=294.0,
        height=36.0
    )

    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        show="*",
        font="Arial, 18"
    )
    entry_2.place(
        x=553.0,
        y=438.0,
        width=294.0,
        height=36.0
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        700.0,
        341.0,
        image=image_image_9
    )

    entry_3 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        show="*",
        font="Arial, 18"
    )
    entry_3.place(
        x=553.0,
        y=323.0,
        width=294.0,
        height=36.0
    )
    window.resizable(False, False)
    window.mainloop()

def printMenu():
    global userName
    global house

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

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenuVisitorView, "frame_menuvisitorview"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button logout
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        475.0,
        434.0,
        image=image_image_4
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printTicketSearchByRef, "frame_ticketsearchbyref"),
        relief="flat"
    )
    button_3.place(
        x=29.0,
        y=554.0,
        width=299.0,
        height=85.0
    )

    #Button search ticket by day
    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printTicketSearchByDay, "frame_ticketsearchbyday"),
        relief="flat"
    )
    button_4.place(
        x=628.0,
        y=461.0,
        width=299.0,
        height=84.0
    )

    #Button Ticket List
    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printTicketList, "frame_ticketlist"),
        relief="flat"
    )
    button_5.place(
        x=328.0,
        y=461.0,
        width=299.0,
        height=84.0
    )

    #Button Issue Ticket
    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printIssueTicket, "frame_issueticket"),
        relief="flat"
    )
    button_6.place(
        x=26.0,
        y=461.0,
        width=299.0,
        height=84.0
    )

    #Button Add Amusement
    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printAddAmusement, "frame_addamusement"),
        relief="flat"
    )
    button_7.place(
        x=327.0,
        y=269.0,
        width=299.0,
        height=84.0
    )

    #Button AddAccommodation
    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    button_8 = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printAddAccommodation, "frame_addaccommodation"),
        relief="flat"
    )
    button_8.place(
        x=628.0,
        y=269.0,
        width=299.0,
        height=84.0
    )

    #Button AddZone
    button_image_9 = PhotoImage(
        file=relative_to_assets("button_9.png"))
    button_9 = Button(
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printAddZone, "frame_addzone"),
        relief="flat"
    )
    button_9.place(
        x=26.0,
        y=269.0,
        width=299.0,
        height=84.0
    )

    #Button Train Stop
    button_image_10 = PhotoImage(
        file=relative_to_assets("button_10.png"))
    button_10 = Button(
        image=button_image_10,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printTrainStop, "frame_addtrainstop"),
        relief="flat"
    )
    button_10.place(
        x=26.0,
        y=365.0,
        width=299.0,
        height=85.0
    )

    #Add train connection
    button_image_11 = PhotoImage(
        file=relative_to_assets("button_11.png"))
    button_11 = Button(
        image=button_image_11,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printAddTrainConnection, "frame_addtrainconnection"),
        relief="flat"
    )
    button_11.place(
        x=328.0,
        y=365.0,
        width=299.0,
        height=85.0
    )

    #Button add Train Route
    button_image_12 = PhotoImage(
        file=relative_to_assets("button_12.png"))
    button_12 = Button(
        image=button_image_12,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printAddTrainRoute, "frame_addtrainroute"),
        relief="flat"
    )
    button_12.place(
        x=628.0,
        y=365.0,
        width=299.0,
        height=85.0
    )

    #Button Change Status
    button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
    button_13 = Button(
        image=button_image_13,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printChangeStatus, "frame_changestatus"),
        relief="flat"
    )
    button_13.place(
        x=330.0,
        y=554.0,
        width=299.0,
        height=85.0
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        78.0,
        223.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        476.0,
        252.0,
        image=image_image_6
    )
    window.resizable(False, False)
    window.mainloop()

def printMenuVisitorView():
    global userName
    global house

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
        434.0,
        image=image_image_3
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
        command=lambda: changeMenuOption(printAmusementList, "frame_amusementlist"),
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

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        78.0,
        223.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        476.0,
        252.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        474.0,
        126.0,
        image=image_image_6
    )

    canvas.create_text(
        35.0,
        91.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        35.0,
        130.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    changeViewBtn_image = PhotoImage(
        file=relative_to_assets("button_8.png"))
    changeViewBtn = Button(
        image=changeViewBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    changeViewBtn.place(
        x=497.0,
        y=91.0,
        width=217.0,
        height=71.0
    )

    logoutBtn_image = PhotoImage(
        file=relative_to_assets("button_9.png"))
    logoutBtn = Button(
        image=logoutBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    logoutBtn.place(
        x=706.0,
        y=91.0,
        width=217.0,
        height=71.0
    )
    window.resizable(False, False)
    window.mainloop()

def printAddZone():
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

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        77.0,
        276.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        89.0,
        390.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        105.0,
        504.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        413.0,
        390.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_8
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_9
    )

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    #Button Back
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button Logout
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button Insert
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: addZone(entry_4.get(), entry_3.get(), entry_5.get(), entry_1.get("1.0", "end-1c")),
        relief="flat"
    )
    button_3.place(
        x=710.0,
        y=612.0,
        width=217.0,
        height=73.0
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        102.0,
        223.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        476.0,
        252.0,
        image=image_image_11
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        480.0,
        563.0,
        image=image_image_12
    )

    #Entry Description
    entry_1 = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=58.0,
        y=542.0,
        width=845.0,
        height=45.0
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        181.12197875976562,
        441.731689453125,
        image=image_image_14
    )

    #Entry latitude
    entry_3 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_3.place(
        x=48.6341552734375,
        y=425.8536376953125,
        width=265.31707763671875,
        height=32.292694091796875
    )

    
    #Zonename image
    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        181.1219787597656,
        327.731689453125,
        image=image_image_15
    )

    #Entry zoneName
    entry_4 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_4.place(
        x=48.6341552734375,
        y=311.8536682128906,
        width=265.31707763671875,
        height=32.292686462402344
    )

    image_image_16 = PhotoImage(
        file=relative_to_assets("image_16.png"))
    image_16 = canvas.create_image(
        498.1219787597656,
        441.731689453125,
        image=image_image_16
    )

    #Entry longitude
    entry_5 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_5.place(
        x=365.6341552734375,
        y=425.8536376953125,
        width=265.31707763671875,
        height=32.292694091796875
    )
    window.resizable(False, False)
    window.mainloop()

def printAddAmusement():

    amusementTypes, zones = getAddAmusementInitialData()

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
        70.0,
        271.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        300.0,
        271.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        530.0,
        271.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        94.0,
        517.0,
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

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text="Gonçalo Silva",
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text="Slytherin",
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )
       
    #Button Insert
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: addAmusement(entry_6.get(), entry_2.get(), entry_3.get(), entry_4.get(),                                     
                        entry_5.get(), entry_9.get(), entry_12.get(), entry_10.get(), 
                        entry_11.get(), entry_1.get("1.0", "end-1c"), amusementTypes, zones),
        relief="flat"
    )
    button_3.place(
        x=710.0,
        y=612.0,
        width=217.0,
        height=73.0
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        151.0,
        222.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        480.0,
        573.0,
        image=image_image_11
    )

    entry_1 = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=58.0,
        y=552.0,
        width=845.0,
        height=45.0
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        367.0,
        309.0,
        image=image_image_12
    )

    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=269.0,
        y=298.0,
        width=198.0,
        height=21.0
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        589.0,
        309.0,
        image=image_image_13
    )

    entry_3 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_3.place(
        x=492.0,
        y=298.0,
        width=196.0,
        height=21.0
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        147.0,
        309.0,
        image=image_image_14
    )

    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        284.0,
        353.0,
        image=image_image_15
    )

    image_image_16 = PhotoImage(
        file=relative_to_assets("image_16.png"))
    image_16 = canvas.create_image(
        555.0,
        353.0,
        image=image_image_16
    )

    image_image_17 = PhotoImage(
        file=relative_to_assets("image_17.png"))
    image_17 = canvas.create_image(
        768.0,
        271.0,
        image=image_image_17
    )

    image_image_18 = PhotoImage(
        file=relative_to_assets("image_18.png"))
    image_18 = canvas.create_image(
        117.0,
        351.0,
        image=image_image_18
    )

    image_image_19 = PhotoImage(
        file=relative_to_assets("image_19.png"))
    image_19 = canvas.create_image(
        747.0,
        353.0,
        image=image_image_19
    )

    image_image_20 = PhotoImage(
        file=relative_to_assets("image_20.png"))
    image_20 = canvas.create_image(
        811.0,
        309.0,
        image=image_image_20
    )

    entry_4 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_4.place(
        x=713.0,
        y=298.0,
        width=198.0,
        height=21.0
    )

    image_image_21 = PhotoImage(
        file=relative_to_assets("image_21.png"))
    image_21 = canvas.create_image(
        146.0,
        390.0,
        image=image_image_21
    )

    entry_5 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_5.place(
        x=49.0,
        y=379.0,
        width=196.0,
        height=21.0
    )

    image_image_22 = PhotoImage(
        file=relative_to_assets("image_22.png"))
    image_22 = canvas.create_image(
        103.0,
        433.0,
        image=image_image_22
    )

    entry_6 = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_6.place(
        x=48.0,
        y=298.0,
        width=198.0,
        height=21.0
    )

    entry_10 = ttk.Combobox(window, values=list(intensity.values()), state="readonly")
    entry_10.place(
        x=713.0,
        y=372.0,
        width=198.0,
        height=32.0
    )

    entry_10.set("Select an option")

    #Current Status
    entry_11 = ttk.Combobox(window, values=list(currentState.values()), state="readonly")
    entry_11.place(
        x=47.0,
        y=450.0,
        width=198.0,
        height=32.0
    )

    entry_11.set("Select an option")

    #Amusement Type
    entry_9 = ttk.Combobox(window, values=list(amusementTypes.values()), state="readonly")
    entry_9.place(
        x=269.0,
        y=372.0,
        width=198.0,
        height=32.0
    )

    entry_9.set("Select an option")

    #Zonas
    entry_12 = ttk.Combobox(window, values=list(zones.values()), state="readonly")
    entry_12.place(
        x=491.0,
        y=372.0,
        width=198.0,
        height=32.0
    )

    entry_12.set("Select an option")

    window.resizable(False, False)
    window.mainloop()

def printAddAccommodation():

    zones = addAccommodationInitialData()

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
        75.0,
        276.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        381.0,
        276.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        684.0,
        276.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        94.0,
        517.0,
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

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    #Button Back
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button Logout
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: addAccommodation(name.get(), latitude.get(), longitude.get(), zonesComboBox.get(), currentStatusComboBox.get(), description.get("1.0", "end-1c"), zones),
        relief="flat"
    )
    button_3.place(
        x=710.0,
        y=612.0,
        width=217.0,
        height=73.0
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        179.0,
        222.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_10
    )

    canvas.create_rectangle(
        36.0,
        530.0,
        927.0,
        614.0,
        fill="#354C80",
        outline="")

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        480.0,
        573.0,
        image=image_image_11
    )

    description = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    description.place(
        x=58.0,
        y=552.0,
        width=845.0,
        height=45.0
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        475.0,
        325.0,
        image=image_image_12
    )

    latitude = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    latitude.place(
        x=345.0,
        y=311.0,
        width=262.0,
        height=28.0
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        769.0,
        325.0,
        image=image_image_13
    )

    longitude = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    longitude.place(
        x=641.0,
        y=311.0,
        width=259.0,
        height=28.0
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        183.0,
        325.0,
        image=image_image_14
    )

    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        129.0,
        394.0,
        image=image_image_15
    )

    image_image_16 = PhotoImage(
        file=relative_to_assets("image_16.png"))
    image_16 = canvas.create_image(
        409.0,
        394.0,
        image=image_image_16
    )

    name = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    name.place(
        x=52.0,
        y=311.0,
        width=263.0,
        height=28.0
    )

    #Current Status
    currentStatusComboBox = ttk.Combobox(window, values=list(currentState.values()), state="readonly")
    currentStatusComboBox.place(
        x=337.0,
        y=417.0,
        width=270.0,
        height=40.0
    )
    currentStatusComboBox.set("Select an option")

    #Zonas
    zonesComboBox = ttk.Combobox(window, values=list(zones.values()), state="readonly")
    zonesComboBox.place(
        x=47.0,
        y=417.0,
        width=270.0,
        height=40.0
    )
    zonesComboBox.set("Select an option")

    window.resizable(False, False)
    window.mainloop()

def printTrainStop():

    zones = addTrainStopInitialData()

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
        75.0,
        276.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        381.0,
        276.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        684.0,
        276.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        94.0,
        517.0,
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

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    #Button Back
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button Logout
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: addTrainStop(name.get(), latitude.get(), longitude.get(), zonesComboBox.get(), description.get("1.0", "end-1c"), zones),
        relief="flat"
    )
    button_3.place(
        x=710.0,
        y=612.0,
        width=217.0,
        height=73.0
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        138.0,
        222.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        480.0,
        573.0,
        image=image_image_11
    )

    description = Text(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    description.place(
        x=58.0,
        y=552.0,
        width=845.0,
        height=45.0
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        475.0,
        325.0,
        image=image_image_12
    )

    latitude = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    latitude.place(
        x=345.0,
        y=311.0,
        width=262.0,
        height=28.0
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        769.0,
        325.0,
        image=image_image_13
    )

    longitude = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    longitude.place(
        x=641.0,
        y=311.0,
        width=259.0,
        height=28.0
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        183.0,
        325.0,
        image=image_image_14
    )

    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        129.0,
        394.0,
        image=image_image_15
    )

    name = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    name.place(
        x=52.0,
        y=311.0,
        width=263.0,
        height=28.0
    )

    #Zonas
    zonesComboBox = ttk.Combobox(window, values=list(zones.values()), state="readonly")
    zonesComboBox.place(
        x=47.0,
        y=417.0,
        width=270.0,
        height=40.0
    )
    zonesComboBox.set("Select an option")

    window.resizable(False, False)
    window.mainloop()

def printIssueTicket():

    ticketTypes, nationalities = getIssueTicketInitialData()

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
        106.0,
        275.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        392.0,
        274.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        687.0,
        274.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_7
    )

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button Logout
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: addTicket(personName.get(), nationalitiesComboBox.get(), ticketTypesComboBox.get(), startDate.get(), startHour.get(), endDate.get(), endHour.get(), ticketTypes),
        relief="flat"
    )
    button_3.place(
        x=710.0,
        y=612.0,
        width=217.0,
        height=73.0
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        117.0,
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
        184.0,
        321.0,
        image=image_image_10
    )

    personName = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    personName.place(
        x=52.0,
        y=308.0,
        width=265.0,
        height=26.0
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        86.0,
        401.0,
        image=image_image_11
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        391.0,
        401.0,
        image=image_image_12
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        474.0,
        449.0,
        image=image_image_13
    )

    startHour = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        state='disabled',
        disabledbackground="white"
    )
    startHour.place(
        x=343.0,
        y=435.0,
        width=265.0,
        height=28.0
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        180.0,
        449.0,
        image=image_image_14
    )

    startDate = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        state='disabled',
        disabledbackground="white"
    )
    startDate.place(
        x=48.0,
        y=435.0,
        width=265.0,
        height=28.0
    )

    image_image_15 = PhotoImage(
        file=relative_to_assets("image_15.png"))
    image_15 = canvas.create_image(
        88.0,
        509.0,
        image=image_image_15
    )

    image_image_16 = PhotoImage(
        file=relative_to_assets("image_16.png"))
    image_16 = canvas.create_image(
        391.0,
        509.0,
        image=image_image_16
    )

    image_image_17 = PhotoImage(
        file=relative_to_assets("image_17.png"))
    image_17 = canvas.create_image(
        478.0,
        557.0,
        image=image_image_17
    )

    endHour = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        state='disabled',
        disabledbackground="white"
    )
    endHour.place(
        x=347.0,
        y=543.0,
        width=265.0,
        height=28.0
    )

    image_image_18 = PhotoImage(
        file=relative_to_assets("image_18.png"))
    image_18 = canvas.create_image(
        184.0,
        557.0,
        image=image_image_18
    )

    endDate = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        state='disabled',
        disabledbackground="white"
    )
    endDate.place(
        x=52.0,
        y=543.0,
        width=265.0,
        height=28.0
    )

    #Ticket Types
    #ticketTypesComboBox = ttk.Combobox(window, values=list(ticketTypes.values()), state="readonly")
    ticketTypesComboBox = ttk.Combobox(window, values=[var[0] for var in list(ticketTypes.values())], state="readonly")
    ticketTypesComboBox.place(
        x=635.0,
        y=298.0,
        width=270.0,
        height=43.0
    )
    ticketTypesComboBox.set("Select an option")
    ticketTypesComboBox.bind("<<ComboboxSelected>>", lambda event: setTicketDate(event, ticketTypes, startDate, startHour, endDate, endHour))

    #Nationalities
    nationalitiesComboBox = ttk.Combobox(window, values=list(nationalities.values()), state="readonly")
    nationalitiesComboBox.place(
        x=337.0,
        y=298.0,
        width=270.0,
        height=43.0
    )
    nationalitiesComboBox.set("Select a nationality")

    window.resizable(False, False)
    window.mainloop()

def printTicketList():

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

    #Ref
    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        52.0,
        275.0,
        image=image_image_2
    )

    #Name
    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        141.0,
        274.0,
        image=image_image_3
    )

    #Nationality
    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        262.0,
        274.0,
        image=image_image_4
    )

    #Ticket Type
    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        433.0,
        274.0,
        image=image_image_5
    )

    #Start Date
    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        545.0,
        274.0,
        image=image_image_6
    )

    #End date
    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        770.0,
        274.0,
        image=image_image_7
    )

    #StartHour
    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        657.0,
        274.0,
        image=image_image_8
    )

    #End hour
    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        876.0,
        274.0,
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

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    #Button Back
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button Logout
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )
    
    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        104.0,
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

    canvasForTickets = Canvas(
        window,
        bg = "#354C80",
        height = 310,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        
    )
    canvasForTickets.place(x=30, y=300)

    previousBtn = ""
    nextBtn = ""

    tickets = getTicketListing()

    previousBtn_image = PhotoImage(
        file=relative_to_assets("button_4.png"))
    previousBtn = Button(
        image=previousBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printTicketsPrevious(tickets, canvasForTickets, nextBtn, previousBtn, 10),
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
        command=lambda: printTicketsNext(tickets, canvasForTickets, nextBtn, previousBtn, 10),
        relief="flat"
        )
    nextBtn.place(
        x=716.0,
        y=612.0,
        width=207.0,
        height=74.0
        )
    
    printTicketsNext(tickets, canvasForTickets, nextBtn, previousBtn, 10)

    window.resizable(False, False)
    window.mainloop()

def printTicketSearchByRef():
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

    #Ref
    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        52.0,
        388.0,
        image=image_image_2
    )

    #Name
    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        141.0,
        388.0,
        image=image_image_3
    )

    #Nationality
    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        262.0,
        388.0,
        image=image_image_4
    )

    #Ticket Type
    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        433.0,
        388.0,
        image=image_image_5
    )

    #Start Date
    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        545.0,
        388.0,
        image=image_image_6
    )

    #End date
    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        770.0,
        388.0,
        image=image_image_7
    )

    #StartHour
    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        657.0,
        388.0,
        image=image_image_8
    )

    #End hour
    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        876.0,
        388.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        119.0,
        275.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_11
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_12
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_13
    )

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    #Button Back
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button Logout
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        126.0,
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

    image_image_16 = PhotoImage(
        file=relative_to_assets("image_16.png"))
    image_16 = canvas.create_image(
        184.0,
        321.0,
        image=image_image_16
    )

    ref = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    ref.place(
        x=52.0,
        y=308.0,
        width=265.0,
        height=26.0
    )

    canvasForTicket = Canvas(
        window,
        bg = "#354C80",
        #bg = "red",
        height = 110,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"     
    )
    canvasForTicket.place(x=30, y=410)

    #Button Search
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: getTicketByRef(ref.get(), canvasForTicket),
        relief="flat"
    )
    button_3.place(
        x=331.0,
        y=290.0,
        width=122.0,
        height=60.0
    )

    window.resizable(False, False)
    window.mainloop()

def printTicketSearchByDay():
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

   #Ref
    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        52.0,
        388.0,
        image=image_image_2
    )

    #Name
    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        141.0,
        388.0,
        image=image_image_3
    )

    #Nationality
    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        262.0,
        388.0,
        image=image_image_4
    )

    #Ticket Type
    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        433.0,
        388.0,
        image=image_image_5
    )

    #Start Date
    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        545.0,
        388.0,
        image=image_image_6
    )

    #End date
    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        770.0,
        388.0,
        image=image_image_7
    )

    #StartHour
    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        657.0,
        388.0,
        image=image_image_8
    )

    #End hour
    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        876.0,
        388.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        88.0,
        275.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_11
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_12
    )

    image_image_13 = PhotoImage(
        file=relative_to_assets("image_13.png"))
    image_13 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_13
    )

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    #Button Back
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button Logout
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    image_image_14 = PhotoImage(
        file=relative_to_assets("image_14.png"))
    image_14 = canvas.create_image(
        126.0,
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

    image_image_16 = PhotoImage(
        file=relative_to_assets("image_16.png"))
    image_16 = canvas.create_image(
        184.0,
        321.0,
        image=image_image_16
    )

    image_image_17 = PhotoImage(
        file=relative_to_assets("image_17.png"))
    image_17 = canvas.create_image(
        385.0,
        275.0,
        image=image_image_17
    )

    image_image_18 = PhotoImage(
        file=relative_to_assets("image_18.png"))
    image_18 = canvas.create_image(
        485.0,
        321.0,
        image=image_image_18
    )

    startDay = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="grey",
        highlightthickness=0
    )
    startDay.place(
        x=52.0,
        y=308.0,
        width=265.0,
        height=26.0
    )

    startDay.insert(0, "DD/MM/YYYY")
    startDay.bind('<FocusIn>', lambda event: onEntryClick(event, "DD/MM/YYYY"))
    startDay.bind('<FocusOut>', lambda event: onEntryFocusOut(event, "DD/MM/YYYY"))

    endDay = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="grey",
        highlightthickness=0
    )
    endDay.place(
        x=353.0,
        y=308.0,
        width=265.0,
        height=26.0
    )

    endDay.insert(0, "DD/MM/YYYY")
    endDay.bind('<FocusIn>', lambda event: onEntryClick(event, "DD/MM/YYYY"))
    endDay.bind('<FocusOut>', lambda event: onEntryFocusOut(event, "DD/MM/YYYY"))

    canvasForTickets = Canvas(
        window,
        bg = "#354C80",
        #bg = "red",
        height = 200,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"     
    )
    canvasForTickets.place(x=30, y=410)

    previousBtn = ""
    nextBtn = ""
    tickets = []

    previousBtn_image = PhotoImage(
        file=relative_to_assets("button_4.png"))
    previousBtn = Button(
        image=previousBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printTicketsPrevious(tickets, canvasForTickets, nextBtn, previousBtn, 7),
        relief="flat"
        )
    previousBtn.place(
        x=500.0,
        y=612.0,
        width=207.0,
        height=74.0
        )

    previousBtn.place_forget()

    nextBtn_image = PhotoImage(
        file=relative_to_assets("button_5.png"))
    nextBtn = Button(
        image=nextBtn_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: printTicketsNext(tickets, canvasForTickets, nextBtn, previousBtn, 7),
        relief="flat"
        )
    nextBtn.place(
        x=716.0,
        y=612.0,
        width=207.0,
        height=74.0
        )

    nextBtn.place_forget()

    #Button Search
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: (tickets.clear() ,tickets.extend(getTicketByDay(startDay.get(), endDay.get(), endDay, canvasForTickets, nextBtn, previousBtn))),
        relief="flat"
    )
    button_3.place(
        x=640.0,
        y=290.0,
        width=122.0,
        height=60.0
    )

    window.resizable(False, False)
    window.mainloop()

def printAddTrainConnection():

    trainStops = getAddTrainConnectionInitialData()

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
        357.0,
        276.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        678.0,
        276.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_6
    )

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    #Button Back
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button Logout
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        149.0,
        222.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_8
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        769.0,
        325.0,
        image=image_image_9
    )

    distance = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        state='disabled',
        disabledbackground="white"
    )
    distance.place(
        x=641.0,
        y=311.0,
        width=259.0,
        height=28.0
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        69.0,
        276.0,
        image=image_image_10
    )

    #Train Stop Start
    startTrainStopComboBox = ttk.Combobox(window, values=[var[0] for var in list(trainStops.values())], state="readonly")
    startTrainStopComboBox.place(
        x=45.0,
        y=300.0,
        width=270.0,
        height=45.0
    )
    startTrainStopComboBox.set("Select an option")

    #Train Stop End
    endTrainStopComboBox = ttk.Combobox(window, values=[var[0] for var in list(trainStops.values())], state="readonly")
    endTrainStopComboBox.place(
        x=340.0,
        y=300.0,
        width=270.0,
        height=45.0
    )
    endTrainStopComboBox.set("Select an option")

    startTrainStopComboBox.bind('<FocusIn>', lambda event: (calculateDistanceBetweenTrainStops(startTrainStopComboBox.get(), endTrainStopComboBox.get(), trainStops, distance)))
    endTrainStopComboBox.bind('<FocusIn>', lambda event: (calculateDistanceBetweenTrainStops(startTrainStopComboBox.get(), endTrainStopComboBox.get(), trainStops, distance)))

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: addTrainStopConnection(startTrainStopComboBox.get(), endTrainStopComboBox.get(), trainStops, distance),
        relief="flat"
    )
    button_3.place(
        x=710.0,
        y=612.0,
        width=217.0,
        height=73.0
    )

    window.resizable(False, False)
    window.mainloop()

def printAddTrainRoute():

    trainStops = getAddTrainConnectionInitialData()

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
        75.0,
        276.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        687.0,
        395.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_6
    )

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    #Button Back
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button Logout
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: addTrainRoute(name.get(), startTrainStopComboBox.get(), endTrainStopComboBox.get(), periodicity.get(), trainStops),
        relief="flat"
    )
    button_3.place(
        x=710.0,
        y=612.0,
        width=217.0,
        height=73.0
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        117.0,
        222.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_8
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        769.0,
        444.0,
        image=image_image_9
    )

    periodicity = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    periodicity.place(
        x=641.0,
        y=430.0,
        width=259.0,
        height=28.0
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        183.0,
        325.0,
        image=image_image_10
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        70.0,
        394.0,
        image=image_image_11
    )

    image_image_12 = PhotoImage(
        file=relative_to_assets("image_12.png"))
    image_12 = canvas.create_image(
        357.0,
        394.0,
        image=image_image_12
    )

    name = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    name.place(
        x=52.0,
        y=311.0,
        width=263.0,
        height=28.0
    )

    #Train Stop Start
    startTrainStopComboBox = ttk.Combobox(window, values=[var[0] for var in list(trainStops.values())], state="readonly")
    startTrainStopComboBox.place(
        x=45.0,
        y=420.0,
        width=270.0,
        height=45.0
    )
    startTrainStopComboBox.set("Select an option")

    #Train Stop End
    endTrainStopComboBox = ttk.Combobox(window, values=[var[0] for var in list(trainStops.values())], state="readonly")
    endTrainStopComboBox.place(
        x=340.0,
        y=420.0,
        width=270.0,
        height=45.0
    )
    endTrainStopComboBox.set("Select an option")

    window.resizable(False, False)
    window.mainloop()

def printChangeStatus():
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
        68.0,
        382.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        385.0,
        382.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        475.0,
        32.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        119.0,
        32.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        475.0,
        125.0,
        image=image_image_6
    )

    canvas.create_text(
        36.0,
        90.0,
        anchor="nw",
        text=userName,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 24 * -1)
    )

    canvas.create_text(
        36.0,
        129.0,
        anchor="nw",
        text=house,
        fill="#FFFFFF",
        font=("BerkshireSwash Regular", 20 * -1)
    )

    #Button Back
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printMenu, "frame_menu"),
        relief="flat"
    )
    button_1.place(
        x=498.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    #Button Logout
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: changeMenuOption(printLogin, "frame_login"),
        relief="flat"
    )
    button_2.place(
        x=707.0,
        y=90.0,
        width=217.0,
        height=71.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: editStatus(inputCode.get(), changeFilesComboBox.get(), currentStateComboBox.get(), changeFiles),
        relief="flat"
    )
    button_3.place(
        x=710.0,
        y=612.0,
        width=217.0,
        height=73.0
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        129.0,
        222.0,
        image=image_image_7
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        475.0,
        247.0,
        image=image_image_8
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        181.0,
        431.0,
        image=image_image_9
    )

    inputCode = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    inputCode.place(
        x=53.0,
        y=417.0,
        width=259.0,
        height=28.0
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        129.0,
        276.0,
        image=image_image_10
    )

    #Current Status
    currentStateComboBox = ttk.Combobox(window, values=list(currentState.values()), state="readonly")
    currentStateComboBox.place(
        x=350.0,
        y=405.0,
        width=270.0,
        height=45.0
    )
    currentStateComboBox.set("Select an option")

    changeFiles = {"amusements.txt" : ("Diversão", 9),
                   "accommodations.txt" : ("Comodidades", 5),
                   "trainRoute.txt" : ("Trajeto de Comboio", 4)}
    
    changeFilesComboBox = ttk.Combobox(window, values=[var[0] for var in changeFiles.values()], state="readonly")
    changeFilesComboBox.place(
        x=45.0,
        y=295.0,
        width=270.0,
        height=45.0
    )
    changeFilesComboBox.set("Select an option")

    window.resizable(False, False)
    window.mainloop()

''' UI CHANGE VIEW '''

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
        command=lambda: changeMenuOption(printMenuVisitorView, "frame_menuvisitorview"),
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
        command=lambda: searchAndPrintAmusementInfo(entryNameToSearch.get(), entryName, entryLatitude, entryLongitude, entryMinAge, entryMinHeight, entryAmusementType, entryZone, entryIntensity, entryCurrentState, entryDescription),
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
        63.0,
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

    #Entry Name To Seach
    entryNameToSearch = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entryNameToSearch.place(
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
        command=lambda: changeMenuOption(printMenuVisitorView, "frame_menuvisitorview"),
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
        command=lambda: changeMenuOption(printMenuVisitorView, "frame_menuvisitorview"),
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
        command=lambda: changeMenuOption(printMenuVisitorView, "frame_menuvisitorview"),
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
        command=lambda: changeMenuOption(printMenuVisitorView, "frame_menuvisitorview"),
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
        command=lambda: changeMenuOption(printMenuVisitorView, "frame_menuvisitorview"),
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
        command=lambda: changeMenuOption(printMenuVisitorView, "frame_menuvisitorview"),
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

userName = ""
house = ""

ticketPosition = 0
actualPosition = -1

currentState = {0:"Aberto", 1:"Fechado"}
intensity = {0:"Baixo", 1:"Médio", 2:"Alto", 3:"Extremo"}

printLogin()



