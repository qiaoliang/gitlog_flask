'''
解析下面 Git log 命令的输出
$> git log --name-status --abbrev-commit --format="Revision: %h%n###%s%n>>>>Detail:%n%b<<<<End" HEAD...224d > 1.txt
'''
import json
from repo.revmode import ChangedFile,Revision
from repo.db import saveRev

def convert_to_dict(obj):
  '''把Object对象转换成Dict对象'''
  dict = {}
  dict.update(obj.__dict__)
  return dict
def convert_to_dicts(objs):
  '''把对象列表转换为字典列表'''
  obj_arr = []
  for o in objs:
    #把Object对象转换成Dict对象
    dict = {}
    dict.update(o.__dict__)
    obj_arr.append(dict)
  return obj_arr
def class_to_dict(obj):
  '''把对象(支持单个对象、list、set)转换成字典'''
  is_list = obj.__class__ == [].__class__
  is_set = obj.__class__ == set().__class__
  if is_list or is_set:
    obj_arr = []
    for o in obj:
      #把Object对象转换成Dict对象
      dict = {}
      dict.update(o.__dict__)
      obj_arr.append(dict)
    return obj_arr
  else:
    dict = {}
    dict.update(obj.__dict__)
    return dict

def parseLog(path):
    '''path 是git log 文件路径'''
    lines =[]
    with open(path) as f:
        lines = f.readlines()
    return parse(lines)  # -> 解析字符串数组，返回 RevisionInfo 的 List

    # result = class_to_dict(ris) # -> 将class list 转成 Dict
    # return json.dumps(result,ensure_ascii=False) # 返回json 字串
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
