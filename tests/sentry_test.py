# _*_coding: utf-8_*_

from raven import Client

dsn = "http://73531a04ebc4423ebb4b927e1cf479b5:0b52d4e5f75d45e48cec2cacd43ef10d@112.74.176.52:9000/5"
client = Client(dsn)

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()
