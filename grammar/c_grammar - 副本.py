# =============================================================================
# 文件名：c_grammar.py
# 功能：基于python-lex和python-yacc的C-语法分析器
# 作者： 武起龙，张峥
# 时间：2019/12/29
#==============================================================================
# *接口说明*
#   - getGrammar() : 生成parsetab.py和parse.out文件
#
#
# *如何使用*
#   - 作为模块使用时注释/关闭末尾的测试代码，调用getGrammar即可
#
# *有用参考*
#   - 英文文档：http://www.dabeaz.com/ply/ply.html （强烈推荐）
#   - 中文文档：https://www.cnblogs.com/P_Chou/p/python-lex-yacc.html
# =============================================================================
# *实现思路*
#   1.输入标识符和界符等符号
#   2.定义注释和回车的忽略规则
#   3.设置递进规约规则
#   4.输入产生式列表
# =============================================================================
import sys

#字母表结构定义
class IDLIST:
    def __init__(self,t,n,v):
        self.type=t;
        self.name=n;
        self.value=v;
        self.data="data";
MyIdList = []

error_num = 0 #用于记录错误次数

# =============================================================================
# 1. tokens 列表定义
#   tokens必须要有，多于一个字符的终结符的命名写在这
#   里面的每个符号都要有对应正则定义,且以 t_ 开头，详细见后文
# =============================================================================

tokens = (
    'INT','IF','ELSE','WHILE','NUM','NUMF','ID','GE','LE','EE','NE','ANNOTATION','READ','WRITE','REAL'
    )

# =============================================================================
# 1. literals 列表定义
#   一个字符的终结符的命名写在这
#   字符对应终结符，不需要正则定义
# =============================================================================
literals = ['=','+','-','*','/', '(',')',';','<','>','{','}',',','[',']']

# =============================================================================
# 2.以下为各个token的正则表达式定义，采用 t_tokenName 的命名方式
# 若要对其进行运算，可通过定义函数的方式
# =============================================================================

t_INT = r'int'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_ID    = r'(?!real|int|if|else|while|read|write)[a-zA-Z_][a-zA-Z0-9_]*'
t_NUM = r'[0-9]+'
t_NUMF = r'[0-9]*\.[0-9]+'
t_GE = r'>='
t_LE = r'<='
t_EE = r'=='
t_NE = r'!='
t_REAL = r'real'
t_WRITE = r'write'
t_READ = r'read'

#定义忽略注释的正则表达式
def t_ANNOTATION(t):
    r'(/\*(.*?[.\n])*\*/)|(//[^\n]*)' # 第一行写正则表达式
    t.lexer.lineno += t.value.count('\n') # 累计行数
    pass # 表示忽略该token

# 定义忽略字符的正则表达式，忽略空格回车换行

t_ignore = " \t\r"


#==============================================================================
# 通过函数定义正则表达式，可以增加额外动作，比如给value重新赋值，或增加其余字段信息
#==============================================================================

# 增加行数
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    pass

# 错误处理：输出错误符号，行数，列数后跳过当前错误继续扫描
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    print("(%d," % t.lexer.lineno, "%d)" % t.lexer.lexpos)
    t.lexer.skip(1)

import ply.lex as lex # 导入python lex模块

lex.lex()# 调用Lex模块，构建词法分析器

#==============================================================================
#产生式列表
#==============================================================================
def p_program_1(p):
    '''program : statement_list'''
    print("---END---")
# def p_declaration_list_1(p):
#     '''declaration_list : declaration_list declaration'''
# def p_declaration_list_2(p):
#     '''declaration_list : declaration'''

# def p_declaration_1(p):
#     '''declaration : var_declaration'''
# # def p_declaration_2(p):
# #     '''declaration : fun_declaration'''
#
# def p_var_declaration_1(p):
#     '''var_declaration : type_specifier ID ';' '''
# def p_var_declaration_2(p):
#     '''var_declaration : type_specifier ID '[' NUM ']' ';' '''
#
# def p_type_specifier_1(p):
#     '''type_specifier : INT'''
# def p_type_specifier_2(p):
#     '''type_specifier : REAL'''
# def p_type_specifier_2(p):
#     '''type_specifier : VOID'''

