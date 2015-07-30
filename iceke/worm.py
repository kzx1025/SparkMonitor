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

    def __init__(self, url, stage_url, has_proxy, has_gc,  property):
        self.property = property
        self.running_spark = SparkData(property)
        self.finish_spark = SparkData(property)
        self.url = url
        self.stage_url = stage_url
        self.running_stages = []
        self.finished_stages = []
        self.failed_stages = []
        self.has_proxy = has_proxy
        self.has_gc = has_gc

    @staticmethod
    def get_html(url, has_proxy, time_out):
        if has_proxy is True:
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1314)
            socket.socket = socks.socksocket
            page = urllib2.urlopen(url, timeout=time_out)
            return page.read()
        else:
            page = urllib2.urlopen(url, timeout=time_out)
            return page.read()

    '''
    only support a running task
    if more than one raise exception
    '''

    def get_running_spark(self):
        html = self.get_html(self.url, self.has_proxy, 9)
        soup = BeautifulSoup(html, "html.parser")

        for div in soup.find_all('div', 'row-fluid'):
            if div.h4 is not None:
                # print div.h4.string
                if div.h4.string.find(' Running Applications ') != -1:
                    tr_tags = div.find_all('tr')
                    if len(tr_tags) != 1 and len(tr_tags) != 0:
                        raise ValueError('there is maybe more than  one running spark Task')
                    if len(tr_tags) == 0:
                        return None  # if 0 return none
                    tds = tr_tags[0].find_all('td')
                    # print tds[0].find_all('a')[0].string
                    self.running_spark.set_app_id(tds[0].find_all('a')[0].string.strip())
                    self.running_spark.set_app_name(tds[1].find_all('a')[0].string.strip())
                    self.running_spark.set_total_time(tds[7].string)
                    self.running_spark.set_status(tds[6].string)

        # start to get information about stages of running spark
        stage_html = self.get_html(self.stage_url, self.has_proxy, 9)
        stage_soup = BeautifulSoup(stage_html, 'html.parser')

        tables = stage_soup.find_all('table', 'table table-bordered table-striped table-condensed sortable')
        Worm.logger.debug(len(tables))
        divs = stage_soup.find_all('div', 'container-fluid')
        all_h4 = divs[0].find_all('h4')
        i = 0
        for h4 in all_h4:
            if h4.string.find('Active Stages') != -1:
                running_trs = tables[i].find_all('tr')
                self.running_stages.extend(Worm.get_stages(running_trs, self.stage_url, self.has_gc))
            elif h4.string.find('Completed Stages') != -1:
                finished_trs = tables[i].find_all('tr')
                self.finished_stages.extend(Worm.get_stages(finished_trs, self.stage_url, self.has_gc))
            else:
                pass
            i += 1

        '''
        for table in tables:
             if table.h4.string.find('Active Stages') != -1:
                 running_trs = tables[0].find_all('tr')
                 self.running_stages.extend(Worm.get_stages(running_trs, self.stage_url, self.has_gc))
             elif table.h4.string.find('Completed Stages') != -1:
                 finished_trs = tables[1].find_all('tr')
                 self.finished_stages.extend(Worm.get_stages(finished_trs, self.stage_url, self.has_gc))
             elif table.h4.string.find('Failed Stages') != -1:
                 finished_trs = tables[1].find_all('tr')
                 self.finished_stages.extend(Worm.get_stages(finished_trs, self.stage_url, self.has_gc))
             else:
                 pass

        if len(tables) >= 1:
            running_trs = tables[0].find_all('tr')
            self.running_stages.extend(Worm.get_stages(running_trs, self.stage_url, self.has_gc))

        if len(tables) >= 2:
            finished_trs = tables[0].find_all('tr')
            self.finished_stages.extend(Worm.get_stages(finished_trs, self.stage_url, self.has_gc))

        if len(tables) >= 3:
            failed_trs = tables[2].find_all('tr')
            self.failed_stages.extend(Worm.get_stages(failed_trs, self.stage_url, self.has_gc))
        '''

        self.running_spark.set_running_stages(self.running_stages)
        self.running_spark.set_finished_stages(self.finished_stages)
        self.running_spark.set_failed_stages(self.failed_stages)

        return self.running_spark

    def get_finish_spark(self):
        html = self.get_html(self.url, self.has_proxy, 9)
        soup = BeautifulSoup(html, "html.parser")
        for div in soup.find_all('div', 'row-fluid'):
            if div.h4 is not None:
                # print div.h4.string
                if div.h4.string.find('Completed Applications') != -1:
                    tr_tags = div.find_all('tr')
                    if len(tr_tags) == 0:
                        print 'there is no finish spark Task'
                        return None  # if 0 return none
                    tds = tr_tags[0].find_all('td')  #return the first
                    # print tds[0].find_all('a')[0].string
                    self.finish_spark.set_app_id(tds[0].find_all('a')[0].string.strip())
                    self.finish_spark.set_app_name(tds[1].find_all('a')[0].string.strip())
                    self.finish_spark.set_total_time(tds[7].string)
                    self.finish_spark.set_status(tds[6].string)

        stage_html = self.get_html(self.url+'history/'+self.finish_spark.get_app_id()+'/stages/', self.has_proxy, 9)
        stage_soup = BeautifulSoup(stage_html, 'html.parser')
        tables = stage_soup.find_all('table', 'table table-bordered table-striped table-condensed sortable')
        Worm.logger.debug(len(tables))
        divs = stage_soup.find_all('div', 'container-fluid')
        all_h4 = divs[0].find_all('h4')
        tables = stage_soup.find_all('table', 'table table-bordered table-striped table-condensed sortable')
        Worm.logger.debug(len(tables))
        divs = stage_soup.find_all('div', 'container-fluid')
        all_h4 = divs[0].find_all('h4')
        i = 0
        for h4 in all_h4:
            if h4.string.find('Completed Stages') != -1:
                finished_trs = tables[i].find_all('tr')
                self.finished_stages.extend(Worm.get_stages(finished_trs, self.url+'history/' +
                               self.finish_spark.get_app_id()+'/stages/', self.has_gc))
            else:
                pass
            i += 1

        self.finish_spark.set_running_stages(self.running_stages)
        self.finish_spark.set_finished_stages(self.finished_stages)
        self.finish_spark.set_failed_stages(self.failed_stages)
        return self.finish_spark

    @staticmethod
    def get_stages(trs, stage_url, has_gc):
        final_stages = []
        for tr in trs:
            tds = tr.find_all('td')
            temp_stage = Stage()
            temp_stage.set_stage_id(int(tds[0].string.strip()))
            temp_stage.set_submit_time(tds[2].string.strip())
            temp_stage.set_duration(tds[3].string.strip())
            temp_stage.set_tasks_percent(tds[4].find('span').string.strip())
            temp_stage.set_input('0MB' if tds[5].string is None else tds[5].string)
            temp_stage.set_shuffle_read('0MB' if tds[7].string is None else tds[6].string)
            temp_stage.set_shuffle_write('0MB' if tds[8].string is None else tds[7].string)
            gc_total = 0.0
            try:
              if has_gc is True:
                  gc_html = Worm.get_html(stage_url+'stage/?id='+str(temp_stage.get_stage_id())+'&attempt=0', True, 6)
                  print stage_url+'stage/?id='+str(temp_stage.get_stage_id())+'&attempt=0'
                  gc_soup = BeautifulSoup(gc_html, 'html.parser')
                  tables = gc_soup.find_all('table', 'table table-bordered table-condensed sortable table-striped')
                  trs = tables[1].find_all('tr')
                  for i in range(0, len(trs)):
                      tds = trs[i].find_all('td')
                      gc_str = tds[10].string.strip()
                      if gc_str != '':
                        # print  gc_str
                          gc_total += Util.format_second(gc_str)
            except Exception, e:
                print e
                gc_total = 0.0
            temp_stage.set_gc_time(gc_total)

            final_stages.append(temp_stage)

        return final_stages





