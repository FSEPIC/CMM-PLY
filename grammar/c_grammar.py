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
from grammar.TREEAAA.c_SemanticsAnalysis import Node

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
    p[0] = Node('father', [p[1]])

def p_statement_list_1(p):
    '''statement_list : statement_list statement'''
    p[0] = Node('stmt_list', [p[1],p[2]])

def p_statement_list_empty(p):
    '''statement_list : '''


def p_statement_1(p):
    '''statement : expression_stmt'''
    p[0] = Node('stmt', [p[1]])


def p_statement_2(p):
    '''statement : compound_stmt'''
    p[0] = Node('stmt', [p[1]])


def p_statement_3(p):
    '''statement : selection_stmt'''
    p[0] = Node('stmt', [p[1]])


def p_statement_4(p):
    '''statement : iteration_stmt'''
    p[0] = Node('stmt', [p[1]])


def p_statement_5(p):
    '''statement : var_declaration'''
    p[0] = Node('stmt', [p[1]])


def p_statement_6(p):
    '''statement : write_stmt'''
    p[0] = Node('stmt', [p[1]])


def p_statement_7(p):
    '''statement : read_stmt'''
    p[0] = Node('stmt', [p[1]])


def p_write_stmt_1(p):
    '''write_stmt : WRITE '(' expression ')' '''
    p[0] = Node('write', [p[1],p[2],p[3],p[4]])


def p_read_stmt_1(p):
    '''read_stmt : READ '(' ID ')' '''
    p[0] = Node('read', [p[1],p[2],p[3],p[4]])


def p_compound_stmt_1(p):
    '''compound_stmt : '{' local_declarations statement_list '}' '''
    p[0] = Node('compound', [p[1],p[2],p[3],p[4]])


def p_local_declarations_1(p):
    '''local_declarations : local_declarations var_declaration'''
    p[0] = Node('local', [p[1],p[2]])


def p_local_declarations_empty(p):
    '''local_declarations : '''


def p_var_declaration_1(p):
    '''var_declaration : type_specifier ID ';' '''
    p[0] = Node('var_declaration', [p[1],p[2],p[3]],'assign')


def p_var_declaration_2(p):
    '''var_declaration : type_specifier ID '[' NUM ']' ';' '''
    p[0] = Node('var_declaration', [p[1],p[2],p[3],p[4],p[5],p[6]],'assign')


def p_var_declaration_3(p):
    '''var_declaration : type_specifier ID '=' expression ';' '''
    p[0] = Node('var_declaration', [p[1],p[2],p[3],p[4],p[5]],'assign')


def p_type_specifier_1(p):
    '''type_specifier : INT'''
    p[0] = Node('type',[p[1]],'gettype')


def p_type_specifier_2(p):
    '''type_specifier : REAL'''
    p[0] = Node('type', [p[1]],'gettype')


def p_expression_stmt_1(p):
    '''expression_stmt : expression ';' '''
    p[0] = Node('expr_stmt', [p[1],p[2]])


def p_expression_stmt_2(p):
    '''expression_stmt : ';' '''
    p[0] = Node('expr_stmt', [p[1]])


def p_selection_stmt_1(p):
    '''selection_stmt : IF '(' expression ')' statement'''
    p[0] = Node('selection_stmt', [p[1],p[2],p[3],p[4],p[5]],'conditionsp')


def p_selection_stmt_2(p):
    '''selection_stmt : IF '(' expression ')' statement ELSE statement'''
    p[0] = Node('selection_stmt', [p[1],p[2],p[3],p[4],p[5],p[6],p[7]],'condition')


def p_iteration_stmt_1(p):
    '''iteration_stmt : WHILE '(' expression ')' statement'''
    p[0] = Node('iteration_stmt', [p[1],p[2],p[3],p[4],p[5]],'loop')


def p_expression_1(p):
    '''expression : var '=' expression'''
    p[0] = Node('exp', [p[1],p[2],p[3]],'as')


def p_expression_2(p):
    '''expression : simple_expression'''
    p[0] = Node('expr', [p[1]])

def p_expression_3(p):
    '''expression : '[' array ']' '''
    p[0] = Node('expr', [p[1],p[2],p[3]])

def p_array_1(p):
    '''array : array_list'''
    p[0] = Node('array', [p[1]],'arrayto')


def p_array_empty(p):
    '''array : '''


def p_array_list_1(p):
    ''' array_list : array_list ',' array_list'''
    p[0] = Node('arr_list', [p[1],p[2],p[3]])


def p_arg_list_2(p):
    ''' array_list : factor'''
    p[0] = Node('arr_list', [p[1]],'array')


def p_var_1(p):
    ''' var : ID'''
    p[0] = Node('var', [p[1]],'getid')


def p_var_2(p):
    ''' var : ID '[' expression ']' '''
    p[0] = Node('var', [p[1],p[2],p[3],p[4]],'getarraynum')


def p_simple_expression_1(p):
    '''simple_expression : additive_expression relop additive_expression'''
    p[0] = Node('simple_expression', [p[1],p[2],p[3]],'binop')


def p_simple_expression_2(p):
    '''simple_expression : additive_expression'''
    p[0] = Node('simple_expr', [p[1]])


def p_relop_1(p):
    '''relop : LE'''
    p[0] = Node('relop', [p[1]],'getop')


def p_relop_2(p):
    '''relop : '<' '''
    p[0] = Node('relop', [p[1]],'getop')


def p_relop_3(p):
    '''relop : '>' '''
    p[0] = Node('relop', [p[1]],'getop')


def p_relop_4(p):
    '''relop : GE'''
    p[0] = Node('relop', [p[1]],'getop')


def p_relop_5(p):
    '''relop : EE'''
    p[0] = Node('relop', [p[1]],'getop')


def p_relop_6(p):
    '''relop : NE'''
    p[0] = Node('relop', [p[1]],'getop')


def p_additive_expression_1(p):
    '''additive_expression : additive_expression addop term'''
    p[0] = Node('additive_expression', [p[1],p[2],p[3]],'binop')


def p_additive_expression_2(p):
    '''additive_expression : term'''
    p[0] = Node('addi_expr', [p[1]])


def p_addop_1(p):
    '''addop : '+' '''
    p[0] = Node('addop', [p[1]],'getop')


def p_addop_2(p):
    '''addop : '-' '''
    p[0] = Node('addop', [p[1]],'getop')


def p_term_1(p):
    '''term : term mulop factor'''
    p[0] = Node('term', [p[1],p[2],p[3]],'binop')


def p_term_2(p):
    '''term : factor'''
    p[0] = Node('term', [p[1]])


def p_mulop_1(p): 
    ''' mulop : '*' '''
    p[0] = Node('mulop', [p[1]])


def p_mulop_2(p):
    ''' mulop : '/' '''
    p[0] = Node('mulop', [p[1]])


def p_factor_1(p):
    '''factor : '(' expression ')' '''
    p[0] = Node('factor', [p[1],p[2],p[3]])


def p_factor_2(p):
    '''factor : var'''
    p[0] = Node('factor', [p[1]])


def p_factor_3(p):
    '''factor : NUM'''
    p[0] = Node('factor', [int(p[1])],'getnum')


def p_factor_4(p):
    '''factor : NUMF'''
    p[0] = Node('factor', [float(p[1])],'getnum')


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
# ISTEST = False # 关闭测试
if ISTEST:
    try:
        get_Grammar()
        with open('6.c')as f:
            contents = f.read()
        x = yacc.parse(contents)
        # Node.star(x)
        Node.resolve(x)
        if(error_num==0):
            print("grammar is true")
    except EOFError:
        print("Can't open file")
