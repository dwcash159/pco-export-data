import requests
import config
import time


class api:
  def get(self, url):
    print("        " + url)
    resp = requests.get(
      url,
      auth=(config.API_USERNAME, config.API_PASSWORD)
    )

    while resp.status_code != 200:
      print("Trying API call again...waiting 10 seconds")
      print(resp.text)
      print(url)
      time.sleep(10)
      resp = requests.get(
        url,
        auth=(config.API_USERNAME, config.API_PASSWORD)
      )      

    return resp.json()
