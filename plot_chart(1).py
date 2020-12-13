from matplotlib import pyplot as plt
import matplotlib.pyplot as mpld3
import numpy as np 
from datetime import datetime
import os
  
home_dir=os.getenv("HOME") + "/wellnessapp/"  
# Reading dataset 
dates = []
time_taken = []
app_list = []
main_dict = {}

def make_autopct(values):
    def my_autopct(pct):
    	total = 0
    	for i in range(len(values)):
    		total = total + int(values[i])
    	val = int(round((pct)*total/100.0))
    	return '{p:.2f}%  ({v:.2f})'.format(p=pct,v=float(val/60))
    return my_autopct

def app_usage_plot():
	#Plot for app usage
	for dat in open(home_dir + "foregroundtime.csv").readlines():
		if dat in ['\n']:
			continue
		else:
			for apps in (dat.split(':',1)[1:]):
				app_info = {}
				for x in apps.strip('{}').split(',')[:-1]:
					app_info[str(x.split(':')[0])] = x.split(':')[1]
			main_dict[dat.split(':',1)[0].strip()] = app_info
	#print(main_dict)

	for dat in main_dict :
		today_dat = str(datetime.today().strftime('%Y-%m-%d'))
		if str(dat) == today_dat:
			for apps in main_dict[dat]:
				app_list.append(apps)
				time_taken.append(main_dict[dat][apps])

			# Creating plot 
			fig = plt.figure(figsize =(10, 5))
			plt.pie(time_taken, autopct=make_autopct(time_taken))  
			plt.legend(app_list,loc='best', bbox_to_anchor=(-0.1, 1.))  
			plt.savefig(home_dir + 'app_usage_plot.png')
			#plt.show()
	total_work_hours = 0
	for i in time_taken:
		total_work_hours = total_work_hours+ int(i)
	#print("Total work hours:{}".format(total_work_hours/(60*60)))


def internet_usage_plot():
	#Reading internet usuage dataset
	date_time = []
	upload_speed = []
	download_speed = []
	
	for line in open(home_dir + "internetspeed.csv").readlines()[1:]:
		#speed = []
		today_dat = str(datetime.today().strftime('%Y-%m-%d'))
		dat = " "
		dat = dat + str(line.split(' ')[0])
		if str(dat.strip()) == today_dat:
			date = str(str(line.split(',')[0]).split(' ')[1]).split('.')[0]
			date_time.append(str(date.split(':')[0])+":"+str(date.split(':')[1]))
			upload_speed.append(round(float(line.split(',')[1].strip('MB\n')),3))
			download_speed.append(round(float(line.split(',')[2].strip('MB\n')),3))


	# Plotting internet speeds
	fig = plt.figure(figsize = (10, 5))
	plt.plot(date_time, upload_speed,label = "Upload Speed")
	plt.plot(date_time, download_speed,label = "Download Speed")
	plt.xlabel("Time of Day")
	plt.ylabel("Speed(Mbps)")
	plt.legend(loc='best')
	plt.savefig(home_dir + 'internet_usage.png')
	#plt.show()

def total_meeting_hours():
	#Plot for meeting times

	meet_times = {}
	#Creating dataset
	for dat in open(home_dir + "meeting_usage.csv").readlines()[1:]:
		dat1 = str(dat.split(' ')[0]).strip()
		if dat1 in meet_times.keys():
			meet_times[dat1] = meet_times[dat1] + (int(dat.split(',')[-1])/60)
		else:
			meet_times[dat1] =  int(dat.split(',')[-1]) / 60
	#print(meet_times)
	return meet_times

def idle_time_plot():
	#Plot for idle time
	idle_times = {}
	for line in open(home_dir + "idle_time.csv").readlines()[1:]:
		dat1 = str(line.split(' ')[0]).strip()
		if dat1 in idle_times.keys():
			idle_times[dat1] = idle_times[dat1] + (int(line.split(',')[-1])/(60*60))
		else:
			idle_times[dat1] =  int(line.split(',')[-1]) / (60*60)
	#print(idle_times)
	return idle_times

def plot_mutiple_bars():

	m_time = total_meeting_hours()
	i_time = idle_time_plot()
	x_axis = sorted(list(set(m_time.keys()) | set(i_time.keys())))
	meet = []
	idle = []

	for i in x_axis:
		if i in m_time.keys():
			meet.append(m_time[i])
		else:
			meet.append(0)

		if i in i_time.keys():
			idle.append(i_time[i])
		else:
			idle.append(0)

	ind = np.arange(len(x_axis))
	width = 0.3
	fig = plt.figure(figsize = (10, 5))
	plt.bar(ind, meet , width, label='Meeting time')
	plt.bar(ind + width, idle, width, label='Idle time')
	plt.xlabel('Dates')
	plt.ylabel('Total time (hours)')
	plt.xticks(ind + width / 2, x_axis)
	plt.legend(loc='best')
	#plt.show()
	plt.savefig(home_dir + 'meetingvsidle.png')


	
app_usage_plot()
internet_usage_plot()
plot_mutiple_bars()