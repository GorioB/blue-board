from django.core.management.base import CommandError
from daemon_command import DaemonCommand
from notices.models import Notice
from bluetoothtools import *


class Command(DaemonCommand):
    help = 'Does some magical work'

    def loop_callback(self, *args, **options):
        """ Do your work here """
        #self.stdout.write('There are {} things!'.format(Notice.objects.count()))
        bluetoothServer = BluetoothServer()
        bluetoothServer.start()