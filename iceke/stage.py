__author__ = 'iceke'


class Stage(object):
    def __init__(self):
        self.__stage_id = -1
        self.__duration = ''
        self.__tasks_percent = 0.0
        self.__input_memory = ''
        self.__shuffle_read = ''
        self.__shuffle_write = ''
        self.__submit_time = ''
        self.__gc_time = 0.0

    def object2dict(self, obj):
        # convert object to a dict
        d = {}
        d['__class__'] = obj.__class__.__name__
        d['__module__'] = obj.__module__
        d.update(obj.__dict__)
        return d

    def get_gc_time(self):
        return self.__gc_time

    def set_gc_time(self, gc_time):
        self.__gc_time = gc_time

    def get_stage_id(self):
        return self.__stage_id

    def set_stage_id(self, stage_id):
        self.__stage_id = stage_id

    def get_duration(self):
        return self.__duration

    def set_duration(self, duration):
        self.__duration = duration

    def get_tasks_percent(self):
        return self.__tasks_percent

    def set_tasks_percent(self, tasks_percent):
        self.__tasks_percent = tasks_percent

    def get_input(self):
        return self.__input_memory

    def set_input(self, input_memory):
        self.__input_memory = input_memory

    def get_shuffle_read(self):
        return self.__shuffle_read

    def set_shuffle_read(self, shuffle_read):
        self.__shuffle_read = shuffle_read

    def get_shuffle_write(self):
        return self.__shuffle_write

    def set_shuffle_write(self, shuffle_write):
        self.__shuffle_write = shuffle_write

    def get_submit_time(self):
        return self.__submit_time

    def set_submit_time(self, submit_time):
        self.__submit_time = submit_time

