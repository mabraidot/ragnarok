from time import localtime, strftime
import time
import math
from collections import deque, namedtuple

class PIDAutoTune:
    def __init__(self, app, kettle, config):
        self.app = app
        self.kettle = kettle
        self.config = config
        self.running = False

        # Default: 100. Sets the output when stepping up/down.
        self.a_outstep = self.config.getint('OUTSTEP')
        # Default: 100. Sets the max power output.
        self.b_maxout = self.config.getint('MAXOUT')
        # Default: 30. How far back to look for min/max temps.
        self.c_lookback = self.config.getint('LOOKBACK')
    
    def stop(self):
        self.kettle.setHeater('false')

    def run(self):

        sampleTime = 5
        wait_time = 5
        outstep = float(self.a_outstep)
        outmax = float(self.b_maxout)
        lookbackSec = float(self.c_lookback)
        setpoint = self.kettle.getTemperatureSetPoint()
        try:
            atune = AutoTuner(setpoint, outstep, sampleTime, lookbackSec, 0, outmax)
        except Exception as e:
            # await self.app.ws.send('[PIDAUTOTUNE] Error: ' + e, self.config['LOG_ERROR_LABEL'])
            self.kettle.setLog({self.config['LOG_ERROR_LABEL']: '[PID] Autotune error: ' + e})

        # await self.app.ws.send('[PIDAUTOTUNE] Autotune process will now begin', self.config['LOG_NOTICE_LABEL'])
        self.kettle.setLog({self.config['LOG_NOTICE_LABEL']: '[PID] Autotune process will now begin'})
        self.running = True

        while not atune.run(self.kettle.getTemperature()):
            heat_percent = atune.output
            heating_time = sampleTime * heat_percent / 100
            wait_time = sampleTime - heating_time
            # @TODO: set the heater power as heat_percent
            
            # self.kettle.setLog({self.config['LOG_NOTICE_LABEL']: '[PID] Set Point: ' + str(setpoint)})
            # self.kettle.setLog({self.config['LOG_NOTICE_LABEL']: '[PID] Kettle Temperature: ' + str(self.kettle.getTemperature())})
            self.kettle.setLog({self.config['LOG_NOTICE_LABEL']: '[PID] Heat Percent: ' + str(heat_percent)})
            # self.kettle.setLog({self.config['LOG_NOTICE_LABEL']: '[PID] Heating Time: ' + str(heating_time)})
            # self.kettle.setLog({self.config['LOG_NOTICE_LABEL']: '[PID] Wait Time: ' + str(wait_time)})

            if heating_time == sampleTime:
                self.kettle.setHeater('true')
                self.kettle.getTemperature() # testing. DELETE
                # print('HEATER: ' ,self.kettle.getHeater())
                time.sleep(heating_time)
            elif wait_time == sampleTime:
                self.kettle.setHeater('false')
                self.kettle.getTemperature() # testing. DELETE
                # print('HEATER: ' ,self.kettle.getHeater())
                time.sleep(wait_time)
            else:
                self.kettle.setHeater('true')
                self.kettle.getTemperature() # testing. DELETE
                # print('HEATER: ' ,self.kettle.getHeater())
                time.sleep(heating_time)
                self.kettle.setHeater('false')
                self.kettle.getTemperature() # testing. DELETE
                # print('HEATER: ' ,self.kettle.getHeater())
                time.sleep(wait_time)
            

        self.stop()
        if atune.state == atune.STATE_SUCCEEDED:
            # await self.app.ws.send('[PIDAUTOTUNE] PID AutoTune was successful', self.config['LOG_NOTICE_LABEL'])
            self.kettle.setLog({self.config['LOG_NOTICE_LABEL']: '[PID] AutoTune was successful'})
            for rule in atune.tuningRules:
                params = atune.getPIDParameters(rule)
                atune.log('rule: {0}'.format(rule))
                atune.log('P: {0}'.format(params.Kp))
                atune.log('I: {0}'.format(params.Ki))
                atune.log('D: {0}'.format(params.Kd))
                atune.log('--------------------------------------------------------')
                if rule == "brewing":
                    # await self.app.ws.send('[PIDAUTOTUNE] AutoTune P Value ' + str(params.Kp), self.config['LOG_ERROR_LABEL'])
                    # await self.app.ws.send('[PIDAUTOTUNE] AutoTune I Value ' + str(params.Ki), self.config['LOG_ERROR_LABEL'])
                    # await self.app.ws.send('[PIDAUTOTUNE] AutoTune D Value ' + str(params.Kd), self.config['LOG_ERROR_LABEL'])
                    self.kettle.setLog({self.config['LOG_NOTICE_LABEL']: '[PID] AutoTune P Value: ' + str(params.Kp)})
                    self.kettle.setLog({self.config['LOG_NOTICE_LABEL']: '[PID] AutoTune I Value: ' + str(params.Ki)})
                    self.kettle.setLog({self.config['LOG_NOTICE_LABEL']: '[PID] AutoTune D Value: ' + str(params.Kd)})
        elif atune.state == atune.STATE_FAILED:
            # await self.app.ws.send('[PIDAUTOTUNE] PID AutoTune was successful', self.config['LOG_ERROR_LABEL'])
            self.kettle.setLog({self.config['LOG_ERROR_LABEL']: '[PIDAUTOTUNE] PID AutoTune was successful'})

        self.running = False



