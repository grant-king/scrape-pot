#first used pip install python-crontab
from crontab import CronTab
#get access to crontab on windows
#call task defined in 'testfile.tab'
#cron = CronTab(tabfile='testfile.tab')

#alternatively, define the task according to cron's syntax
cron = CronTab(tab="""* * * * * command""")

#create a new job and define the task to be executed by command line
job = cron.new(command='python scrape_save.py scrape_log.py')

#run every 23 hours; no duplicates but sample from full range of day-times
job.hour.every(23)

#add this job to cron
cron.write()
