import subprocess

ip = "google.com"
p = subprocess.Popen(["ping -c 5 "+ip], stdout = subprocess.PIPE, shell=True)
#(output, err) = p.communicate()
#p_status = p.wait()
#print "Command output : ", output
#print "Command exit status/return code : ", p_status
p.wait()
#print p.poll()

response = p.communicate()[0]

print response

i = response.find('mdev =')
j = response.find('/', i + 10)
k = response.find('/', j + 1)

time = response[j+1:k]

print time