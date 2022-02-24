from api import api

class events:
  eventUrl = 'https://api.planningcenteronline.com/calendar/v2/events'
  eventId = ""
  ownerUrl = ""

  def __init__(self, eventId):
    self.eventId = eventId
  def getAll(self):
    return api().get('%s?per_page=100' % (self.eventUrl))
  def getDetails(self):
    resp = api().get('%s/%s' % (self.eventUrl, self.eventId))
    self.ownerUrl = resp["data"]["links"]["owner"]
    return resp
  # def getMembers(self):
  #   return api().get('%s/%s/memberships' % (self.eventUrl, self.eventId))
  def getOwner(self):
    if self.ownerUrl == None:
      return None
    else:
      return api().get(self.ownerUrl)