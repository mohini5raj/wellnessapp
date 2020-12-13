import time
from time import perf_counter
import os
from subprocess import Popen, PIPE
import sys
import csv
import os.path
import datetime
import subprocess

time_dict = {}
stack = []
home_dir=os.getenv("HOME")

def check_display_state():
	command = "ioreg -w 0 -c IODisplayWrangler -r IODisplayWrangler | grep CurrentPowerState | awk -F \"CurrentPowerState\\\"=\" '{print $2}' | awk -F \",\" '{print $1}'"
	output = os.popen(command)
	if '4' in str(output.read().split()) :
		return 1 
	else :
		return 0

def create_csvs():
	global home_dir
	if not os.path.isdir(home_dir+"/wellnessapp"):
		os.mkdir(home_dir+"/wellnessapp")
	file_list=["idle_time.csv","internetspeed.csv","foregroundtime.csv","meeting_usage.csv"]
	for filename in file_list:
		file_path=home_dir+"/wellnessapp/"+filename
		file_exists = os.path.isfile(file_path)
		if not file_exists:
			with open(os.path.join(home_dir+"/wellnessapp/", filename), 'w') as fp: 
				pass

def delete_csv_entries():
	global home_dir
	file_list=["idle_time.csv","internetspeed.csv","meeting_usage.csv"]	
	for filename in file_list:
		lines = list()
		with open(home_dir+"/wellnessapp/"+filename, 'r') as readFile:
			reader = csv.reader(readFile)
			for row in reader:
				lines.append(row)
				for field in row:
					try:
						if (datetime.datetime.now()-datetime.datetime.strptime(field, '%Y-%m-%d %H:%M:%S.%f')).days > 7:							
							lines.remove(row)
							break
					except ValueError:
						pass

		with open(home_dir+"/wellnessapp/"+filename, 'w') as writeFile:

			writer = csv.writer(writeFile)
			writer.writerows(lines)

def appchange():
	app2 = os.popen("osascript -e 'tell application \"System Events\"' -e 'set frontApp to name of first application process whose frontmost is true' -e 'end tell'")
	app2 = app2.read()
	app2 = app2.replace("\n","")
	return app2

def check_app_time():

	csvpath = home_dir+"/wellnessapp/foregroundtime.csv"
	totaltime = 0
	value = 0
	app_list = []
	time_dict = {}
	line_to_insert = {}
	app = os.popen("osascript -e 'tell application \"System Events\"' -e 'set frontApp to name of first application process whose frontmost is true' -e 'end tell'")
	app = app.read()
	app = app.replace("\n","")
	valid_days = [0,1,2,3,4,5,6]
	app_times = ""
	script_start_time = int(time.time())

	while True:
		#print("I'm here")
		if datetime.datetime.today().weekday() in valid_days and check_display_state() == 1:
			time_dict = {}
			app_times = ""
			st = int(time.time())
			time.sleep(1)
			while appchange() == app and (int(time.time()) - st) % 60 != 0 :
				continue
			et = int(time.time())
			timetaken = et - st 
		
			time_dict[app] = timetaken
			totaltime = totaltime + timetaken
		
			app = appchange()		
			today = datetime.datetime.now()
			today_onlydate = today.strftime("%Y-%m-%d")
		
			fin = open(csvpath, "r")
			data = fin.read().splitlines(True)
			fin.close()

			if len(data) != 0 :
				main_dict = {}
				for dat in open(csvpath).readlines():
					if dat in ['\n']:
						continue
					else:
						for apps in (dat.split(':',1)[1:]):
							app_info = {}
							for x in apps.strip('{}').split(',')[:-1]:
								app_info[str(x.split(':')[0])] = x.split(':')[1]
						main_dict[dat.split(':',1)[0].strip()] = app_info

				last_element = list(main_dict.keys())[-1]
				agg_dict = main_dict[last_element]

				list1 = list(time_dict.keys())
				list2 = list(agg_dict.keys())
				applications = set(list1 + list2)

				if last_element == today_onlydate :
					data1 = data[0:len(data)-1]
					for application in applications:
						if application in time_dict and application in agg_dict :
							line_to_insert[application] = time_dict[application] + int(agg_dict[application])
						elif application in time_dict :
							line_to_insert[application] = time_dict[application]
						else:
							line_to_insert[application] = int(agg_dict[application])
						app_times = app_times + "{}:{},".format(application, line_to_insert[application])
					newdataline = "{}:".format(today_onlydate) + "{" + "{}".format(app_times) + "}\n"
					data1.append(newdataline)
					open(csvpath, 'w').close()
					csvfile = open(csvpath, 'a')
					print("Updating to CSV....")
					for line in data1 :
						csvfile.write("{}".format(line))
					csvfile.close()

				elif last_element != today_onlydate and len(data) != 5 :
					for application in time_dict.keys():
						app_times = app_times + "{}:{},".format(application, time_dict[application])
					newdataline = "{}:".format(today_onlydate) + "{" + "{}".format(app_times) + "}\n"
					csvfile = open(csvpath, 'a')
					print("Updating to CSV....")
					csvfile.write(newdataline)
					csvfile.close()

				elif last_element != today_onlydate and len(data) == 5 :
					data1 = data[1:len(data)]
					for application in time_dict.keys():
						app_times = app_times + "{}:{},".format(application, time_dict[application])
					newdataline = "{}:".format(today_onlydate) + "{" + "{}".format(app_times) + "}\n"
					data1.append(newdataline)
					csvfile = open(csvpath, 'w')
					print("Updating to CSV....")
					for line in data1 :
						csvfile.write("{}".format(line))
					csvfile.close()

			else :
				csvfile = open(csvpath, 'w')
				print("Updating to CSV....")
				for application in time_dict.keys():
					app_times = app_times + "{}:{},".format(application, time_dict[application])
				newdataline = "{}:".format(today_onlydate) + "{" + "{}".format(app_times) + "}\n"
				csvfile.write(newdataline)
				csvfile.close()

