#!/usr/bin/python3

# Import section

import numpy as np
import pexpect
import re

# Var section

IP_WAPs = 'data/ip_list.txt'
login = 'admin'
password = ['password','Wepp@ssword']
command = 'wl -i wlan1 probsup_dump'
MAC_addr = 'f4:f5:db:2d:b5:16'
raw_files = ['data/info_WAP-1.txt','data/info_WAP-2.txt','data/info_WAP-3.txt']
RSSI = [None, None, None]
RSSI_file = 'data/RSSI_info.txt'

# Func section

def readfile(filename):	# Func for reading 1 file
	with open(filename) as f:
		return f.readlines()

def readfiles(filelist):	# Func for reading list of files
	buffer = [None, None, None, None]
	for index in range(len(filelist)):
		with open(filelist[index]) as f:
			buffer[index] = f.readlines()
	return buffer

def writefile(data, filename):	# Func for writing data in file
	with open(filename, 'w+') as f:
		for index in range(len(data)):
			if data[index] is not None:
				f.write(data[index] + '\n')

def try_to_extract(IP_list, login, password, command):
	IP_addr = readfile(IP_WAPs)
	for i in range(len(IP_addr)):
		stream = pexpect.spawn('telnet ' + IP_addr[i])	# Connection attempt to WAP via telnet

		stream.expect('ogin:')	# Expecting Login/login string as an answer
		stream.sendline(login)	# Sending login on this WAP

		stream.expect('assword:')	# Expecting Password/password string as an answer
		if i == 0:
			stream.sendline(password[0])	# Sending password for specified login
		else:
			stream.sendline(password[1])	# Sending password for specified login

		stream.expect('#')	# Expecting prompt string after successfull loging
		stream.sendline(command)	#  Attempt to extract needed info 'bout connected users
		stream.expect('#')	# Waiting for prompt string

		stream.before	# Moving all previous info into cache var

		_file = open(raw_files[i], 'wb+')
		_file.write(stream.before)
		_file.close()
		stream.close()



def convert_to_dist(signals):
	buffer = [None, None, None]
	for index in range(len(signals)):
		if signals[index] is not None:
			buffer[index] = 10**((27.55 - int(signals[index])) / 20.0)
	return buffer


# Code section

try_to_extract(IP_WAPs, login, password, command)

print('Please, enter MAC-address of user:')	# Receiving needed MAC-address of user we want to locate in future
#MAC_addr = input()
is_correct = re.match(r'[0-9a-fA-F]{2}(?:[:-][0-9a-fA-F]{2}){5}', MAC_addr)	# Checking correction of input address via regular expressions
try:
	print(is_correct.group(0))
except AttributeError:
	print('[ERROR]\tMAC-address you entered is incorrect!')
	exit(1)

MAC_addr = MAC_addr + ','	# The first (but not the last) crutch :(

cache = readfiles(raw_files)	# Reading whole file string-by-string
for index in range(len(cache)):
	for line in cache[index]:	# For-loop for searching unknow RSSI of known MAC-address
		tokens = line.split()
		if MAC_addr not in tokens:
			continue
		i = tokens.index(MAC_addr)
		RSSI[index] = tokens[i + 6]
		RSSI[index] = RSSI[index].replace(',', '')	# The second crutch, which helps to format RSS value correctly
		print('WAP-', index + 1,'\tRSSI: ' + RSSI[index])	# If it printed, congratulations :3

writefile(RSSI, RSSI_file)

cnt = 0
for index in range(len(RSSI)):
	if RSSI[index] is not None:
		cnt = cnt + 1
if cnt < 3:
	print('[ERROR]\tNot enough data for tracking!')
#	exit(1)

dist = convert_to_dist(RSSI)
print(dist)
