#Server Mod
from code import interact
from glob import glob
import os
import time
import threading
from turtle import Turtle
import main as single
import main_multi as multi
from loghelper import log
import json
time_interval=720   #默认签到间隔时间，单位minute(分钟)
mod=1  #单用户模式/自动判断
def runingtime():
    return int(time.time())
def control(time_interval,mod,event):
    last_time=runingtime()
    while True:
        now_time=runingtime()
        if now_time>last_time+time_interval*60:
            if mod==1:
                try:
                    single.main()
                except:
                    log.info("single_user start failed")

            else:
                try:
                    multi.main_multi(True)
                except:
                    log.info("multi_user start failed")
            last_time=runingtime()
        if event.is_set():
            log.info("Stoping")
            break
        log.info("The Next check time is {}s".format(last_time-now_time+time_interval*60))
        time.sleep(20)
def command():
    global mod
    global time_interval
    help="command windows\nstop:stop server\nreload:reload config and refish tiem\nsingle:test single config\nmulit:test mulit conifg\nmod x:x is refer single or multi 1 is single 2 is multi\nadd 'yourcookie'\nset user attribute value: such set username(*.json) enable(attribute) Ture(value)\ntime x:set interval time (minute)"
    log.info(help)
    while True: 
        command=input()
        if command=="help" or command=="?" or command=="":
            log.info(help)
        if command=="stop" or command=="exit":
            return False

        if command=="reload":
            return True
        if command=="test":
            try:
                single.main()
            except:
                log.info("single_user start failed")
        if command=="single":
            try:
                single.main()
            except:
                log.info("single_user start failed")
        if command=="mulit":
            try:
                multi.main_multi(True)
            except:
                log.info("multi_user start failed")
        command=command.split(' ')
        for i in range(0,len(command)):
            if command[i]=="time":
                if len(command)==2:
                    time_interval=int(command[1])
                    log.info("switching interval to {} minute".format(mod))
            if command[i]=="mod":
                if len(command)==2:
                    
                    if mod >2 or mod <0:
                        log.info("error mod")
                    else:
                        mod=int(command[1])
                        log.info("switching mod to {}".format(mod))
                else:
                    log.info("Error Command")
            if command[i]=="add":
                if len(command)==2:

                    log.info("adding")
                    if (mod==1):
                        name="config"
                    else:
                        log.info("Plase input your config name(*.json):")
                        name=input()
                    config = {
                    'enable': True, 'version': 5,
                    'account': {
                         'cookie': command[1],
                         'login_ticket': '',
                         'stuid': '',
                         'stoken': ''
                    },
                        'mihoyobbs': {
                            'enable': True, 'checkin': True, 'checkin_multi': True, 'checkin_multi_list': [2, 5],
                            'read_posts': True, 'like_posts': True, 'un_like': True, 'share_post': True
                        },
                        'games': {
                            'cn': {
                                'enable': True,
                                'genshin': {'auto_checkin': True, 'black_list': []},
                                'hokai2': {'auto_checkin': False, 'black_list': []},
                                'honkai3rd': {'auto_checkin': False, 'black_list': []},
                                'tears_of_themis': {'auto_checkin': False, 'black_list': []},
                            },
                            'os': {
                                'enable': False, 'cookie': '',
                                'genshin': {'auto_checkin': False, 'black_list': []}
                            }
                        }
                        }
                        
                        
                    file_path = os.path.dirname(os.path.realpath(__file__)) + "/config/"+name+".json"
                    file=open(file_path,'w')
                    file.write(json.dumps(config))
                    file.close()
                else:
                    log.info("Error Command")
            if command[i]=="set":
                if len(command)==4:
                    file_path = os.path.dirname(os.path.realpath(__file__)) + "/config/"+command[1]+".json"
                    if os.path.exists(file_path)==False:
                        log.info("User is not exist")
                    else:
                        with open(file_path, "r") as f:
                            new_conifg=json.load(f)
                            value=command[3]
                            if (command[3]=="true"):
                                value=True
                            if (command[3]=="false"):
                                value=False
                            if (command[3].isdigit()):
                                value=int(command[3])
                            new_conifg[command[2]]=value

                            file=open(file_path,'w')
                            file.write(json.dumps(new_conifg))
                            file.close()


if __name__=='__main__':
    log.info('Running in Server Mod')
    time_interval = 720
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/config/config.json"
    if os.path.exists(file_path):
        mod=1
    else:
        mod=2

    while True:
        log.info("switching to mod {}".format(mod))
        t1_stop = threading.Event()
        thread1 = threading.Thread(name='time_check',target= control,args=(time_interval,mod,t1_stop))
        thread1.start()
        
        if command():
            t1_stop.set()
            continue
        else:
            t1_stop.set()
            break
               




    