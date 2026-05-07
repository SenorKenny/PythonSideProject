import datetime

def terminaloutput(start_time,purchased,schema,i):
    end_time=datetime.datetime.now()
    print("="*100)
    print(f"Script started at {start_time}")
    print(f"Products purchased: {len(purchased)}")
    print(f"Number of products we're watching:{len(schema)}")
    print(f"Number of loops: {i}")
    print(f"End time: {end_time}")
    print("="*100)
