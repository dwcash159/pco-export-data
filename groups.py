from api import api

class groups:
  groupUrl = 'https://api.planningcenteronline.com/groups/v2/groups'
  groupId = ""
  locationUrl = ""

  def __init__(self, grpId):
    self.groupId = grpId
  def getAll(self):
    groups = api().get('%s?per_page=100' % (self.groupUrl))
    links = groups["links"]

    while 'next' in links:
      groups_next = api().get(links["next"])
      links = groups_next["links"]
      groups["data"] = groups["data"] + groups["data"]

    print("Number of groups %s" % len(groups["data"]))

    return groups
  def getDetails(self):
    resp = api().get('%s/%s' % (self.groupUrl, self.groupId))
    self.locationUrl = resp["data"]["links"]["location"]
    return resp
  def getMembers(self):
    memberships = api().get('%s/%s/memberships?per_page=100' % (self.groupUrl, self.groupId))
    links = memberships["links"]

    while 'next' in links:
      memberships_next = api().get(links["next"])
      links = memberships_next["links"]
      memberships["data"] = memberships["data"] + memberships_next["data"]

    print("Number of members %s" % len(memberships["data"]))

    return memberships
  def getLocation(self):
    if self.locationUrl == None:
      return None
    else:
      return api().get(self.locationUrl)
