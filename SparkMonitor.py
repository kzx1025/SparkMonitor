from flask import Flask, render_template
from iceke.worm import Worm
import json
from iceke.util import Util
import random

app = Flask(__name__)


@app.route('/')
def show_spark():
    return render_template('show_spark.html', ctx='ab')


@app.route('/get_json/')
def get_json():
    """
    you can transform the ip of node which you want to monitor
    :return:
    """
    final_dict = {}
    try:
       spark_worm = Worm("http://211.69.198.208:8080/", "http://192.168.226.211:8012/stages/", True, "Spark")
       running_spark = spark_worm.get_running_spark()
       flint_worm = Worm("http://211.69.198.208:8080/", "http://192.168.226.211:8012/stages/", True, "Flint")
       running_flint = flint_worm.get_running_spark()
       if running_flint is None and running_spark is None:
           return None
       final_dict = {'Spark': format_spark_json(running_spark), 'Flint': format_spark_json(running_flint)}
    except Exception, e:
        print e
        return None
    final_json = json.dumps(final_dict)
    print(final_json)
    return final_json


@app.route('/get_cpu_mem/')
def get_cpu_mem():
    spark_param = Worm.get_html('http://192.168.226.212:5000/', True).split('#')
    spark_cpu = float(spark_param[0])
    spark_mem = float(spark_param[1])
    flint_param = Worm.get_html('http://192.168.226.213:5000/', True).split('#')
    flint_cpu = float(flint_param[0])
    flint_mem = float(flint_param[1])
    fuck = {'spark_cpu': spark_cpu, 'spark_mem': spark_mem, 'flint_cpu': flint_cpu, 'flint_mem': flint_mem}
    print fuck
    shit = json.dumps(fuck)

    return shit


def format_spark_json(running_spark):
     if running_spark is not None:
        # spark_json = json.dumps(running_spark, default=running_spark.object2dict)
        running_stages = running_spark.get_running_stages()
        finished_stages = running_spark.get_finished_stages()
        failed_stages = running_spark.get_failed_stages()
        stages_num = running_spark.get_stage_num()
        format_spark = {}
        stages = []
        for finished_stage in finished_stages:
            stage_dict = {'stage_id': finished_stage.get_stage_id(), 'stage_duration': Util.format_time(
                finished_stage.get_duration()), 'submit_time': finished_stage.get_submit_time(),
                'tasks_percent': 100.0}
            stages.append(stage_dict)
        stages.reverse()
        for running_stage in running_stages:
            stage_dict = {'stage_id': running_stage.get_stage_id(), 'stage_duration': Util.format_time(
                running_stage.get_duration()), 'submit_time': running_stage.get_submit_time(),
                'tasks_percent': Util.format_tasks_percent(running_stage.get_tasks_percent())}
            stages.append(stage_dict)
        format_spark['app_name'] = running_spark.get_app_name()
        format_spark['total_time'] = Util.format_time(running_spark.get_total_time())
        format_spark['status'] = running_spark.get_status()
        format_spark['property'] = running_spark.get_property()
        format_spark['stages'] = stages
        return format_spark
     else:
         return None

if __name__ == '__main__':
    app.run(port=2555)
