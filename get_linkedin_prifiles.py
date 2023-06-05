import requests
for id in profile_ids:
    print(type(id))
    payload = {
        "profile_id": id,
        "profile_type": "personal",
        "contact_info": False,
        "recommendations": False,
        "related_profiles": False
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "875ab400c6msh860842639ef4a3bp15418djsn8b421257c7a3",
        "X-RapidAPI-Host": "linkedin-profiles-and-company-data.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response:
        print("data retrieved")
    else:
        pass
    print(response.json())