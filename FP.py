import csv

path = 'dataset.csv'
data = []
min_sup = 500

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

num_count1={}
sort_count1={}
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

#print(num_count1)
sort_count1={k: v for k, v in sorted(num_count1.items(), key=lambda item: item[1],reverse = True)}
print(sort_count1)

sort_list = []
sort_data = []
for key in sort_count1:
    sort_list.append(key)
print(sort_list)
print("-----------------")

for i in range(length):
    n = int(data[i][0])
    temp_str=[]
    for j in range(len(sort_list)):
        for k in range(1,n+1):
            if(data[i][k]==sort_list[j]):
                temp_str.append(data[i][k])
    sort_data.append(temp_str)
                
                
print(sort_data)
#####以下待研究
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue # 節點名稱
        self.count = numOccur # 節點出現次數
        self.nodeLink = None # 不同項集的相同項通過nodeLink連線在一起
        self.parent = parentNode # 指向父節點
        self.children = {} # 儲存葉子節點

    def inc(self, numOccur):
        """inc(對count變數增加給定值)
        """
        self.count += numOccur

    def disp(self, ind=1):
        """disp(用於將樹以文字形式顯示)
        """
        print('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)
            
    def __lt__(self, other):
        return self.count < other.count
    
