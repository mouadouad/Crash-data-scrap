import json
def merge(file1,file2):
    merged = {}
    for i in file2:
        if i in file1.keys():
            merged[i] = file1[i] + file2[i]
    for i in file1:
        if i not in file2.keys():
            merged[i] = file1[i]
    return merged

def open_file(name):
    with open(name, 'r') as json_file:
        file = json.load(json_file)
    return file

def iterate(names_list):
    data = {}
    for i in range(len(names_list)):
        data = merge(open_file(names_list[i]),data)
    return data

# data = iterate(["data1.txt","data2.txt","data3.txt"])

# count_list = []
# for i in data:
#     count_list.append(int(i))
# max_number = max(count_list)
# data_list = [0.0]*max_number
# counter = 0
# for i in data:
#     data_list[int(i)-1] = data[i]
#     counter += data[i]
#
#
# for i in range(max_number):
#     count = 0
#     for j in range(i, max_number):
#         count += data_list[j]
#     data_list[i] = count*(i+1)/counter
#
# winner = data_list.index(max(data_list))+1
# print("number of tries : " + str(counter) + "\n")
# print("percentage list : " + "\n" + str(data_list) + "\n")
# print("winner number : " + str(winner) + "\n")
# if max(data_list) > (2*winner)/(2*winner-1):
#     print("yes")
# else:
#     print("no")

data = open_file("data.txt")
data_list = []
counter = data["1.0"]
for i in data:
    if i != "counter":
        data_list.append(data[i]*float(i)/counter)
winner = data_list.index(max(data_list))/10 + 1
print("number of tries : " + str(counter) + "\n")
print("percentage list : " + "\n" + str(data_list) + "\n")
print("winner number : " + str(winner) + "\n")