def main():
    worm = Worm("http://11.11.0.64:8099/", "http://11.11.0.64:4041/stages/", True, False, "Flint")
    # worm = Worm("http://211.69.198.208:8080/", "http://211.69.198.208:8080/history/app-20150722101951-0008/stages/", "Flint")
    # finish_sparks = worm.get_finish_sparks()
    running_spark = worm.get_finish_spark()
    if running_spark != None:
        running_stages = running_spark.get_running_stages()
        finished_stages = running_spark.get_finished_stages()
        stages = []
        for finished_stage in finished_stages:
            stage_dict = {'stage_id': finished_stage.get_stage_id(), 'stage_duration': Util.format_time(
                finished_stage.get_duration()), 'submit_time': finished_stage.get_submit_time(),
                'tasks_percent': 100.0, 'gc_time': round(finished_stage.get_gc_time(), 1)}
            stages.append(stage_dict)
        for running_stage in running_stages:
            stage_dict = {'stage_id': running_stage.get_stage_id(), 'stage_duration': Util.format_time(
                running_stage.get_duration()), 'submit_time': running_stage.get_submit_time(),
                'tasks_percent': Util.format_tasks_percent(running_stage.get_tasks_percent()),
                'gc_time': round(running_stage.get_gc_time(), 1)}
            stages.append(stage_dict)
        #print stages
        format_spark = {}
        format_spark['app_name'] = running_spark.get_app_name()
        format_spark['total_time'] = Util.format_time(running_spark.get_total_time())
        format_spark['status'] = running_spark.get_status()
        format_spark['property'] = running_spark.get_property()
        format_spark['stages'] = stages
        print format_spark


if __name__ == '__main__':
    main()
