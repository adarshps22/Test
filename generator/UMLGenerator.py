class WSDFileCreator:
    def __init__(self, filename):
        self.filename = filename

    def create_wsd_file(self):
        with open(self.filename, 'w') as file:
            file.write('\' Co Simulation timing diagram\n')

    def add_startuml(self):
        with open(self.filename, 'a') as file:
            file.write('@startuml\n')

    def add_enduml(self):
        with open(self.filename, 'a') as file:
            file.write('@enduml\n')

    def add_parallel_processuml(self):
        with open(self.filename, 'a') as file:
            file.write('\' Define the parallel process\n')

    def add_timestamp_to_file(self, end_time, step):
        with open(self.filename, 'a') as file:
            file.write('\' Define the time axis\n')
            file.write('@-1\n')
            for time in range(0, end_time + step, step):
                file.write(f'@{time}\n')
            file.write('\n')
                
    def add_models_to_file(self, models):
        with open(self.filename, 'a') as file:
            file.write('\' Define models in the system\n')
            for model in models:
                file.write(f'concise "{model.get_model_name()}" as {model.get_name_without_spaces()}\n')
            file.write('\n')

    def add_clocks_to_file(self, model):
        with open(self.filename, 'a') as file:
            file.write('\' Define Model and Clocks in the system\n')
            file.write(f'concise "{model.get_model_name()}" as {model.get_name_without_spaces()}\n')
            for clock in model.get_all_clocks():
                if clock.isTimeBased():
                    file.write(f'concise "{clock.get_name()}" as {clock.get_name_without_spaces()}\n')
            file.write('\n')

    def add_process(self, model, local = False):
        with open(self.filename, 'a') as file:
            file.write(f'@{model.get_name_without_spaces()}\n')
            intervals = model.get_execution_intervals() if not local else model.get_local_execution_intervals()
            for interval in intervals:
                file.write(interval)
            file.write('\n')

    def add_time_scale(self, model_name, time, time_unit):
        with open(self.filename, 'a') as file:
            file.write(f'@{model_name}\n')
            file.write(f'@{int(time/4)} <-> @{int(time - (time/4))} : Time scale in {str(time_unit)}\n')