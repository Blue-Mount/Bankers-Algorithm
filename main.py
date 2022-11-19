N = 5
M = 3
# 初始已分配资源
Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
# 最大申请资源
Max = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
# 可用资源
Available = [3, 3, 2]
# 待满足资源
Need = [[0 for i in range(M)] for i in range(N)]
# 请求队列
RequestList = [[1, [1, 2, 2]], [4, [2, 1, 0]], [0, [2, 4, 0]], [2, [3, 0, 0]],
               [3, [0, 1, 1]], [0, [5, 0, 3]], [2, [3, 0, 0]], [4, [2, 2, 1]]]
# 计算待满足资源数量
for i in range(N):
    for j in range(M):
        Need[i][j] = Max[i][j] - Allocation[i][j];

# 打印上述列表
def show(Max, Allocation, Available, Need):
    print("ID\t\tMax\t\tAlloc\t\tNeed")
    for i in range(N):
        print(i)
        print(Max[i], "\t\t\t")
        print(Allocation[i], "\t\t\t")
        print(Need[i], "\t\t\t")

    print("各资源剩余:", Available, "\n")

# 核心：安全性检查，在循环中不断检查尝试分配，满足条件则分配，否则推迟到下一个循环
# 所有资源都满足了则释放，卡在死循环中则死锁
def checkSecurity(Allocation, Available, Need):
    unfinished = N
    finish = [0] * N
    work = [0] * M
    for i in range(M):
        work[i] = Available[i]
    flag = True
    while(unfinished) > 0:
        for i in range(N):
            if finish[i] == False:
                flag = True
                for j in range(M):
                    if Need[i][j] > work[j]:
                        flag = False
                        break
                if flag:
                    finish[i] = True
                    for j in range(M):
                        work[j] += Allocation[i][j]
        unfinished -= 1

    flag = True
    for i in finish:
        if i == False:
            flag = False
            break

    if flag == False:
        print("当前处于不安全状态！\n")
        return False

    print("当前处于安全状态\n")
    return True

def request(RequestItem, ID, Allocation, Available, Need):
    # 尝试分配用的临时数组
    p_available = [0] * M
    p_allocation = [0] * M
    p_need = [0] * M
    for i in range(M):
        p_available[i] = Available[i]
        p_allocation[i] = Allocation[ID][i]
        p_need[i] = Need[ID][i]
    # 首先判断够不够分配，不够直接驳回
    for j in range(M):
        if RequestItem[j] > Need[ID][j]:
            print(RequestItem[j], Need[ID][j], "请求数量大于需求，请求失败\n")
            return False
        if RequestItem[j] > Available[j]:
            print("当前资源不足，请等待\n")
            return False

    # 尝试分配
    for j in range(M):
        Available[j] -= RequestItem[j]
        Need[ID][j] -= RequestItem[j]
        Allocation[ID][j] += RequestItem[j]

    if(checkSecurity(Allocation, Available, Need) == False):
        for i in range(M):
            Available[i] = p_available[i]
            Allocation[ID][i] = p_allocation[i]
            Need[ID][i] = p_need[i]

        show(Max, Allocation, Available, Need)
        return False

    if(Need[ID] == [0] * M):
        for i in range(M):
            Available[i] += Allocation[ID][i]
            Allocation[ID][i] = 0

    show(Max, Allocation, Available, Need)
    return True

# 循环申请，直到请求列表清空，否则死锁
while(len(RequestList)):
    flag = False
    index = -1
    for i in range(len(RequestList)):
        ID = RequestList[i][0]
        RequestItem = RequestList[i][1]
        if request(RequestItem, ID, Allocation, Available, Need) == True:
            flag = True
            index = i
            break
    # 申请成功则将对应进程删除
    if flag:
        del RequestList[index]

    print("RequestList:", RequestList)
