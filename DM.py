import csv
import copy
import time



path = 'dataset.csv'
data = []
min_sup = float(input('min_support:'))
min_confi = float(input('min_confidence:'))
start = time.time()



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
        

#print(data)
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
                    
for i in range(length):
    n = int(data[i][0])
    temp_str1 = ""
    temp_str2 = ""
    temp_str3 = ""
    temp_str4 = ""
    temp_str5 = ""
    temp_str6 = ""
    for j in range(1,n+1):
        for k in range(j,n+1):
            for m in range(k,n+1):
                if ((data[i][j]!=data[i][k])and(data[i][j]!=data[i][m])and(data[i][m]!=data[i][k])):
                    temp_str1 = data[i][j]+","+data[i][k]+","+data[i][m]
                    temp_str2 = data[i][j]+","+data[i][m]+","+data[i][k]
                    temp_str3 = data[i][k]+","+data[i][j]+","+data[i][m]
                    temp_str4 = data[i][k]+","+data[i][m]+","+data[i][j]
                    temp_str5 = data[i][m]+","+data[i][k]+","+data[i][j]
                    temp_str6 = data[i][m]+","+data[i][j]+","+data[i][k]
                    if(temp_str1 in num_count3):
                        num_count3[temp_str1] +=1
                    elif(temp_str2 in num_count3):
                        num_count3[temp_str2] +=1
                    elif(temp_str3 in num_count3):
                        num_count3[temp_str3] +=1
                    elif(temp_str4 in num_count3):
                        num_count3[temp_str4] +=1
                    elif(temp_str5 in num_count3):
                        num_count3[temp_str5] +=1
                    elif(temp_str6 in num_count3):
                        num_count3[temp_str6] +=1

for key, value in dict(num_count3).items():
    if value < min_sup:
        del num_count3[key]                

count3_list= []
count3_value= []
count2_list= []
count2_value= []
for key in (num_count3):
    count3_list.append(key)
    count3_value.append(num_count3[key])
for key in (num_count2):
    count2_list.append(key)
    count2_value.append(num_count2[key])
    
for i in range(len(count3_list)):
    count3_list[i]=count3_list[i].split(",")
#print(count3_list)

#print("minimum support :",min_sup)
#print("minimum confidence :",min_confi,"\n")
print("Numbers of data:",length)
print("\n")
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    for i in range(len(count2_list)):
        count2_list[i]=count2_list[i].split(",")
        for j in range(len(count3_list)):
            if ((count2_list[i][0] in count3_list[j]) and (count2_list[i][1] in count3_list[j])):
                temp3 = copy.deepcopy(count3_list[j])
                temp3.remove(count2_list[i][0])
                temp3.remove(count2_list[i][1])
                confidence = int(count3_value[j])/int(count2_value[i])
                if (confidence>min_confi):
                    temp_str=count2_list[i][0]+","+count2_list[i][1]+"->"+temp3[0]
                    print("Relation rules: {",count2_list[i][0],",",count2_list[i][1],"->",temp3[0],"}")
                    print("Support:",(count3_value[j]/length))
                    print("Confidence :",confidence)
                    print("Count of",count3_list[j],':',count3_value[j])
                    print("Count of",count2_list[i],":",count2_value[i])
                    print("--------------------")
                    writer.writerow([temp_str, count3_value[j]/length, confidence])


#print(count3_list)
#print(count3_value)
#print(count2_list)
#print(count2_value)
#print(min_sup)
#print(length)
#print(num_count1) 
#print(num_count2) 
#print(num_count3)  
#print(single_count2) 
#print(number)
end = time.time()

print(end - start)