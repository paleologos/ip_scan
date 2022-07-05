import subprocess
import os
import re


# dir path
dir_path="./reports"

# network enviornment
p = subprocess.Popen("ip n", stdout=subprocess.PIPE,  stderr=None, shell=True)
result = p.communicate()[0].decode('utf-8')

# network enviornment
p2 = subprocess.Popen("ip neigh show ", stdout=subprocess.PIPE,  stderr=None, shell=True)
result2 = p2.communicate()[0].decode('utf-8')
all_mac= result2.rstrip().split("\n")

#default gateway
p3 = subprocess.Popen("ip r ", stdout=subprocess.PIPE,  stderr=None, shell=True)
result3 = p3.communicate()[0].decode('utf-8')
dg= result3.split("\n")[0].split(" ")[2]


# net mask
p4 = subprocess.Popen("ip -o -f inet addr show ", stdout=subprocess.PIPE,  stderr=None, shell=True)
result4 = p4.communicate()[0].decode('utf-8')
infs= result4.rstrip().split("\n")
c=0
for inf in infs:
    txt=inf.split(" ")
    #detects which list element contains substring "global" - eliminating host scope - localhost
    for i in txt:
        if(re.search("^global$", i)):
            c+=1
#read mask from network scope global            
mask = infs[c].split(" ")[6].split("/")[1]



# list of octets
net_var=result.split(" ")[0].split(".")

net_num1=int(net_var[0])
net_num2=int(net_var[1])



# detects net class
if(net_num1 >= 128 and net_num1 <= 191):
    print("B class network")
elif(net_num1 >= 192 and net_num1 <= 223):
    print("C class network")
else:
        pass

print(f"Gateway: {dg}")
print(f"Subnet mask: {mask}")


subnet=int(input("Enter subnet: "))
start= int(input("Enter startnig IP address: "))
stop= int(input(f"Enter ending IP address value from  {start} to  255 : "))


active_addresses=[]
inactive_addresses=[]
with open(os.devnull, "wb") as temp:
        for n in range(start, stop+1):
                ip="{0}.{1}.{2}.{3}".format(net_num1,net_num2,subnet,n)
                result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                        stdout=temp, stderr=temp).wait()
                if result:
                        print(ip, "Inactive")
                        inactive_addresses.append(ip)
                        # if dir reports don't exists , create and then write in it
                        if(os.path.isdir(dir_path) is False):
                                print(f"Creating directory reports...")
                                os.mkdir(dir_path)
                                f = open("./reports/report_inactive_ip.txt", "w")
                                for i in range(len(inactive_addresses)):
                                        f.write(inactive_addresses[i]+"\n")
                                f.close()
                        else:
                                 # if dir reports exists
                                f = open("./reports/report_inactive_ip.txt", "w")
                                for i in range(len(inactive_addresses)):
                                        f.write(inactive_addresses[i]+"\n")
                                f.close()
                        
                else:
                        active_addresses.append(ip)
                        print(ip, "Active")
                         #  if dir reports don't exists , create and then write in it
                        if(os.path.isdir(dir_path) is False):
                                print(f"Creating directory reports...")
                                os.mkdir(dir_path)
                                f = open("./reports/report_active_ip.txt", "w")
                                for i in range(len(active_addresses)):
                                        f.write(active_addresses[i]+"\n")
                                f.close()
                        else:
                                 # if dir reports exists
                                f = open("./reports/report_active_ip.txt", "w")
                                for i in range(len(active_addresses)):
                                        f.write(active_addresses[i]+"\n")
                                f.close()


# Writting MAC addr
if(os.path.isdir(dir_path) is False):
        print(f"Creating directory reports...")
        os.mkdir(dir_path)
        with open("./reports/report_mac.txt", "w") as f:
                for m in all_mac:
                        ip_mac=m.split(" ")[0]
                        mac_mac=m.split(" ")[4]
                        x=ip_mac +" - "+ mac_mac+"\n"
                        f.write(x)
        
else:
        with open("./reports/report_mac.txt", "w") as f:
                for m in all_mac:
                        ip_mac=m.split(" ")[0]
                        mac_mac=m.split(" ")[4]
                        x=ip_mac +" - "+ mac_mac+"\n"
                        f.write(x)
        
print(f"List of active IP adresses in subnet {subnet}, from starting {start} to ending {stop} ip adress : ")
print(active_addresses)
