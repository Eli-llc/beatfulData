import json
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError
from elasticsearch import Elasticsearch

from common.error import UnknownOutPutFormat, UnknownOutPutType
from common.log import logger


class OutputData:
    def __init__(self, args):
        self.args = args

    def __enter__(self):
        logger.debug("Start class OutputData!")
        self.content_format = self.args.op_format.upper()
        self.output_type = self.args.op_type.upper()
        if self.output_type == "FILE":
            self.fp = open(self.args.op_file, "w")
            self.csv_list = []
        elif self.output_type == "KAFKA":
            # check topic exists
            self.topic = self.args.op_topic
            kafka_topic = NewTopic(name=self.topic, num_partitions=1, replication_factor=1)
            client = KafkaAdminClient(bootstrap_servers=self.args.op_bootstrap)
            try:
                client.delete_topics([kafka_topic])
                client.create_topics([kafka_topic])
            except KafkaError:
                logger.warn("delete or create kafka topic raised error, ignore it!")
            self.producer = KafkaProducer(bootstrap_servers=self.args.op_bootstrap)
        elif self.output_type == "ES" or self.output_type == "ElasticSearch".upper():
            self.es = Elasticsearch(hosts=self.args.op_es_hosts,
                                    sniff_on_start=True,
                                    # sniff_on_connection_fail=True,
                                    sniffer_timeout=20,
                                    # http_auth=('user', 'secret')
                                    )
            self.es_index = self.args.op_index
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"items already output finished, close resource!")
        if self.output_type == "FILE":
            self.fp.close()
        elif self.output_type == "KAFKA":
            self.producer.close()
        elif self.output_type == "ES" or self.output_type == "ElasticSearch".upper():
            self.es.close()

    def _transfer_format(self, fragments_values):
        if self.content_format == "JSON":
            message = json.dumps(fragments_values, ensure_ascii=False)
        elif self.content_format == "CSV":
            values = [str(x) for x in fragments_values.values()]
            message = ",".join(values)
        else:
            message = "Format: {} is not support!".format(self.content_format)
            raise UnknownOutPutFormat(message)
        return message

    def to_file(self, fragments_values):
        message = self._transfer_format(fragments_values)
        self.fp.write(message + "\n")

    def to_kafka(self, fragments_values):
        # message = json.dumps(fragment_with_value, ensure_ascii=False)
        message = self._transfer_format(fragments_values)
        self.producer.send(self.topic, bytes(message, encoding="utf-8"))

    def to_es(self, fragment_with_value):
        self.es.index(index=self.es_index, body=fragment_with_value)

    def to_dest(self, op_type, fragment_with_value):
        if op_type == "FILE":
            self.to_file(fragment_with_value)
        elif op_type == "KAFKA":
            self.to_kafka(fragment_with_value)
        elif "ES" in op_type or "ElasticSearch".upper() in op_type:
            self.to_es(fragment_with_value)
        else:
            message = "Could not handle output type {}!".format(op_type)
            raise UnknownOutPutType(message)
