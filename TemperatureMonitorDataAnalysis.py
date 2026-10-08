import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

file = open("Datalog.txt") 
numberOfReadings = 0
buffer = file.readline().split(";")
numberOfReadings+=1

#setting start date as a day in the first reading at midnight
x = buffer[0].find(" ")
buffer = buffer[0][:x].split("-")
startDate = dt.datetime(int(buffer[2]),int(buffer[1]),int(buffer[0])) 

#reading the number of lines in the file
for buffer in file:
    numberOfReadings+=1
file.close()

Data = np.zeros((12,numberOfReadings))

#storing data to the array
file = open("Datalog.txt")
i = 0
for line in file:
    buffer = line.split(";")
    for j in range (1,11):
        Data[j,i] = float(buffer[j])
    if buffer[11] == "closed\n":
        Data[11,i] = 1.
    else :
        Data[11,i] = 0.
    buffer = buffer[0].split(" ")
    date = buffer[0].split("-")
    time = buffer[1].split(":")
    Data[0,i] = (dt.datetime(int(date[2]),int(date[1]),int(date[0]),int(time[0]),int(time[1])) - startDate) / dt.timedelta(1.) #this recalculates date as a number of days since midnight of the first day of readings
    i+=1

#setting up the x axis in all the plots
fig, ax = plt.subplots(ncols=2,nrows=2)
for column in range(2):
    for row in range(2):
        ax[row,column].set_xlabel("Time [days]")
        ax[row,column].set_xticks(range(0,11))

#top left plot
ax[0,0].set_title("Temperature inside")
ax[0,0].set_ylabel("Temperature [°C]")
ax[0,0].plot(Data[0],Data[2],color = 'blue',label = 'DHT sensor')
ax[0,0].plot(Data[0],Data[6],color = 'red',label = 'thermistor in the Sun')
ax[0,0].plot(Data[0],Data[8],color = 'orange',label = 'hidden thermistor')
ax[0,0].legend()

#top right plot
ax[0,1].set_title("Temperature outside")
ax[0,1].set_ylabel("Temperature [°C]")
ax[0,1].plot(Data[0],Data[10],color = 'green')

#bottom left plot
ax[1,0].set_title("Humidity inside")
ax[1,0].set_ylabel("Humidity [%]")
ax[1,0].plot(Data[0],Data[1])

#bottom right plot
ax[1,1].set_title("Photoresistor readings")
ax[1,1].set_ylabel("Resistance [Ω]")
ax[1,1].set_ylim(-100,20000)
ax[1,1].plot(Data[0],Data[4],color = 'purple')

plt.show()
