import RPi.GPIO as GPIO
import time
from getkey import getkey, keys

# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()


# Define the pins for motor control
front_in1 = 11
front_in2 = 12
front_en1 = 13

rear_in1 = 15
rear_in2 = 16
rear_en2 = 18

# Set GPIO pins as output
GPIO.setup(front_in1, GPIO.OUT)
GPIO.setup(front_in2, GPIO.OUT)
GPIO.setup(front_en1, GPIO.OUT)

GPIO.setup(rear_in1, GPIO.OUT)
GPIO.setup(rear_in2, GPIO.OUT)
GPIO.setup(rear_en2, GPIO.OUT)

# Set the PWM pins for motor speed control
front_pwm = GPIO.PWM(front_en1, 100)
rear_pwm  = GPIO.PWM(rear_en2, 100)

# Start the PWM
front_pwm.start(0)
rear_pwm.start(0)


def set_motor_speed(motor, speed):
	rotation = abs(speed)

	if speed > 0:
		GPIO.output(motor["in1_pin"], GPIO.HIGH)
		GPIO.output(motor["in2_pin"], GPIO.LOW)
	if speed < 0:
                GPIO.output(motor["in1_pin"], GPIO.LOW)
                GPIO.output(motor["in2_pin"], GPIO.HIGH)


	motor["pwm"].ChangeDutyCycle(rotation)


def drive(direction, speed):
	set_motor_speed({"in1_pin": front_in1, "in2_pin": front_in2, "pwm": front_pwm}, direction)
	set_motor_speed({"in1_pin": rear_in1, "in2_pin": rear_in2, "pwm": rear_pwm}, speed)


# Run the motors forward and backwards
try:
	speed = 0
	direction = 0
	while True:
		key = getkey()

		if key == keys.UP:
			print("Forward")
			if speed == 0:
				drive(direction, 100)
				speed = 60

			if speed  == 100:
				print("Already moving forward")
			else:
				speed = speed + 10

		if key == keys.DOWN:
			print("Reverse")
			if speed == 0:
					drive(direction, -100)
					speed = -60 

			if speed == -100:
				print("Already moving backwards")
			else:
				speed = speed - 10

		if key == keys.LEFT:
                        if direction == -100:
                                print("Already turning left")
                        else:
                                direction = direction - 100

		if key == keys.RIGHT:
			if direction == 100:
				print("Already turning right")
			else:
				direction = direction + 100

		else:
			print("Other key")
			#speed = 0
			#direction = 0

		# Drive the vehicle
		drive(direction, speed)
		#time.sleep(1)

		print("direction " + str(direction))


except KeyboardInterrupt:
	front_pwm.stop()
	rear_pwm.stop()
	GPIO.cleanup()
