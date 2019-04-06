# AWS-ElasticBeanstalk-RDS-S3
### Proof Of Concept
#### Python Flask App deployed using Elastic Beanstalk, accessing nba player data from RDS MySQL instance, and accessing Player Photo from AWS S3 bucket

#### Steps to deploy the application : 
1. virtualenv virt [THIS CREATES A VIRTUAL ENVIRONMENT. A FOLDER CALLED 'virt' IS CREATED IN LOCAL PATH]
2. source virt/bin/activate [THIS ACTIVATES THE VIRTUAL ENVIRONMENT]
3. pip install -r requirements.txt [THIS INSTALLS THE DEPENDENCIES FROM requirements.txt]
4. eb init -p python-3.6 <your-application-name> --region <us-east-1 or the region you've chosen>
5. eb create an-env-name
  
#### To check the contents of your RDS MySQL Instance from CLI type in into another terminal the following :
mysql -h <your-rds-domain-name.us-east-2.rds.amazonaws.com> -P 3306 -u <your-rds-username> -p <your-rds-password>

mysql> show databases;

mysql> use name-of-your-db; [ If you haven't created a DB yet, go ahead create one by : CREATE DATABASE your-db-name; ]
  
mysql> select * from yourtablename;



