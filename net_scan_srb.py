import subprocess
import os
import re


# putanja direktorijuma
dir_path="./reports"

# mrezno okruzenje
p = subprocess.Popen("ip n", stdout=subprocess.PIPE,  stderr=None, shell=True)
result = p.communicate()[0].decode('utf-8')

# mrezno okruzenje
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
    #detekcija u kom se elementu liste javlja string scope global - eliminise scope host - localhost
    for i in txt:
        if(re.search("^global$", i)):
            c+=1
# maska se iscitava iz global scope            
mask = infs[c].split(" ")[6].split("/")[1]



# lista okteta
net_var=result.split(" ")[0].split(".")

net_num1=int(net_var[0])
net_num2=int(net_var[1])



# detekcija klase mreze
if(net_num1 >= 128 and net_num1 <= 191):
    print("Mreza B klase")
elif(net_num1 >= 192 and net_num1 <= 223):
    print("Mreza C klase")
else:
        pass

print(f"Gateway: {dg}")
print(f"Subnet maska: {mask}")


subnet=int(input("Unesite opseg: "))
start= int(input("Unesite pocetnu adresu za ping: "))
stop= int(input(f"Unesite krajnju adresu za ping od {start} do 255 : "))


active_addresses=[]
inactive_addresses=[]
with open(os.devnull, "wb") as temp:
        for n in range(start, stop+1):
                ip="{0}.{1}.{2}.{3}".format(net_num1,net_num2,subnet,n)
                result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                        stdout=temp, stderr=temp).wait()
                if result:
                        print(ip, "Neaktivna")
                        inactive_addresses.append(ip)
                        # ukoliko direktorijum reports ne postoji - kreira i upisuje
                        if(os.path.isdir(dir_path) is False):
                                #kod
                                print(f"Kreiranje direktorijuma reports...")
                                os.mkdir(dir_path)
                                f = open("./reports/report_inactive_ip.txt", "w")
                                for i in range(len(inactive_addresses)):
                                        f.write(inactive_addresses[i]+"\n")
                                f.close()
                        else:
                                 # ukoliko direktorijum reports  postoji -  upisuje
                                f = open("./reports/report_inactive_ip.txt", "w")
                                for i in range(len(inactive_addresses)):
                                        f.write(inactive_addresses[i]+"\n")
                                f.close()
                        
                else:
                        active_addresses.append(ip)
                        print(ip, "Aktivna")
                         # ukoliko direktorijum reports ne postoji - kreira i upisuje
                        if(os.path.isdir(dir_path) is False):
                                #kod
                                print(f"Kreiranje direktorijuma reports...")
                                os.mkdir(dir_path)
                                f = open("./reports/report_active_ip.txt", "w")
                                for i in range(len(active_addresses)):
                                        f.write(active_addresses[i]+"\n")
                                f.close()
                        else:
                                 # ukoliko direktorijum reports  postoji -  upisuje
                                f = open("./reports/report_active_ip.txt", "w")
                                for i in range(len(active_addresses)):
                                        f.write(active_addresses[i]+"\n")
                                f.close()


# Upisivanje MAC adresa
if(os.path.isdir(dir_path) is False):
        print(f"Kreiranje direktorijuma reports...")
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
        
print(f"Lista aktivnih adresa na opsegu {subnet}, od pocetne {start} do krajnje {stop} je: ")
print(active_addresses)
