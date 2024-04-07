from pathlib import Path
import ctypes
import qrcode
from PIL import Image, ImageTk

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk
import tkinter as tk

elementPosition = 0
actualPosition = -1

currentStateDic = {0:"Aberto", 1:"Fechado"}
intensityDic = {0:"Baixo", 1:"Médio", 2:"Alto", 3:"Extremo"}

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

def printElementNext(elements, canvasForElements, nextBtn, previousBtn, numberOfElementsToShow, element):
    global elementPosition
    global actualPosition
    positionY = 1
    objective = 0

    if actualPosition == 0 and (((elementPosition + numberOfElementsToShow) - len(elements)) < numberOfElementsToShow):
        elementPosition = elementPosition + numberOfElementsToShow

    canvasForElements.delete('all')

    if elementPosition <= numberOfElementsToShow:
        previousBtn.place_forget()

    if elementPosition + numberOfElementsToShow <= len(elements):
        objective = elementPosition + numberOfElementsToShow
    else:
        objective = len(elements)

    if element == 1:
        printCanvasNextAmusement(elements, canvasForElements, objective, positionY)
    elif element == 2:
        printCanvasNextAccommodation(elements, canvasForElements, objective, positionY)
    elif element == 3:
        printCanvasNextTrainRoute(elements, canvasForElements, objective, positionY)
    elif element == 4:
        printCanvasNextZoneInfo(elements, canvasForElements, objective, positionY)
    elif element == 5:
        printCanvasNextZoneList(elements, canvasForElements, objective, positionY)
    
    actualPosition = 1

    if elementPosition <= numberOfElementsToShow:
        previousBtn.place_forget() 
    else:
        previousBtn.place(
            x=500.0,
            y=612.0,
            width=207.0,
            height=74.0
            ) 
            
    if len(elements) - elementPosition != 0:
        nextBtn.place(
            x=716.0,
            y=612.0,
            width=207.0,
            height=74.0
            ) 
    else:
        nextBtn.place_forget() 

def printElementPrevious(elements, canvasForElements, nextBtn, previousBtn, numberOfElementsToShow, element):
    global elementPosition
    global actualPosition
    positionY = 1
    objective = 0

    canvasForElements.delete('all')

    if actualPosition == 1 and (len(elements) != elementPosition):
        elementPosition = elementPosition - numberOfElementsToShow

    if (elementPosition - numberOfElementsToShow) + 1 <= numberOfElementsToShow:
        previousBtn.place_forget()

    if len(elements) == elementPosition:
        if elementPosition % numberOfElementsToShow != 0:
            objective = (len(elements) - (elementPosition % numberOfElementsToShow)) - numberOfElementsToShow
            elementPosition = elementPosition - (elementPosition % numberOfElementsToShow)
        else:
            objective = len(elements) - (numberOfElementsToShow * 2)
            elementPosition = elementPosition - numberOfElementsToShow
    elif elementPosition == numberOfElementsToShow:
        objective = 0
    else:
        #objective = elementPosition - (numberOfElementsToShow * 2)
        #elementPosition = elementPosition - numberOfElementsToShow
        objective = elementPosition - numberOfElementsToShow

    actualPosition = 0

    if element == 1:
        printCanvasPreviousAmusement(elements, canvasForElements, objective, positionY, numberOfElementsToShow, previousBtn)
    elif element == 2:
        printCanvasPreviousAccommodation(elements, canvasForElements, objective, positionY, numberOfElementsToShow, previousBtn)
    elif element == 3:
        printCanvasPreviousTrainRoute(elements, canvasForElements, objective, positionY, numberOfElementsToShow, previousBtn)
    elif element == 4:
        printCanvasPreviousZoneInfo(elements, canvasForElements, objective, positionY, numberOfElementsToShow, previousBtn)
    elif element == 5:
        printCanvasPreviousZoneList(elements, canvasForElements, objective, positionY, numberOfElementsToShow, previousBtn)

    if len(elements) - elementPosition != 0:
        nextBtn.place(
            x=716.0,
            y=612.0,
            width=207.0,
            height=74.0
            ) 
    else:
        nextBtn.place_forget() 