# Based on a fork of Arduino PID AutoTune Library
# See https://github.com/t0mpr1c3/Arduino-PID-AutoTune-Library
class AutoTuner(object):
    PIDParams = namedtuple('PIDParams', ['Kp', 'Ki', 'Kd'])

    PEAK_AMPLITUDE_TOLERANCE = 0.05
    STATE_OFF = 'off'
    STATE_RELAY_STEP_UP = 'relay step up'
    STATE_RELAY_STEP_DOWN = 'relay step down'
    STATE_SUCCEEDED = 'succeeded'
    STATE_FAILED = 'failed'

    _tuning_rules = {
        # rule: [Kp_divisor, Ki_divisor, Kd_divisor]
        "ziegler-nichols": [34, 40, 160],
        "tyreus-luyben": [44,  9, 126],
        "ciancone-marlin": [66, 88, 162],
        "pessen-integral": [28, 50, 133],
        "some-overshoot": [60, 40,  60],
        "no-overshoot": [100, 40,  60],
        "brewing": [2.5, 3, 3600]
    }

    def __init__(self, setpoint, outputstep=10, sampleTimeSec=5, lookbackSec=60,
                 outputMin=float('-inf'), outputMax=float('inf'), noiseband=0.5, getTimeMs=None):
        if setpoint is None:
            raise ValueError('Kettle setpoint must be specified')
        if outputstep < 1:
            raise ValueError('Output step % must be greater or equal to 1')
        if sampleTimeSec < 1:
            raise ValueError('Sample Time Seconds must be greater or equal to 1')
        if lookbackSec < sampleTimeSec:
            raise ValueError('Lookback Seconds must be greater or equal to Sample Time Seconds (5)')
        if outputMin >= outputMax:
            raise ValueError('Min Output % must be less than Max Output %')

        self._inputs = deque(maxlen=round(lookbackSec / sampleTimeSec))
        self._sampleTime = sampleTimeSec * 1000
        self._setpoint = setpoint
        self._outputstep = outputstep
        self._noiseband = noiseband
        self._outputMin = outputMin
        self._outputMax = outputMax

        self._state = AutoTuner.STATE_OFF
        self._peakTimestamps = deque(maxlen=5)
        self._peaks = deque(maxlen=5)

        self._output = 0
        self._lastRunTimestamp = 0
        self._peakType = 0
        self._peakCount = 0
        self._initialOutput = 0
        self._inducedAmplitude = 0
        self._Ku = 0
        self._Pu = 0

        if getTimeMs is None:
            self._getTimeMs = self._currentTimeMs
        else:
            self._getTimeMs = getTimeMs

    @property
    def state(self):
        return self._state

    @property
    def output(self):
        return self._output

    @property
    def tuningRules(self):
        return self._tuning_rules.keys()

    def getPIDParameters(self, tuningRule='ziegler-nichols'):
        divisors = self._tuning_rules[tuningRule]
        kp = self._Ku / divisors[0]
        ki = kp / (self._Pu / divisors[1])
        kd = kp * (self._Pu / divisors[2])
        return AutoTuner.PIDParams(kp, ki, kd)

    def log(self, text):
        filename = "./app/logs/autotune.log"
        formatted_time = strftime("%Y-%m-%d %H:%M:%S", localtime())

        with open(filename, "a") as file:
            file.write("%s,%s\n" % (formatted_time, text))
        
    def run(self, inputValue):
        now = self._getTimeMs()

        if (self._state == AutoTuner.STATE_OFF
                or self._state == AutoTuner.STATE_SUCCEEDED
                or self._state == AutoTuner.STATE_FAILED):
            self._initTuner(inputValue, now)
        elif (now - self._lastRunTimestamp) < self._sampleTime:
            return False

        self._lastRunTimestamp = now

        # check input and change relay state if necessary
        if (self._state == AutoTuner.STATE_RELAY_STEP_UP
                and inputValue > self._setpoint + self._noiseband):
            self._state = AutoTuner.STATE_RELAY_STEP_DOWN
            self.log('switched state: {0}'.format(self._state))
            self.log('input: {0}'.format(inputValue))
        elif (self._state == AutoTuner.STATE_RELAY_STEP_DOWN
                and inputValue < self._setpoint - self._noiseband):
            self._state = AutoTuner.STATE_RELAY_STEP_UP
            self.log('switched state: {0}'.format(self._state))
            self.log('input: {0}'.format(inputValue))

        # set output
        if (self._state == AutoTuner.STATE_RELAY_STEP_UP):
            self._output = self._initialOutput + self._outputstep
        elif self._state == AutoTuner.STATE_RELAY_STEP_DOWN:
            self._output = self._initialOutput - self._outputstep

        # respect output limits
        self._output = min(self._output, self._outputMax)
        self._output = max(self._output, self._outputMin)

        # identify peaks
        isMax = True
        isMin = True

        for val in self._inputs:
            isMax = isMax and (inputValue > val)
            isMin = isMin and (inputValue < val)

        self._inputs.append(inputValue)

        # we don't want to trust the maxes or mins until the input array is full
        if len(self._inputs) < self._inputs.maxlen:
            return False

        # increment peak count and record peak time for maxima and minima
        inflection = False

        # peak types:
        # -1: minimum
        # +1: maximum
        if isMax:
            if self._peakType == -1:
                inflection = True
            self._peakType = 1
        elif isMin:
            if self._peakType == 1:
                inflection = True
            self._peakType = -1

        # update peak times and values
        if inflection:
            self._peakCount += 1
            self._peaks.append(inputValue)
            self._peakTimestamps.append(now)
            self.log('found peak: {0}'.format(inputValue))
            self.log('peak count: {0}'.format(self._peakCount))

        # check for convergence of induced oscillation
        # convergence of amplitude assessed on last 4 peaks (1.5 cycles)
        self._inducedAmplitude = 0

        if inflection and (self._peakCount > 4):
            absMax = self._peaks[-2]
            absMin = self._peaks[-2]
            for i in range(0, len(self._peaks) - 2):
                self._inducedAmplitude += abs(self._peaks[i] - self._peaks[i+1])
                absMax = max(self._peaks[i], absMax)
                absMin = min(self._peaks[i], absMin)

            self._inducedAmplitude /= 6.0

            # check convergence criterion for amplitude of induced oscillation
            amplitudeDev = ((0.5 * (absMax - absMin) - self._inducedAmplitude)
                            / self._inducedAmplitude)

            self.log('amplitude: {0}'.format(self._inducedAmplitude))
            self.log('amplitude deviation: {0}'.format(amplitudeDev))

            if amplitudeDev < AutoTuner.PEAK_AMPLITUDE_TOLERANCE:
                self._state = AutoTuner.STATE_SUCCEEDED

        # if the autotune has not already converged
        # terminate after 10 cycles
        if self._peakCount >= 20:
            self._output = 0
            self._state = AutoTuner.STATE_FAILED
            return True

        if self._state == AutoTuner.STATE_SUCCEEDED:
            self._output = 0

            # calculate ultimate gain
            self._Ku = 4.0 * self._outputstep / (self._inducedAmplitude * math.pi)

            # calculate ultimate period in seconds
            period1 = self._peakTimestamps[3] - self._peakTimestamps[1]
            period2 = self._peakTimestamps[4] - self._peakTimestamps[2]
            self._Pu = 0.5 * (period1 + period2) / 1000.0
            return True

        return False

    def _currentTimeMs(self):
        return time.time() * 1000

    def _initTuner(self, inputValue, timestamp):
        self._peakType = 0
        self._peakCount = 0
        self._output = 0
        self._initialOutput = 0
        self._Ku = 0
        self._Pu = 0
        self._inputs.clear()
        self._peaks.clear()
        self._peakTimestamps.clear()
        self._peakTimestamps.append(timestamp)
        self._state = AutoTuner.STATE_RELAY_STEP_UP
