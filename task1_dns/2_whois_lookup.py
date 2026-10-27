import whois

domain = input("Enter domain: ")
info = whois.whois(domain)

print("Registrar:", info.registrar)
print("Created:", info.creation_date)
print("Expires:", info.expiration_date)
print("Name servers:", info.name_servers)