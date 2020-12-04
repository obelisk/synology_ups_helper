#!/usr/bin/env python3

import socket

HOST = 'XXX.XXX.XXX.XXX'  # The server's hostname or IP address
PORT = 3493        # The port used by the server

def recvdata(sock):
  data = bytearray()
  newlines = 0
  while newlines < 4:
    char = sock.recv(1)
    if char[0] == 0x0A:
      newlines += 1
    data.extend(char)
  return data

def parsedata(rawdata):
    strdata = rawdata.decode("ascii")
    lines = strdata.split("\n")
    assert(len(lines) == 5)
    lines = lines[:4]
    parsedlines = []
    for line in lines:
      parts = line.split()
      parsedLine = parts[2] + "=" + parts[3][1:-1]
      parsedlines.append(parsedLine)
    return parsedlines


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))
  s.settimeout(2)
  s.sendall(b'GET VAR ups battery.charge\nGET VAR ups input.voltage\nGET VAR ups battery.runtime\nGET VAR ups ups.load\nLOGOUT')

  data = parsedata(recvdata(s))
  print("house_ups " + ','.join(data))
