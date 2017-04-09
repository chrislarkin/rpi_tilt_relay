import logging
import time
import urllib2
import TiltHydrometer

from logging.handlers import TimedRotatingFileHandler
from urllib import urlencode

### update as necessary
CLOUD_URL = ''            # found on the 'report' tab of the sheet
TILT_COLOR = 'Black'      # hopefully obvious...
LOG_PATH = 'logs/log.txt' # relative path, set to '' to disable logging
###

def main():
  # start logging
  configure_logging(LOG_PATH)
  logger = logging.getLogger(__name__)
  logger.info('starting pi_tilt_relay')

  # get hydrometer data & send to cloud via query string 
  url = CLOUD_URL
  params = get_tilt_data()

  if not params['SG']:
    logger.error('no Tilt detected')
  else:
    if '?' not in url:
      url += '?'

    post_to_cloud(url + urlencode(params))

  # kbye
  logger.info('stopping pi_tilt_relay')

def configure_logging(LOG_PATH):
  if LOG_PATH:
    try:
      # wipe logs every 30d 
      handler = logging.handlers.TimedRotatingFileHandler(LOG_PATH, when='D', interval=30)
      # prepend messages with timestamps
      formatter = logging.Formatter('%(asctime)s: %(message)s')
      handler.setFormatter(formatter)
      logger = logging.getLogger(__name__)
      logger.addHandler(handler)
      # log all severities
      logger.setLevel(logging.INFO)
    except Exception:
      raise

def get_tilt_data():
  # start logging
  logger = logging.getLogger(__name__)
  logger.info('listening for Tilt ({0})'.format(TILT_COLOR))

  # start a timer & build default dict
  start = time.time()
  data = {'Beer': '',
          'Color': TILT_COLOR,
          'Comment': '',
          'SG': '',
          'Temp': '',
          'Timepoint': ''}

  # init hydrometer listener
  manager = TiltHydrometer.TiltHydrometerManager(True, 60, 40)
  manager.loadSettings()
  manager.start()

  # listen for a beacon for ~60s
  # typically heard within 15s
  while time.time() - start < 60:
    beacon = manager.getValue(TILT_COLOR)

    if beacon:
      # update dict with hydrometer readings
      logger.info('heard Tilt beacon')
      data['SG'] = beacon.gravity
      data['Temp'] = beacon.temperature
      data['Timepoint'] = beacon.timestamp
      break
    else:
      # try again in 10s
      time.sleep(10)

  # shut down listener & return dict  
  manager.stop()
  return data

def post_to_cloud(url):
  # start logging
  logger = logging.getLogger(__name__)
  logger.info('posting data to cloud')
  
  # attempt to connect, log result
  try:
    urllib2.urlopen(url, data=None, timeout=60)
    logger.info('update successful')
  except urllib2.HTTPError as e:
    logger.error('update failed ({0})'.format(e.code))
  except urllib2.URLError as e:
    logger.error('update failed ({0})'.format(e.reason))
  except ValueError as e:
    logger.error('update failed (invalid url)')

if __name__ == '__main__':
  main()
