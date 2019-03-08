#!/usr/bin/env python
import json
from kafka import KafkaConsumer

class Consumer():
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='100.96.0.22:9092',
                                 auto_offset_reset='largest', 
                                 enable_auto_commit=True)
        consumer.subscribe(['gnmi-telemetry'])

        for message in consumer:
                out = json.loads( message.value )
                print(json.loads(message.value))
                print(type(out))

                # find index of "key"; "name" succeeding that occurrence will always be the interface name
                index_of_key = out.find("key")
                print(index_of_key)
                if index_of_key != -1:
                    name_index = out[index_of_key:].find("name")
                    print(name_index)
                    if name_index != -1:
                        # find the first occurence of " to grep name between quotes
                        intf_name = out[name_index + 9 : out[name_index + 9:].find('"')]
                        print(intf_name)

                        #find index of oper-status
                        index_of_operstatus = out.find("oper-status")
                        print(index_of_operstatus)
                        if index_of_operstatus != -1:
                            #get substring starting from oper-status
                            operstatus_substr = out[index_of_operstatus:]
                            # finde the first occurence of stringVal from there
                            index_of_oper_status_string = out[index_of_operstatus:].find("stringVal")
                            print("here: " + str(index_of_oper_status_string))
                            if index_of_oper_status_string != -1:
                                # grep two characters succeeding "stringVal" : "
                                oper_status_val = operstatus_substr[index_of_oper_status_string + 13 : index_of_oper_status_string + 17]
                                print(oper_status_val)

                                if (oper_status_val == "DOWN"):
                                    # find which interface it is
                                    print("Intf %s, status %s"%(intf_name, oper_status_val))


def main():
    consumer =  Consumer()
    consumer.run()


if __name__ == "__main__":
    main()

