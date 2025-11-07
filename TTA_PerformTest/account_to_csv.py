import csv

field_names=["email", "password", "pk", "device_name"]
data_dict = []

for i in range(0,100):
    data_dict.append({
        "email" : f"tta_test{i}@gmail.com",
        "password" : f"tta_password{i}",
        "pk": 50+i,
        "device_name": f"tta-iml-user{i}"    
    })
    
file_path_dict = 'example_dict.csv'

with open(file_path_dict, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(data_dict)