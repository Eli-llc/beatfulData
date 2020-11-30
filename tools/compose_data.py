import datetime
import random
import time

from common.log import logger


class ComposeData:
    def __init__(self, args, raw):
        logger.info("Start class ComposeData")
        self.args = args
        self.raw = raw

    def get_time(self):
        time_fragment_name = self.args.time_fragment
        time_format = self.args.time_format
        time_start = self.args.time_start
        if not time_start:
            # time start defaults to now
            time_start = datetime.datetime.now().timestamp()
        time_end = self.args.time_end
        time_duration = self.args.time_duration or 31536000  # defaults to 365 days
        if not time_end:
            # if not provide end time, calculate it as time start plus time duration
            time_end = time_duration + time_start
        time_interval = self.args.time_interval or 60
        time_delta = self.args.time_delta or 10
        count = self.args.count
        realtime = self.args.realtime
        current_time = time_start

        # for simple code
        def add_time(current_base_time):
            delta = random.randint(time_interval - time_delta, time_interval + time_delta)
            logger.debug(f"realtime was setting to {realtime}")
            if realtime:
                current_base_time = time.time() + delta
                sleep_time = delta
            else:
                sleep_time = 0
                current_base_time += delta
            return current_base_time, sleep_time

        # count has high priority
        sleep_time = 0
        if count > 0:
            while count > 0:
                time.sleep(sleep_time)
                current_time, sleep_time = add_time(current_time)
                return_time = {time_fragment_name: self.format_time(time_format, current_time)}
                logger.debug(f"get time is {return_time}")
                yield return_time
                count -= 1
        else:
            while current_time <= time_end:
                time.sleep(sleep_time)
                return_time = {time_fragment_name: self.format_time(time_format, current_time)}
                logger.debug(f"get time is {return_time}")
                yield return_time
                current_time, sleep_time = add_time(current_time)

    def fill_fragment_values(self, all_fragments: dict) -> dict:
        fragments_with_value = {}
        # replace fragments' value
        for key in all_fragments:
            category = all_fragments[key]
            values = self.raw.get_data(category)
            fragments_with_value[key] = random.choice(values)
        return fragments_with_value

    @staticmethod
    def format_time(time_format: str, timestamp=None):
        if not timestamp:
            cur_time_obj = datetime.datetime.now()
        else:
            cur_time_obj = datetime.datetime.fromtimestamp(timestamp)
        if "mill" in time_format.lower():
            return int(cur_time_obj.timestamp() * 1000)
        elif "timestamp" in time_format.lower():
            return int(cur_time_obj.timestamp())
        else:
            return cur_time_obj.strftime(time_format)
