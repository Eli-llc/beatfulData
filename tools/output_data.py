import json
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError

from common.error import UnknownOutPutFormat
from common.log import logger


class OutputData:
    def __init__(self, args):
        logger.debug("Start class OutputData!")
        self.content_format = args.op_format.upper()
        self.output_type = args.op_type.upper()
        if self.output_type == "FILE":
            self.fp = open(args.op_file, "w")
            self.csv_list = []
        elif self.output_type == "KAFKA":
            # check topic exists
            self.topic = args.op_topic
            kafka_topic = NewTopic(name=self.topic, num_partitions=1, replication_factor=1)
            client = KafkaAdminClient(bootstrap_servers=args.op_bootstrap)
            try:
                client.delete_topics([kafka_topic])
                client.create_topics([kafka_topic])
            except KafkaError:
                logger.warn("delete or create kafka topic raised error, ignore it!")
            self.producer = KafkaProducer(bootstrap_servers=args.op_bootstrap)

    def to_file(self, fragments_values):
        message = self.transfer_format(fragments_values)
        self.fp.write(message + "\n")

    def transfer_format(self, fragments_values):
        if self.content_format == "JSON":
            message = json.dumps(fragments_values, ensure_ascii=False)
        elif self.content_format == "CSV":
            values = [str(x) for x in fragments_values.values()]
            message = ",".join(values)
        else:
            message = "Format: {} is not support!".format(self.content_format)
            raise UnknownOutPutFormat(message)
        return message

    def to_kafka(self, fragments_values):
        # message = json.dumps(fragment_with_value, ensure_ascii=False)
        message = self.transfer_format(fragments_values)
        print(message)
        self.producer.send(self.topic, bytes(message, encoding="utf-8"))

    def to_es(self, fragment_with_value):
        pass

    def close(self):
        logger.info(f"items already output finished, close resource!")
        if self.output_type == "FILE":
            self.fp.close()
        elif self.output_type == "KAFKA":
            self.producer.close()
