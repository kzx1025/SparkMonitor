__author__ = 'iceke'


class Util(object):

    def a(self):
        pass

    '''
    transform all kinds of time to minute
    '''
    @staticmethod
    def format_time(time_str):
        final_time = 0.0
        time_array = time_str.split(' ')
        unit = time_array[1]
        value = float(time_array[0])
        if unit == 's':
            final_time = round(value/60.0, 2)
        elif unit == 'min':
            final_time = round(value+0.0, 2)
        elif unit == 'h':
            final_time = round(value*60.0, 2)
        else:
            raise ValueError('spark total time\'s unit is illegal')
        return final_time

    '''
    transform all kinds of time to second
    '''
    @staticmethod
    def format_second(time_str):
        final_time = 0.0
        time_array = time_str.split(' ')
        unit = time_array[1]
        if time_array[0].find(".") is False:
            print time_array[0]
            value = int(time_array[0], 10)
            value = value * 1.0
        else:
            value = float(time_array[0])
        if unit == 's':
            final_time = value
        elif unit == 'ms':
            final_time = round(value/1000.0, 2)
        elif unit == 'min':
            final_time = round(value*60.0, 2)
        elif unit == 'h':
            final_time = round(value*3600.0, 2)
        else:
            raise ValueError('spark total time\'s unit is illegal')
        return final_time

    @staticmethod
    def format_tasks_percent(percent_str):
        final_percent = 0.0
        percent_array = percent_str.strip().split('/')
        print percent_array[0],percent_array[1]
        final_percent = round((float(percent_array[0])/float(percent_array[1]))*100, 1)
        return final_percent




