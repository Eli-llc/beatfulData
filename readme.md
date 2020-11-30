# 使用说明

## 1. 参数设置 
    所有参数均可以在config/config.yaml中配置
    所有参数均可以通过命令行选项来临时配置，以覆盖配置文件中的默认配置

## 2. 时间参数说明（时间单位均为秒）
-    time-start 为数据的起始时间，默认为当前时间
-    time-format 时间的输出格式，python的时间字符串均可使用。如%Y-%m-%d %H:%M:%S
-    time-end 为数据的结束时间，当提供time-duration参数时，time-end不生效，由time-start + time-duration计算得出。
-    time-duration 数据的持续时间，会覆盖time-end
-    time-interval 两条数据之间的间隔
-    time-delta 为time-interval提供可变性，相邻数据的时间间隔具体为(time-interval - time-delta, time-interval + time-delta)
-    count 共产生多少条数据，将覆盖除time-start的其它所有参数
-    realtime 产生数据过程中是否需要等待，等待时间为两条数据的间隔时间。无参数，默认为False

## 3. 字段参数
    字段默认配置在data.fragment，其中key是字段的名称，value是字段的值是什么类型。这个类型具体定义在raw_data.py中，每个value都必须在raw_data.py中找到对应的定义。
    字段参数可以通过--fragments参数来定义，格式为"--fragments key1=value1 key2=value2"

## 4. 输出参数
    定义数据具体的输出类型，格式，位置。
    类型包括file, kafka, es
    格式包括json, csv
    位置对于不同的类型，设置对应的参数。

## 5. 帮助信息
```
usage: start.py [-h] [-v] [-q] [--time-fragment TIME_FRAGMENT]  
                [--time-format TIME_FORMAT] [--time-start TIME_START]  
                [--time-end TIME_END] [--time-duration TIME_DURATION]  
                [--time-interval TIME_INTERVAL] [--time-delta TIME_DELTA]  
                [--count COUNT] [--realtime {true,false}]  
                [--fragments [INPUT_FRAGMENTS [INPUT_FRAGMENTS ...]]]  
                [--output] [--output-type OP_TYPE] [--output-file OP_FILE]  
                [--output-format OP_FORMAT] [--output-bootstrap OP_BOOTSTRAP]  
                [--output-topic OP_TOPIC]  
                [--output-es-hosts [OP_ES_HOSTS [OP_ES_HOSTS ...]]]  
                [--output-index OP_INDEX]  
  
Customize your special data  
  
optional arguments:  
  -h, --help            show this help message and exit  
  -v, --verbose         show more detail info  
  -q, --quite           quite standard output  
  
Control time principle of data:  
  --time-fragment TIME_FRAGMENT  
                        the fragment's name of time  
  --time-format TIME_FORMAT  
                        specify the format of time.Available format for string  
                        is along with time module, or you can inputtimestamp  
                        or mill(timestamp)  
  --time-start TIME_START  
                        specify the start time. Defaults to current time.  
  --time-end TIME_END   specify the end time. Note: it would not take effect  
                        while --count provide.  
  --time-duration TIME_DURATION  
                        how long logs you need to produce. Note: it would not  
                        take effect when --time-end is provided.  
  --time-interval TIME_INTERVAL  
                        the time gap of two items.  
  --time-delta TIME_DELTA  
                        adjust the interval, make two items has dynamic time  
                        gap.  
  --count COUNT         the count of items to produce. Note: It would disable  
                        --time-end setting.  
  --realtime {true,false}  
                        realtime make two items wait the interval time.  
  
Control data content:  
  --fragments [INPUT_FRAGMENTS [INPUT_FRAGMENTS ...]]  
                        additional fragments. key-type separate as '=',  
                        fragments separate as space  
  
Control data output:  
  --output  
  --output-type OP_TYPE  
                        the type of output, current available values: kafka,  
                        es, file.  
  --output-file OP_FILE  
                        specify the file path while type setting to file  
  --output-format OP_FORMAT  
                        specify the format of output contents.  
  --output-bootstrap OP_BOOTSTRAP  
                        specify the kafka's bootstrap server while type  
                        setting to kafka  
  --output-topic OP_TOPIC  
                        specify the kafka's topic while type setting to kafka  
  --output-es-hosts [OP_ES_HOSTS [OP_ES_HOSTS ...]]  
                        specify the ElasticSearch's hosts while type setting  
                        to ElasticSearch  
  --output-index OP_INDEX  
                        specify the ElasticSearch's index while type setting  
                        to ElasticSearch  
```

## 6. 示例
```bash
    ./start.py --output-type file --output-format json --count 4 --realtime false
```
表示从当前时间开始，输出4条日志到文件中，非实时数据。
```bash
    ./start.py --time-start 1601481600 --time-format "%m--%d %H:%M:%S" --time-interval 60 --time-delta 0 --time-duration 7200 --output-type kafka --output-bootstrap 192.168.31.132:9092 --topic test1
```
表示从2020/10/01 00:00:00 开始，产生2小时的数据，每条数据之间的间隔是（60-10, 60+10）秒，输出到kafka，服务地址192.168.31.132:9092，topic为test1
