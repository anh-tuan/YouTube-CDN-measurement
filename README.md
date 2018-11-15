# YouTube CDN measurement
#### This instruction for CentOS / RHEL

### Requirements
- Python ***2.7*** installed
- Package ***requests***, ***mysql-connector***, ***schedule*** installed
- MySQL Database server

### Installation (Linux, UNIX)
1. Open Terminal
2. Check ***PIP*** version: ```pip -V```
3. If got ```pip: command not found``` we need to install ***pip*** by command:
- ```yum --enablerepo=extras install epel-release```
- ```yum install python-pip```
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
  
