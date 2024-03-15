from Model import Model, TimeUnit
import copy

class Task:
    def __init__(self, name, raster, timeunit):
        self.name = name
        self.raster = raster
        self.timeunit = timeunit
        self.models = {}

    def add_model(self, model, priority = 0):
        self.models[priority] = copy.deepcopy(model)

    
