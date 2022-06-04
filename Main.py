import time
import datetime
import sched
from Scraper import scraper
from Pexcel import write_data

event_schedule = sched.scheduler(time.time, time.sleep)
links = str(input('Insira os links separados por vírgula: ')).split(',')

def next_int(iteration_time:int):
    t = datetime.timedelta(hours = datetime.datetime.now().hour, minutes = datetime.datetime.now().minute + iteration_time/60)
    return t

def log(string:str):
    file = open('log.txt', 'w+')
    file.write(string)
    return None

def use(urls):
    listp = []
    #[[[]],[[]]]
    for i in range(len(urls)):
        products = scraper(f'{urls[i]}')
        listp.append(products)
    for product in listp:
        for pro in product:
            try:
                if int(pro[2]) > 70:
                    print(f'O produto {pro[3]} está com {pro[2]} de desconto!')
            except:
                None
    write_data(listp)
def bot():
    use(links)
    event_schedule.enter(600, 1, bot)
    log(str(next_int(600)))
    print(f'A proxima iteracao sera {next_int(600)}')
    



event_schedule.enter(1, 1, bot)
event_schedule.run()
