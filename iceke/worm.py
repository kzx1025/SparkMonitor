__author__ = 'iceke'

import urllib2
from stage import Stage
from bs4 import BeautifulSoup
from spark_data import SparkData
from mylog import MyLog
import json
from util import Util
import socks
import socket


class Worm(object):
    logger = MyLog.get_logger('Worm.class')

    def __init__(self, url, stage_url, has_proxy, property):
        self.property = property
        self.running_spark = SparkData(property)
        self.finish_spark = []
        self.url = url
        self.stage_url = stage_url
        self.running_stages = []
        self.finished_stages = []
        self.failed_stages = []
        self.has_proxy = has_proxy

    @staticmethod
    def get_html(url, has_proxy):
        if has_proxy is True:
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1314)
            socket.socket = socks.socksocket
            page = urllib2.urlopen(url)
            return page.read()
        else:
            page = urllib2.urlopen(url)
            return page.read()

    '''
    only support a running task
    if more than one raise exception
    '''

    def get_running_spark(self):
        html = self.get_html(self.url, self.has_proxy)
        soup = BeautifulSoup(html, "html.parser")

        for div in soup.find_all('div', 'row-fluid'):
            if div.h4 is not None:
                # print div.h4.string
                if div.h4.string.find(' Running Applications ') != -1:
                    aTag = div.find_all('a')
                    if len(aTag) != 2 and len(aTag) != 0:
                        raise ValueError('there is maybe more than  one running spark Task')
                    if len(aTag) == 0:
                        return None  # if 0 return none
                    print aTag[0].string
                    print aTag[1].string
                    self.running_spark.set_app_id(aTag[0].string.strip())
                    self.running_spark.set_app_name(aTag[1].string.strip())
                    td = div.find_all('td')
                    print td[7].string
                    self.running_spark.set_total_time(td[7].string)
                    print td[6].string
                    self.running_spark.set_status(td[6].string)


        # start to get information about stages of running spark
        stage_html = self.get_html(self.stage_url, self.has_proxy)
        stage_soup = BeautifulSoup(stage_html, 'html.parser')
        uls = stage_soup.find_all('ul', 'unstyled')
        lis = uls[0].find_all('li')
        self.running_spark.set_total_time(lis[0].contents[2].strip())  # get the total
        Worm.logger.debug(lis[0].contents[2].strip())

        running_num = int(lis[2].contents[2].strip())
        finished_num = int(lis[3].contents[2].strip())
        failed_num = int(lis[4].contents[2].strip())
        self.running_spark.set_stage_num(running_num + finished_num + failed_num)

        tables = stage_soup.find_all('table', 'table table-bordered table-striped table-condensed sortable')
        Worm.logger.debug(len(tables))
        running_trs = tables[0].find_all('tr')
        self.running_stages.extend(Worm.get_stages(running_trs))

        finished_trs = tables[1].find_all('tr')
        self.finished_stages.extend(Worm.get_stages(finished_trs))

        failed_trs = tables[2].find_all('tr')
        self.failed_stages.extend(Worm.get_stages(failed_trs))

        self.running_spark.set_running_stages(self.running_stages)
        self.running_spark.set_finished_stages(self.finished_stages)
        self.running_spark.set_failed_stages(self.failed_stages)

        return self.running_spark

    @staticmethod
    def get_stages(trs):
        final_stages = []
        for tr in trs:
            tds = tr.find_all('td')
            temp_stage = Stage()
            temp_stage.set_stage_id(int(tds[0].string.strip()))
            temp_stage.set_submit_time(tds[2].string.strip())
            temp_stage.set_duration(tds[3].string.strip())
            temp_stage.set_tasks_percent(tds[4].find('span').string.strip())
            temp_stage.set_input('0MB' if tds[5].string is None else tds[5].string)
            temp_stage.set_shuffle_read('0MB' if tds[6].string is None else tds[6].string)
            temp_stage.set_shuffle_write('0MB' if tds[7].string is None else tds[7].string)
            final_stages.append(temp_stage)

        return final_stages

    def get_finish_sparks(self):
        html = self.get_html(self.url, self.has_proxy)
        soup = BeautifulSoup(html, "html.parser")
        for div in soup.find_all('div', 'row-fluid'):
            if div.h4 is not None:
                # print div.h4.string
                if div.h4.string.find(' Completed Applications ') != -1:
                    a = div.find_all('a')
                    # print len(a)/2     # how many completed applications
                    if len(a) == 0:
                        break
                    i = 0
                    for m in range(0, len(a) / 2, 1):
                        self.finish_spark.append(SparkData(self.property))
                    for x in range(0, len(a), 1):
                        if x % 2 == 0:
                            self.finish_spark[i].set_app_id(a[x].string)
                            print self.finish_spark[i].get_app_id()
                        else:
                            self.finish_spark[i].set_app_name(a[x].string)
                            print self.finish_spark[i].get_app_name()
                            i += 1

                    # print len(finish_spark)
                    td = div.find_all('td')
                    # print len(td)/8
                    if len(td) / 8 != len(a) / 2:
                        raise ValueError('have errors !!!!!')
                    j = 0
                    for y in range(0, len(td), 1):
                        if (y + 1) % 8 == 0:  # the 8th td is the time task cost
                            print td[y].string
                            self.finish_spark[j].set_total_time(td[y].string)
                            j += 1
                        elif (y + 1) % 8 == 7:
                            print td[y].string
                            self.finish_spark[j].set_status(td[y].string)

        if self.finish_spark is not None:
            for finish in self.finish_spark:
                print finish.get_app_id() + ',' + finish.get_app_name() + ',' + finish.get_total_time()
        return self.finish_spark


def main():
    worm = Worm("http://211.69.198.208:8080/", "http://192.168.226.211:8012/stages/", True, "Flint")
    # worm = Worm("http://211.69.198.208:8080/", "http://211.69.198.208:8080/history/app-20150722101951-0008/stages/", "Flint")
    # finish_sparks = worm.get_finish_sparks()
    running_spark = worm.get_running_spark()
    if running_spark != None:
        spark_json = json.dumps(running_spark, default=running_spark.object2dict)
        running_stages = running_spark.get_running_stages()
        finished_stages = running_spark.get_finished_stages()
        failed_stages = running_spark.get_failed_stages()
        stages_num = running_spark.get_stage_num()
        stages = []
        for finished_stage in finished_stages:
            stage_dict = {'stage_id': finished_stage.get_stage_id(), 'stage_duration': Util.format_time(
                finished_stage.get_duration()), 'submit_time': finished_stage.get_submit_time(),
                'tasks_percent': 100.0}
            stages.append(stage_dict)
        for running_stage in running_stages:
            stage_dict = {'stage_id': running_stage.get_stage_id(), 'stage_duration': Util.format_time(
                running_stage.get_duration()), 'submit_time': running_stage.get_submit_time(),
                'tasks_percent': Util.format_tasks_percent(running_stage.get_tasks_percent())}
            stages.append(stage_dict)
        print stages
        format_spark = {}
        format_spark['app_name'] = running_spark.get_app_name()
        format_spark['total_time'] = Util.format_time(running_spark.get_total_time())
        format_spark['status'] = running_spark.get_status()
        format_spark['property'] = running_spark.get_property()
        format_spark['stages'] = stages
        print format_spark


if __name__ == '__main__':
    main()
