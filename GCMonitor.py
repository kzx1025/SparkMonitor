from flask import Flask, render_template
from iceke.worm import Worm
import json
from iceke.util import Util

app = Flask(__name__)

flint_url = 'http://11.11.0.64:8099/'
flint_stage_url = 'http://11.11.0.64:4041/stages/'
spark_url = 'http://11.11.0.55:8090/'
spark_stage_url = 'http://11.11.0.55:4040/stages/'


@app.route('/')
def show_gc():
    return render_template('show_gc.html', ctx='ab')


@app.route('/get_gc/')
def get_gc():
    final_dict = {}
    try:
       spark_worm = Worm(spark_url, spark_stage_url, True, True, "Spark")
       running_spark = spark_worm.get_running_spark()
       if running_spark is None:
           running_spark = spark_worm.get_finish_spark()  #get the first finished
       flint_worm = Worm(flint_url, flint_stage_url, True, True,  "Flint")
       running_flint = flint_worm.get_running_spark()
       if running_flint is None:
           running_flint = flint_worm.get_finish_spark()
    except Exception, e:
        print e
        return None
    if running_flint is None and running_spark is None:
        return None
    elif running_flint is None and running_spark is not None:
        final_dict = {'spark': format_spark_json(running_spark), 'flint': 'none'}
    elif running_flint is not None and running_spark is None:
        final_dict = {'spark': 'none', 'flint': format_spark_json(running_flint)}
    else:
        final_dict = {'spark': format_spark_json(running_spark), 'flint': format_spark_json(running_flint)}
    final_json = json.dumps(final_dict)
    print(final_json)
    return final_json


def format_spark_json(running_spark):
     if running_spark is not None:
        # spark_json = json.dumps(running_spark, default=running_spark.object2dict)
        running_stages = running_spark.get_running_stages()
        finished_stages = running_spark.get_finished_stages()
        failed_stages = running_spark.get_failed_stages()
        format_spark = {}
        stages = []
        for finished_stage in finished_stages:
            stage_dict = {'stage_id': finished_stage.get_stage_id(), 'stage_duration': Util.format_time(
                finished_stage.get_duration()), 'submit_time': finished_stage.get_submit_time(),
                'tasks_percent': 100.0, 'gc_time': round(finished_stage.get_gc_time(), 1)}
            stages.append(stage_dict)
        stages.reverse()
        for running_stage in running_stages:
            stage_dict = {'stage_id': running_stage.get_stage_id(), 'stage_duration': Util.format_time(
                running_stage.get_duration()), 'submit_time': running_stage.get_submit_time(),
                'tasks_percent': Util.format_tasks_percent(running_stage.get_tasks_percent()),
                'gc_time': round(running_stage.get_gc_time(), 1)}
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
    app.run(port=7000)
