import subprocess

interface = input("Enter the interface:")
new_mac = input("Enter the new mac upto 12 chars")

subprocess.call("ifconfig" + interface + "down",shell=True)
subprocess.call("ifconfig"+interface+ "hw ether" + new_mac,shell=True)
subprocess.call("ifconfig"+ interface + "up",shell=True)



