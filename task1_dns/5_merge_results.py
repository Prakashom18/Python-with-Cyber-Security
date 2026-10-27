import json

from_crtsh = ["www.example.com", "mail.example.com"]
from_securitytrails = ["www.example.com", "dev.example.com"]

result = {}
for name in from_crtsh:
    result[name] = ["crtsh"]
for name in from_securitytrails:
    if name in result:
        result[name].append("securitytrails")   # duplicate: just add the source
    else:
        result[name] = ["securitytrails"]

with open("result.json", "w") as file:
    json.dump(result, file, indent=2)
print(result)