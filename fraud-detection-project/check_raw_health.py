import http.client
conn = http.client.HTTPConnection("localhost", 8000)
conn.request("GET", "/health")
r = conn.getresponse()
print(r.read().decode())
conn.close()
