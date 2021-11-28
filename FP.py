import csv



path = 'dataset.csv'
data = []
min_sup = float(input('min_support:'))

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
#print(sort_list)
#print("-----------------")

for i in range(length):
    n = int(data[i][0])
    temp_str=[]
    for j in range(len(sort_list)):
        for k in range(1,n+1):
            if(data[i][k]==sort_list[j]):
                temp_str.append(data[i][k])
    sort_data.append(temp_str)
                
                
#print(sort_data)

# FP樹類
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue  #節點元素名稱，在構造時初始化爲給定值
        self.count = numOccur   # 出現次數，在構造時初始化爲給定值
        self.nodeLink = None   # 指向下一個相似節點的指針，默認爲None
        self.parent = parentNode   # 指向父節點的指針，在構造時初始化爲給定值
        self.children = {}  # 指向子節點的字典，以子節點的元素名稱爲鍵，指向子節點的指針爲值，初始化爲空字典

    # 增加節點的出現次數值
    def inc(self, numOccur):
        self.count += numOccur

    # 輸出節點和子節點的FP樹結構
    def disp(self, ind=1):
        print(' ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)

# =======================================================構建FP樹==================================================

# 對不是第一個出現的節點，更新頭指針塊。就是添加到相似元素鏈表的尾部
def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

# 根據一個排序過濾後的頻繁項更新FP樹
def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        # 有該元素項時計數值+1
        inTree.children[items[0]].inc(count)
    else:
        # 沒有這個元素項時創建一個新節點
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # 更新頭指針表或前一個相似元素項節點的指針指向新節點
        if headerTable[items[0]][1] == None:  # 如果是第一次出現，則在頭指針表中增加對該節點的指向
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])

    if len(items) > 1:
        # 對剩下的元素項迭代調用updateTree函數
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

# 主程序。創建FP樹。dataSet爲事務集，爲一個字典，鍵爲每個事物，值爲該事物出現的次數。minSup爲最低支持度
def createTree(dataSet, minSup=1):
    # 第一次遍歷數據集，創建頭指針表
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # 移除不滿足最小支持度的元素項
    keys = list(headerTable.keys()) # 因爲字典要求在迭代中不能修改，所以轉化爲列表
    for k in keys:
        if headerTable[k] < minSup:
            del(headerTable[k])
    # 空元素集，返回空
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    # 增加一個數據項，用於存放指向相似元素項指針
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # 每個鍵的值，第一個爲個數，第二個爲下一個節點的位置
    retTree = treeNode('Null Set', 1, None) # 根節點
    # 第二次遍歷數據集，創建FP樹
    for tranSet, count in dataSet.items():
        localD = {} # 記錄頻繁1項集的全局頻率，用於排序
        for item in tranSet:
            if item in freqItemSet:   # 只考慮頻繁項
                localD[item] = headerTable[item][0] # 注意這個[0]，因爲之前加過一個數據項
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)] # 排序
            updateTree(orderedItems, retTree, headerTable, count) # 更新FP樹
    return retTree, headerTable

# =================================================查找元素條件模式基===============================================

# 直接修改prefixPath的值，將當前節點leafNode添加到prefixPath的末尾，然後遞歸添加其父節點。
# prefixPath就是一條從treeNode（包括treeNode）到根節點（不包括根節點）的路徑
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

# 爲給定元素項生成一個條件模式基（前綴路徑）。basePet表示輸入的頻繁項，treeNode爲當前FP樹中對應的第一個節點
# 函數返回值即爲條件模式基condPats，用一個字典表示，鍵爲前綴路徑，值爲計數值。
def findPrefixPath(basePat, treeNode):
    condPats = {}  # 存儲條件模式基
    while treeNode != None:
        prefixPath = []  # 用於存儲前綴路徑
        ascendTree(treeNode, prefixPath)  # 生成前綴路徑
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count  # 出現的數量就是當前葉子節點的數量
        treeNode = treeNode.nodeLink  # 遍歷下一個相同元素
    return condPats

# =================================================遞歸查找頻繁項集===============================================
# 根據事務集獲取FP樹和頻繁項。
# 遍歷頻繁項，生成每個頻繁項的條件FP樹和條件FP樹的頻繁項
# 這樣每個頻繁項與他條件FP樹的頻繁項都構成了頻繁項集

# inTree和headerTable是由createTree()函數生成的事務集的FP樹。
# minSup表示最小支持度。
# preFix請傳入一個空集合（set([])），將在函數中用於保存當前前綴。
# freqItemList請傳入一個空列表（[]），將用來儲存生成的頻繁項集。
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    # 對頻繁項按出現的數量進行排序進行排序
    sorted_headerTable = sorted(headerTable.items(), key=lambda p: p[1][0])  #返回重新排序的列表。每個元素是一個元組，[（key,[num,treeNode],()）
    bigL = [v[0] for v in sorted_headerTable]  # 獲取頻繁項
    for basePat in bigL:
        newFreqSet = preFix.copy()  # 新的頻繁項集
        newFreqSet.add(basePat)     # 當前前綴添加一個新元素
        freqItemList.append(newFreqSet)  # 所有的頻繁項集列表
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])  # 獲取條件模式基。就是basePat元素的所有前綴路徑。它像一個新的事務集
        myCondTree, myHead = createTree(condPattBases, minSup)  # 創建條件FP樹

        if myHead != None:
            # 用於測試
            print('conditional tree for:', newFreqSet)
            myCondTree.disp()
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)  # 遞歸直到不再有元素


# 將數據集轉化爲目標格式
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

if __name__=='__main__':
    minSup =3
    simpDat = sort_data  # 加載數據集
    initSet = createInitSet(simpDat)  # 轉化爲符合格式的事務集
    myFPtree, myHeaderTab = createTree(initSet, minSup)  # 形成FP樹
    # myFPtree.disp()  # 打印樹

    freqItems = []  # 用於存儲頻繁項集
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)  # 獲取頻繁項集
    #print(freqItems)  # 打印頻繁項集
    #print(sort_data)
    