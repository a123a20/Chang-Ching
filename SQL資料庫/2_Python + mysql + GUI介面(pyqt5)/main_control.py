#此為加入邏輯判斷的程式 (另一個ui_mainwindow.py檔會被刷新，需在Pyqt5的Ui介面修改，只需注意ui變數名稱即可)

from PyQt5.QtWidgets import QMainWindow
from ui_mainwindow import Ui_MainWindow #載入Ui介面(ui_mainwindow.py)檔 
from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql

#%%載入外面的.py檔需import檔名 import xxx 或是 from xxx(xxx.py) import yyy(def(yyy))
import add_py_file

#%%不須更動
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        #標準模板，照打就對了
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #呼叫自己設定的按鈕觸發function()
        self.run()

        # 與資料庫連線
        self.db = pymysql.connect(host='127.0.0.1',
                              user='root',
                              password='123456',
                              database='testDB')  # 需在Workbench先建立空的database
        
        self.cursor = self.db.cursor()
        print("--資料庫已連線--")
        
#%%所有按鈕觸發條件加在這裡------------------------------------
# lineEdit: 輸入SQL語法用  參考: https://blog.csdn.net/cpf945/article/details/90215725
# textEdit: 顯示SQL語法用
# TableWidget: 顯示查詢結果用  參考: https://www.cnblogs.com/linyfeng/p/11832237.html, https://stackoverflow.com/questions/37355294/qt-clearing-a-qtablewidget-in-order-to-display-new-items
# QComboBox: 下拉選單 參考: https://shengyu7697.github.io/python-pyqt-qcombobox/

    def run(self):
        self.pushButton.clicked.connect(self.select_show)  # pushButton: 按鈕觸發
        self.power_off.clicked.connect(self.shut_down)  # pushButton: 按鈕觸發


        self.textEdit.setText('顯示輸入指令')  # textEdit: 重新顯示字串
        self.textEdit.append('追加字串')  # textEdit: 追加字串(格行顯示)
        number = 777
        show_num = str(number)
        self.textEdit.append(show_num)  # textEdit: 顯示數字(必須先轉字串)
        
        
        
#%%自行定義的function()-------------------------------------------
    #1.讀取自己class的def()
    # 搜尋Query
    def select_show(self):
        aggregate = self.comboBox.currentText()  # comboBox: aggregate_func
        print("下拉選單=", aggregate)
        
        SELECT = self.lineEdit.text()  # lineEdit: 接收外部字串
        FROM = self.lineEdit_2.text()
        WHERE = self.textEdit_2.toPlainText()
        GROUP_BY = self.lineEdit_3.text()
        HAVING = self.lineEdit_4.text()

        
        # 排除沒有where, group_by時
        if GROUP_BY == '':
            if WHERE == '':
                sql = """
                    SELECT %s
                    FROM %s
                """ %(SELECT, FROM)
                print('WHERE NULL')
            else:
                sql = """
                    SELECT %s
                    FROM %s
                    WHERE %s
                """ %(SELECT, FROM, WHERE)
        else:
            if HAVING == '':       
                if WHERE == '':
                    sql = """
                        SELECT %s
                        FROM %s
                        GROUP BY %s
                    """ %(SELECT, FROM, GROUP_BY)
                    print('WHERE NULL')
                else:
                    sql = """
                        SELECT %s
                        FROM %s
                        WHERE %s
                        GROUP BY %s
                    """ %(SELECT, FROM, WHERE, GROUP_BY)
            else:
                if WHERE == '':
                    sql = """
                        SELECT %s
                        FROM %s
                        GROUP BY %s
                        HAVING %s
                    """ %(SELECT, FROM, GROUP_BY, HAVING)
                    print('WHERE NULL')
                else:
                    sql = """
                        SELECT %s
                        FROM %s
                        WHERE %s
                        GROUP BY %s
                        HAVING %s
                    """ %(SELECT, FROM, WHERE, GROUP_BY, HAVING)
                
        

        # -------------------------------textEdit (顯示SQL指令)-------------------------
        print(sql)
        self.textEdit.setText(sql)  # textEdit: 顯示字串
        # -----------------------------------------------------------------------------

        # show_table = """
        #     SHOW tables
        # """
        # self.cursor.execute(show_table)
        # show = self.cursor.fetchall()
        # print("ttttt\n",show,"\n")
        
        try:
            self.cursor.execute(sql)  # 執行select命令
 
            
            # 獲取所有紀錄列表
                # fetchone(): 獲取單條數據 (若為單變數，需加%(,))
                # fetchall(): 獲取全部數據
            results = self.cursor.fetchall()
            print("資料列數:", len(results))
            print("Result=%s" %(results,))
            
            

            
            # -------------------------------TableWidget (顯示查詢結果)-------------------------
            self.tableWidget.setRowCount(0)  # 清除前一次查詢的表格
            # 抓出想要的值
            for row in results:
                
                # 抓出Table屬性attribute--------------------
                title = []
                for i in range(len(row)):
                    title.append(self.cursor.description[i][0])  # 抓取欄位名稱
                #print("屬性:", title)
                # ------------------------------------------
                
                # 最簡易寫法:
                """
                print(row)
                id = row[0]  # 單條看有幾個attribute
                fname = row[1]
                lname = row[2]
                age = row[3]
                sex = row[4]
                dno = row[5]
                print("id=%s, fname=%s, lname=%s, age=%s, sex=%s, dno=%s" %(id, fname, lname, age, sex, dno))    
                """            
                
                self.tableWidget.setColumnCount(len(row))  # QTableWidget: 設置欄位的"長度"
                #self.tableWidget.setHorizontalHeaderLabels(['id','first_name','last_name','age','sex','dno'])  # 設定欄位"Title"
                self.tableWidget.setHorizontalHeaderLabels(title)  # 設定欄位"Title"
                
                print("查詢Table屬性個數:", len(row), "\n")
                
                self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)  # 自適應表格寬度
                # self.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
                # self.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
                # self.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
                self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 設置表格不可更改(預設:可以更改)
                        
                # 在表格中添加內容-前處理(算出有幾個attribute)
                    #items = [['1','Mac','Mohan','20','M','1'],['2','NN','GG','10','G','2']]  # 範例格式1
                    #items = [[id, fname, lname, age, se0x, dno]]  # 範例格式2
                items = []
                for i in range(len(row)):  # 抓取attribute (寫一個可調變的items空間)
                    items.append(row[i])
                    self.tableWidget.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents) 
                items = [items]
                
                print(items)
                
                # 在表格中添加內容-屬性插入表格
                for i in range(len(items)):
                    item = items[i]
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    print("item=",item)
                    for j in range(len(item)):
                        item = QtWidgets.QTableWidgetItem(str(items[i][j]))
                        self.tableWidget.setItem(row,j,item)
            # -----------------------------------------------------------------------------------------------
                
        except:
            print("QUERY error")
            

    def shut_down(self):
        print("--資料庫連線結束--")
        self.db.close()
        


