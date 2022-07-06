import math
import speedtest
import pandas as pd
import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler


def bytes_to_mb(size_bytes):
    i = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, i)
    size = round(size_bytes / power, 2)
    return size


filename = 'speedtest.csv'

# create new dataframe with 2 columns
download_column_name = 'download'
upload_column_name = 'upload'
date_column_name = 'date'

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=1)
def iterate_speedtest():
    wifi = speedtest.Speedtest()
    download_speed = wifi.download()
    upload_speed = wifi.upload()

    formatted_download_speed = bytes_to_mb(download_speed)
    formatted_upload_speed = bytes_to_mb(upload_speed)

    # if file does not exist, create it
    df = pd.read_csv(filename) if os.path.exists(filename) else pd.DataFrame(
        columns=[download_column_name, upload_column_name, date_column_name])
    # add new row to the end of the file
    new_line = {download_column_name: formatted_download_speed, upload_column_name: formatted_upload_speed,
                date_column_name: datetime.datetime.now()}

    print(f'adding new line in mbps: {new_line}')

    # save the file
    df = df.append(new_line, ignore_index=True)
    df.to_csv(filename, index=False)


scheduler.start()
