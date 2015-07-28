__author__ = 'iceke'


class SparkData(object):
    def __init__(self, property):
        self.__property = property
        self.__app_id = ''
        self.__app_name = ''
        self.__stage__num = 0
        self.__total_time = ''
        self.__status = 'Finished'
        self.__finished_stages = []      # only running spark need these variable
        self.__running_stages = []
        self.__failed_stages = []

    def object2dict(self, obj):
        # convert object to a dict
        d = {}
        d['__class__'] = obj.__class__.__name__
        d['__module__'] = obj.__module__
        d.update(obj.__dict__)
        return d

    def set_property(self, property):
        self.__property = property

    def get_property(self):
        return self.__property

    def set_app_name(self, app_name):
        self.__app_name = app_name

    def get_app_name(self):
        return self.__app_name

    def set_stage_num(self, stage_num):
        self.__stage__num = stage_num

    def get_stage_num(self):
        return self.__stage__num

    def set_total_time(self, total_time):
        self.__total_time = total_time

    def get_total_time(self):
        return self.__total_time

    def set_app_id(self, app_id):
        self.__app_id = app_id

    def get_app_id(self):
        return self.__app_id

    def set_status(self, status):
        self.__status = status

    def get_status(self):
        return self.__status

    def set_running_stages(self, running_stages):
        self.__running_stages = running_stages

    def get_running_stages(self):
        return self.__running_stages

    def set_finished_stages(self, finished_stages):
        self.__finished_stages = finished_stages

    def get_finished_stages(self):
        return self.__finished_stages

    def set_failed_stages(self, failed_stages):
        self.__failed_stages = failed_stages

    def get_failed_stages(self):
        return self.__failed_stages
