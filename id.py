import requests
token = "Np3PIkNHfTH4I3Atq-nycTf9aK1AQKUqkFlIMVePwim-7uSXF_6KJY1AS_pqOe6LahpCICDFFpmBRoATa_SsE0qizENY91aVLRR7"
service_id = "17346853"
headers = {"Authorization": f"Bearer {token}"}

url = f"https://api.nitrado.net/services/{service_id}"
response = requests.get(url, headers=headers)

if response.ok:
    data = response.json()
    print("✅ Service is accessible.")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

# Now try accessing the gameserver endpoint
gameserver_url = f"https://api.nitrado.net/services/{service_id}/gameservers"
r = requests.get(gameserver_url, headers=headers)
print("🎯 Gameserver response:", r.status_code)
print(r.text)
