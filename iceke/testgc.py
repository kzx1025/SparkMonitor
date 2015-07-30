__author__ = 'iceke'

import urllib2
from stage import Stage
from bs4 import BeautifulSoup
from spark_data import SparkData
from worm import Worm
from util import Util

def main():
    stage_url = 'http://192.168.226.211:8012/stages/'
    gc_html = Worm.get_html(stage_url+'stage/?id='+str(1)+'&attempt=0', True)
    gc_soup = BeautifulSoup(gc_html, 'html.parser')
    tables = gc_soup.find_all('table', 'table table-bordered table-striped table-condensed sortable')
    trs = tables[1].find_all('tr')
    gc_total = 0.0
    for i in range(0, len(trs)):
        tds = trs[i].find_all('td')
        gc_str = tds[8].string.strip()
        if gc_str != '':
            gc_total += Util.format_second(gc_str)
    print gc_total

if __name__ == '__main__':
    main()
