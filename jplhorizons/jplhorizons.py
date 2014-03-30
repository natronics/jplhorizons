#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import telnetlib
from telnetlib import IAC, WILL, WONT, DONT, DO, SB, SE, TTYPE, NAWS

IS = chr(0)

def negotiate(sock, cmd, opt):
    if cmd == DO:
        if opt == NAWS:
            sock.send(''.join([IAC, WILL, NAWS]))
            sock.send(''.join([IAC, SB, NAWS, IS, chr(200), IS, chr(254), IAC, SE]))

class UnknownObject(Exception):
    def __init__(self, craft):
        msg = "Object '%s' unknown (in jplhorizons library)" % craft
        Exception.__init__(self, msg)

class BrokenNavigaion(Exception):
    def __init__(self, craft):
        Exception.__init__(self, "The navigation of JPL HORIZONS failed :(")


class Telnet(object):
    """Telnet implementation of JPL HORIZONS

    :param str host: telnet host (default 'ssd.jpl.nasa.gov')
    :param int port: telnet port (default 6775)
    :returns: Telnet instance

    Exposes abstraction to interact with the JPL system through telnet
    """

    def __init__(self, host='ssd.jpl.nasa.gov', port=6775):
        self.host = host
        self.port = port

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, 'horizons'):
            self.horizons.close()
            delattr(self, 'horizons')

    def _login(self):
        if not hasattr(self, 'horizons'):
            self.horizons = telnetlib.Telnet()
            self.horizons.set_debuglevel(5)
            self.horizons.set_option_negotiation_callback(negotiate)
            self.horizons.open(self.host, self.port)
            match, re, s = self.horizons.expect([r"Horizons\>"], 2)
            if match < 0:
                self._logout()
                raise(BrokenNavigaion())
                return

    def _logout(self):
        if hasattr(self, 'horizons'):
            self.horizons.close()
            delattr(self, 'horizons')

    def _walk_instructions(self, inst):
        for i in inst:
            self.horizons.write(i['i']+'\n')
            re = i.get('re', None)
            if re is not None:
                match, r, s = self.horizons.expect([re], 2)
                if match < 0:
                    self._logout()
                    raise(BrokenNavigaion())
                    return
            else:
                data = self.horizons.read_until("$$EOE")
                return data.split("$$SOE")[1]

    def get_spacecraft_elements(self, craft, center='sun'):

        if craft not in SPACECRAFT:
            raise(UnknownObject(craft))
            return
        self._login()

        now = datetime.datetime.utcnow()
        data = self._walk_instructions([
            {'i': SPACECRAFT[craft], 're': r"(?=Select)(?=(?:.*\[E\])(?:.*\<cr\>:))"},
            {'i': "E",      're': r"Elements"},
            {'i': "e",      're': r"Coordinate system center"},
            {'i': "500@10", 're': r"Confirm"},
            {'i': 'y',      're': r"Reference plane"},
            {'i': 'frame',  're': r"Starting CT"},
            {'i': now.strftime("%Y-%b-%d %H:00"), 're': r"CT"},
            {'i': now.strftime("%Y-%b-%d %H:01"), 're': r"Output interval"},
            {'i': '1d',     're': r"Accept default output"},
            {'i': 'y'},
        ])

        print data

        self._logout()


# Spacecraft definitions
SPACECRAFT = {
    'juno': '-61',
}

BODIES = {
    'sun': '500',
}
