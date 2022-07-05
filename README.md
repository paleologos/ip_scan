# net_scan

(SRB) Jednostavni linux mrezni skener napisan u Python 3 

Jednostavni mrezni skener koristi 3 ugradjena python modula - subprocess, os i re. Nije potrebno nikakvo dodatno instaliranje.

Glavna ideja je da se mrezne ip komande izvrsavaju shell-u pomocu subprocess modula. 

Program identifikuje da li je mreza klase B ili C, podrazumevani gateway, kao i mreznu masku. 

Program sam kreira direktorijum reports (ukoliko ne postoji), i unutar njega kreira 3 fajla - report_active_ip.txt, report_inactive_ip.txt i report_mac.txt, u koje upisuje aktivne i neaktivne ip adrese, ako i MAC adrese.

Nakon skidanja dovoljno je smao u shell-u pokrenuti fajl net_scan_srb.py

python net_scan_srb.py

Ukoliko postoji problem sa pokretanjem fajla, dodati  pravo egzekucije

sudo chmod a+x net_scan-srb.py






(ENG) Simple linux network scanner written in Python 3

Simple network scaner uses 3 built-in python modules - subprocess, os and re. It's not required any additional installation.

Main idea is, to execute ip shell commands, by using subprocess module.

Program idenitfies network class (B or C), default gateway, and subnet mask.

Program automatically creates directory reports (if it is missing),and inside that directory creates 3 files - report_active_ip.txt, report_inactive_ip.txt i report_mac.txt. 

After downloading, it's enough just to run file net_scan_eng.py, in shell.

python net_scan_eng.py

If there are problems with execution , just add exec priviledges 

sudo chmod a+x net_scan_eng.py










