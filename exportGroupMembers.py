from groups import groups
from people import people
from maps import maps
import config
import time
from geopy import distance

# from pprint import pprint


outputFile = open("groupsExport.csv", "w+")
# add new columns to csvHeader AND update the number of columns in csvPlaceholder
csvHeader = "ID, First Name, Last Name, Email, Phone, Gender, Birthdate, City, State, Zip, Location Long, Location Lat, Distance to Group, Marital Status, Membership, Status, Person Record Updated, Person Record Created, Joined Group At, Role, Group ID, Group, Group Location, Group Long, Group Lat\r\n"
csvPlaceholder = ("\"%s\"," * 25) + "\r\n"
outputFile.write(csvHeader)

groupsList = groups('').getAll()

for group_idx, grp in enumerate(groupsList["data"]):
    time.sleep(3)  # slowing down API calls to not exceed rates of 100 in 20s
    print("Group Index: %s - %s" % (group_idx, grp["attributes"]["name"]))
    groupObj = groups(grp["id"])
    groupDetail = groupObj.getDetails()
    members = groupObj.getMembers()
    grpLocation = groupObj.getLocation()
    if grpLocation != None:
        groupAddress = grpLocation["data"]["attributes"]["full_formatted_address"].replace("\n", ", ")
        groupLong = grpLocation["data"]["attributes"]["longitude"]
        groupLat = grpLocation["data"]["attributes"]["latitude"]
    else:
        groupAddress = ""
        groupLong = ""
        groupLat = ""

    for member_idx, member in enumerate(members["data"]):
        # try:
        print("    Member Index: %s %s %s" % (member_idx, member["attributes"]["first_name"], member["attributes"]["last_name"]))
        time.sleep(1.00)  # a little more slow down
        personObj = people(member["attributes"]["account_center_identifier"])
        person = personObj.getPerson()
        maritalStatus = personObj.getMaritalStatus()
        addresses = personObj.getAddress()
        try:
            email = member["attributes"]["email_address"]
        except:
            email = ""

        try:
            phone = member["attributes"]["phone_number"]
        except:
            phone = ""

        if addresses != None and len(addresses["data"]) > 0:
            address = addresses["data"][0]
            mapApi = maps("%s,%s,%s" % (address["attributes"]["city"] if address["attributes"]["city"] != None else '',
                                        address["attributes"]["state"] if address["attributes"][
                                                                              "state"] != None else '',
                                        address["attributes"]["zip"] if address["attributes"]["zip"] != None else ''))
            mapLocation = mapApi.getLocation()
            if grpLocation != None:
                distanceUnit = config.UNIT if hasattr(config, 'UNIT') else 'miles'
                memberDistance = eval(
                    'distance.distance((groupLat, groupLong),(mapLocation["lat"], mapLocation["lng"])).' + distanceUnit)
            else:
                memberDistance = ""

        outputFile.write(csvPlaceholder % (
            person["data"]["id"],
            person["data"]["attributes"]["first_name"],
            person["data"]["attributes"]["last_name"],
            email,
            phone,
            person["data"]["attributes"]["gender"],
            person["data"]["attributes"]["birthdate"],
            address["attributes"]["city"] if address["attributes"]["city"] != None else '',
            address["attributes"]["state"] if address["attributes"]["state"] != None else '',
            address["attributes"]["zip"] if address["attributes"]["zip"] != None else '',
            mapLocation["lng"],
            mapLocation["lat"],
            memberDistance,
            maritalStatus["data"]["attributes"]["value"] if maritalStatus != None else '',
            person["data"]["attributes"]["membership"],
            person["data"]["attributes"]["status"],
            person["data"]["attributes"]["updated_at"],
            person["data"]["attributes"]["created_at"],
            member["attributes"]["joined_at"],
            member["attributes"]["role"],
            grp["id"],
            groupDetail["data"]["attributes"]["name"],
            groupAddress,
            groupLong,
            groupLat
        ))
    # except:
    #   print("errored for %s %s" % (member["attributes"]["first_name"], member["attributes"]["last_name"]))

outputFile.close()
