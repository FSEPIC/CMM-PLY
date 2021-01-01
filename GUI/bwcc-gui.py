import _thread
import keyword
import os
import sys
from os import path
from PyQt5 import QtWidgets
from PyQt5.Qsci import QsciLexerPython, QsciScintilla, QsciAPIs
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import (QFileDialog)
from PyQt5.QtWidgets import QMainWindow
from ply import yacc

import GUI.bwcc
from grammar.TREEAAA.c_SemanticsAnalysis import Node
from grammar.c_grammar import Treedisplay, get_Grammar, compile, RDisplay


class highlight(QsciLexerPython):
    def __init__(self, parent):
        QsciLexerPython.__init__(self, parent)
        font = QFont()
        font.setFamily('Courier')
        font.setPointSize(12)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setColor(QColor(0, 0, 0))
        self.setPaper(QColor(255, 255, 255))

        self.setColor(QColor("#00FF00"), QsciLexerPython.ClassName)
        self.setColor(QColor("#B0171F"), QsciLexerPython.Keyword)
        self.setColor(QColor("#00FF00"), QsciLexerPython.Comment)
        self.setColor(QColor("#FF00FF"), QsciLexerPython.Number)
        self.setColor(QColor("#0000FF"), QsciLexerPython.DoubleQuotedString)
        self.setColor(QColor("#0000FF"), QsciLexerPython.SingleQuotedString)
        self.setColor(QColor("#288B22"), QsciLexerPython.TripleSingleQuotedString)
        self.setColor(QColor("#288B22"), QsciLexerPython.TripleDoubleQuotedString)
        self.setColor(QColor("#0000FF"), QsciLexerPython.FunctionMethodName)
        self.setColor(QColor("#191970"), QsciLexerPython.Operator)
        self.setColor(QColor("#000000"), QsciLexerPython.Identifier)
        self.setColor(QColor("#00FF00"), QsciLexerPython.CommentBlock)
        self.setColor(QColor("#0000FF"), QsciLexerPython.UnclosedString)
        self.setColor(QColor("#FFFF00"), QsciLexerPython.HighlightedIdentifier)
        self.setColor(QColor("#FF8000"), QsciLexerPython.Decorator)
        self.setFont(QFont('Courier', 12, weight=QFont.Bold), 5)
        self.setFont(QFont('Courier', 12, italic=True), QsciLexerPython.Comment)


