from enum import Enum
from TimeUnit import TimeUnit

class ClockType(Enum):
    NOTDEFINED = "NotDefined"
    TIME = "Time"
    TRIGGER = "Trigger"

class VariabilityType(Enum):
    NOTDEFINED = "NotDefined"
    CONSTANT = "Constant"
    FIXED = "Fixed"
    TUNABLE = "Tunable"
    CHANGING = "Changing"
    COUNTDOWN = "Countdown"

class TimeBasedClockType(Enum):
    NOTDEFINED = "NotDefined"
    PERIODIC = "Periodic"
    APERIODIC = "Aperiodic"

class Clock:
    def __init__(self, name, time_unit = TimeUnit.S, start_time = -1, end_time = -1):
        if(start_time > end_time):
            raise Exception("End time cannot be greater than start time")
        
        self.__name = name
        self.__clock_type = ClockType.NOTDEFINED
        self.__variability_type = VariabilityType.NOTDEFINED
        self.__time_based_clock_type = TimeBasedClockType.NOTDEFINED
        self.__raster = -1
        self.__timeunit = time_unit
        self.__color = '#F5F5F5;line:black'
        self.__execution_intervals = []
        self.__start_time = start_time
        self.__end_time = end_time
        self.__offset = 0

    def get_name(self):
        return self.__name
    
    def get_name_without_spaces(self):
        return self.__name.replace(" ", "_")
    
    def get_time_unit(self):
        return self.__timeunit
    
    def set_time_unit(self, timeunit):
        self.__timeunit = timeunit

    def set_raster(self, raster):
        self.__raster = raster

    def get_raster(self):
        return self.__raster
    
    def get_offset(self):
        return self.__offset
    
    def get_end_time(self):
        return self.__end_time
    
    def add_execution_intervals(self, intervals):
        self.__execution_intervals.extend(intervals)

    def get_execution_intervals(self):
        return self.__execution_intervals
        
    def is_active_in_time(self, time):
        if self.__start_time == -1 and self.__end_time == -1:
            return True
        
        if self.__end_time == -1:
            return self.__start_time <= time
        
        return self.__start_time <= time < self.__end_time
    
    def configure_constant_clock(self, raster, offset = -1):
        self.__clock_type = ClockType.TIME
        self.__variability_type = TimeBasedClockType.PERIODIC
        self.__variability_type = VariabilityType.CONSTANT
        self.__raster = raster
        if offset != -1:
            self.__offset = offset
            self.__start_time = offset

    def configure_fixed_clock(self, raster, offset = -1):
        self.__clock_type = ClockType.TIME
        self.__variability_type = TimeBasedClockType.PERIODIC
        self.__variability_type = VariabilityType.FIXED 
        self.__raster = raster
        if offset != -1:
            self.__offset = offset
            self.__start_time = offset

    def configure_tunable_clock(self, raster):
        self.__clock_type = ClockType.TIME
        self.__variability_type = TimeBasedClockType.PERIODIC
        self.__variability_type = VariabilityType.TUNABLE  
        self.__raster = raster

    def configure_changing_clock(self):
        self.__clock_type = ClockType.TIME
        self.__variability_type = TimeBasedClockType.APERIODIC
        self.__variability_type = VariabilityType.CHANGING

    def configure_countdown_clock(self):
        self.__clock_type = ClockType.TIME
        self.__variability_type = TimeBasedClockType.APERIODIC
        self.__variability_type = VariabilityType.COUNTDOWN

    def configure_trigger_clock(self):
        self.__clock_type = ClockType.TRIGGER

    def isTimeBased(self):
        return self.__clock_type == ClockType.TIME
    
    def get_color(self):
        return self.__color
