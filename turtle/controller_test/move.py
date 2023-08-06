import time
from servo import Servo

'''
1(外)2(内)   左前鳍
4(外)5(内)   右前鳍
9(外)10(内)  左后鳍
12(外)13(内) 右后鳍
'''
class Motion():
	def __init__(self):
		self.servo = Servo()
			
	def servoReset(self,sleepingtime=0.5):
		self.servo.UARTServo(2,0)
		self.servo.UARTServo(5,0)
		self.servo.UARTServo(10,0)
		self.servo.UARTServo(13,0)
		time.sleep(sleepingtime)
		self.servo.UARTServo(1,0)
		self.servo.UARTServo(4,0)
		self.servo.UARTServo(9,0)
		self.servo.UARTServo(12,0)
		time.sleep(sleepingtime)

	def userDefined(self,str):
		groups = str.split(',')
		for group in groups:
			key, value = group.split(':')
			if int(key)==99:
				time.sleep(int(value))
			else:
				self.servo.UARTServo(int(key),int(value))

	def move(self,sleepingtime=2):
		self.servoReset(sleepingtime)
		self.servoServo.UARTServo(2,180)
		self.servoServo.UARTServo(5,180)
		self.servoServo.UARTServo(10,180)
		self.servoServo.UARTServo(13,180)
		time.sleep(sleepingtime)
		self.servoServo.UARTServo(1,180)
		self.servoServo.UARTServo(4,180)
		self.servoServo.UARTServo(9,180)
		self.servoServo.UARTServo(12,180)
		time.sleep(sleepingtime)
		self.servoReset(sleepingtime)
                
	def turnLeft(self,sleepingtime=2):
		self.servoReset(sleepingtime)
		self.servoServo.UARTServo(5,180)
		self.servoServo.UARTServo(13,180)
		time.sleep(sleepingtime)
		self.servoServo.UARTServo(4,180)
		self.servoServo.UARTServo(12,180)
		self.servoReset(sleepingtime)
		...

	def turnRight(self,sleepingtime=2):
		self.servoReset(sleepingtime)
		self.servoServo.UARTServo(2,180)
		self.servoServo.UARTServo(10,180)
		time.sleep(sleepingtime)
		self.servoServo.UARTServo(1,180)
		self.servoServo.UARTServo(9,180)
		time.sleep(sleepingtime)
		self.servoReset(sleepingtime)
		...

	def crawl_init(self):
		# 9:80,10:20,12:100,13:160,1:90,2:150,4:90,5:30
		self.servo.UARTServo(self.index_calibrate(9),80)
		self.servo.UARTServo(self.index_calibrate(10),20)
		self.servo.UARTServo(self.index_calibrate(12),100)
		self.servo.UARTServo(self.index_calibrate(13),160)
		self.servo.UARTServo(self.index_calibrate(1),90)
		self.servo.UARTServo(self.index_calibrate(2),150)
		self.servo.UARTServo(self.index_calibrate(4),90)
		self.servo.UARTServo(self.index_calibrate(5),30)

	def crawl(self, sleeping_time = 1):
		# 9:60,12:70,4:120,13:120,12:120,13:160,[12:100,4:90],9:80,2:140,12:120,9:120,1:60,10:50,9:60,10:20,[9:80,1:90],[12:100,2:150]
		self.servo.UARTServo(self.index_calibrate(9),60)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(12),70)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(4),120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(13),120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(12),120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(13),160)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(12),100)
		self.servo.UARTServo(self.index_calibrate(4),90)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(9),80)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(2),140)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(12),120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(9),120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(1),60)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(10),50)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(9),60)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(10),20)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(9),80)
		self.servo.UARTServo(self.index_calibrate(1),90)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(12),100)
		self.servo.UARTServo(self.index_calibrate(2),150)

	def crawl_left(self, sleeping_time = 1):
		# 9:50,12:50,4:120,13:120,12:120,13:160,[12:100,4:90]
		self.servo.UARTServo(self.index_calibrate(9),50)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(12),50)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(4),120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(13),120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(12),120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(13),160)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(12),100)
		self.servo.UARTServo(self.index_calibrate(4),90)

	def crawl_right(self, sleeping_time = 1):
		# 2:140,12:120,9:130,1:60,10:50,9:60,10:20,[9:80,1:90]
		self.servo.UARTServo(self.index_calibrate(2),140)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(12),120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(9),130)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(1),60)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(10),50)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(9),60)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(10),20)
		time.sleep(sleeping_time)
		self.servo.UARTServo(self.index_calibrate(9),80)
		self.servo.UARTServo(self.index_calibrate(1),90)

	#360
	def comeUp():
		...

	def comeDown():
		...

	def wifi(self, op_time, direction):
		if direction == 0:
			self.servo.UARTServo(16,95) #顺时针
		else:
			self.servo.UARTServo(16,75) #逆时针
		time.sleep(op_time)
		self.servo.UARTServo(16,85) #stop

	def index_calibrate(index):
		return int(int(index)+2)