def getAmusementListInitialData():
    global elementPosition
    elementPosition = 0

    amusementList = []

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

    file = open("../Dados/amusements.txt", "r")   

    for var in file.readlines():
        amusement = {}
        var = var.strip("\n").split(",")

        amusement["code"] = var[0] 
        amusement["name"] = var[1]
        amusement["zone"] =  getValueByKey(zones, var[2])
        amusement["amusementType"] = getValueByKey(amusementTypes, var[3])   
        #amusement["latitude"] = var[4]
        #amusement["longitude"] = var[5]
        amusement["minAge"] = var[6]
        amusement["minHeight"] = var[7]
        amusement["intensity"] = getValueByKey(intensityDic, int(var[8]))
        amusement["currentState"] = var[9]
        
        amusementList.append(amusement)

    file.close()

    return amusementTypes, zones, amusementList

def printCanvasNextAmusement(elements, canvasForElements, objective, positionY):
    global elementPosition

    for var in range(elementPosition, objective):
        try:
            canvasForElements.create_text(
            7,
            positionY,
            anchor="nw",
            text=elements[var]["code"],
            fill="#FFFFFF"
            )
     
            canvasForElements.create_text(
                78,
                positionY,
                anchor="nw",
                text=elements[var]["name"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                213,
                positionY,
                anchor="nw",
                text=elements[var]["zone"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                335,
                positionY,
                anchor="nw",
                text=elements[var]["amusementType"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                455.0,
                positionY,
                anchor="nw",
                text=elements[var]["minAge"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                545.0,
                positionY,
                anchor="nw",
                text=(elements[var]["minHeight"] + "cm"),
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                670.0,
                positionY,
                anchor="nw",
                text=elements[var]["intensity"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                768.0,
                positionY,
                anchor="nw",
                text=elements[var]["currentState"],
                fill="#FFFFFF"
            )
           
            positionY = positionY + 30
            elementPosition = elementPosition + 1
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

def printCanvasPreviousAmusement(elements, canvasForElements, objective, positionY, numberOfElementsToShow, previousBtn):
    global elementPosition
    global actualPosition

    for var in range(elementPosition - 1, objective - 1, -1):
        try:
            canvasForElements.create_text(
            7,
            positionY,
            anchor="nw",
            text=elements[var]["code"],
            fill="#FFFFFF"
            )
     
            canvasForElements.create_text(
                78,
                positionY,
                anchor="nw",
                text=elements[var]["name"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                213,
                positionY,
                anchor="nw",
                text=elements[var]["zone"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                335,
                positionY,
                anchor="nw",
                text=elements[var]["amusementType"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                455.0,
                positionY,
                anchor="nw",
                text=elements[var]["minAge"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                545.0,
                positionY,
                anchor="nw",
                text=(elements[var]["minHeight"] + "cm"),
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                670.0,
                positionY,
                anchor="nw",
                text=elements[var]["intensity"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                768.0,
                positionY,
                anchor="nw",
                text=elements[var]["currentState"],
                fill="#FFFFFF"
            )

            positionY = positionY + 30
            elementPosition = elementPosition - 1
            if elementPosition == 0:
                elementPosition = numberOfElementsToShow
                actualPosition = 1
                previousBtn.place_forget()
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

def searchAmusementList(zone, amusementType, intensity, status, zoneDic, amusementTypeDic):
    global elementPosition
    elementPosition = 0

    amusementList = []

    file = open("../Dados/amusements.txt", "r")   

    for var in file.readlines():
        amusement = {}
        var = var.strip("\n").split(",")

        if (zone == "Select an option" or zone == getValueByKey(zoneDic, var[2])) and \
           (amusementType == "Select an option" or amusementType == getValueByKey(amusementTypeDic, var[3])) and \
           (intensity == "Select an option" or intensity == getValueByKey(intensityDic, int(var[8]))) and \
           (status == "Select an option" or status == var[9]):
            amusement["code"] = var[0] 
            amusement["name"] = var[1]
            amusement["zone"] =  getValueByKey(zoneDic, var[2])
            amusement["amusementType"] = getValueByKey(amusementTypeDic, var[3])   
            #amusement["latitude"] = var[4]
            #amusement["longitude"] = var[5]
            amusement["minAge"] = var[6]
            amusement["minHeight"] = var[7]
            amusement["intensity"] = getValueByKey(intensityDic, int(var[8]))
            amusement["currentState"] = var[9]
            
            amusementList.append(amusement)

    file.close()

    return amusementList

def resetFields(currentStateComboBox, amusementTypeComboBox, zonesComboBox, intensityComboBox):
    currentStateComboBox.set("Select an option")
    amusementTypeComboBox.set("Select an option")
    zonesComboBox.set("Select an option")
    intensityComboBox.set("Select an option")

def insertEntryInfo(entry, data):
    entry.configure(state="normal")
    entry.delete(0, "end")
    entry.insert(0, data)
    entry.configure(state="disabled")

def searchAndPrintAmusementInfo(entryCodeToSearch, entryName, entryLatitude, entryLongitude, entryMinAge, entryMinHeight, entryAmusementType, entryZone, entryIntensity, entryCurrentState, entryDescription):
    global intensityDic

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

    file = open("../Dados/amusements.txt", "r")   

    for var in file.readlines():
        var = var.strip("\n").split(",")

        if (var[0] == entryCodeToSearch):
            insertEntryInfo(entryName, var[1])
            insertEntryInfo(entryZone, getValueByKey(zones ,var[2]))
            insertEntryInfo(entryAmusementType, getValueByKey(amusementTypes, var[3]))
            insertEntryInfo(entryLatitude, var[4])
            insertEntryInfo(entryLongitude, var[5])
            insertEntryInfo(entryMinAge, var[6])
            insertEntryInfo(entryMinHeight, var[7] + "cm")
            insertEntryInfo(entryIntensity, getValueByKey(intensityDic, int(var[8])))
            insertEntryInfo(entryCurrentState, var[9])

            entryDescription.configure(state="normal")
            entryDescription.delete(1.0, "end")
            entryDescription.insert("end", var[10]) 
            entryDescription.configure(state="disabled")
            break
            
    file.close()

def getAccommodationListInitialData():
    global elementPosition
    elementPosition = 0

    accommodationList = []
    zones = {}

    zonesFile = open("../Dados/zones.txt", "r")

    for line in zonesFile:
        line = line.strip().split(",")
        zones[line[0]] = line[1]
        
    zonesFile.close()

    file = open("../Dados/accommodations.txt", "r")   

    for var in file.readlines():
        accommodation = {}
        var = var.strip("\n").split(",")

        accommodation["code"] = var[0] 
        accommodation["name"] = var[1]
        accommodation["zone"] =  getValueByKey(zones, var[2])  
        accommodation["latitude"] = var[3]
        accommodation["longitude"] = var[4]
        accommodation["currentState"] = var[5]
        
        accommodationList.append(accommodation)

    file.close()

    return zones, accommodationList

def searchAccommodationList(zone, status, zoneDic):
    global elementPosition
    elementPosition = 0

    accommodationList = []

    file = open("../Dados/accommodations.txt", "r")   

    for var in file.readlines():
        accommodation = {}
        var = var.strip("\n").split(",")

        if (zone == "Select an option" or zone == getValueByKey(zoneDic, var[2])) and \
           (status == "Select an option" or status == var[5]):
            accommodation["code"] = var[0] 
            accommodation["name"] = var[1]
            accommodation["zone"] =  getValueByKey(zoneDic, var[2])
            accommodation["latitude"] = var[3]
            accommodation["longitude"] = var[4]
            accommodation["currentState"] = var[5]
            
            accommodationList.append(accommodation)

    file.close()

    return accommodationList

def printCanvasNextAccommodation(elements, canvasForElements, objective, positionY):
    global elementPosition

    for var in range(elementPosition, objective):
        try:
            canvasForElements.create_text(
            7,
            positionY,
            anchor="nw",
            text=elements[var]["code"],
            fill="#FFFFFF"
            )
     
            canvasForElements.create_text(
                93,
                positionY,
                anchor="nw",
                text=elements[var]["name"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                257,
                positionY,
                anchor="nw",
                text=elements[var]["zone"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                407,
                positionY,
                anchor="nw",
                text=elements[var]["latitude"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                580.0,
                positionY,
                anchor="nw",
                text=elements[var]["longitude"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                779.0,
                positionY,
                anchor="nw",
                text=elements[var]["currentState"],
                fill="#FFFFFF"
            )
           
            positionY = positionY + 30
            elementPosition = elementPosition + 1
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

def printCanvasPreviousAccommodation(elements, canvasForElements, objective, positionY, numberOfElementsToShow, previousBtn):
    global elementPosition
    global actualPosition

    for var in range(elementPosition - 1, objective - 1, -1):
        try:
            canvasForElements.create_text(
            7,
            positionY,
            anchor="nw",
            text=elements[var]["code"],
            fill="#FFFFFF"
            )
     
            canvasForElements.create_text(
                93,
                positionY,
                anchor="nw",
                text=elements[var]["name"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                257,
                positionY,
                anchor="nw",
                text=elements[var]["zone"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                407,
                positionY,
                anchor="nw",
                text=elements[var]["latitude"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                580.0,
                positionY,
                anchor="nw",
                text=elements[var]["longitude"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                779.0,
                positionY,
                anchor="nw",
                text=elements[var]["currentState"],
                fill="#FFFFFF"
            )

            positionY = positionY + 30
            elementPosition = elementPosition - 1
            if elementPosition == 0:
                elementPosition = numberOfElementsToShow
                actualPosition = 1
                previousBtn.place_forget()
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

def getTrainRouteListInitialData():
    global elementPosition
    elementPosition = 0

    trainRouteList = []
    zones = {}

    trainStops = {}

    trainStopsFile = open("../Dados/trainStops.txt", "r")

    for line in trainStopsFile:
        line = line.strip().split(",")
        trainStops[line[0]] = line[1]

    trainStopsFile.close()

    #connections = {}
    '''
    trainConnectionsfile = open("../Dados/trainStopsConnections.txt", "r")

    for line in trainConnectionsfile:
        line = line.strip().split(",")
        connections[line[1]].append((line[2], line[3]))
        connections[line[2]].append((line[1], line[3]))

    trainConnectionsfile.close()
    '''
    #isPossible = verifyConnection(connections, startTrainStopCode, endTrainStopCode)

    zonesFile = open("../Dados/zones.txt", "r")

    for line in zonesFile:
        line = line.strip().split(",")
        zones[line[0]] = line[1]
        
    zonesFile.close()

    file = open("../Dados/trainRoute.txt", "r")   

    for var in file.readlines():
        trainRoute = {}
        var = var.strip("\n").split(",")

        trainRoute["code"] = var[0] 
        trainRoute["name"] = var[1] 
        trainRoute["initialStop"] = getValueByKey(trainStops, var[2])
        trainRoute["finalStop"] = getValueByKey(trainStops, var[3])
        trainRoute["currentState"] = var[4]
        trainRoute["frequency"] = var[5] + " minutes"
        
        trainRouteList.append(trainRoute)

    file.close()

    return zones, trainStops, trainRouteList

def searchTrainRouteList(zone, zoneDic, trainStopsDic):
    global elementPosition
    elementPosition = 0

    trainStops = []
    zoneCode = getKeyByValue(zoneDic, zone)

    file = open("../Dados/trainStops.txt", "r")  

    for line in file:
        line = line.strip("\n").split(",")
        if line[2] == zoneCode:
            trainStops.append(line[0])

    file.close()

    trainRouteList = []

    file = open("../Dados/trainRoute.txt", "r")   

    for var in file.readlines():
        trainRoute = {}
        var = var.strip("\n").split(",")

        if var[2] in trainStops:
            trainRoute["code"] = var[0] 
            trainRoute["name"] = var[1] 
            trainRoute["initialStop"] = getValueByKey(trainStopsDic, var[2])
            trainRoute["finalStop"] = getValueByKey(trainStopsDic, var[3])
            trainRoute["currentState"] = var[4]
            trainRoute["frequency"] = var[5] + " minutes"
            
            trainRouteList.append(trainRoute)

    file.close()

    return trainRouteList

def printCanvasNextTrainRoute(elements, canvasForElements, objective, positionY):
    global elementPosition

    for var in range(elementPosition, objective):
        try:
            canvasForElements.create_text(
            7,
            positionY,
            anchor="nw",
            text=elements[var]["code"],
            fill="#FFFFFF"
            )
     
            canvasForElements.create_text(
                93,
                positionY,
                anchor="nw",
                text=elements[var]["name"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                260,
                positionY,
                anchor="nw",
                text=elements[var]["initialStop"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                452,
                positionY,
                anchor="nw",
                text=elements[var]["finalStop"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                620.0,
                positionY,
                anchor="nw",
                text=elements[var]["frequency"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                779.0,
                positionY,
                anchor="nw",
                text=elements[var]["currentState"],
                fill="#FFFFFF"
            )
           
            positionY = positionY + 30
            elementPosition = elementPosition + 1
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

def printCanvasPreviousTrainRoute(elements, canvasForElements, objective, positionY, numberOfElementsToShow, previousBtn):
    global elementPosition
    global actualPosition

    for var in range(elementPosition - 1, objective - 1, -1):
        try:
            canvasForElements.create_text(
            7,
            positionY,
            anchor="nw",
            text=elements[var]["code"],
            fill="#FFFFFF"
            )
     
            canvasForElements.create_text(
                93,
                positionY,
                anchor="nw",
                text=elements[var]["name"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                260,
                positionY,
                anchor="nw",
                text=elements[var]["initialStop"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                452,
                positionY,
                anchor="nw",
                text=elements[var]["finalStop"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                620.0,
                positionY,
                anchor="nw",
                text=elements[var]["frequency"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                779.0,
                positionY,
                anchor="nw",
                text=elements[var]["currentState"],
                fill="#FFFFFF"
            )

            positionY = positionY + 30
            elementPosition = elementPosition - 1
            if elementPosition == 0:
                elementPosition = numberOfElementsToShow
                actualPosition = 1
                previousBtn.place_forget()
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

def searchAndPrintZoneInfo(entryCodeToSearch, searchFor, entryName, entryLatitude, entryLongitude, entryDescription, searchForDic):
    global elementPosition
    elementPosition = 0
    searchForList = []

    file = open("../Dados/zones.txt", "r")   

    for var in file:
        var = var.strip("\n").split(",")

        if (var[0] == entryCodeToSearch):
            insertEntryInfo(entryName, var[1])
            insertEntryInfo(entryLatitude, var[2])
            insertEntryInfo(entryLongitude, var[3])

            entryDescription.configure(state="normal")
            entryDescription.delete(1.0, "end")
            entryDescription.insert("end", var[4]) 
            entryDescription.configure(state="disabled")
            break
            
    file.close()

    searchFor = getKeyByValue(searchForDic, searchFor)

    if searchFor == 0:
        file = open("../Dados/amusements.txt", "r")

        for var in file.readlines():
            amusement = {}
            var = var.strip("\n").split(",")

            if entryCodeToSearch == var[2]:
                amusement["code"] = var[0] 
                amusement["name"] = var[1]
                #amusement["amusementType"] = getValueByKey(amusementTypes, var[3])   
                #amusement["minAge"] = var[6]
                #amusement["minHeight"] = var[7]
                #amusement["intensity"] = getValueByKey(intensityDic, int(var[8]))
                amusement["currentState"] = var[9]
                
                searchForList.append(amusement)

        file.close()
    elif searchFor == 1:
        file = open("../Dados/accommodations.txt", "r")   

        for var in file.readlines():
            accommodation = {}
            var = var.strip("\n").split(",")

            if entryCodeToSearch == var[2]:
                accommodation["code"] = var[0] 
                accommodation["name"] = var[1]
                #accommodation["latitude"] = var[3]
                #accommodation["longitude"] = var[4]
                accommodation["currentState"] = var[5]
                
                searchForList.append(accommodation)

        file.close()
    elif searchFor == 2:
        trainStops = []

        file = open("../Dados/trainStops.txt", "r")  

        for line in file:
            line = line.strip("\n").split(",")
            if line[2] == entryCodeToSearch:
                trainStops.append(line[0])

        file.close()

        file = open("../Dados/trainRoute.txt", "r")   

        for var in file:
            trainRoute = {}
            var = var.strip("\n").split(",")

            if var[2] in trainStops:
                trainRoute["code"] = var[0] 
                trainRoute["name"] = var[1] 
                #trainRoute["initialStop"] = getValueByKey(trainStopsDic, var[2])
                #trainRoute["finalStop"] = getValueByKey(trainStopsDic, var[3])
                trainRoute["currentState"] = var[4]
                #trainRoute["frequency"] = var[5] + " minutes"
                
                searchForList.append(trainRoute)

        file.close()

    return searchForList

def printCanvasNextZoneInfo(elements, canvasForElements, objective, positionY):
    global elementPosition

    for var in range(elementPosition, objective):
        try:
            canvasForElements.create_text(
            7,
            positionY,
            anchor="nw",
            text=elements[var]["code"],
            fill="#FFFFFF"
            )
     
            canvasForElements.create_text(
                107,
                positionY,
                anchor="nw",
                text=elements[var]["name"],
                fill="#FFFFFF"
            )

            '''
            canvasForElements.create_text(
                335,
                positionY,
                anchor="nw",
                text=elements[var]["amusementType"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                455.0,
                positionY,
                anchor="nw",
                text=elements[var]["minAge"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                545.0,
                positionY,
                anchor="nw",
                text=(elements[var]["minHeight"] + "cm"),
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                670.0,
                positionY,
                anchor="nw",
                text=elements[var]["intensity"],
                fill="#FFFFFF"
            )

            '''

            canvasForElements.create_text(
                300.0,
                positionY,
                anchor="nw",
                text=elements[var]["currentState"],
                fill="#FFFFFF"
            )
           
            positionY = positionY + 30
            elementPosition = elementPosition + 1
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

def printCanvasPreviousZoneInfo(elements, canvasForElements, objective, positionY, numberOfElementsToShow, previousBtn):
    global elementPosition
    global actualPosition

    for var in range(elementPosition - 1, objective - 1, -1):
        try:
            canvasForElements.create_text(
            7,
            positionY,
            anchor="nw",
            text=elements[var]["code"],
            fill="#FFFFFF"
            )
     
            canvasForElements.create_text(
                107,
                positionY,
                anchor="nw",
                text=elements[var]["name"],
                fill="#FFFFFF"
            )

            '''
            canvasForElements.create_text(
                335,
                positionY,
                anchor="nw",
                text=elements[var]["amusementType"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                455.0,
                positionY,
                anchor="nw",
                text=elements[var]["minAge"],
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                545.0,
                positionY,
                anchor="nw",
                text=(elements[var]["minHeight"] + "cm"),
                fill="#FFFFFF"
            )

            canvasForElements.create_text(
                670.0,
                positionY,
                anchor="nw",
                text=elements[var]["intensity"],
                fill="#FFFFFF"
            )

            '''

            canvasForElements.create_text(
                300.0,
                positionY,
                anchor="nw",
                text=elements[var]["currentState"],
                fill="#FFFFFF"
            )

            positionY = positionY + 30
            elementPosition = elementPosition - 1
            if elementPosition == 0:
                elementPosition = numberOfElementsToShow
                actualPosition = 1
                previousBtn.place_forget()
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

def getZoneListInitialData():
    global elementPosition
    elementPosition = 0

    zoneList = []

    file = open("../Dados/zones.txt", "r")   

    for var in file.readlines():
        zone = {}
        var = var.strip("\n").split(",")

        zone["code"] = var[0] 
        zone["name"] = var[1]
        zone["latitude"] = var[2]
        zone["longitude"] = var[3]
        
        zoneList.append(zone)

    file.close()

    return zoneList

def printCanvasNextZoneList(elements, canvasForElements, objective, positionY):
    global elementPosition

    for var in range(elementPosition, objective):
        try:
            canvasForElements.create_text(
            15,
            positionY,
            anchor="nw",
            text=elements[var]["code"],
            fill="#FFFFFF",
            font=("Arial", 11)
            )
     
            canvasForElements.create_text(
                137,
                positionY,
                anchor="nw",
                text=elements[var]["name"],
                fill="#FFFFFF",
                font=("Arial", 11)
            )
    
            canvasForElements.create_text(
                357,
                positionY,
                anchor="nw",
                text=elements[var]["latitude"],
                fill="#FFFFFF",
                font=("Arial", 11)
            )

            canvasForElements.create_text(
                604.0,
                positionY,
                anchor="nw",
                text=elements[var]["longitude"],
                fill="#FFFFFF",
                font=("Arial", 11)
            )
           
            positionY = positionY + 30
            elementPosition = elementPosition + 1
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

def printCanvasPreviousZoneList(elements, canvasForElements, objective, positionY, numberOfElementsToShow, previousBtn):
    global elementPosition
    global actualPosition

    for var in range(elementPosition - 1, objective - 1, -1):
        try:
            canvasForElements.create_text(
            15,
            positionY,
            anchor="nw",
            text=elements[var]["code"],
            fill="#FFFFFF",
            font=("Arial", 11)
            )
     
            canvasForElements.create_text(
                137,
                positionY,
                anchor="nw",
                text=elements[var]["name"],
                fill="#FFFFFF",
                font=("Arial", 11)
            )
    
            canvasForElements.create_text(
                357,
                positionY,
                anchor="nw",
                text=elements[var]["latitude"],
                fill="#FFFFFF",
                font=("Arial", 11)
            )

            canvasForElements.create_text(
                604.0,
                positionY,
                anchor="nw",
                text=elements[var]["longitude"],
                fill="#FFFFFF",
                font=("Arial", 11)
            )

            positionY = positionY + 30
            elementPosition = elementPosition - 1
            if elementPosition == 0:
                elementPosition = numberOfElementsToShow
                actualPosition = 1
                previousBtn.place_forget()
        except:  
            ctypes.windll.user32.MessageBoxW(0, "Something went wrong!\nTry again later.", "Error!", 0)                 
            break

def generateTicketQRCode(ref, canvasForQRCode):
    file = open("../Dados/ticket.txt", "r")   
    ticket = {}
    for line in file:  
        line = line.strip("\n").split(",")
        if ref == line[0]:
            ticket["ref"] = line[0] 
            ticket["finalDate"] = line[6]

    file.close()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=7,
        border=4,
    )
    qr.add_data("Referência: " + ticket["ref"] + "\nVálido até: " + ticket["finalDate"])
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_tk = ImageTk.PhotoImage(img)

    canvasForQRCode.delete("all")
    canvasForQRCode.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvasForQRCode.image = img_tk

