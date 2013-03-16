from django.db import models

class Hall(models.Model):
    name = models.TextField(max_length=100)
    location_id = models.IntegerField() # id used by esuds

class LaundryMachine(models.Model):
    WASHER = 'Washer'
    DRYER = 'Dryer'
    MACHINE_TYPES = (
            ('Washer', 'Washer'),
            ('Dryer', 'Dryer'),
    )
    number = models.PositiveSmallIntegerField() # number assigned by esuds
    type = models.TextField(choices=MACHINE_TYPES)
    hall = models.ForeignKey('Hall')

    def get_latest_record(self):
        records = self.records.all()
        return records[len(records)-1]

class LaundryRecord(models.Model):
    AVAILABLE = 'Available'
    IN_USE = 'In Use'
    CYCLE_COMPLETE = 'Cycle Complete'
    UNAVAILABLE = 'Unavailable'
    AVAILABILITIES = (
            (AVAILABLE, 'Available'),
            (IN_USE, 'In Use'),
            (CYCLE_COMPLETE, 'Cycle Complete'),
            (UNAVAILABLE, 'Unavailable'),
    )
    machine = models.ForeignKey('LaundryMachine', related_name='records')
    availability = models.TextField(choices=AVAILABILITIES)
    time_remaining = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
