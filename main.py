import pyrebase
from flask import Flask, json, request, jsonify, render_template
import os
import urllib.request
from werkzeug.utils import secure_filename
import pandas as pd #import csv
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.secret_key = "Chaski_Demo"

firebaseConfig = {
  "apiKey": os.environ["apiKey"],
  "authDomain": os.environ["authDomain"],
  "databaseURL": os.environ["databaseURL"],
  "projectId": os.environ["projectId"],
  "storageBucket": os.environ["storageBucket"],
  "messagingSenderId": os.environ["messagingSenderId"],
  "appId": os.environ["appId"],
  "measurementId": os.environ["measurementId"]
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

UPLOAD_FOLDER = "public"
UPLOAD_FOLDER = "/tmp"
REPORT_URL = "http://localhost:8080/report"
REPORT_URL = "https://carbon-atrium-330502.uc.r.appspot.com/report"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

names = ["Zone 1 Warm up", 
         "Zone 2 Easy", 
         "Zone 3 Aerobic", 
         "Zone 4 Threshold", 
         "Zone 5 Maximum", 
         ]

ALLOWED_EXTENSIONS = set(["txt", "csv"])

def allowed_file(filename):
	return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
	return "Homepage"

@app.route("/upload", methods = ["POST"])
def upload_file():
	# check if the post request has the file part
	if "uploadFile" not in request.files:
		print("request:::: ", request)
		resp = jsonify({"message" : "No file part in the request", "ALGO": request.files})
		resp.status_code = 400
		return resp

	errors = {}
	success = False
	
	uploadFile = request.files['uploadFile'] #request.files.getlist("uploadFile")
	if uploadFile and allowed_file(uploadFile.filename):
			filename = secure_filename(uploadFile.filename)
			uploadFile.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
			success = True
	else:
		errors[uploadFile.filename] = "File type is not allowed"

	if success and errors:
		errors["message"] = "File successfully uploaded"
		resp = jsonify(errors)
		resp.status_code = 500
		return resp

	if success:
		result_data = processed_data(uploadFile.filename, request.form)
		return result_data
	else:
		resp = jsonify(errors)
		resp.status_code = 500
		return resp

def processed_data(csv_file, args):
	duration = int(args.get('duration'))
	maxBpmZone0 = int(args.get('maxBpmZone0'))
	maxBpmZone1 = int(args.get('maxBpmZone1'))
	maxBpmZone2 = int(args.get('maxBpmZone2'))
	maxBpmZone3 = int(args.get('maxBpmZone3'))
	DevMAC = args.get('DevMAC')
	samplePeriod = int(args.get('samplePeriod'))
	startTimestamp = int(args.get('startTimestamp'))
	
	csv_file = app.config["UPLOAD_FOLDER"] + "/" + csv_file

	import urllib.request
	import pandas as pd

	n_info_rows = 0
	file1 = open(csv_file, 'r')
	Lines = file1.readlines()

	for line in Lines:
	  if "timeSeconds" in line:
	    break
	  if "Init_time" in line:
	    Init_time = line[:-1].split(" ")[1]
	    print("Init_time:", Init_time)
	    DeviceMAC0, Init_time = Init_time.split("_")
	    print("Init_time:", Init_time)
	    print("DeviceMAC0:", DeviceMAC0)
	    Init_time1 = Init_time[:Init_time.index(".txt")]
	    print("Init_time1:", Init_time1)
	  if "Duration" in line:
	    DurationStr, Duration, DeviceMACStr, DeviceMAC = line.strip().split(",")
	    print(DurationStr, Duration, DeviceMACStr, DeviceMAC)
	  n_info_rows += 1
	print("n_info_rows: ", n_info_rows)

	df = pd.read_csv(csv_file, skiprows = n_info_rows )
	histogram = select_data(df)

	max_val = df.signalFrequencyBpm.max()
	min_val = df.signalFrequencyBpm.min()
	avg_val = df.signalFrequencyBpm.mean()


	data = {
		"duration": duration,
		"maxBpmZone0": maxBpmZone0,
		"maxBpmZone1": maxBpmZone1,
		"maxBpmZone2": maxBpmZone2,
		"maxBpmZone3": maxBpmZone3,
		"DevMAC": DevMAC,
		"samplePeriod": samplePeriod,
		"startTimestamp": startTimestamp,
	}
	import json
	zone_threshold =  [maxBpmZone0,maxBpmZone1,maxBpmZone2,maxBpmZone3]

	data["info"] = {
		"total_time": Duration, 
		"avg": avg_val,
		"max": max_val,
		"min": min_val,
		"zones": get_range(df, zone_threshold),
		"zone_threshold": zone_threshold,
		"date_time": Init_time1,
		"histogram":json.dumps( histogram.values.tolist() ),
		"histogram_values": json.dumps( histogram.signalFrequencyBpm.values.tolist() ),
		}

	id_data = db.push(data)["name"]
	print("\n\nid_data:", id_data, "\n\n\n")

	data["info"]["visual_report"] =  REPORT_URL +  "?id=" + id_data
	resp = jsonify(data["info"])
	resp.status_code = 201
	return resp


def get_range(df, zone_threshold):
  zones = [0]  + zone_threshold
  vals = []
  n = len(df)
  for z in range(len(zones) - 1):
    vals.append( len( df[ (df.signalFrequencyBpm >= zones[z]) & (df.signalFrequencyBpm < zones[z + 1]) ] ) / n )
  vals.append( ( 1 - sum(vals) )  )
  return vals

def select_data(df, n_resample = 100):
  ts = df[["timeSeconds", "signalFrequencyBpm"]]#.set_index('timeSeconds')
  N = len(df)
  filtered_data = ts.iloc[::int((N)/100),:] # filter N+1 points
  print("filtered_data")
  print(filtered_data.head().values)
  return filtered_data

@app.route("/report", methods = ["GET"])
def report():
	page_id = request.args.get("id") # report id

	import requests
	import datetime
	id_data = page_id
	info = db.child(id_data).get().val()
	info["info"]["visual_report"] = REPORT_URL +  "?id=" + id_data

	labels = [i for i in range(100)] # 
	values = info["info"]["histogram"] #

	date_time_val = datetime.datetime.fromisoformat(info["info"]["date_time"])
    
	from datetime import datetime as dt
	def suffix(d):
	  return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
	def custom_strftime(format, t):
	  return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

	title =  custom_strftime('%A {S} of %B of %Y, %I:%M%p', date_time_val)

	round_values = [round(v * 100) for v in info["info"]["zones"]]
	return render_template('chart.html', 
		info = info["info"],
		values = values, 
		labels = labels, 
		labels_bar = names,
		round_values = round_values, 
		title = title
		)

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    # app.run(threaded=True, host='0.0.0.0', port=port)
    #app.run(host='172.17.0.4', port=8080, debug=True)
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)
# http://localhost:8080/report?id=-MpIFa7Btk1HX7mGtuco