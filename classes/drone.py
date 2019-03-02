import RPi.GPIO as GPIO


class Drone:
    """
    La clase drone es un Singleton debido a que solo
    puede haber un dron
    """
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
            GPIO.output(self.motor_A1, GPIO.HIGH)
            GPIO.output(self.motor_A2, GPIO.LOW)
            GPIO.output(self.motor_B1, GPIO.LOW)
            GPIO.output(self.motor_B2, GPIO.HIGH)

        def down(self):
            """Método para retroceder"""
            GPIO.output(self.motor_A1, GPIO.LOW)
            GPIO.output(self.motor_A2, GPIO.HIGH)
            GPIO.output(self.motor_B1, GPIO.HIGH)
            GPIO.output(self.motor_B2, GPIO.LOW)

        def left(self):
            """Método para que el dron gire a la izquierda"""
            GPIO.output(self.motor_A1, GPIO.LOW)
            GPIO.output(self.motor_A2, GPIO.HIGH)
            GPIO.output(self.motor_B1, GPIO.LOW)
            GPIO.output(self.motor_B2, GPIO.HIGH)

        def right(self):
            """Método para que el dron gire a la derecha"""
            GPIO.output(self.motor_A1, GPIO.HIGH)
            GPIO.output(self.motor_A2, GPIO.LOW)
            GPIO.output(self.motor_B1, GPIO.HIGH)
            GPIO.output(self.motor_B2, GPIO.LOW)

        def stop(self):
            """Método para parar el dron"""
            GPIO.output(self.motor_A1, GPIO.LOW)
            GPIO.output(self.motor_A2, GPIO.LOW)
            GPIO.output(self.motor_B1, GPIO.LOW)
            GPIO.output(self.motor_B2, GPIO.LOW)

        def encender_bomba(self):
            """Método para encender la bomba de succión"""
            self.bomba = 'on'

        def apagar_bomba(self):
            """Método para apagar la bomba de succión"""
            self.bomba = 'off'

        @property
        def is_moving(self):
            """Método para conocer si el dron se está moviendo"""
            if GPIO.input(self.motor_A1) or GPIO.input(self.motor_A2) or \
                    GPIO.input(self.motor_B1) or GPIO.input(self.motor_B2):
                return True
            return False

        @property
        def bomba(self):
            """Estado de la bomba"""
            if GPIO.input(self.motor_bomba_1):
                return True
            return False

        @bomba.setter
        def bomba(self, action):
            """Seteo del estado de la bomba"""
            if action == 'on':
                GPIO.output(self.motor_bomba_1, GPIO.HIGH)
            elif action == 'off':
                GPIO.output(self.motor_bomba_1, GPIO.LOW)

    instance = None

    def __init__(self):
        """Crea la instancia solo si no existe"""
        if not Drone.instance:
            Drone.instance = Drone.__Drone()
        else:
            pass

    def __getattr__(self, name):
        return getattr(self.instance, name)
