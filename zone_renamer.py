
from archicad import ACConnection
import archicad
import sys
conn = ACConnection.connect()

assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

#get element by type, zone in this case
elem_all_zones = acc.GetElementsByType('Zone')
#get Zone Number to edit
prop_znumber = acu.GetBuiltInPropertyId('Zone_ZoneNumber')
#input property by group, name of property
prop_pnumber = acu.GetUserDefinedPropertyId('ZONES','DKO Zone - Apartment Number')

#propvallist_pnumber holds the actual value of the property. loop to go through each prop of zone
propvallist_pnumber = [val.propertyValues[0].propertyValue.value for val in acc.GetPropertyValuesOfElements(elem_all_zones, [prop_pnumber])]

for i, elem in enumerate(elem_all_zones):
    new_zonenumber = act.ElementPropertyValue(
                elem.elementId, prop_znumber, act.NormalStringPropertyValue(propvallist_pnumber[i]))
    # write number back
    acc.SetPropertyValuesOfElements([new_zonenumber])
