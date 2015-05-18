import motor

motor_client = motor.MotorClient('localhost', 27017)
vote_db = motor_client.vote_db
