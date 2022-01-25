from api import api
import config
import time


class maps:
    mapUrl = 'https://maps.googleapis.com/maps/api/geocode/json?key=%s' % (config.GOOGLE_APIKEY)
    address = ''
    addresses = {}

    def __init__(self, address):
        self.address = address

    def getLocation(self):
        if self.address not in self.addresses:

            if self.address == '':
                self.address = 'Unknown TX 76071'

            resp = api().get('%s&address=%s' % (self.mapUrl, self.address))
            try:
                self.addresses[self.address] = resp["results"][0]["geometry"][
                    "location"]  # expects { "lat": 00.000, "lng": 00.000 }
            except IndexError:
                self.addresses[self.address] = {"lat": 00.000, "lng": 00.000}

        return self.addresses[self.address]