def check_meeting_time():
	csvpath = home_dir+"/wellnessapp/meeting_usage.csv"
	time_now = datetime.datetime.now()
	time_dict={}
	while True:
		webcount=0
		mccount=0
		#time_now = datetime.datetime.now()
		app1= os.popen("osascript \
			-e 'tell application \"System Events\"' \
			-e '    get every window of (every process ¬' \
			-e '        whose background only is false  ¬' \
			-e '        and visible is true)' \
			-e 'end tell'")
		app1 = app1.read()
		app1=app1.split(",")
		for i in range(0,len(app1)):
			if "application process Meeting Center" in app1[i]:
				mccount=mccount+1
				break
			if "application process Webex Teams" in app1[i]:
				webcount=webcount+1
				
		if webcount==2 or mccount==1:
			time.sleep(1)
			time_dict["Meeting"] = (datetime.datetime.now()-time_now).seconds
			continue
		else:
			
			if "Meeting" in time_dict.keys():
				file_exists = os.path.isfile(csvpath)
				file_stat=os.stat(csvpath).st_size
				with open(csvpath, 'a', newline='') as file:
					writer = csv.writer(file)
					headers=["Start Time", "End Time","Meeting time in minutes"]
					if file_stat==0:
						writer.writerow(headers)
					if int(time_dict["Meeting"]/60) > 0:
						writer.writerow([time_now,datetime.datetime.now(),int(time_dict["Meeting"]/60)])	
				time_dict={}
			time_now = datetime.datetime.now()



def check_internet_speed(): 
	csvpath = home_dir+"/wellnessapp/internetspeed.csv"
	import speedtest
	st=speedtest.Speedtest()
	download_speed=st.download()/(1024*1024)
	upload_speed=st.upload()/(1024*1024)
	file_exists = os.path.isfile(csvpath)
	file_stat=os.stat(csvpath).st_size

	with open(csvpath, 'a', newline='') as file:
		writer = csv.writer(file)
		if file_stat==0:
			writer.writerow(["Time", "Upload Speed", "Download Speed"])
		writer.writerow([datetime.datetime.now(),str(upload_speed)+"MB",str(download_speed)+"MB"])
		time.sleep(3600)


def check_idle_time():
	csvpath = home_dir+"/wellnessapp/idle_time.csv"
	idle_seconds_command = 'echo $((`ioreg -c IOHIDSystem | sed -e \'/HIDIdleTime/ !{ d\' -e \'t\' -e \'}\' -e \'s/.* = //g\' -e \'q\'` / 1000000000))'
	idle_sec_old=0
	idle_seconds=0
	while True:
		idle_sec_old=idle_seconds
		idle_seconds = os.popen(idle_seconds_command)  
		idle_seconds=idle_seconds.read()  
		if(int(idle_sec_old) > 600): 
			idle_time_end = datetime.datetime.now()
			idle_time_start = idle_time_end - datetime.timedelta(seconds = int(idle_sec_old))
			idle_seconds = os.popen(idle_seconds_command)  
			idle_seconds=idle_seconds.read() 
			file_exists = os.path.isfile(csvpath)
			file_stat=os.stat(csvpath).st_size
			if int(idle_seconds)==0 or int(idle_seconds) < int(idle_sec_old):
				with open(csvpath, 'a', newline='') as file:
					writer = csv.writer(file)
					if file_stat==0:
						writer.writerow(["Idle Time Start", "Idle Time End", "Idle Time Seconds"])
					writer.writerow([str(idle_time_start),str(idle_time_end),str(idle_sec_old).strip()])
		time.sleep(0.9)


if __name__ == "__main__":
	#if datetime.datetime.today().weekday() !=5 or datetime.datetime.today().weekday() !=6:
	if datetime.datetime.today().weekday() !=8 or datetime.datetime.today().weekday() !=9:
		create_csvs()
		delete_csv_entries()
		option=sys.argv[1]
		if int(option) == 1:
			check_app_time()
		elif int(option) == 2:
			while True:
				check_internet_speed()
				sleep(900)
		elif int(option) == 3:
			check_idle_time()
		elif int(option) ==4 :
			check_meeting_time()
