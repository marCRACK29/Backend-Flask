import requests

BASE = "http://127.0.0.1:5000/"

# data = [{"nombre": "Torres del Paine", "likes":10, "views":1000}, 
#         {"nombre": "Viaje en Tokio", "likes":23, "views":3400}, 
#         {"nombre": "Un día como...", "likes":1123, "views":3000}]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), json=data[i])
#     print(response.json())

# input()
# response = requests.get(BASE + "video/2")
# print(response.json()) 
response = requests.patch(BASE + "video/2",json={"views":112378, "likes": 1})
print(response.json())