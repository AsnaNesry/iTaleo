import csv
import random

data = [{'mountain': 'Everest', 'height': '8848'},
        {'mountain': 'K2 ', 'height': '8611'},
        {'mountain': 'Kanchenjunga', 'height': '8586'}]

random_data = []
# Success Cases
for i in range(250):
    random_dict = {'salaries': random.randint(500000, 900000), 'experience': random.randint(4, 8),
                   'primary_skill_score': random.randint(200, 1000), 'secondary_skill_score': random.randint(200, 1000),
                   'education': random.randint(3, 4), 'selected': 1}
    random_data.append(random_dict)

# Failure Case 1
for i in range(50):
    random_dict = {'salaries': random.randint(1000000, 2000000), 'experience': random.randint(4, 8),
                   'primary_skill_score': random.randint(200, 1000), 'secondary_skill_score': random.randint(200, 1000),
                   'education': random.randint(3, 4), 'selected': 0}
    random_data.append(random_dict)

# Failure case 2
for i in range(50):
    random_dict = {'salaries': random.randint(500000, 900000), 'experience': random.randint(1, 3),
                   'primary_skill_score': random.randint(200, 1000), 'secondary_skill_score': random.randint(200, 1000),
                   'education': random.randint(3, 4), 'selected': 0}
    random_data.append(random_dict)

# Failure case 3
for i in range(50):
    random_dict = {'salaries': random.randint(500000, 900000), 'experience': random.randint(4, 8),
                   'primary_skill_score': random.randint(100, 200), 'secondary_skill_score': random.randint(200, 1000),
                   'education': random.randint(3, 4), 'selected': 0}
    random_data.append(random_dict)

# Failure case 4
for i in range(50):
    random_dict = {'salaries': random.randint(500000, 900000), 'experience': random.randint(4, 8),
                   'primary_skill_score': random.randint(200, 1000), 'secondary_skill_score': random.randint(100, 200),
                   'education': random.randint(3, 4), 'selected': 0}
    random_data.append(random_dict)

# Failure case 5
for i in range(50):
    random_dict = {'salaries': random.randint(500000, 900000), 'experience': random.randint(4, 8),
                   'primary_skill_score': random.randint(200, 1000), 'secondary_skill_score': random.randint(200, 1000),
                   'education': random.randint(1, 2), 'selected': 0}
    random_data.append(random_dict)
random.shuffle(random_data)
with open('dataset.csv', 'w', newline='') as csvFile:
    fields = ['salaries', 'experience', 'primary_skill_score', 'secondary_skill_score', 'education', 'selected']
    writer = csv.DictWriter(csvFile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(random_data)

print("writing completed")

csvFile.close()
