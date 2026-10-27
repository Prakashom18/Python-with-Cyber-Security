import dns.resolver

domain = input("Enter domain: ")

for record_type in ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]:
    try:
        answers = dns.resolver.resolve(domain, record_type)
        for answer in answers:
            print(record_type, "->", answer.to_text())
    except Exception:
        print(record_type, "-> none")