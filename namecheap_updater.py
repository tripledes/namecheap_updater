#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys
import xml.etree.ElementTree as ET

from json import load
from socket import gethostbyname, error
from urllib import urlencode
from urllib2 import urlopen, URLError

SERVICE = "http://jsonip.com"
HOSTNAME = os.environ.get("NAMECHEAP_HOST")
DOMAIN = os.environ.get("NAMECHEAP_DOMAIN")
NAMECHEAP_URL = "https://dynamicdns.park-your-domain.com/update?"
TOKEN = os.environ.get("NAMECHEAP_TOKEN")


def get_public_ip():
    """ Query SERVICE to find out our public IP """
    try:
        resp = load(urlopen(SERVICE))
    except URLError as e:
        print "Error querying %s: %s" % (SERVICE, str(e.reason))
        sys.exit(1)

    return resp.get("ip")

def get_current_ip():
    """ Get hostname's current IP """
    try:
        return gethostbyname(HOSTNAME + "." + DOMAIN)
    except error as e:
        print "Error getting current IP: %s" % str(e)
        sys.exit(1)

def update_namecheap_ip(ip):
    """ POST the new IP to namecheap """
    data = dict()
    data["ip"] = ip
    data["password"] = TOKEN
    data["host"] = HOSTNAME
    data["domain"] = DOMAIN
    url_data = urlencode(data)

    try:
        full_url = NAMECHEAP_URL + url_data
        return urlopen(full_url)
    except URLError as e:
        if hasattr(e, "reason"):
            print "Error updating namecheap with IP %s: %s" % (ip, str(e.reason))
        elif hasattr(e, "code"):
            print "Namecheap couldn't fulfill the request. Error code: %d" % e.code
        sys.exit(1)

def check_response(resp):
    """ Check Namecheap XML response """
    root = ET.fromstring(resp.read())
    errors_count = root.find("ErrCount").text

    if errors_count == 0:
        return None

    errors = root.findall("errors")
    err_msgs = list()

    for i in range(0, len(errors)):
        err_msgs.append(errors[i].find("Err" + str(i + 1)).text)
    return err_msgs

def main():
    current = get_current_ip()
    new = get_public_ip()

    if current == new:
        print "Nothing to see here, move along..."
        sys.exit(0)

    print "Updating with IP: %s" % new
    resp = update_namecheap_ip(new)
    msgs = check_response(resp)

    if msgs is None:
        print "Updated successfully"
        sys.exit(0)

    print "Errors:"
    print "\n".join(msgs)
    sys.exit(1)

if __name__ == "__main__":
    main()
