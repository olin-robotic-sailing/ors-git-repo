import serial

serial = serial.Serial(timeout = 2)
serial.port = "/dev/ttyUSB0"

def find_rate(ser):
	baudrates = [19200, 4800]
	for rate in baudrates:
		ser.baudrate = rate
		ser.open()
		ser.flush()
		print 'here'
		try:
			msg = ser.read(40)
		except:
			msg = ''
		print msg
		if len(msg) > 0:
			chars = msg.split(',')
			if len(chars)>3:
				#Given 40 bytes and longest message size, should still be
				#at least 3 commas
				print 'banana'
				print ser.readline()
				return rate
		ser.close()

def find_device():
	while True:
		baud = find_rate(serial)
		if baud == 4800:
			return 'airmar'
		elif baud == 19200:
			return 'hemisphere'

print find_device()