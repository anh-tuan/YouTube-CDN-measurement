import requests
import os
import sys
import datetime
import mysql.connector
from mysql.connector import Error
import subprocess
import time
import schedule
import random


#**************************** Init *************************
error = 1
resCode = 0
connected = 'false'

#************************ Functions define *********************
def parseInfo(arg1):
   i = arg1.find('(')
   start = i + 2
   i = arg1.find(',')
   end = i - 1
   start_port = i + 2
   end_port = arg1.find(')', i)
   final_str = arg1[start:end] + ':' + arg1[start_port:end_port]
   return final_str;

def getIP(arg1):
   i = arg1.find('(')
   start = i + 2
   i = arg1.find(',')
   end = i - 1
   final_str = arg1[start:end]
   return final_str;

def geoIPlocation(ip):
	check_url = 'http://sea.anhtuan.eu/geoiploc/?f=text&loc=true&detail=true&ip=' + ip
	response = requests.get(check_url)
	answer = response.content.replace("<br>", "\n")
	return answer

def geoIPlocationMin(ip):
	check_url = 'http://sea.anhtuan.eu/geoiploc/?f=min&loc=true&detail=true&ip=' + ip
	response = requests.get(check_url)
	return response.content

def geoIPlocationSrcMin():
	check_url = 'http://sea.anhtuan.eu/geoiploc/?f=min&loc=true&detail=true'
	response = requests.get(check_url)
	return response.content

def getPingTime(ip):
	p = subprocess.Popen(["ping -c 5 " + str(ip)], stdout = subprocess.PIPE, shell=True)
	p.wait()
	#parse data
	if(p.poll() == 0):
		response = p.communicate()[0]
		i = response.find('dev =')
		j = response.find('/', i + 10)
		k = response.find('/', j + 1)
		time = response[j+1:k]
	else:
		time = '-1'
	return time

#********************* End functions defined ******************

