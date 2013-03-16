from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import pygal
from pygal.style import Style
from models import LaundryMachine, LaundryRecord
import logging
logging.basicConfig(filename='laundry.log',level=logging.DEBUG)
logging.debug('starting...')

WASHER = LaundryMachine.WASHER
DRYER = LaundryMachine.DRYER
AVAILABLE = LaundryRecord.AVAILABLE
IN_USE = LaundryRecord.IN_USE
CYCLE_COMPLETE = LaundryRecord.CYCLE_COMPLETE
UNAVAILABLE = LaundryRecord.UNAVAILABLE
BASE_URL_QUERY = 'http://gmu.esuds.net/RoomStatus/machineStatus.i?bottomLocationId='

def load_data(hall):
    """Extract table data from esuds for specified hall"""
    html = urlopen(BASE_URL_QUERY+str(int(hall.location_id))).read()
    soup = BeautifulSoup(html) # Start cook'n
    rows = [row for row in soup.findAll('tr')[1:] if len(row('td')) > 1]
    return rows

def get_num_machines_per_status(status, hall):
    """
    Count the number of machines in a hall which have the desired status and
    return a list that can be inputed to the pygal add series function.

    Returns a list of two ints. The first element is the number of washers
    with the desired status and the second is the number of dryers.
    """
    return [len([m for m in LaundryMachine.objects.filter(type=WASHER,
                hall=hall) if m.get_latest_record().availability == status]),
            len([m for m in LaundryMachine.objects.filter(type=DRYER,
                hall=hall) if m.get_latest_record().availability == status])]



def generate_current_chart(filepath, hall):
    """
    Generate stacked bar chart of current laundry usage for specified hall and
    save svg at filepath.
    """
    custom_style = Style(colors=('#B6E354', '#FF5995', '#FEED6C', '#E41B17'))
    chart = pygal.StackedBar(style=custom_style, width=800, height=512, explicit_size=True)
    chart.title = 'Current laundry machine usage in ' + hall.name
    chart.x_labels = ['Washers', 'Dryers']
    chart.add('Available', get_num_machines_per_status(AVAILABLE, hall))
    chart.add('In Use', get_num_machines_per_status(IN_USE, hall))
    chart.add('Cycle Complete', get_num_machines_per_status(CYCLE_COMPLETE, hall))
    chart.add('Unavailable', get_num_machines_per_status(UNAVAILABLE, hall))
    chart.range = [0, 11]
    chart.render_to_file(filepath)

def update(hall, filepath=None):
    """
    Scrape data from esuds for the specified hall, create a new LaundryRecord
    for each machine, and optionally save a new current chart for the hall.

    To generate a current chart with this update, set filepath to a valid
    filepath to save and svg file.
    """
    rows = load_data(hall)
    for row in rows:
        cells = row('td')
        number = int(cells[1].contents[0])
        type = cells[2].contents[0]
        if type == 'Stacked Dryer': type = type[8:]
        availability = cells[3].contents[1].contents[0]
        time_remaining = None
        if cells[4].contents[0] != '&nbsp;':
            time_remaining = int(cells[4].contents[0])
        machine = LaundryMachine.objects.get(number=number, type=type,
                hall=hall)
        record = LaundryRecord(machine=machine, availability=availability,
                time_remaining=time_remaining)
        record.save()
    if filepath:
        generate_current_chart(filepath, hall)
