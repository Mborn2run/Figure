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

	def swim_init(self):
		# 12:30,11:0,15:150,14:180,7:30,6:180,4:150,3:0
		self.servo.UARTServo(12,30)
		self.servo.UARTServo(11,0)
		self.servo.UARTServo(15,150)
		self.servo.UARTServo(14,180)
		self.servo.UARTServo(7,30)
		self.servo.UARTServo(6,180)
		self.servo.UARTServo(4,150)
		self.servo.UARTServo(3,0)

	def swim(self,sleepingtime=5):
		#[11:0,14:180,6:180,3:0],[12:150,15:30,7:150,4:30],[11:180,14:0,6:0,3:180],[12:30,15:150,7:30,4:150]
		self.servo.UARTServo(11,0)
		self.servo.UARTServo(14,180)
		self.servo.UARTServo(6,180)
		self.servo.UARTServo(3,0)
		time.sleep(2)
		self.servo.UARTServo(12,150)
		self.servo.UARTServo(15,30)
		self.servo.UARTServo(7,150)
		self.servo.UARTServo(4,30)
		time.sleep(sleepingtime)
		self.servo.UARTServo(11,180)
		self.servo.UARTServo(14,0)
		self.servo.UARTServo(6,0)
		self.servo.UARTServo(3,180)
		time.sleep(2)
		self.servo.UARTServo(12,30)
		self.servo.UARTServo(15,150)
		self.servo.UARTServo(7,30)
		self.servo.UARTServo(4,150)
		time.sleep(sleepingtime)
		self.servo.UARTServo(11,0)
		self.servo.UARTServo(14,180)
		self.servo.UARTServo(6,180)
		self.servo.UARTServo(3,0)

                
	def swim_left(self,sleepingtime=1):
		# [14:180,3:180],[15:30,4:30],[14:0,3:0],[15:150,4:150]
		self.servo.UARTServo(14,180)
		self.servo.UARTServo(3,180)
		time.sleep(sleepingtime)
		self.servo.UARTServo(15,30)
		self.servo.UARTServo(4,30)
		time.sleep(sleepingtime)
		self.servo.UARTServo(14,0)
		self.servo.UARTServo(3,0)
		time.sleep(sleepingtime)
		self.servo.UARTServo(15,150)
		self.servo.UARTServo(4,150)
		

	def swim_right(self,sleepingtime=1):
		# [11:0,6:0],[12:150,7:150],[11:180,6:180],[12:30,7:30]
		self.servo.UARTServo(11,0)
		self.servo.UARTServo(6,0)
		time.sleep(sleepingtime)
		self.servo.UARTServo(12,150)
		self.servo.UARTServo(7,150)
		time.sleep(sleepingtime)
		self.servo.UARTServo(11,180)
		self.servo.UARTServo(6,180)
		time.sleep(sleepingtime)
		self.servo.UARTServo(12,30)
		self.servo.UARTServo(7,30)

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

	def crawl_20(self, sleeping_time = 1):
		# 11:60,14:60,[6:110,7:10],15:135,14:120,15:160,[14:100,6:80],14:120,11:120,3:60,12:50,11:60,12:20,[11:80,3:90],[14:100,7:30,6:90]
		self.servo.UARTServo(11,60)
		time.sleep(sleeping_time)
		self.servo.UARTServo(14,60)
		time.sleep(sleeping_time)
		self.servo.UARTServo(6,110)
		self.servo.UARTServo(7,10)
		time.sleep(sleeping_time)
		self.servo.UARTServo(15,135)
		time.sleep(sleeping_time)
		self.servo.UARTServo(14,120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(15,160)
		time.sleep(sleeping_time)
		self.servo.UARTServo(14,100)
		self.servo.UARTServo(6,80)
		time.sleep(sleeping_time)
		self.servo.UARTServo(14,120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(11,120)
		time.sleep(sleeping_time)
		self.servo.UARTServo(3,60)
		time.sleep(sleeping_time)
		self.servo.UARTServo(12,50)
		time.sleep(sleeping_time)
		self.servo.UARTServo(11,60)
		time.sleep(sleeping_time)
		self.servo.UARTServo(12,20)
		time.sleep(sleeping_time)
		self.servo.UARTServo(11,80)
		self.servo.UARTServo(3,90)
		time.sleep(sleeping_time)
		self.servo.UARTServo(14,100)
		self.servo.UARTServo(7,30)
		self.servo.UARTServo(6,90)


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

	def index_calibrate(self,index):
		return int(int(index)+2)
	