from Model import Model, TimeUnit
from Scheduler import Scheduler
from Utility import Utility
from TaskMap import Task
from UMLGenerator import WSDFileCreator
from Clock import Clock, ClockType, VariabilityType, TimeBasedClockType

def create_wsd_file(scheduler):
    creator = WSDFileCreator('GlobalSchedule.wsd')
    creator.create_wsd_file()
    creator.add_startuml()

    creator.add_models_to_file(Utility.get_models(scheduler.get_tasks()))

    for model in Utility.get_models(scheduler.get_tasks()):
        creator.add_process(model)
    
    create_wsd_file_model(scheduler)
    
    creator.add_timestamp_to_file(scheduler.get_end_time(), scheduler.get_global_time_scale())
    creator.add_time_scale(Utility.get_models(scheduler.get_tasks())[0].get_name_without_spaces(), scheduler.get_end_time(), scheduler.get_global_time_unit())
    creator.add_enduml()

def create_wsd_file_model(scheduler):
    for model in Utility.get_models(scheduler.get_tasks()):
        creator = WSDFileCreator(model.get_name_without_spaces() + '.wsd')
        creator.create_wsd_file()
        creator.add_startuml()

        creator.add_clocks_to_file(model)

        creator.add_process(model, True)
        for clock in model.get_all_clocks():
            if clock.isTimeBased():
                creator.add_process(clock)
    
        creator.add_timestamp_to_file(scheduler.get_end_time(), model.get_local_hcf_time())
        creator.add_time_scale(model.get_name_without_spaces(), scheduler.get_end_time(), scheduler.get_global_time_unit())
        creator.add_enduml()

def main():    
    A = Model('FMU A')
    B = Model('FMU B')
    C = Model('FMU C')
    D = Model('FMU D')
    E = Model('FMU E')

    clock1 = Clock('Clock 1', TimeUnit.MS)
    clock1.configure_constant_clock(4000)
    clock2 = Clock('Clock 2', TimeUnit.MS, 0, 2000)
    clock2.configure_tunable_clock(1000)
    clock3 = Clock('Clock 3', TimeUnit.MS)
    clock3.configure_constant_clock(500)
    clock4 = Clock('Clock 4', TimeUnit.MS)
    clock4.configure_constant_clock(3000, 4000)
    clock5 = Clock('Clock 5', TimeUnit.MS, 2000, 2500)
    clock5.configure_tunable_clock(100)

    B.add_clock(clock1)
    B.add_clock(clock4)
    D.add_clock(clock2)  
    D.add_clock(clock3)
    D.add_clock(clock5)

    task = Task('Task 1', 3, TimeUnit.S)
    task.add_model(A, 2)
    task.add_model(B, 3)
    task.add_model(C, 1)

    task2 = Task('Task 2', 2, TimeUnit.S)
    task2.add_model(D)

    scheduler = Scheduler()
    
    scheduler.add_task(task)
    scheduler.add_task(task2)

    scheduler.normalize_system_time()
    scheduler.configure_local_time()
    scheduler.configure_global_time()

    scheduler.set_end_time(6, TimeUnit.S)

    scheduler.generate_global_schedule()
    scheduler.generate_local_schedule()

    create_wsd_file(scheduler)

if __name__ == "__main__":
    main()