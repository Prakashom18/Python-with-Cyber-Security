import subprocess

interface = "eth0"
new_mac= "00:11:22:33:44:55"

print("[+] Changing MAC Address for" + interface + "to"+ new_mac);

subprocess.item("ifconfig" + interface + "down",shell=True)
subprocess.item("ifconfig" +interface + "hw ether " + new_mac,shell=True)
subprocess.item("ifconfig" + interface + "hw ether " + new_mac, shell=True)
