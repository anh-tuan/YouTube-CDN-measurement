# YouTube-CDN-measurement

### Requirements
- Python 2.7
- Package requests, mysql-connector, schedule
- MySQL Database server

### Installation (Linux, UNIX)
1. Open Terminal
2. Check PIP version: ```pip -V```
3. Upgrade to latest version of PIP: ```sudo pip install --upgrade pip```
4. Install required packages: 
  - ```pip install requests```
  - ```pip install mysql-connector```
  - ```pip install schedule```
5. Edit MySQL connection:
```python
conn = mysql.connector.connect(host='you_server_ip',
	                              database='your_db_name',
	                              user='your_username',
	                              password='your_password')
```
6. run with command: ```sudo python measurement.py```
  