def main():

	print "Starting..."

	video_id = ''
	log = open("output/out.log", "a")
	log.write(str(datetime.datetime.now()))
	log.write("\n")

	#******************** Connect database *********************
	print('Connecting to database...')
	try:
		conn = mysql.connector.connect(host='you_server_ip',
	                              database='your_db_name',
	                              user='your_username',
	                              password='your_password')
		if conn.is_connected():
			print('Connection to database established.')
			log.write("Connecting to database: Success\n")
		  
		  #Write data to database
			mycursor = conn.cursor()
			connected = 'true'
		else:
			print('Connection to database failed.')
			log.write("Connecting to dabatase: Failed\n")

	except Error as error:
		print(error)

	#******************* Getting Data from DB *************
	if(connected == 'true'):
		
		#Get random ID of video in list
		vid_id = random.randint(1, 50)

		mycursor.execute ("SELECT ParamValue FROM parameters WHERE ID='" + str(vid_id) + "'")
		data = mycursor.fetchall()
		for row in data:
			video_id = row[0]

	#*************** End Getting Data from DB *************

	#Get requester information
	dbSrcData = str(geoIPlocationSrcMin()).split(";")

	#get URL
	#url = "https://www.youtube.com/watch?v=" + sys.argv[1]

	if(video_id != ''):
		url = "https://www.youtube.com/watch?v=" + video_id
	else:
		url = "https://www.youtube.com/watch?v=kpBCzzzX6zA"

	print url

	#Get URL to store
	dbURL = url

	print "Connecting web server..."

	#set Header
	headers = {
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
	}

	#set Params
	params = (
	)

	#make Request
	response = requests.get(url, headers=headers, params=params, stream=True)

	#get destination IP & port
	dest_info = response.raw._fp.fp._sock.getpeername()

	#Check and create folder it not exist
	if not os.path.exists("output"):
	    os.makedirs("output")

	#delete old file
	if os.path.exists("output/response_youtube.html"):
	    os.remove("output/response_youtube.html")

	#write new file
	res = open("output/response_youtube.html", "w")
	res.write(response.content)

	#replacing characters
	content = response.content.replace("%20", " ")
	content = content.replace("%21", "!")
	content = content.replace('%22', '"')
	content = content.replace("%23", "#")
	content = content.replace("%24", "$")
	content = content.replace("%25", "%")
	content = content.replace("%26", "&")
	content = content.replace("%27", "'")
	content = content.replace("%28", "(")
	content = content.replace("%28", ")")
	content = content.replace("%2A", "*")
	content = content.replace("%2B", "+")
	content = content.replace("%2C", ",")
	content = content.replace("%2D", "-")
	content = content.replace("%2E", ".")
	content = content.replace("%2F", "/")
	content = content.replace("%3A", ":")
	content = content.replace("%3B", ";")
	content = content.replace("%3D", "=")
	content = content.replace("%3F", "?")
	content = content.replace("%40", "@")
	content = content.replace("%5B", "[")
	content = content.replace("%5D", "]")
	content = content.replace("%5F", "_")
	content = content.replace("%96", "-")
	content = content.replace("%A6", "|")
	content = content.replace("\u0026", "&")

	#print content
	print "Finishing receive web data. Parsing data..."

	#ignore first URL
	i = content.find('<script>')
	i = content.find('&url=https://', i + 10)
	#get second URL
	start = content.find('&url=https://', i + 10)
	#get the end of URL
	end_and = content.find('&type=', start + 10)
	end_comma = content.find(',type=', start + 10)

	end = -1

	#if in video url exist , or &, get this position
	if end_and < end_comma and end_and > -1:
		end = end_and
	elif end_and < end_comma and end_and == -1:
		end = end_comma
	elif end_and > end_comma and end_comma == -1:
		end = end_and
	elif end_and > end_comma and end_comma > -1:
		end = end_comma
	elif end_and == end_comma:
		end = end_and

	#it not error, get this video url
	if end != -1:
		video_url = content[start+5:end]
	else:
		video_url = ""

	#write log
	log.write("Positions: ")
	log.write(str(start))
	log.write("\t")
	log.write(str(end_and))
	log.write("\t")
	log.write(str(end_comma))
	log.write("\t")
	log.write(str(end))
	log.write("\n")

	log.write(url)
	log.write("\n")

	#Geo IP Location:
	dest_ip = getIP(str(dest_info))
	log.write("\n")
	log.write(str(geoIPlocation(dest_ip)))
	#Geo IP Location end

	pingTimeWeb = getPingTime(dest_ip)
	#print time

	#Get response from web to store
	dbWebData = str(geoIPlocationMin(dest_ip)).split(";")

	#if video url not empty and start with valid string
	if video_url != "" and video_url[0:8] == "https://":

		print "Finishing parsing data. Connecting to video playback server..."

		#write log
		log.write(video_url)

		#Get web data
		error = 0
		dbVideoURL = video_url	

		headers = {
		    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
		}

		params = (
		)

		#make request
		response = requests.get(video_url, headers=headers, params=params, stream=True)

		#get destination information
		dest_info = response.raw._fp.fp._sock.getpeername()

		#if succesful
		if response.status_code == 200:
			print 'Connected: 200'
			#log.write(parseInfo(str(dest_info)))

			#Geo IP Location:
			dest_ip = getIP(str(dest_info))
			log.write("\n")
			log.write(str(geoIPlocation(dest_ip)))
			#Geo IP Location end

			pingTimeVideo = getPingTime(dest_ip)

			#get video data
			dbVideoData = str(geoIPlocationMin(dest_ip)).split(";")
			resCode = 200

			log.write("Connected: 200")
			log.write("\n")

			#********** Write DB ***********
			if(connected == 'true'):
				sql = "INSERT INTO data (RunDateTime, URL, VideoURL, ResCode, "
				sql += "SrcIP, SrcCountry, SrcRegion, SrcCity, SrcISP, SrcAS, SrcZIP, SrcLat, SrcLon, SrcOrg, "
				sql += "WebIP, WebPing, WebCountry, WebRegion, WebCity, WebISP, WebAS, WebZIP, WebLat, WebLon, WebOrg, "
				sql += "VideoIP, VideoPing, VideoCountry, VideoRegion, VideoCity, VideoISP, VideoAS, VideoZIP, VideoLat, VideoLon, VideoOrg) "
				sql += "VALUES (NOW(), %s, %s, %s, "
				sql += "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
				sql += "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
				sql += "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				val = (dbURL, dbVideoURL, resCode, 
					dbSrcData[0], dbSrcData[1], dbSrcData[2], dbSrcData[3], dbSrcData[4], dbSrcData[5], dbSrcData[6], dbSrcData[7], dbSrcData[8], dbSrcData[9], 
					dbWebData[0], pingTimeWeb, dbWebData[1], dbWebData[2], dbWebData[3], dbWebData[4], dbWebData[5], dbWebData[6], dbWebData[7], dbWebData[8], dbWebData[9], 
					dbVideoData[0], pingTimeVideo, dbVideoData[1], dbVideoData[2], dbVideoData[3], dbVideoData[4], dbVideoData[5], dbVideoData[6], dbVideoData[7], dbVideoData[8], dbVideoData[9])

				mycursor.execute(sql, val)
				conn.commit()
				print("Record inserted.")
				log.write("Record inserted.\n")
			#********** End Write DB ***********

			#if os.path.exists("output/play.mp4"):
			#	os.remove("output/play.mp4")

			#f = open("output/play.mp4", "w")
			#f.write(response.content)
		#or error
		else:
			print '---- Failed. HTTP code: ',response.status_code
			#log.write(parseInfo(str(dest_info)))

			#Geo IP Location:
			dest_ip = getIP(str(dest_info))
			log.write("\n")
			log.write(str(geoIPlocation(dest_ip)))
			#Geo IP Location end

			pingTimeVideo = getPingTime(dest_ip)

			#Get video data
			dbVideoData = str(geoIPlocationMin(dest_ip)).split(";")
			resCode = response.status_code

			log.write("Failed:\t")
			log.write(str(response.status_code))
			log.write("\n")

			#********** Write DB ***********
			if(connected == 'true'):
				sql = "INSERT INTO data (RunDateTime, URL, VideoURL, ResCode, "
				sql += "SrcIP, SrcCountry, SrcRegion, SrcCity, SrcISP, SrcAS, SrcZIP, SrcLat, SrcLon, SrcOrg, "
				sql += "WebIP, WebPing, WebCountry, WebRegion, WebCity, WebISP, WebAS, WebZIP, WebLat, WebLon, WebOrg, "
				sql += "VideoIP, VideoPing, VideoCountry, VideoRegion, VideoCity, VideoISP, VideoAS, VideoZIP, VideoLat, VideoLon, VideoOrg) "
				sql += "VALUES (NOW(), %s, %s, %s, "
				sql += "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
				sql += "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
				sql += "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				val = (dbURL, dbVideoURL, resCode, 
					dbSrcData[0], dbSrcData[1], dbSrcData[2], dbSrcData[3], dbSrcData[4], dbSrcData[5], dbSrcData[6], dbSrcData[7], dbSrcData[8], dbSrcData[9], 
					dbWebData[0], pingTimeWeb, dbWebData[1], dbWebData[2], dbWebData[3], dbWebData[4], dbWebData[5], dbWebData[6], dbWebData[7], dbWebData[8], dbWebData[9], 
					dbVideoData[0], pingTimeVideo, dbVideoData[1], dbVideoData[2], dbVideoData[3], dbVideoData[4], dbVideoData[5], dbVideoData[6], dbVideoData[7], dbVideoData[8], dbVideoData[9])

				mycursor.execute(sql, val)
				conn.commit()
				print("Record inserted.")
				log.write("Record inserted.\n")
			#********** End Write DB ***********

	#if can not get video url or it in wrong format
	else:
		print "---- Error parsing video playback url ----"

		log.write("Error parsing video playback url.")
		log.write("\n")

		if(connected == 'true'):
			sql = "INSERT INTO data (RunDateTime, URL, "
			sql += "SrcIP, SrcCountry, SrcRegion, SrcCity, SrcISP, SrcAS, SrcZIP, SrcLat, SrcLon, SrcOrg, "
			sql += "WebIP, WebPing, WebCountry, WebRegion, WebCity, WebISP, WebAS, WebZIP, WebLat, WebLon, WebOrg)"
			sql += "VALUES (NOW(), %s, "
			sql += "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
			sql += "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			val = (dbURL, 
				dbSrcData[0], dbSrcData[1], dbSrcData[2], dbSrcData[3], dbSrcData[4], dbSrcData[5], dbSrcData[6], dbSrcData[7], dbSrcData[8], dbSrcData[9], 
				dbWebData[0], pingTimeWeb, dbWebData[1], dbWebData[2], dbWebData[3], dbWebData[4], dbWebData[5], dbWebData[6], dbWebData[7], dbWebData[8], dbWebData[9])
			mycursor.execute(sql, val)
			conn.commit()
			print("Record inserted.")
			log.write("Record inserted.\n")


	conn.close()
	print('Connection closed.')
	log.write("Connection to Database: Closed.\n")

	log.write("\n-----------------------------\n\n")

	print pingTimeWeb
	try:
	  pingTimeVideo
	except NameError:
	  print "-1"
	else:
	  print pingTimeVideo

	#let user know it
	print "All done. View log file for more details."

#Set scheduler
schedule.every(20).to(1200).seconds.do(main)

while 1:
    schedule.run_pending()
    time.sleep(1)
