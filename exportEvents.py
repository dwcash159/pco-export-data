from events import events
from people import people
from maps import maps
import config
import time
from geopy import distance

outputFile = open("eventsExport.csv", "w+")
# add new columns to csvHeader AND update the number of columns in csvPlaceholder
csvHeader = "Event ID, Approval Status, Created At, Updated At, Archived At, Name, Details, Image Url, Percent Approved, Percent Rejected, Visible In Church Center, Owner Status, Owner First Name, Owner Middle Name, Owner Last Name, Event Permission Type, Owner Email\r\n"
csvPlaceholder = ("\"%s\"," * 17) + "\r\n"
outputFile.write(csvHeader)

eventsList = events('').getAll()

for evt in eventsList["data"]:
  time.sleep(.4) # slowing down API calls to not exceed rates of 100 in 20s
  print(evt["attributes"]["name"])
  eventObj = events(evt["id"])
  eventDetail = eventObj.getDetails()
  evtOwner = eventObj.getOwner()
  # members = groupObj.getMembers()

  # if evtLocation != None:
  #   groupAddress = evtLocation["data"]["attributes"]["full_formatted_address"].replace("\n", ", ")
  #   groupLong = evtLocation["data"]["attributes"]["longitude"]
  #   groupLat = evtLocation["data"]["attributes"]["latitude"]
  # else:
  #   groupAddress = ""
  #   groupLong = ""
  #   groupLat = ""

  # for member in members["data"]:
  #   # try:
  #     print("    %s %s" % (member["attributes"]["first_name"], member["attributes"]["last_name"]))
  #     time.sleep(.2) # a little more slow down
  #     personObj = people(member["attributes"]["account_center_identifier"])
  #     person = personObj.getPerson()
  #     maritalStatus = personObj.getMaritalStatus()
  #     addresses = personObj.getAddress()
  #     if addresses != None and len(addresses["data"]) > 0:
  #       address = addresses["data"][0]
  #       mapApi = maps("%s %s %s" % (address["attributes"]["city"] if address["attributes"]["city"] != None else '',
  #         address["attributes"]["state"] if address["attributes"]["state"] != None else '',
  #         address["attributes"]["zip"] if address["attributes"]["zip"] != None else ''))
  #       mapLocation = mapApi.getLocation()
  #       if evtLocation != None:
  #         distanceUnit = config.UNIT if hasattr(config, 'UNIT') else 'miles'
  #         memberDistance = eval('distance.distance((groupLat, groupLong),(mapLocation["lat"], mapLocation["lng"])).' + distanceUnit)
  #       else:
  #         memberDistance = ""

  ownerStatus = ""
  ownerFirstName = ""
  ownerMiddleName = ""
  ownerLastName = ""
  ownerEventPermissionsTypes = ""
  ownerEmail = ""

  if "data" in evtOwner:
    ownerStatus = evtOwner["data"]["attributes"]["status"]
    ownerFirstName = evtOwner["data"]["attributes"]["first_name"]
    ownerMiddleName = evtOwner["data"]["attributes"]["middle_name"]
    ownerLastName = evtOwner["data"]["attributes"]["last_name"]
    ownerEventPermissionsTypes = evtOwner["data"]["attributes"]["event_permissions_type"]

    try:
      if len(evtOwner["data"]["attributes"]["contact_data"]["email_addresses"]) > 0:
        ownerEmail = evtOwner["data"]["attributes"]["contact_data"]["email_addresses"][0]["address"]
    except:
      print("    Warning: No Owner details")

  print("    Owner email%s " % ownerEmail)
  outputFile.write(csvPlaceholder % (
    evt["id"],
    evt["attributes"]["approval_status"],
    evt["attributes"]["created_at"],
    evt["attributes"]["updated_at"],
    evt["attributes"]["archived_at"],
    evt["attributes"]["name"],
    evt["attributes"]["details"],
    evt["attributes"]["image_url"],
    evt["attributes"]["percent_approved"],
    evt["attributes"]["percent_rejected"],
    evt["attributes"]["visible_in_church_center"],
    ownerStatus,
    ownerFirstName,
    ownerMiddleName,
    ownerLastName,
    ownerEventPermissionsTypes,
    ownerEmail
    ))
    # except:
    #   print("errored for %s %s" % (member["attributes"]["first_name"], member["attributes"]["last_name"]))

outputFile.close()