# def p_fun_declaration_1(p):
#     '''fun_declaration : type_specifier ID '(' params ')' '''
# def p_fun_declaration_2(p):
#     '''fun_declaration : compound_stmt'''

# def p_params_1(p):
#     '''params : param_list'''
# def p_params_2(p):
#     '''params : VOID'''
# def p_params_empty(p):
#     '''params : '''

# def p_param_list_1(p):
#     '''param_list : param_list ',' param'''
# def p_param_list_2(p):
#     '''param_list : param'''

# def p_param_1(p):
#     '''param : type_specifier ID'''
# def p_param_2(p):
#     '''param : type_specifier ID '[' ']' '''

# def p_compound_stmt_1(p):
#     '''compound_stmt : '{' local_declarations statement_list '}' '''



def p_statement_list_1(p):
    '''statement_list : statement_list statement'''

def p_statement_list_empty(p):
    '''statement_list : '''

def p_statement_1(p):
    '''statement : expression_stmt'''
def p_statement_2(p):
    '''statement : compound_stmt'''
def p_statement_3(p):
    '''statement : selection_stmt'''
def p_statement_4(p):
    '''statement : iteration_stmt'''
# def p_statement_5(p):
#     '''statement : return_stmt'''
def p_statement_5(p):
    '''statement : var_declaration'''
def p_statement_6(p):
    '''statement : write_stmt'''
def p_statement_7(p):
    '''statement : read_stmt'''

def p_write_stmt_1(p):
    '''write_stmt : WRITE '(' expression ')' '''
    print(p[3])

def p_read_stmt_1(p):
    '''read_stmt : READ '(' ID ')' '''
    for a in MyIdList:
        if a.name == p[3] :
            a.value = input()
            return
    print("ERROR!The current variable is not declared! \nIn line : %d" % p.lexer.lineno, "\nVariable name : %s" % p[1])
    sys.exit()

def p_compound_stmt_1(p):
    '''compound_stmt : '{' local_declarations statement_list '}' '''

def p_local_declarations_1(p):
    '''local_declarations : local_declarations var_declaration'''
def p_local_declarations_empty(p):
    '''local_declarations : '''

def p_var_declaration_1(p):
    '''var_declaration : type_specifier ID ';' '''
def p_var_declaration_2(p):
    '''var_declaration : type_specifier ID '[' NUM ']' ';' '''
    id = IDLIST(p[1],p[2],p[4])
    id.data = "error"
    MyIdList.append(id)

def p_var_declaration_3(p):
    '''var_declaration : type_specifier ID '=' expression ';' '''
    if type(p[4]) == list:
        id = IDLIST(p[1],p[2],len(p[4]))
        id.data = p[4]
        MyIdList.append(id)
        return
    id = IDLIST(p[1],p[2],p[4])
    MyIdList.append(id)

def p_type_specifier_1(p):
    '''type_specifier : INT'''
    p[0] = p[1]
def p_type_specifier_2(p):
    '''type_specifier : REAL'''
    p[0] = p[1]

def p_expression_stmt_1(p):
    '''expression_stmt : expression ';' '''
def p_expression_stmt_2(p):
    '''expression_stmt : ';' '''

def p_selection_stmt_1(p):
    '''selection_stmt : IF '(' expression ')' statement'''

def p_selection_stmt_2(p):
    '''selection_stmt : IF '(' expression ')' statement ELSE statement'''

def p_iteration_stmt_1(p):
    '''iteration_stmt : WHILE '(' expression ')' statement'''

# def p_return_stmt_1(p):
#     '''return_stmt : RETURN ';' '''
# def p_return_stmt_2(p):
#     '''return_stmt : RETURN expression ';' '''

def p_expression_1(p):
    '''expression : var '=' expression'''
def p_expression_2(p):
    '''expression : simple_expression'''
    p[0] = p[1]
def p_expression_3(p):
    '''expression : '[' array ']' '''
    p[0] = p[2]

def p_array_1(p):
    '''array : array_list'''
    p[0] = p[1]
def p_array_empty(p):
    '''array : '''

def p_array_list_1(p):
    ''' array_list : array_list ',' factor'''
    if type(p[1]) != list:
        array = [p[1],p[3]]
        p[0] = array
        return
    p[1].append(p[3])
    p[0] = p[1]
