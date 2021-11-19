import time
from smtp import SmtpClient
from gpu import NvidiaClient
import json
from obj import DictObj
import schedule
import datetime

last_free = None

def job():
    global last_free
    logfile = f"log/{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
    with open("data/email.json","r",encoding="utf-8") as f:
        smtp_config = DictObj(json.load(f))
    with open("data/subscribe.json","r",encoding="utf-8") as f:
        subscribe = json.load(f)
    with NvidiaClient() as gpu_client:
        usage = gpu_client.get_usage()
        cur_free = False
        for device in usage:
            if len(device["used_by"])==0:
                cur_free = True
                break
        # when state change
        if last_free is not None and last_free != cur_free:
            with SmtpClient(smtp_config.server,smtp_config.port,smtp_config.useSSL) as smtp_client:
                smtp_client.login(smtp_config.username,smtp_config.password)
                smtp_client.sendText(subscribe,subject="GPU MACHINE FREE NOTIFICATION",contain=json.dumps(usage,indent=4,ensure_ascii=False))
        last_free = cur_free
        with open(logfile,"a+",encoding="utf-8") as f:
            obj = {
                "usage":usage,
                "timestamp": datetime.datetime.now().timestamp(),
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            f.write(f"{json.dumps(obj,ensure_ascii=False)}\n")
            f.flush()


if __name__=="__main__":
    schedule.every(60).seconds.do(job)
    try:
        while True:
            schedule.run_pending()
            time.sleep(10)        
    except KeyboardInterrupt:
        schedule.clear()

