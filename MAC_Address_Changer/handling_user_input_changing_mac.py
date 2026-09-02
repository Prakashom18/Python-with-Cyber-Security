import subprocess

interface = input("Enter the interface:")
new_mac = input("Enter the new mac upto 12 chars")

# handling the user input

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw","ether",new_mac])
subprocess.call(["ifconfig", interface, "up"])