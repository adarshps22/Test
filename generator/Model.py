from enum import Enum
import hashlib
import copy
from Clock import ClockType, VariabilityType, TimeBasedClockType, Clock
from TimeUnit import TimeUnit

class Clock:
    def __init__(self, time, timeunit):
        self.time = time
        self.timeunit = timeunit

class Model:
    __COLORS = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF']

    def __init__(self, model_name):
        self.__model_name = model_name  
        self.__color = self.__assign_color(self.__model_name)
        self.__raster = -1
        self.__timeunit = TimeUnit.S
        self.__execution_intervals = []
        self.__local_execution_intervals = []
        self.__Clocks = set()

        self.__local_hcf_time = -1
        self.__local_lcm_time = -1
        self.__local_time_unit = TimeUnit.S

    def __assign_color(self, model_name):
        hash_value = int(hashlib.sha256(model_name.encode()).hexdigest(), 16)
        index = hash_value % len(self.__COLORS)
        return self.__COLORS[index]   

    def add_execution_intervals(self, intervals):
        self.__execution_intervals.extend(intervals)

    def get_execution_intervals(self):
        return self.__execution_intervals
    
    def add_local_execution_intervals(self, intervals):
        self.__local_execution_intervals.extend(intervals)

    def get_local_execution_intervals(self):
        return self.__local_execution_intervals
    
    def get_model_name(self):
        return self.__model_name
    
    def get_name_without_spaces(self):
        return self.__model_name.replace(" ", "_")
    
    def get_color(self):
        return self.__color
    
    def add_clock(self, clock):
        self.__Clocks.add(copy.deepcopy(clock))

    def remove_clock(self, clock):
        self.__Clocks.remove(clock)

    def get_clocks(self, time):
        clocks = []
        for clock in self.__Clocks:
            if clock.is_active_in_time(time):
                clocks.append(clock)
        return clocks
    
    def get_end_time_clocks(self, time):
        clocks = []
        for clock in self.__Clocks:
            if clock.get_end_time() == time:
                clocks.append(clock)
        return clocks
    
    def get_all_clocks(self):
        return self.__Clocks
    
    def get_raster(self):
        return self.__raster
    
    def set_raster(self, raster):
        self.__raster = raster

    def get_time_unit(self):
        return self.__timeunit
    
    def set_time_unit(self, timeunit):
        self.__timeunit = timeunit

    def get_local_hcf_time(self):
        return self.__local_hcf_time
    
    def get_local_lcm_time(self):
        return self.__local_lcm_time
    
    def set_local_hcf_time(self, time):
        self.__local_hcf_time = time

    def set_local_lcm_time(self, time):
        self.__local_lcm_time = time
