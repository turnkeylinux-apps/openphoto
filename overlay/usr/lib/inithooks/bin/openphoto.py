#!/usr/bin/python
"""Set OpenPhoto owner password, email and domain to serve

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
    --domain=   unless provided, will ask interactively
                DEFAULT=www.example.com

"""

import os
import re
import sys
import getopt
import hashlib

from dialog_wrapper import Dialog
from mysqlconf import MySQL
from executil import system

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

DEFAULT_DOMAIN="www.example.com"

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email=', 'domain='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    domain = ""
    email = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val
        elif opt == '--domain':
            domain = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "OpenPhoto Password",
            "Enter new password for the OpenPhoto 'owner' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "OpenPhoto Email",
            "Enter email address for the OpenPhoto 'owner' account.",
            "admin@example.com")

    if not domain:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        domain = d.get_input(
            "OpenPhoto Domain",
            "Enter the domain to serve OpenPhoto.",
            DEFAULT_DOMAIN)

    if domain == "DEFAULT":
        domain = DEFAULT_DOMAIN

    # calculate hashed password with salt
    salt = ""
    DEFAULTINI = "/var/www/openphoto/src/configs/defaults.ini"
    for s in file(DEFAULTINI).readlines():
        s = s.strip()
        m = re.match("passwordSalt=\"(.*)\"", s)
        if m:
            salt = m.group(1)
            break

    if not salt:
        usage("could not determine salt: %s" % DEFAULTINI)

    hash = hashlib.sha1("-".join([password, salt])).hexdigest()

    # rename default site domain configuration
    CONFIGDIR = "/var/www/openphoto/src/userdata/configs"
    configs = os.listdir(CONFIGDIR)
    if len(configs) > 1:
        usage("multiple site configurations found: %s" % CONFIGDIR)

    config_old = os.path.join(CONFIGDIR, configs[0])
    config_new = os.path.join(CONFIGDIR, domain + ".ini")
    os.rename(config_old, config_new)

    # tweak configuration files
    system("sed -i \"s|fsHost=.*|fsHost=\\\"%s/photos\\\"|\" %s" % (domain, config_new))
    system("sed -i \"s|email=.*|email=\\\"%s\\\"|\" %s" % (email, config_new))
    system("sed -i \"s|from=.*|from=\\\"%s\\\"|\" %s" % (email, DEFAULTINI))

    # set email and hashed password
    m = MySQL()
    m.execute('UPDATE openphoto.user SET id=\"%s\" LIMIT 1;' % email)
    m.execute('UPDATE openphoto.user SET password=\"%s\" WHERE id=\"%s\";' % (hash, email))

if __name__ == "__main__":
    main()

