import threading 
#this is for python 3.0 and above. use import thread for python2.0 versions
from threading import*
import time

d={} #'d' is the dictionary in which we store data in key value formate

#create operation
def create(key,value,timeout=0):
    if key in d:
        print("error: this key already exists") #error message1
    else:
        if(key.isalpha()):
            if len(d)<(1024*1024*1024) and value<=(16*1024*1024): #constraints for file size less than 1GB and Jasonobject value less than 16KB 
                if timeout==0:
                    l=[value,timeout]
                else:
                    l=[value,time.time()+timeout]
                if len(key)<=32: #constraints for input key_name capped at 32chars
                    d[key]=l
            else:
                print("error: Memory limit exceeded!! ")#error message2
        else:
            print("error: Invalind key_name!! key_name must contain only alphabets and no special characters or numbers")#error message3

#for read operation            
def read(key):
    if key not in d:
        print("error: given key does not exist in database. Please enter a valid key") #error message4
    else:
        b=d[key]
        if b[1]!=0:
            if time.time()<b[1]: #comparing the present time with expiry time
                stri=str(key)+":"+str(b[0]) #to return the value in the format of JasonObject i.e.,"key_name:value"
                return stri
            else:
                print("error: time-to-live of",key,"has expired") #error message5
        else:
            stri=str(key)+":"+str(b[0])
            return stri

        
#for delete operation
def delete(key):
    if key not in d:
        print("error: given key does not exist in database. Please enter a valid key") #error message4
    else:
        b=d[key]
        if b[1]!=0:
            if time.time()<b[1]: #comparing the current time with expiry time
                del d[key]
                print("key is successfully deleted")
            else:
                print("error: time-to-live of",key,"has expired") #error message5
        else:
            del d[key]
            print("key is successfully deleted")
#for modify operation 
def modify(key,value):
    b=d[key]
    if b[1]!=0:
        if time.time()<b[1]:
            if key not in d:
                print("error: given key does not exist in database. Please enter a valid key") #error message6
            else:
                l=[]
                l.append(value)
                l.append(b[1])
                d[key]=l
        else:
            print("error: time-to-live of",key,"has expired") #error message5
    else:
        if key not in d:
            print("error: given key does not exist in database. Please enter a valid key") #error message6
        else:
            l=[]
            l.append(value)
            l.append(b[1])
            d[key]=l


#run with some data

create("year",2021)
#to create a key wirh key_name, value given and with no time-to-live property
create("Dec",31)
#add another key

read("year")
#read value 
#it return the value of the respective key in jasonobject formate
#output: 'year:2021'


read("Dec")
#read secound value 
#it return the value of the respective key in jasonobject formate
#output: Dec:31


create("Dec",22)
#it returns an ERROR since the key_name already exists in the database
#To overcome this error 
#either use modify operation to change the value of a key
#or use delete operation and recreate it
#output: error: this key already exists

modify("Dec",55)
#it replaces the initial value of the respective key with new value 
read("Dec")
#read update value
#output: Dec:55

delete("Dec")
#it deletes the respective key and its value from the database(memory is also freed)
read("Dec")
#show error: given key does not exist in database
#output: key is successfully deleted
        #error: given key does not exist in database. Please enter a valid key


create("NewYear",2021,60)
#after 60sec(1_min)
read("NewYear")
#show error: time-to-live of NewYear has expired
#update error: time-to-live of NewYear has expired
