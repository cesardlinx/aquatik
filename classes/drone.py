import RPi.GPIO as GPIO


class Drone:
    class __Drone:
        def __init__(self):
            """Inicialización de pines GPIO para control de motor y de bomba"""
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            self.motor_A1 = 29  # color tomate y verde
            self.motor_A2 = 31
            self.motor_B1 = 33  # azul morado
            self.motor_B2 = 35
            self.motor_bomba_1 = 21
            self.motor_bomba_2 = 23
            self.trig = 11
            self.echo = 13
            GPIO.setup(self.motor_A1, GPIO.OUT)
            GPIO.setup(self.motor_B1, GPIO.OUT)
            GPIO.setup(self.motor_A2, GPIO.OUT)
            GPIO.setup(self.motor_B2, GPIO.OUT)
            GPIO.setup(self.motor_bomba_1, GPIO.OUT)
            GPIO.setup(self.motor_bomba_2, GPIO.OUT)
            GPIO.setup(self.trig, GPIO.OUT)
            GPIO.setup(self.echo, GPIO.IN)

        def up(self):
            """Método para que el dron avance recto"""
            print('up')
            GPIO.output(self.motor_A1, GPIO.HIGH)
            GPIO.output(self.motor_A2, GPIO.LOW)
            GPIO.output(self.motor_B1, GPIO.LOW)
            GPIO.output(self.motor_B2, GPIO.HIGH)

        def down(self):
            """Método para retroceder"""
            print('down')
            GPIO.output(self.motor_A1, GPIO.LOW)
            GPIO.output(self.motor_A2, GPIO.HIGH)
            GPIO.output(self.motor_B1, GPIO.HIGH)
            GPIO.output(self.motor_B2, GPIO.LOW)

        def left(self):
            """Método para que el dron gire a la izquierda"""
            print('left')
            GPIO.output(self.motor_A1, GPIO.HIGH)
            GPIO.output(self.motor_A2, GPIO.LOW)
            GPIO.output(self.motor_B1, GPIO.HIGH)
            GPIO.output(self.motor_B2, GPIO.LOW)

        def right(self):
            """Método para que el dron gire a la derecha"""
            print('right')
            GPIO.output(self.motor_A1, GPIO.LOW)
            GPIO.output(self.motor_A2, GPIO.HIGH)
            GPIO.output(self.motor_B1, GPIO.LOW)
            GPIO.output(self.motor_B2, GPIO.HIGH)

        def stop(self):
            """Método para parar el dron"""
            print('stop')
            GPIO.output(self.motor_A1, GPIO.LOW)
            GPIO.output(self.motor_A2, GPIO.LOW)
            GPIO.output(self.motor_B1, GPIO.LOW)
            GPIO.output(self.motor_B2, GPIO.LOW)

        def encender_bomba(self):
            """Método para encender la bomba de succión"""
            print('bomba encendida')
            self.bomba = 'on'

        def apagar_bomba(self):
            """Método para apagar la bomba de succión"""
            print('bomba apagada')
            self.bomba = 'off'

        @property
        def bomba(self):
            if GPIO.input(self.motor_bomba_1):
                return True
            return False

        @bomba.setter
        def bomba(self, action):
            if action == 'on':
                GPIO.output(self.motor_bomba_1, GPIO.HIGH)
            elif action == 'off':
                GPIO.output(self.motor_bomba_1, GPIO.LOW)

    instance = None

    def __init__(self):
        if not Drone.instance:
            Drone.instance = Drone.__Drone()
        else:
            pass

    def __getattr__(self, name):
        return getattr(self.instance, name)