class BWCC(GUI.bwcc.Ui_CMM_Parse, QMainWindow):

    def __init__(self, title='CMM解释器'):
        super(GUI.bwcc.Ui_CMM_Parse, self).__init__()
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)

        self.setWindowTitle(title)
        font = QFont()
        font.setFamily('Courier')
        font.setPointSize(12)
        font.setFixedPitch(True)
        self.setFont(font)
        self.editor = QsciScintilla(self.someEdit)
        self.editor.setFont(font)
        # self.setCentralWidget(self.editor)
        self.editor.setUtf8(True)
        self.editor.setGeometry(0, 0, 851, 451)
        # 1.设置文档的编码格式为 “utf8” ，换行符为 windows
        self.editor.setUtf8(True)
        self.editor.setEolMode(QsciScintilla.SC_EOL_CRLF)  # 文件中的每一行都以EOL字符结尾（换行符为 \r \n）
        # 2.设置括号匹配模式
        self.editor.setBraceMatching(QsciScintilla.StrictBraceMatch)  #
        # 3.设置 Tab 键功能
        self.editor.setIndentationsUseTabs(True)
        self.editor.setIndentationWidth(4)
        self.editor.setTabIndents(True)
        self.editor.setAutoIndent(True)
        self.editor.setBackspaceUnindents(True)
        self.editor.setTabWidth(4)

        # 自动补全
        self.editor.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.editor.setAutoCompletionCaseSensitivity(True)
        self.editor.setAutoCompletionReplaceWord(False)
        self.editor.setAutoCompletionThreshold(1)
        self.editor.setAutoCompletionUseSingle(QsciScintilla.AcusExplicit)

        # 代码高亮
        self.lexer = highlight(self.editor)
        self.editor.setLexer(self.lexer)
        self.mod = False
        self.__api = QsciAPIs(self.lexer)
        kwlist = ["real", "void", "int", 'printf', "main",
                  "for", "read", "while", "write", "if", "else", ";"]

        autocompletions = keyword.kwlist + kwlist
        for ac in autocompletions:
            self.__api.add(ac)
        self.__api.prepare()
        self.editor.autoCompleteFromAll()

        self.editor.setCaretWidth(2)  # 光标宽度（以像素为单位），0表示不显示光标
        self.editor.setCaretForegroundColor(QColor("darkCyan"))  # 光标颜色
        self.editor.setCaretLineVisible(True)  # 是否高亮显示光标所在行
        self.editor.setCaretLineBackgroundColor(QColor("#99cccc"))  # 光标所在行的底色
        # 设置页边特性。        这里有3种Margin：[0]行号    [1]改动标识   [2]代码折叠
        self.editor.setFolding(QsciScintilla.PlainFoldStyle)
        self.editor.setMarginWidth(2, 12)
        # 设置代码折叠和展开时的页边标记 - +
        self.editor.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPEN)
        self.editor.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDER)
        self.editor.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.editor.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDEREND)
        # 设置代码折叠后，+ 的颜色FFFFFF
        self.editor.setMarkerBackgroundColor(QColor("#FFBCBC"), QsciScintilla.SC_MARKNUM_FOLDEREND)
        self.editor.setMarkerForegroundColor(QColor("red"), QsciScintilla.SC_MARKNUM_FOLDEREND)
        # 设置行号
        self.editor.setMarginLineNumbers(0, True)  # 设置标号为0的页边显示行号
        self.editor.setMarginWidth(0, '00000')  # 行号宽度
        # 设置改动标记
        self.editor.setMarginType(1, QsciScintilla.SymbolMargin)  # 设置标号为1的页边用于显示改动标记
        self.editor.setMarginWidth(1, "0000")  # 改动标记占用的宽度

        self.setAttribute(Qt.WA_DeleteOnClose)
        # 设置函数名为关键字2    KeyWord = sdcc_kwlistcc  ;KeywordSet2 = 函数名
        self.editor.SendScintilla(QsciScintilla.SCI_SETKEYWORDS,
                                  0, " ".join(kwlist).encode(encoding='utf-8'))

    def openButtonClicked(self):
        try:

            filename = QFileDialog.getOpenFileName(self, '保存源程序', './')
            if filename[0]:
                with open(filename[0], 'r') as f:
                    src = f.read()

            # self.someEdit.setText(src)
            self.editor.setText(src)

        except Exception as e:
            print(e)

    def saveButtonClicked(self):
        try:
            str = self.someEdit.toPlainText()
            filepath = QFileDialog.getSaveFileName(self, '保存源程序', './',
                                                   "txt files (*.txt);;all files(*.*);;c files(*.c)")
            if filepath[0]:
                with open(filepath[0], 'w') as f:
                    f.write(str)
                    f.close()

        except Exception as e:
            print(e)

    def runClicked(self):
        try:
            result = open('result', 'r+')
            self.resultEdit.setText(result.read())
        except Exception as e:
            print(e)

    def treeButtonClicked(self):
        filepath1 = path.dirname(__file__)
        with open(path.join(filepath1, "Tree.txt"))as f:
            contents = f.read()
            self.treeEdit.setText(contents)


    def compiles(self):
        get_Grammar()
        x = yacc.parse(str(self.editor.text()))
        RDisplay()
        Node.resolve(x)
        Treedisplay(x)
        del x
        Node.GCollec()


    def parseButtonClicked(self):
        try:
            _thread.start_new_thread(self.compiles,())
        except Exception as e:
            print(e)


    def exitClicked(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myform = BWCC()
    myform.show()
    sys.exit(app.exec_())
