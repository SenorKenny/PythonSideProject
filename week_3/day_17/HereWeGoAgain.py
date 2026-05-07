#back to the bot


import time
import datetime


from config import config
import fetcher
import decision
import parser
import output
import storage



i=0

def main():
    i=0
    start_time=datetime.datetime.now()
    schema,purchased=storage.load_files()
    try:
        while True:
            
            i=i+1
            print(f"Loop {i}")
            
            url=config["url"]
            converted_request,Status_code=fetcher.url_requester(url)
            boolean_dictionary=parser.json_parser(converted_request,schema,purchased)
            decision.status_updater(schema,boolean_dictionary)
            schema,fails=decision.buyer(schema,boolean_dictionary,purchased)
            storage.file_saver(schema,purchased,boolean_dictionary)
            storage.logger(purchased,fails)
            time.sleep(10)
    except KeyboardInterrupt:
        output.terminaloutput(start_time,purchased,schema,i)

if __name__ == "__main__":
    main()