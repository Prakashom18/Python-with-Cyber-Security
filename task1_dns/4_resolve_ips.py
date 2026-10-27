import socket

for name in open("subdomains.txt").read().split():
    try:
        print(name, "->", socket.gethostbyname(name))
    except Exception:
        print(name, "-> no IP")