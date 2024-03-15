from Model import Model
from TaskMap import Task
import math

from TimeUnit import TimeUnit

class Utility:

    @staticmethod
    def normalize_system_time(tasks):
        lowest = TimeUnit.S

        # Find the lowest time unit in tasks
        for task in tasks:
            if task.timeunit.value > lowest.value:
                lowest = TimeUnit(task.timeunit)

        # Find the lowest time unit in clocks of models
        for model in Utility.get_models(tasks):
            for clock in model.get_all_clocks() :
                if clock.isTimeBased() and clock.get_time_unit().value > lowest.value:
                    lowest = TimeUnit(clock.get_time_unit())

        # Normalize all tasks to the lowest time unit
        for task in tasks:
            task.raster = int(task.raster * (lowest.value / task.timeunit.value))
            task.timeunit = lowest 

        # Normalize all clocks of models to the lowest time unit
        for model in Utility.get_models(tasks):
            for clock in model.get_all_clocks() :
                if clock.isTimeBased():
                    clock.set_raster(int(clock.get_raster() * (lowest.value / clock.get_time_unit().value)))
                    clock.set_time_unit(lowest)

        return lowest
    
    @staticmethod
    def assign_model_raster(tasks):
        # Assign raster to models
        for task in tasks:
            for model in task.models.values():
                model.set_raster(task.raster)
                model.set_time_unit(task.timeunit)            

    @staticmethod
    def get_global_hcf_time(tasks, time = -1):
        hcf = []

        if time >= 0:
            hcf.append(time)

        for task in tasks:
            hcf.append(task.raster)
        
        return math.gcd(*hcf)
    
    @staticmethod
    def get_global_lcm_time(tasks):
        lcm = []
        for task in tasks:
            lcm.append(task.raster)
        
        for model in Utility.get_models(tasks):
            lcm.append(model.get_raster())
        
        return math.lcm(*lcm)
    
    @staticmethod
    def get_local_hcf_time(model, time = -1):
        clocks = set()
        if time == -1:
            clocks.update(model.get_all_clocks())
        else:
            local_hcf = []
            for clock in model.get_all_clocks():
                local_hcf.append(clock.get_raster() + clock.get_offset())
            
            if len(local_hcf) > 0:
                step = math.gcd(*local_hcf)
                for step_time in range(time ,time + model.get_raster(), step):
                    clocks.update(model.get_clocks(step_time))
        
        hcf = [] if time == -1 else [time]
        hcf.append(model.get_raster())

        for clock in clocks:
            hcf.append(clock.get_raster() + clock.get_offset())
        
        return math.gcd(*hcf)
    
    @staticmethod
    def get_local_lcm_time(model, time = -1):
        lcm = []
        lcm.append(model.get_raster())
        clocks = model.get_all_clocks() if time == -1 else model.get_clocks(time)

        for clock in clocks:
            if clock.isTimeBased():
                lcm.append(clock.get_raster())
        return math.lcm(*lcm)

    @staticmethod
    def get_models(tasks):
        models = []
        for task in tasks:
            for model in task.models.values():
                models.append(model)
        return models

    @staticmethod
    def get_global_time_scale(__tasks):
        hcf_time = []
        for model in Utility.get_models(__tasks):
            hcf_time.append(model.get_local_hcf_time())
        return min(hcf_time)
     
    @staticmethod
    def get_execution_interval(time, execution_time, color):
        interval = f'{time} is \"{execution_time}\" {color}\n'
        return interval
    
    @staticmethod
    def get_execution_interval_hidden(time):
        interval = f'{time} is {{hidden}}\n'
        return interval
    
    @staticmethod
    def get_execution_interval_dashed(time):
        interval = f'{time} is {{-}}\n'
        return interval
    
    # @staticmethod
    # def get_execution_interval_parallel_process(time):
    #     interval = f'{time} is {{hidden}}\n'
    #     return interval
    
    # @staticmethod
    # def get_execution_interval_sequential_process(time, task, priority):
    #     intervals = []
    #     for priority_pos in range(0, len(task.models)):
    #         if priority == priority_pos + 1:
    #             intervals.append(f'{time + int(priority_pos * (task.raster/len(task.models)))} is \"{task.raster}\" {task.models[priority].get_color()}\n')
    #         else:
    #             intervals.append(f'{time + int(priority_pos * (task.raster/len(task.models)))} is {{hidden}}\n')
    #     return intervals
    
    @staticmethod
    def get_execution_interval_for_end_time(time):
        return f'{time} is {{hidden}}\n'
    
    @staticmethod
    def get_comment_for_raster_change( start_time, end_time, original_raster, new_raster, is_clock = False):
        duration = end_time - start_time
        arrow_start = start_time + duration/4
        arrow_end = end_time - duration/4
        steps = original_raster/new_raster

        if(original_raster != new_raster and is_clock == False):
            comment = f'@{int(arrow_start)} <-> @{int(arrow_end)} : Raster change from {original_raster} to {new_raster} with {steps} step\n'
        else:
            comment = f'@{int(arrow_start)} <-> @{int(arrow_end)} : Raster {new_raster} with {steps} step\n'

        return comment