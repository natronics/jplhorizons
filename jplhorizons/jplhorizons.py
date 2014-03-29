#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import closing
import telnetlib


class UnknownObject(Exception):
    def __init__(self, craft):
        msg = "Object '%s' unknown (in jplhorizons library)" % craft
        Exception.__init__(self, msg)

class Telnet(object):
    """Telnet implementation of JPL HORIZONS

    :param str host: telnet host (default 'ssd.jpl.nasa.gov')
    :param int port: telnet port (default 6775)
    :param float timeout: connection timeout (default 0.5)
    :returns: Telnet instance

    Exposes abstraction to interact with the JPL system through telnet
    """

    def __init__(self, host='ssd.jpl.nasa.gov', port=6775, timeout=0.5):
        self.host = host
        self.port = port
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, 'horizons'):
            self.horizons.close()
            delattr(self, 'horizons')

    def _login(self):
        if not hasattr(self, 'horizons'):
            telnet_connection = telnetlib.Telnet(self.host, self.port, self.timeout)
            self.horizons = telnet_connection

    def _logout(self):
        if hasattr(self, 'horizons'):
            self.horizons.close()
            delattr(self, 'horizons')

    def get_spacecraft_elements(self, craft, center='sun'):

        if craft not in SPACECRAFT:
            raise(UnknownObject(craft))
        self._login()
        self.horizons.read_until('>')
        self._logout()


# Spacecraft definitions
SPACECRAFT = {
    'juno': -61,
}

BODIES = {
    'sun': '500',
}
