'''
解析下面 Git log 命令的输出
$> git log --name-status --abbrev-commit --format="Revision: %h%n###%s%n>>>>Detail:%n%b<<<<End" HEAD...224d > 1.txt
'''
import json
from repo.revmode import ChangedFile,Revision
from repo.db import saveRev
def parseLog(path):
    '''path 是git log 文件路径'''
    lines =[]
    with open(path) as f:
        lines = f.readlines()
    return parse(lines)  # -> 解析字符串数组，返回 RevisionInfo 的 List
def parse(content):
    ris =[]
    ri = None
    detailFlag = False # -> 是否开始收集 该 revision 的 detail 字段信息
    changeFlag = False # -> 是否开始收集 该 revision 的 变更文件列表
    for line in content:
        if(line.startswith("Revision: ")):  # -> 是否为新的一个 Revision
            changeFlag = False              # -> 设置 Change File 段已结束
            detailFlag = False              # -> 设置 Detail 段已结束
            ri = Revision()             # -> 创建一个新增的 Revision
            ri.setRev(line[10:-1])          # -> 保存 revision 信息
            ris.append(ri)                  # -> 将其加入到 Revision 集合中
            continue
        elif(line.startswith('###')):   # -> 解析当前Revision的 Brief
            ri.setBrief(line[3:-1])     # -> 去除行首的空白和行尾的换行符
            continue
        elif(line.startswith('>>>>Detail:')):   # -> Detail 段是否开始
            detailFlag = True                   # -> 设置 Detail 段开始
            continue
        elif(line.startswith('<<<<End')):   #-> Detail 段是否结束
            detailFlag = False              # -> 设置 Detail 段已结束
            changeFlag = True               # -> 设置 Change File 段已开始
            continue
        elif (detailFlag):              # -> 收集 Detail信息
            ri.addDetail(line[0:-1])    # -> 去除行尾的换行符
            continue
        elif(changeFlag):               # -> 收集变更文件名信息
            if(line !=''):              # -> 去除多余的空行
                ri.addChange(ChangedFile.create(line[0:-1]))# -> 去除行尾的换行符
            continue
        elif(line.strip() == ""):       # -> 如果两个 Revision 之间有空行就忽略空行
            continue
    return ris