def p_arg_list_2(p):
    ''' array_list : factor'''
    p[0] = p[1]


def p_var_1(p):
    ''' var : ID'''
    p[0] = p[1]
def p_var_2(p):
    ''' var : ID '[' expression ']' '''
    for a in MyIdList:
        if a.name == p[1]:
            if int(p[3]) >= a.value:
                print("ERROR!Array out of bounds! \nIn line : %d"%p.lexer.lineno)
            if a.type == 'int':
                p[0] = int(a.data[int(p[3])])
                return
            if a.type == 'real':
                p[0] = float(a.data[int(p[3])])
                return
def p_simple_expression_1(p):
    '''simple_expression : additive_expression relop additive_expression'''
    if p[2] == 'LE':
        p[0] = p[1] <= p[3]
        print(p[0])
def p_simple_expression_2(p):
    '''simple_expression : additive_expression'''
    p[0] = p[1]

def p_relop_1(p):
    '''relop : LE'''
    p[0] = p[1]
def p_relop_2(p):
    '''relop : '<' '''
    p[0] = p[1]
def p_relop_3(p):
    '''relop : '>' '''
    p[0] = p[1]
def p_relop_4(p):
    '''relop : GE'''
    p[0] = p[1]
def p_relop_5(p):
    '''relop : EE'''
    p[0] = p[1]
def p_relop_6(p):
    '''relop : NE'''
    p[0] = p[1]

def p_additive_expression_1(p):
    '''additive_expression : additive_expression addop term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    if p[2] == '-':
        p[0] = p[1] - p[3]
def p_additive_expression_2(p):
    '''additive_expression : term'''
    p[0] = p[1]

def p_addop_1(p):
    '''addop : '+' '''
    p[0] = p[1]
def p_addop_2(p):
    '''addop : '-' '''
    p[0] = p[1]

def p_term_1(p):
    '''term : term mulop factor'''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    if p[2] == '/':
        p[0] = p[1] / p[3]

def p_term_2(p):
    '''term : factor'''
    p[0] = p[1]

def p_mulop_1(p):
    ''' mulop : '*' '''
    p[0] = p[1]
def p_mulop_2(p):
    ''' mulop : '/' '''
    p[0] = p[1]

def p_factor_1(p):
    '''factor : '(' expression ')' '''
def p_factor_2(p):
    '''factor : var'''
    if type(p[1]) == int or  type(p[1]) == float:
        p[0] = p[1]
        return
    for a in MyIdList:
        if a.name == p[1]:
            if type(a.data) == list:
                p[0]=int(a.data[0])
                return
            p[0] = int(a.value)
            return
    print("ERROR!The current variable is not declared! \nIn line : %d"%p.lexer.lineno,"\nVariable name : %s"%p[1])
    sys.exit()
# def p_factor_3(p):
#     '''factor : call'''
def p_factor_3(p):
    '''factor : NUM'''
    p[0] = int(p[1])
def p_factor_4(p):
    '''factor : NUMF'''
    p[0] = float(p[1])
#
# def p_call_1(p):
#     ''' call : ID '(' args ')' '''
#
# def p_args_1(p):
#     '''args : arg_list'''
# def p_args_empty(p):
#     '''args : '''
#
# def p_arg_list_1(p):
#     ''' arg_list : arg_list ',' expression'''
# def p_arg_list_2(p):
#     ''' arg_list : expression'''

#错误处理，输出错误所在单词
def p_error(p):
    global error_num
    error_num+=1
    if p:
        print("Syntax error at '%s'" %p.value," line:%d"%p.lexer.lineno)
    else:

        print("Syntax error at EOF")

# =============================================================================
# 接口：运行时生成相应的parse.out和parsetab.py文件供之后使用
# =============================================================================
import ply.yacc as yacc
def get_Grammar():
    yacc.yacc()

# =============================================================================
# 测试部分：真正运行时将其注释掉 / 将ISTEST设为False
# =============================================================================
ISTEST = True # 打开测试
#ISTEST = False # 关闭测试
if ISTEST:
    try:
        get_Grammar()
        with open('test.c')as f:
            contents = f.read()
        yacc.parse(contents)
        if(error_num==0):
            print("grammar is true")
    except EOFError:
        print("Can't open file")
