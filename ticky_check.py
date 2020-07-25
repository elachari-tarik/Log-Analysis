#!/usr/bin/env python3

import re
import operator
import csv

def getErrors(filename):
    err = {}
    with open(filename) as sysFile:
        for log in sysFile:
            log = log.strip()
            if (re.search("ERROR",log)):
                errType = re.findall('(?<=ERROR ).+(?=\ )', log)
                errType="".join(errType)   
                err[errType] = err.get(errType, 0) + 1        
    return err

def getUsers(filename):
    users = {}
    with open(filename) as sysFile:
        for log in sysFile:
            log = log.strip()
            user = re.findall('\((.*?)\)', log)
            user="".join(user)
            if user not in users.keys():
                users[user] = {}
                users[user]["ERROR"] = 0
                users[user]["INFO"] = 0  
            if (re.search("ERROR",log)):
                users[user]["ERROR"] +=1
            elif (re.search("INFO",log)):
                users[user]["INFO"] +=1                
    return users


def generate_user_statistics_csv(per_user):
    
    header = ['Username', 'INFO', 'ERROR']
    per_user = sorted(per_user.items(), key=operator.itemgetter(0))

    with open('user_statistics.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(i for i in header)

        for user in per_user:
            writer.writerow((user[0],user[1]['INFO'],user[1]['ERROR']))




def generate_error_csv(errors):
    header = ['Error', 'Count']
    errors = sorted(errors.items(), key = operator.itemgetter(1), reverse=True)    
    with open('error_message.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(i for i in header)

        for key in errors:
            writer.writerow((key[0],key[1]))





per_user = getUsers("syslog.log")

generate_user_statistics_csv(per_user)

errors = getErrors("syslog.log")
generate_error_csv(errors)
