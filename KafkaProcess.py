import json
from kafka import KafkaProducer
import heapq

TOPIC_NAME = "try1"
COUNT = 0

runners_db = {}
runner_ts = {}

path = "/home/anduin/PycharmProjects/WisePrice/Phone/"
# KAFKA
def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


# KAFKA prducer
def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))

    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


def get_data_folder_list(root):
    path_const = "/home/anduin/PycharmProjects/WisePrice/Phone/"
    data_folder_list = os.listdir(root + path_const)
    return data_folder_list, root + path_const


def unzip_all_data_files(data_folder_list, _loc):
    for i in data_folder_list:
        _iloc = _loc + "/" + i
        get_bz2_list = os.listdir(_iloc)
        for j in get_bz2_list:
            if ".bz2" in j:
                ifinal = _iloc + "/" + j
                os.system('bzip2 -d ' + ifinal)



def get_specific(filename):
    with open(filename) as json_data:
        data = json.load(json_data)
        json_data.close()
    kafka_producer = connect_kafka_producer()



def get_specific(file_name):
    sample_file = open(file_name)
    kafka_producer = connect_kafka_producer()
    flag = True
    for line in sample_file:

        kafka_value = ""
        # print(line)
        json_line = json.loads(line)
        for mc in json_line['mc']:
            if 'marketDefinition' in mc:
                if 'marketType' in mc['marketDefinition']:
                    # print(mc['marketDefinition']['marketType'])
                    if mc['marketDefinition']['bettingType'] == "ODDS" and mc['marketDefinition'][
                        'marketType'] == "MATCH_ODDS" and mc['marketDefinition']['status'] == "OPEN" and flag:
                        # update Event Database
                        flag = False
                        kafka_value = kafka_value + "NM_" + str(mc['marketDefinition']['eventId']) + "_" + str(
                            mc['id']) + "_" + str(json_line['pt']) + "_"
                        kafka_key = "NM"
                        # PUBLISH MESSAGE
                        for runner in mc['marketDefinition']['runners']:
                            kafka_value = kafka_value + "NMR_" + str(runner['id']) + "_" + runner['name'] + "_" + str(
                                runner['status']) + "_"
                            runners_db[runner['id']] = {'startTime': json_line['pt'], 'endTime': None}
                        publish_message(kafka_producer, 'try1', kafka_key, kafka_value)  # KAFKA

                    if mc['marketDefinition']['bettingType'] == "ODDS" and mc['marketDefinition'][
                        'marketType'] == "MATCH_ODDS" and mc['marketDefinition']['status'] == "CLOSED":
                        kafka_value = kafka_value + "CM_" + str(mc['marketDefinition']['eventId']) + "_" + str(
                            mc['id']) + "_" + str(json_line['pt']) + "_"
                        for runner in mc['marketDefinition']['runners']:
                            kafka_value = kafka_value + "CMR_" + str(runner['id']) + "_" + runner['name'] + "_" + str(
                                runner['status']) + "_"
                            flag = True
                            # d = runners_db[runner['id']]
                            # d['endTime'] = json_line['pt']
                            # d['status'] = runner['status']
                            # runners_db[runner['id']] = d
                        kafka_key = "CM"
                        publish_message(kafka_producer, 'try1', kafka_key, kafka_value)  # KAFKA
                        # event_ts[mc['marketDefinition']['eventId']]=event_ts.get(mc['marketDefinition']['eventId'],[])+[(i,i['startTime'],i['endTime'])for i in d]
                if 'rc' in mc:
                    kafka_value = "RC_" + str(mc['id']) + "_" + str(json_line['pt']) + "_"
                    for rc in mc['rc']:
                        if rc['id'] in runners_db:
                            if rc['id'] not in runner_ts:
                                runner_ts[rc['id']] = []
                            heapq.heappush(runner_ts[rc['id']], (json_line['pt'], rc['ltp']))
                            kafka_value = kafka_value + "_" + str(rc['id']) + "_" + str(rc['ltp'])
                    kafka_key = "RR"
                    publish_message(kafka_producer, 'try1', kafka_key, kafka_value)


def parse_folder(folder_list, _loc):
    event_details = {}
    count = 0
    for f in folder_list:
        if "." in f:
            continue
        list_of_files = os.listdir(_loc + "/" + f)
        for file in list_of_files:
            file_name = _loc + "/" + f + "/" + file
            # print(file_name)

            count = get_all_event_name(file_name, event_details, file, count)
    return count
    # print(event_details)
    # print(len(event_details))

    # get_specific(file_name)


def get_all_


def get_all_event_name(file_name, event_details, file, count):
    sample_file = open(file_name)
    for line in sample_file:
        json_line = json.loads(line)
        for mc in json_line['mc']:
            count += 1
            print(mc['marketDefinition']['eventName'], count)
            # event_details['file']={
            #     'eventName':json_line['mc']['marketDefinition']['eventName'],
            #     'fileLocation':file
            # }
    return count


def testingGround():
    sample_file = open('football_basic_sample')
    for line in sample_file:
        json_line = json.loads(line)
        for mc in json_line['mc']:
            if 'marketDefiniton' in mc:
        # check if event in database

    # return event_details


if __name__ == '__main__':
    import os

    testingGround()
    data_folder_list, _loc = get_data_folder_list(os.getcwd())
    print(data_folder_list)
    # folder_list=['27507963','27517298','27517299','27517300','27517302','27517303','27517304','27517305','27517306','27517307','27517308','27517309']
    count = parse_folder(data_folder_list, _loc)
    # unzip_all_data_files(data_folder_list,_loc)

