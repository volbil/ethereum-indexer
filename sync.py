from apscheduler.schedulers.blocking import BlockingScheduler
from service.sync import sync_index

background = BlockingScheduler()
background.add_job(sync_index, "interval", seconds=30)
background.start()
