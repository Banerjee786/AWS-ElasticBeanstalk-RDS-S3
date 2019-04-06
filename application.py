

from flask import Flask, render_template, request, url_for,redirect
import pymysql
import sys
import rds_config
import logging
import options
import boto3
from botocore.client import Config
import botocore
from flask_bootstrap import Bootstrap


rds_host  = rds_config.db_hostname
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

ACCESS_KEY_ID = rds_config.s3_access_key_id
ACCESS_SECRET_KEY = rds_config.s3_access_secret_key
BUCKET_NAME = rds_config.s3_bucket_name

logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)
con = pymysql.connect(rds_host,name,password,db_name)
application = Flask(__name__)
bootstrap = Bootstrap(application)

@application.route('/')
def home():
    return render_template('home.html')

@application.route('/',methods=['GET', 'POST'])
def retrieve():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Publish':    
            return render_template('addPlayer.html')
        elif request.form['submit_button'] == 'Retrieve':
            with con: 
                cur = con.cursor()
                cur.execute("SELECT * FROM nba_players")
                rows = cur.fetchall() 
            return render_template('getPlayers.html',options=rows)
        elif request.form['submit_button'] == 'AddPhoto':
            return render_template('addPlayerPhoto.html')
        elif request.form['submit_button'] == 'DownloadPhoto':
            return render_template('downloadPhoto.html')
        elif request.form['submit_button'] == 'DisplayPhoto':
            return render_template('enterDisplayPhotoName.html')
        elif request.form['submit_button'] == 'ListBucketContents':
            s3_resource = boto3.resource('s3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4'))
            my_bucket = s3_resource.Bucket(BUCKET_NAME)
            summaries = my_bucket.objects.all()
            return render_template('bucketContents.html',my_bucket=my_bucket, files=summaries)

@application.route('/Publish',methods=['GET','POST'])
def publish():
    player_name = request.form['player']
    print(player_name)
    try:
        cursr = con.cursor()
        query = "INSERT INTO nba_players(name) VALUES ('{}')".format(player_name)
        cursr.execute(query)
        print("Inserted Player Name")
        con.commit()
        return "Player Name inserted successfully"
    except Exception as e:
        return(str(e))


@application.route('/AddPhoto',methods=['GET','POST'])
def addPhoto():
    try:
        player_photo_name = str(request.form['playerPhoto'])
        data = open("static/"+player_photo_name,'rb')
        s3 = boto3.resource('s3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4'))
        s3.Bucket(BUCKET_NAME).put_object(Key=player_photo_name, Body=data)
        return "Picture uploaded successfully !"
    except Exception as e:
        return(str(e))

@application.route('/DownloadPhoto',methods=['GET','POST'])
def downloadPhoto():
    try:
        playerName_photo_dwnld = str(request.form['playerPhotoDownload'])
        #data = open(playerName_photo_dwnld,'rb')
        print(playerName_photo_dwnld)
        s3 = boto3.resource('s3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY)
        try:
            s3.Bucket(BUCKET_NAME).download_file(playerName_photo_dwnld,'downloads/'+playerName_photo_dwnld)
            return "File successfully downloaded"
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":    
                print("The object does not exist.")
                return "Object does not exist"
            else:
                raise     
    except Exception as e:
        return(str(e))

@application.route('/DisplayPhoto',methods=['GET','POST'])
def displayPhoto():
    player_photo_name = request.form['playerPhotoForPhoto']
    s3_domain = "https://s3.amazonaws.com/"+BUCKET_NAME+"/"
    s3_endpoint = s3_domain+player_photo_name
    return render_template('displayPlayerPhoto.html',endpoint=s3_endpoint)
        

if __name__ == '__main__':
    application.run(debug=True)
