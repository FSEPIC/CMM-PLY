import os
import sys

#字母表
class IDLIST:
    def __init__(self,t,n,v):
        self.type=t;
        self.name=n;
        self.value=v;
        self.data="error";


MyIdList = []
data = []
idline = 0
#树解析
class Node:
    def __init__(self, type, children=None,ac='',lines = 0):
        self.action = ac
        self.type = type
        self.lines = lines
        if children:
            self.children = children
        else:
            self.children = []
        if self.action == '':
            self.action = self.ac(type)

    def execute(self):
        action_dict = {
            'write': self._write,
            'read' : self._read,
            'assign': self._assign,
            'gettype': self._gettype,
            'getid': self._getid,
            'getnum': self._getnum,
            'getop' : self._getop,
            'condition': self._condition,
            'conditionsp' : self._conditionsp,
            'binop': self._binop,
            'array' : self._array,
            'arrayto' : self._arrayto,
            'getarraynum' : self._getarraynum,
            'loop': self._loop,
            'as' : self._as,
            '': self._inside,
        }
        result = action_dict.get(self.action, self._error)()
        return result

    def __str__(self):
        return '%s \n' % (self.type)



    def _inside(self):
        for x in self.children:
            a = Node.resolve(x)
        return a

    @staticmethod
    def GCollec():
        global idline
        global data
        global MyIdList
        idline = 0
        data = []
        MyIdList = []

    @staticmethod
    def dfs_showtree(tree, depth,file):
        if depth == 0:
            file.write("+father\n")
        for item in tree:
            if item is None:
                continue
            elif type(item) is not Node:
                a = "|      " * depth + "+--" + item + "\n"
                file.write(a)
                continue
            a="|      " * depth + "+--" + item.type + "\n"
            file.write(a)
            bitem = item.children
            if not (len(bitem) == 1 and type(bitem[0]) is not Node):
                Node.dfs_showtree(bitem, depth + 1,file)
    @staticmethod
    def star(self):
        if self == None:
            return
        if type(self) != Node:
            Node.resolve(self)
            return
        if len(self.children) >= 1:
            for x in self.children:
                self.star(x)
            Node.resolve(self)

    @staticmethod
    def PT(self,n):
        if self == None:
            return
        if type(self) != Node:
            return
        if len(self.children) >= 1:
            for x in self.children:
                for a in range(n):
                    print("-",end="")
                print(self)
                self.PT(x,n+1)

    @staticmethod
    def ac(s):
        if(s == 'write') : return 'write'
        if (s == 'read'): return 'read'
        if (s == 'assign'): return 'assign'
        if (s == 'get'): return 'get'
        if (s == 'condition'): return 'condition'
        if (s == 'binop'): return 'binop'
        if (s == 'loop'): return 'loop'
        re = ""
        return re

    @staticmethod
    def isADelayedAction(x=None):
        return (x is not None and isinstance(x, Node))

    @staticmethod
    def resolve(x):
        if not Node.isADelayedAction(x):
            return x
        else:
            return x.execute()

    @staticmethod
    def readidfrom():
        file = open('../grammar/idvalue','r+')
        t = 1
        while(t):
            if idline == (t-1):
                return file.__next__()
            file.__next__()
            t = t + 1

    def _read(self):
        global idline
        for id in MyIdList:
            if  id.name == self.children[2]:
                if type(id.data) == list:
                    id.data[0] = Node.readidfrom()
                    idline = idline + 1
                    return
                id.value = Node.readidfrom()
                idline = idline + 1
                return
        self._error()

    def _write(self):
        num = Node.resolve(self.children[2])
        if type(num) == str:
            num = self.getvalue(num)
        file = open('result','a+')
        file.write(str(num) + "\n")
        file.close()
        print(num)

    def clean(self):
        data=[]

    def _assign(self):
        if len(self.children) == 3:
            typ = Node.resolve(self.children[0])
            id = IDLIST(typ,self.children[1],-1)
            MyIdList.append(id)
            return
        if len(self.children) == 6:
            typ = Node.resolve(self.children[0])
            id = IDLIST(typ,self.children[1],self.children[3])
            id.data=[]
            MyIdList.append(id)
            return
        if len(self.children) == 5:
            typ = Node.resolve(self.children[0])
            a = Node.resolve(self.children[3])
            global data
            if data != []:
                num = data
                data = []
            elif type(a) == str:
                num = self.getvalue(a)
            else:
                num = a
            if type(num) == list:
                id = IDLIST(typ, self.children[1], len(num))
                id.data = num
            elif typ == 'real':
                num = float(num)
                id = IDLIST(typ, self.children[1], num)
            elif typ == 'int':
                num = int(num)
                id = IDLIST(typ, self.children[1], num)
            MyIdList.append(id)
        return

    def getvalue(self,name):
        for id in MyIdList:
            if id.name == name:
                if type(id.data) == list:
                    if id.type == 'int':
                        num = int(id.data[0])
                    if id.type == 'real':
                        num = float(id.data[0])
                else:
                    if id.type == 'int':
                        num = int(id.value)
                    if id.type == 'real':
                        num = float(id.value)
                return num
        file = open('result','a+')
        s = "取值出错，无此变量:   %s   " % name + "|   出错行数为:'%d'" % self.lines + "\n"
        file.write(s)
        print("取值出错，无此变量:   %s   " % name, "|   出错行数为:'%d'" % self.lines)


    def _binop(self):
        na = Node.resolve(self.children[0])
        nb = Node.resolve(self.children[2])
        if type(na) == str:
            a = self.getvalue(na)
        else:
            a = na
        if type(nb) == str:
            b = self.getvalue(nb)
        else:
            b = nb
        op = Node.resolve(self.children[1])
        result = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '>': lambda a, b: (a > b),
            '>=': lambda a, b: (a >= b),
            '<': lambda a, b: (a < b),
            '<=': lambda a, b: (a <= b),
            '==': lambda a, b: (a == b),
            '!=': lambda a, b: (a != b),
        }[op](a, b)
        return result

    def _getarraynum(self):
        num = Node.resolve(self.children[2])
        if type(num) == str:
            num = self.getvalue(num)
        for id in MyIdList:
            if id.name == self.children[0]:
                return id.data[num]
        file = open('result','a+')
        s = "取值出错，无此变量:   %s   " % self.children[0] +  "|   出错行数为:'%d'" % self.lines + "\n"
        file.write(s)
        print("取值出错，无此变量:   %s   " % self.children[0], "|   出错行数为:'%d'" % self.lines)

    def _gettype(self):
        return self.children[0]
    def _getid(self):
        for id in MyIdList:
            if id.name == self.children[0]:
                if type(id.data) == list:
                    return id.name
                return id.name
        file = open('result','a+')
        s = "取值出错，无此变量:   %s   " % self.children[0] +  "|   出错行数为:'%d'" % self.lines + "\n"
        file.write(s)
        file.close()
        print("取值出错，无此变量:   %s   " % self.children[0], "|   出错行数为:'%d'" % self.lines)

    def _getnum(self):
        return self.children[0]
    def _getop(self):
        return self.children[0]

    def _array(self):
        d = Node.resolve(self.children[0])
        data.append(d)
    def _arrayto(self):
        data = []
        Node.resolve(self.children[0])
        array = data
        return array

    def _conditionsp(self):
        istrue = Node.resolve(self.children[2])
        if istrue :
            Node.resolve(self.children[4])
    def _condition(self):
        isturn = Node.resolve(self.children[2])
        if isturn:
            Node.resolve(self.children[4])
        else:
            Node.resolve(self.children[6])

    def _loop(self):
        istrue = Node.resolve(self.children[2])
        while(istrue):
            Node.resolve(self.children[4])
            istrue = Node.resolve(self.children[2])

    def _as(self):
        name = Node.resolve(self.children[0])
        num = Node.resolve(self.children[2])
        if type(num) == str:
            num = self.getvalue(num)
        for id in MyIdList:
            if id.name == name:
                id.value = num

    def _error(self):
        print("Error, unsupported operation:", str(self))
        return None