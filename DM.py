import csv

path = 'dataset.csv'
data = []
min_sup = 400

try:
    f = open(path, 'r')
    rows = csv.reader(f, delimiter=',')
    length = 0
    for row in rows:
        n = int(row[0])
        temp = []
        for i in range(n+1):
            temp.append(row[i])

        data.append(temp)
        length = 1 + length
        #print(row)
except:
    print('ERROR: can not found ' + path)
    exit(1)
        


num_count1 = {}
num_count2 = {}
num_count3 = {}
for i in range(length):
    n = int(data[i][0])
    for j in range(1,n+1):
        if(data[i][j] not in num_count1):
            num_count1[data[i][j]] = 1
        else:
            num_count1[data[i][j]] +=1

for key, value in dict(num_count1).items():
    if value < min_sup:
        del num_count1[key]
temp_str1 =""
temp_str2 =""

for key1 in num_count1:
    for key2 in num_count1:
        temp_str1 = key1+","+key2
        temp_str2 = key2+","+key1
        if((temp_str1 not in num_count2) and (temp_str2 not in num_count2)):
            num_count2[temp_str1] = 0        
for i in range(length):
    n = int(data[i][0])
    temp_str1 = ""
    temp_str2 = ""
    for j in range(1,n+1):
        for k in range(j,n+1):
            if  (data[i][j]!=data[i][k]):
                temp_str1 = data[i][j]+","+data[i][k]
                temp_str2 = data[i][k]+","+data[i][j]
                if(temp_str1 in num_count2):
                    num_count2[temp_str1] +=1
                elif(temp_str2 in num_count2):
                    num_count2[temp_str2] +=1

for key, value in dict(num_count2).items():
    if value < min_sup:
        del num_count2[key]

temp_str =""  
single_count2=[]
for key in num_count2:
    temp_str=key.split(',')
    if temp_str[0] not in single_count2:
        single_count2.append(temp_str[0])
    if temp_str[1] not in single_count2:
        single_count2.append(temp_str[1])

temp_str1 =""
temp_str1_2 =""
temp_str2 =""  
temp_str2_2 =""
temp_str3 =""    
temp_str3_2 =""
number=[]
for i in range(len(single_count2)):
    for j in range(i,len(single_count2)):
        for k in range(j,len(single_count2)):
            if((i!=j)and(i!=k)and(j!=k)):
                temp_str1 = single_count2[i]+","+single_count2[j]
                temp_str1_2 = single_count2[j]+","+single_count2[i]
                temp_str2 = single_count2[i]+","+single_count2[k]
                temp_str2_2 = single_count2[k]+","+single_count2[i]
                temp_str3 = single_count2[j]+","+single_count2[k]
                temp_str3_2 = single_count2[k]+","+single_count2[j]
                if(((temp_str1 in num_count2)or(temp_str1_2 in num_count2))and((temp_str2 in num_count2)or(temp_str2_2 in num_count2))and((temp_str3 in num_count2)or(temp_str3_2 in num_count2))):
                    temp_str = single_count2[i]+","+single_count2[j]+","+single_count2[k]
                    num_count3[temp_str] = 0
                    temp_str = str(i)+","+str(j)+","+str(k)
                    number.append(temp_str)
            

print(min_sup)
#print(num_count1)
print(num_count2) 
print(num_count3)  
print(single_count2) 
print(number)