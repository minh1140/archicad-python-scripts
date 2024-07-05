from archicad import ACConnection
import archicad
import sys
import re

from archicad.releases.ac26.b3005types import ElementId, ElementPropertyValue
conn = ACConnection.connect()

assert conn

conn = ACConnection.connect()
acc = conn.commands
act = conn.types
acu = conn.utilities

elementIdBuiltInPropertyUserIds = acc.GetAllElements()
Layer = acu.GetBuiltInPropertyId('ModelView_LayerName')
elemenType=acu.GetBuiltInPropertyId('General_Type')
value =acc.GetPropertyValuesOfElements(elementIdBuiltInPropertyUserIds,[Layer])
value2=acc.GetPropertyValuesOfElements(elementIdBuiltInPropertyUserIds,[elemenType])

def get_classification (system,item):                                                                   #get classification item from classification system
    class1 = acu.FindClassificationSystem(system)
    class2 = acu.FindClassificationItemInSystem(system,item)
    class_id = act.ClassificationId(class1,class2.classificationItemId)
    return class_id

# NumberArray = []                                                                                      #print out element's layer and type
# for index,element in enumerate(elementIdBuiltInPropertyUserIds):
#     element = element.elementId
#     Info1 = value[index].propertyValues[0].propertyValue.value
#     Info2 = value2[index].propertyValues[0].propertyValue.value
#     print("Layer name: ",Info1,"----Element type in layer:", Info2)

def assign_classification (eletype,layerstring,classification):                                          #assign classification based on element type and layer
    elem_classes = []
    for index,element2 in enumerate(elementIdBuiltInPropertyUserIds):
        if eletype == value2[index].propertyValues[0].propertyValue.value:                               #element type filter
            if re.search(layerstring,value[index].propertyValues[0].propertyValue.value):                #layer contains Wall
                elem_class = act.ElementClassification(element2.elementId,classification)
                elem_classes.append(elem_class) 
    acc.SetClassificationsOfElements(elem_classes)
    print(elem_classes)

#command to run: for element type 'eletype', with layer having 'layerstring' in name, assign classification using classification item from get_classification
assign_classification('Wall','Wall',get_classification('Archicad Classification','Wall'))
assign_classification('Slab','Slab',get_classification('Archicad Classification','Slab'))
assign_classification('Slab','Ceiling',get_classification('Archicad Classification','Ceiling'))
assign_classification('Window','',get_classification('Archicad Classification','Window'))
assign_classification('Door','',get_classification('Archicad Classification','Door'))
assign_classification('Slab','Joinery',get_classification('Archicad Classification','Furniture'))
assign_classification('Slab','Fitout',get_classification('Archicad Classification','Furniture'))
assign_classification('Mesh','Site',get_classification('Archicad Classification','Site Geometry'))
assign_classification('Roof','',get_classification('Archicad Classification','Roof'))