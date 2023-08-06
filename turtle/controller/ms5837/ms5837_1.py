try:
    import smbus
except ImportError:
    print('Try sudo apt-get install python3-smbus')

from time import sleep

# Models
MODEL_02BA = 0
MODEL_30BA = 1

# Oversampling options
OSR_256  = 0
OSR_512  = 1
OSR_1024 = 2
OSR_2048 = 3
OSR_4096 = 4
OSR_8192 = 5

# kg/m^3 convenience
DENSITY_FRESHWATER = 997
DENSITY_SALTWATER = 1029

# Conversion factors (from native unit, mbar)
UNITS_Pa     = 100.0
UNITS_hPa    = 1.0
UNITS_kPa    = 0.1
UNITS_mbar   = 1.0
UNITS_bar    = 0.001
UNITS_atm    = 0.000986923
UNITS_Torr   = 0.750062
UNITS_psi    = 0.014503773773022

# Valid units
UNITS_Centigrade = 1
UNITS_Fahrenheit  = 2
UNITS_Kelvin     = 3

class MS5837(object):

    # Registers
    _MS5837_ADDR             = 0x76
    _MS5837_RESET            = 0x1E
    _MS5837_ADC_READ         = 0x00
    _MS5837_PROM_READ        = 0xA0
    _MS5837_CONVERT_D1_256   = 0x40
    _MS5837_CONVERT_D2_256   = 0x50

    def __init__(self, model=MODEL_30BA, bus=1):
        self._model = model

        try:
            self._bus = smbus.SMBus(bus)
        except FileNotFoundError:
            print("Bus %d is not available." % bus)
            print("Available buses are listed as /dev/i2c*")
            self._bus = None

        self._fluidDensity = DENSITY_FRESHWATER
        self._pressure = 0
        self._temperature = 0
        self._D1 = 0
        self._D2 = 0

    def init(self):
        if self._bus is None:
            print("No bus!")
            return False

        self._bus.write_byte(self._MS5837_ADDR, self._MS5837_RESET)

        # Wait for reset to complete
        sleep(0.01)

        self._C = []

        # Read calibration values and CRC
        for i in range(7):
            c = self._bus.read_word_data(self._MS5837_ADDR, self._MS5837_PROM_READ + 2*i)
            c = ((c & 0xFF) << 8) | (c >> 8) # SMBus is little-endian for word transfers, we need to swap MSB and LSB
            self._C.append(c)

        crc = (self._C[0] & 0xF000) >> 12
        if crc != self._crc4(self._C):
            print("PROM read error, CRC failed!")
            return False

        return True

    def read(self, oversampling=OSR_8192):
        if self._bus is None:
            print("No bus!")
            return False

        if oversampling < OSR_256 or oversampling > OSR_8192:
            print("Invalid oversampling option!")
            return False

        # Request D1 conversion (temperature)
        self._bus.write_byte(self._MS5837_ADDR, self._MS5837_CONVERT_D1_256 + 2*oversampling)

        # Wait for conversion to complete
        if oversampling == OSR_256:
            sleep(0.001)
        elif oversampling == OSR_512:
            sleep(0.003)
        elif oversampling == OSR_1024:
            sleep(0.004)
        elif oversampling == OSR_2048:
            sleep(0.006)
        elif oversampling == OSR_4096:
            sleep(0.010)
        else:
            sleep(0.020)

        self._D1 = self._bus.read_i2c_block_data(self._MS5837_ADDR, self._MS5837_ADC_READ, 3)

        # Request D2 conversion (pressure)
        self._bus.write_byte(self._MS5837_ADDR, self._MS5837_CONVERT_D2_256 + 2*oversampling)

        # Wait for conversion to complete
        if oversampling == OSR_256:
            sleep(0.001)
        elif oversampling == OSR_512:
            sleep(0.003)
        elif oversampling == OSR_1024:
            sleep(0.004)
        elif oversampling == OSR_2048:
            sleep(0.006)
        elif oversampling == OSR_4096:
            sleep(0.010)
        else:
            sleep(0.020)

        self._D2 = self._bus.read_i2c_block_data(self._MS5837_ADDR, self._MS5837_ADC_READ, 3)

        self._calculate()

        return True

    def setFluidDensity(self, density):
        self._fluidDensity = density

    def pressure(self):
        return self._pressure

    def temperature(self):
        return self._temperature

    def depth(self):
        return self._pressure/(self._fluidDensity*9.80665)

    def altitude(self, p0=1013.25):
        return (1-pow(self._pressure/p0, 0.190284))*145366.45*0.3048

    def _calculate(self):
        # Temperature offset calculations
        dT = self._D2[0]*256 + self._D2[1] - (self._C[4]*16)
        self._temperature = 2000 + dT*self._C[5]/8388608

        # Second order temperature compensation
        if self._model == MODEL_30BA:
            if self._temperature < 2000:
                T2 = 3*(dT**2)/(2**33)
                off2 = 3*((self._temperature-2000)**2)/2
                sens2 = 5*((self._temperature-2000)**2)/(2**3)
                if self._temperature < -1500:
                    off2 = off2 + 7*((self._temperature+1500)**2)
                    sens2 = sens2 + 4*((self._temperature+1500)**2)
        else:
            if self._temperature < 2000:
                T2 = 2*(dT**2)/(2**37)
                off2 = 1*((self._temperature-2000)**2)/(2**4)
                sens2 = 0
                if self._temperature < -1500:
                    off2 = off2 + 6*((self._temperature+1500)**2)
                    sens2 = sens2 + 4*((self._temperature+1500)**2)

        self._temperature = self._temperature - T2
        self._pressure = ((self._D1[0]*256 + self._D1[1])*self._C[1]/(2**21) - self._C[0])/((2**15) - 1)
        self._pressure = self._pressure - off2
        self._pressure = self._pressure*0.1 + sens2
        self._pressure = self._pressure/100

    def _crc4(self, n_prom):
        n_rem = 0

        n_prom[0] = ((n_prom[0]) & 0x0FFF)
        n_prom.append(0)

        for i in range(16):
            if i%2 == 1:
                n_rem ^= ((n_prom[i>>1]) & 0x00FF)
            else:
                n_rem ^= (n_prom[i>>1] >> 8)

            for n_bit in range(8, 0, -1):
                if n_rem & 0x8000:
                    n_rem = (n_rem << 1) ^ 0x3000
                else:
                    n_rem = (n_rem << 1)

        n_rem = ((n_rem >> 12) & 0x000F)

        return n_rem
    
class MS5837_30BA(MS5837):
    def __init__(self, bus=1):
        MS5837.__init__(self, MODEL_30BA, bus)
        
class MS5837_02BA(MS5837):
    def __init__(self, bus=1):
        MS5837.__init__(self, MODEL_02BA, bus)