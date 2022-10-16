import json
class RevisionInfo(object):
    def __init__(self):
        self.rev = ""
        self.brief = ""
        self.detail= []
        self.changes =[]
    def setRev(self,r):
        self.rev=r
    def setBrief(self,b):
        self.brief = b
    def addDetail(self,d):
        self.detail.append(d)
    def addChange(self,c):
        self.changes.append(c)
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

def get_contends(path):
    '''path 是git log 文件路径'''
    lines =[]
    with open(path) as f:
        lines = f.readlines()
    ris = parse(lines)  # -> 解析字符串数组，返回 RevisionInfo 的 List
    result = convert_to_dicts(ris) # -> 将class list 转成 Dict
    return json.dumps(result,ensure_ascii=False) # 返回json 字串

def parse(content):
    ris =[]
    ri = None
    detailFlag = False # -> 是否开始收集 该 revision 的 detail 字段信息
    changeFlag = False # -> 是否开始收集 该 revision 的 变更文件列表
    for line in content:
        if(line.startswith("Revision: ")):  # -> 开始解析新的一个 Revision
            changeFlag = False
            detailFlag = False
            ri = RevisionInfo()
            ris.append(ri)
            ri.setRev(line[10:])
            continue
        elif(line.startswith('###')):   # -> 解析当前Revision的 Brief
            ri.setBrief(line[3:])
            continue
        elif(line.startswith('>>>>Detail:')): # -> 开始收集 Detail
            detailFlag = True
            continue
        elif(line.startswith('<<<<End')):   #-> Detail 已经结束了
            detailFlag = False
            changeFlag = True
            continue
        elif (detailFlag):              # -> 收集 Detail信息
            ri.addDetail(line)
            continue
        elif(changeFlag):               # -> 收集变更文件名信息
            ri.addChange(line)
            continue
        elif(line.strip() == ""):       # -> 如果两个 Revision 之间有空行就忽略空行
            continue
    return ris