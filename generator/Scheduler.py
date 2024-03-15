import math
from Model import Model, TimeUnit
from UMLGenerator import WSDFileCreator
from Utility import Utility
from TaskMap import Task

class Scheduler:
    def __init__(self):
        self.__tasks = []
        
        self.__global_hcf_time = -1
        self.__global_lcm_time = -1
        self.__global_time_unit = TimeUnit.S

        # minimum of all hcf times of models
        self.__global_time_scale = -1

        self.__start_time = 0
        self.__end_time = 0

    def add_task(self, task):
        self.__tasks.append(task) 

    def get_tasks(self):
        return self.__tasks
    
    def get_global_hcf_time(self):
        return self.__global_hcf_time
    
    def get_global_lcm_time(self):
        return self.__global_lcm_time
    
    def get_global_time_unit(self):
        return self.__global_time_unit  
    
    def get_global_time_scale(self):
        return self.__global_time_scale
    
    def get_end_time(self):
        return self.__end_time
    
    def set_end_time(self, end_time, time_unit):
        time = int(end_time * (self.__global_time_unit.value / time_unit.value))
        if time > self.__end_time:
            self.__end_time = math.ceil(time / self.__global_lcm_time) * self.__global_lcm_time

    def normalize_system_time(self):
        self.__global_time_unit = Utility.normalize_system_time(self.__tasks)
        Utility.assign_model_raster(self.__tasks)

    def configure_global_time(self):
        self.__global_hcf_time = Utility.get_global_hcf_time(self.__tasks)
        self.__global_lcm_time = Utility.get_global_lcm_time(self.__tasks)
        self.__global_time_scale = Utility.get_global_time_scale(self.__tasks)
        self.__end_time = self.__global_lcm_time

    def configure_local_time(self):
        for model in Utility.get_models(self.__tasks):
            self.__configure_model_local_time(model)

    def __configure_model_local_time(self, model, time = -1):
        model.set_local_hcf_time(Utility.get_local_hcf_time(model, time))
        model.set_local_lcm_time(Utility.get_local_lcm_time(model, time))

    def generate_global_schedule(self):
        for time in range(self.__start_time, self.__end_time, self.__global_hcf_time):
            for task in self.__tasks:
                if time % task.raster == 0:
                    # Check if multiple models are present in the task, indicating sequential execution
                    if len(task.models) > 1:
                        for priority in task.models.keys():
                            pass
                            self.__generate_sequential_model_schedule(task.models[priority], time, priority, len(task.models))
                    else:
                        self.__generate_single_model_schedule(task.models[0], time)
        self.__generate_single_model_schedule_hidden(self.__end_time)

    def __generate_sequential_model_schedule(self, model, time, priority, models_count):
        for priority_pos in range(0, models_count): 
            offset_raster_time = (model.get_raster()/models_count)
            offset_start_time = time + (priority_pos * offset_raster_time) # check if this should be converted to int
            offset_end_time = offset_start_time + offset_raster_time
            if priority == priority_pos + 1:
                self.__generate_single_model_schedule(model, offset_start_time, offset_end_time) 

    def __generate_single_model_schedule(self, model, start_time , end_time = -1):
        model.add_execution_intervals(Utility.get_execution_interval(start_time, model.get_raster(), model.get_color()))
        if end_time != -1:
            model.add_execution_intervals(Utility.get_execution_interval_for_end_time(end_time))

    def __generate_single_model_schedule_hidden(self, end_time):
        for task in self.__tasks:
            if len(task.models) == 1:
                task.models[0].add_execution_intervals(Utility.get_execution_interval_for_end_time(end_time))

    def generate_local_schedule(self):
        for model in Utility.get_models(self.__tasks):
            time = self.__start_time
            end_time = self.__end_time
            while time < end_time:
                self.__configure_model_local_time(model, time)
                self.__generate_local_model_schedule(model, time)
                for clock in model.get_clocks(time):
                    if (time - clock.get_offset()) % clock.get_raster() == 0 and clock.isTimeBased():
                        clock.add_execution_intervals(Utility.get_execution_interval(time, clock.get_raster(), clock.get_color()))
                time += model.get_local_hcf_time()
                for clock in model.get_end_time_clocks(time):
                    if clock.isTimeBased():
                        clock.add_execution_intervals(Utility.get_execution_interval_for_end_time(time))
            model.add_local_execution_intervals(Utility.get_execution_interval_for_end_time(end_time))
            for clock in model.get_clocks(end_time):
                if clock.isTimeBased() and (end_time - clock.get_offset())% clock.get_raster() == 0:
                    clock.add_execution_intervals(Utility.get_execution_interval_for_end_time(end_time))

    def __generate_local_model_schedule(self, model, time):
        model.add_local_execution_intervals(Utility.get_execution_interval(time, model.get_local_hcf_time(), model.get_color()))

    def calculate_execution_interval(self):
        for time in range(self.__start_time, self.__end_time, self.__global_hcf_time):
            for task in self.__tasks:
                if time % task.raster == 0:
                    # Check if multiple models are present in the task, indicating sequential execution
                    if len(task.models) > 1:
                        for priority in task.models.keys():
                            self.__calculate_model_offset_execution_interval(task.models[priority], time, priority, len(task.models), self.__global_time_scale)
                    else:
                        self.__calculate_model_execution_interval(task.models[0], time)
        self.__add_models_execution_end_interval(self.__tasks)
    
    def __calculate_model_execution_interval(self, model, time):
        self.__configure_model_local_time(model, time)
        if(model.get_local_hcf_time() != model.get_raster()):
                for modelStepTime in range(time, time + model.get_raster(), model.get_local_hcf_time()):
                    self.__add_single_model_execution_interval(model, modelStepTime, model.get_local_hcf_time(), model.get_color())
        else:
            self.__add_single_model_execution_interval(model,time, model.get_raster(), model.get_color())
        self.__calculate_clock_execution_interval(model, time)

    def __add_single_model_execution_interval(self, model, time, raster, color):
        model.add_execution_intervals(Utility.get_execution_interval(time, raster, color))

    def __calculate_clock_execution_interval(self, model, time):
            for time in range(time, time + model.get_raster(), model.get_local_hcf_time()):
                for clock in model.get_clocks(time):
                    if time % clock.get_raster() == 0 and clock.isTimeBased():
                        clock.add_execution_intervals(Utility.get_execution_interval(time, clock.get_raster(), clock.get_color()))
        
    def __calculate_model_offset_execution_interval(self, model, time, priority, models_count, offset_hcf_time):
        self.__configure_model_local_time(model, time)
        for priority_pos in range(0, models_count):
            offset_raster_time = (model.get_raster()/models_count)
            offset_start_time = time + (priority_pos * offset_raster_time) # check if this should be converted to int
            offset_end_time = offset_start_time + offset_raster_time

            if priority == priority_pos + 1:
                if(model.get_local_hcf_time() != model.get_raster()):
                    model.add_execution_intervals(Utility.get_execution_interval(offset_start_time, model.get_local_hcf_time(), model.get_color()))
                    if(2 * offset_hcf_time != offset_end_time):
                        model.add_execution_intervals(Utility.get_execution_interval_dashed(offset_start_time + offset_hcf_time))
                        model.add_execution_intervals(Utility.get_execution_interval(offset_end_time - offset_hcf_time, model.get_local_hcf_time(), model.get_color()))
                        model.add_execution_intervals(Utility.get_comment_for_raster_change(offset_start_time, offset_end_time, model.get_raster(), model.get_local_hcf_time()))
                    else:
                        t = offset_start_time + (offset_end_time - offset_start_time)/2
                        model.add_execution_intervals(Utility.get_execution_interval(t, model.get_local_hcf_time(), model.get_color()))
                    model.add_execution_intervals(Utility.get_execution_interval_hidden(offset_end_time))
                else:
                    model.add_execution_intervals(Utility.get_execution_interval(offset_start_time, model.get_raster(), model.get_color()))
                self.__calculate_clock_offset_execution_interval(model, offset_start_time, offset_end_time, offset_hcf_time)
            else:
                model.add_execution_intervals(Utility.get_execution_interval_hidden(offset_start_time))

    def __calculate_clock_offset_execution_interval(self, model, start_time, end_time, offset_hcf_time):
        for clock in model.get_clocks(start_time):
            if(clock.get_raster() != model.get_raster()):
                clock.add_execution_intervals(Utility.get_execution_interval(start_time, clock.get_raster(), clock.get_color()))
                if(2 * offset_hcf_time != end_time):
                    clock.add_execution_intervals(Utility.get_execution_interval_dashed(start_time + offset_hcf_time))
                    clock.add_execution_intervals(Utility.get_execution_interval(end_time - offset_hcf_time, clock.get_raster(), clock.get_color()))
                    clock.add_execution_intervals(Utility.get_comment_for_raster_change(start_time, end_time, model.get_raster(), clock.get_raster(), True))
                else:
                    clock.add_execution_intervals(Utility.get_execution_interval(start_time + (end_time - start_time)/2, clock.get_raster(), clock.get_color()))
                clock.add_execution_intervals(Utility.get_execution_interval_hidden(end_time))
            else:
                clock.add_execution_intervals(Utility.get_execution_interval(start_time, clock.get_raster(), clock.get_color()))
                clock.add_execution_intervals(Utility.get_execution_interval_hidden(end_time))

    def __add_models_execution_end_interval(self, tasks):
        # Handling end time
        for task in self.__tasks:
            if len(task.models) > 1:
                for priority in task.models.keys():
                    task.models[priority].add_execution_intervals(Utility.get_execution_interval_for_end_time(self.__end_time))
            else:
                task.models[0].add_execution_intervals(Utility.get_execution_interval_for_end_time(self.__end_time))
        
        for model in Utility.get_models(tasks):
            self.__add_clock_end_interval(model)

    def __add_clock_end_interval(self, model):
        end_time = self.__end_time
        for clock in model.get_clocks(end_time):
            if clock.isTimeBased():
                clock.add_execution_intervals(Utility.get_execution_interval_for_end_time(end_time))