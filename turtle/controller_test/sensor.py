import ms5837
import time

'''
一个print的死循环，读取深度值，需要单独开一个线程读取。
'''
class ReadSensor():
    def __init__(self) -> None:
        self.sensor = ms5837.MS5837_30BA()
        

    def readSensor(self):
        if not self.sensor.init():
            print("Sensor could not be initialized")
            exit(1)

        # We have to read values from sensor to update pressure and temperature
        if not self.sensor.read():
            print("Sensor read failed!")
            exit(1)
        print("Temperature: %.2f C  %.2f F  %.2f K") % (
        self.sensor.temperature(ms5837.UNITS_Centigrade),
        self.sensor.temperature(ms5837.UNITS_Farenheit),
        self.sensor.temperature(ms5837.UNITS_Kelvin))

        freshwaterDepth = self.sensor.depth() # default is freshwater
        self.sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
        saltwaterDepth = self.sensor.depth() # No nead to read() again
        self.sensor.setFluidDensity(1000) # kg/m^3
        print("Depth: %.3f m (freshwater)  %.3f m (saltwater)") % (freshwaterDepth, saltwaterDepth)

        # fluidDensity doesn't matter for altitude() (always MSL air density)
        print("MSL Relative Altitude: %.2f m") % self.sensor.altitude() # relative to Mean Sea Level pressure in air

        correct_value = self.sensor.depth()
        time.sleep(5)
        while True:
            if self.sensor.read():
                print("D: %0.3f m\tP: %0.1f mbar  %0.3f psi\tT: %0.2f C  %0.2f F") % (
                self.sensor.depth() - correct_value,
                self.sensor.pressure(), # Default is mbar (no arguments)
                self.sensor.pressure(ms5837.UNITS_psi), # Request psi
                self.sensor.temperature(), # Default is degrees C (no arguments)
                self.sensor.temperature(ms5837.UNITS_Farenheit)) # Request Farenheit
                time.sleep(2)
            else:
                print("Sensor read failed!")
                exit(1)