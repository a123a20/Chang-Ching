#此為加入邏輯判斷的程式 (另一個ui_mainwindow.py檔會被刷新，需在Pyqt5的Ui介面修改，只需注意ui變數名稱即可)

from PyQt5.QtWidgets import QMainWindow
from ui_mainwindow import Ui_MainWindow #載入Ui介面(ui_mainwindow.py)檔 
from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql

#%%載入外面的.py檔需import檔名 import xxx 或是 from xxx(xxx.py) import yyy(def(yyy))
#import add_py_file

#%%不須更動
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        #標準模板，照打就對了
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        # 與資料庫連線
        self.db = pymysql.connect(host='127.0.0.1',
                              user='root',
                              password='123456',
                              database='rental_system')  # 需在Workbench先建立空的database
        
        self.cursor = self.db.cursor()
        print("--資料庫已連線--")
        
        self.run()
        
        
#%%所有按鈕觸發條件加在這裡------------------------------------
# comboBox(下拉選單): 選擇"租客"、"房東"  
    # 讀取文字: self.comboBox.currentText()
    # 更新讀取: self.comboBox.currentIndexChanged.connect()
    # 手動新增選項: self.comboBox_2.addItem()
    # 清空選項: self.comboBox_2.clear()
    # 參考: https://shengyu7697.github.io/python-pyqt-qcombobox/
# label(純文字): 
    # 印出文字: self.label.setText()
# pushButton(按鈕):
    # self.pushButton.clicked.connect()
# tableWidget(表格控鍵):
    # 設定欄位長度: self.tableWidget.setColumnCount()
    # 設定欄位名稱columns: self.tableWidget.setHorizontalHeaderLabels(columns)
    # 自適應表格寬度: self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch),
                    #self.tableWidget.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)  # i=第幾列
    # 插入第幾列: self.tableWidget.insertRow()
    # 計算目前表格行數/列數: self.tableWidget.columnCount(), self.tableWidget.rowCount()
    # 放入物件: self.tableWidget.setItem(row,j,QTableWidgetItem), QTableWidgetItem = QtWidgets.QTableWidgetItem()
    # 參考: https://www.cnblogs.com/linyfeng/p/11832237.html
# lineEdit(單列字符串):
    # 讀取文字: self.lineEdit.text()
    # 印出文字: self.textEdit.setText()
    # 參考: https://blog.csdn.net/cpf945/article/details/90215725
# textEdit:
    # 讀取輸入之文字: self.textEdit.toPlainText()
# tabWidget(切換視窗):
    # 修該page名稱: self.tabWidget.setTabText(columns,'文字') 
    
    def run(self):
        # 介面選擇
        self.tabWidget.setTabText(0,'查詢')  # 改名子
        self.tabWidget.setTabText(1,'新增合約')
        self.tabWidget.setTabText(2,'刪除合約')
        self.tabWidget.setTabText(3,'更新合約')
        self.tabWidget.setTabText(4,'SQL指令')
        self.add_name()
        
    # Tab1 查詢
        # 當切換comboBox選項時，更新讀取文字
        self.comboBox.currentIndexChanged.connect(self.comboBox_change)  
        self.comboBox_2.currentIndexChanged.connect(self.lendlord_condition)  
        # ---當按下搜尋鍵時，顯示搜尋結果---
        self.pushButton.clicked.connect(self.Query)  
        
    # Tab2 新增
        # 新增合約下拉選單點完-顯示房東/租客身分證、獲取房子地址
        self.comboBox_4.currentIndexChanged.connect(self.show_ID) 
        self.comboBox_5.currentIndexChanged.connect(self.show_ID2) 
        self.comboBox_6.currentIndexChanged.connect(self.show_room_number)
        # 顯示現有合約
        self.pushButton_4.clicked.connect(self.show_contract)
        # ---當按下新增鍵時，新增資料---
        self.pushButton_2.clicked.connect(self.Insert)
        
    # Tab3 刪除
        # 顯示現有合約
        self.pushButton_3.clicked.connect(self.show_contract)
        # ---當按下刪除鍵時，刪除資料---
        self.pushButton_6.clicked.connect(self.Delete_contract)
        
        
    # Tab4 更新
        # 讀取現有合約
        self.pushButton_7.clicked.connect(self.load_contract_number)
        # 指定合約編號
        self.comboBox_8.currentIndexChanged.connect(self.load_now_contract_values) 
        # ---當按下更新鍵時，更新資料---
        self.pushButton_8.clicked.connect(self.Update_contract)
    
    # Tab5 SQL指令
        # 觸發按鈕
        self.pushButton_9.clicked.connect(self.SQL_order)
    
    # 資料庫結束連線
        self.pushButton_5.clicked.connect(self.shut_down)
        

        
        
#%%自行定義的function()-------------------------------------------
    #1.讀取自己class的def()
    # 測試區
    
    #%% ------------------------------------Tab5: SQL指令------------------------------------------------
    # 輸入SQL指令
    def SQL_order(self):
        sql_text = self.textEdit.toPlainText()
        print(sql_text)
        sql = """
            %s
        """ %(sql_text)
        try:
            self.cursor.execute(sql)  # 執行select命令
            results = self.cursor.fetchall()
            self.db.commit()
        except:
            print("SQL order error")
            self.db.rollback()
            
        print("輸入完成")
        
        self.show_tabelWidget(results)
    
    #%% ------------------------------------Tab4: 更新合約------------------------------------------------
    # 按下"更新"時進入
    def Update_contract(self):
        rent = self.lineEdit_13.text()
        ebill = self.lineEdit_15.text()
        water = self.lineEdit_12.text()
        rent_start = self.lineEdit_16.text()
        rent_end = self.lineEdit_14.text()
        
        contract_number = self.comboBox_8.currentText()
        sql = """
            UPDATE 合約
            SET 每月租金 = '%s', 每月電費 = '%s', 每月水費 = '%s', 租期開始 = '%s', 租期結束 = '%s'
            WHERE 合約編號 = '%s'
        """ %(rent, ebill, water, rent_start, rent_end, contract_number)
        try:
            self.cursor.execute(sql)  # 執行select命令
            self.db.commit()
        except:
            print("Update error")
            self.db.rollback()
        
    
    
    # 更新合約-下拉選項(讀取現有合約)
    def load_contract_number(self):
        self.comboBox_8.clear()
        sql = """
            SELECT 合約編號
            FROM 合約
        """
        self.comboBox_8.addItem('')
        self.cursor.execute(sql)  # 執行select命令
        get_contract_number = self.cursor.fetchall()
        
        for i in range(len(get_contract_number)):
            self.comboBox_8.addItem(str(get_contract_number[i][0]))  # 插入合約編號(因編號是int，需轉成str)
        self.show_contract()
    
    # 更新合約-印出當前合約各項內容
    def load_now_contract_values(self):
        contract_number = self.comboBox_8.currentText()
        sql = """
            SELECT 房東.房東姓名, 合約.房東身分證, 租客.租客姓名, 合約.租客身分證, 房子地址, 房號, 每月租金, 每月電費, 每月水費, 租期開始, 租期結束
            FROM 合約, 房東, 租客
            WHERE 合約.房東身分證 = 房東.房東身分證 and 合約.租客身分證 = 租客.租客身分證
                  and 合約.合約編號 = '%s'
        """ %(contract_number)
        self.cursor.execute(sql)  # 執行select命令
        get_contract_values = self.cursor.fetchall()
        print("label23=",get_contract_values[0][0])
        self.label_23.setText(get_contract_values[0][0])
        self.label_24.setText(get_contract_values[0][1])
        self.label_27.setText(get_contract_values[0][2])
        self.label_28.setText(get_contract_values[0][3])
        self.label_36.setText(get_contract_values[0][4])
        self.label_37.setText(get_contract_values[0][5])
        self.lineEdit_13.setText(str(get_contract_values[0][6]))
        self.lineEdit_15.setText(str(get_contract_values[0][7]))
        self.lineEdit_12.setText(str(get_contract_values[0][8]))
        self.lineEdit_16.setText(str(get_contract_values[0][9]))
        self.lineEdit_14.setText(str(get_contract_values[0][10]))
        print(get_contract_values)
        
    
    #%% ------------------------------------Tab3: 刪除合約------------------------------------------------
    # 按下"刪除"時進入
    def Delete_contract(self):
        contract_numbers = self.lineEdit_9.text()
        sql = """
            DELETE FROM 合約
            WHERE 合約.合約編號 = '%s'
        """ %(contract_numbers)
        try:
            self.cursor.execute(sql)  # 執行select命令
            self.db.commit()
        except:
            print("Delete error")
            self.db.rollback()
    
    # 刪除合約-顯示現有合約
    def show_contract(self):
        sql = """
            SELECT 合約編號, 房東.房東姓名, 合約.房東身分證, 租客.租客姓名, 合約.租客身分證, 房子地址, 房號, 每月租金, 每月電費, 每月水費, 租期開始, 租期結束
            FROM 合約, 房東, 租客
            WHERE 合約.房東身分證 = 房東.房東身分證 and 合約.租客身分證 = 租客.租客身分證
        """
        
        
        self.cursor.execute(sql)  # 執行select命令
        
        # 獲取所有紀錄列表(重複)
        try:
            # fetchone(): 獲取單條數據 (若為單變數，需加%(,))
            # fetchall(): 獲取全部數據
            self.cursor.execute(sql)  # 執行select命令

            results = self.cursor.fetchall()
            print("資料列數:", len(results))
            print("Result=%s" %(results,), '\n')
            
        except:
            print("Select Error") 
        self.show_tabelWidget(results)  # 顯示表格搜尋結果

    #%% ------------------------------------Tab2: 新增合約------------------------------------------------
    # 按下"新增"時進入
    def Insert(self):
        rent = self.lineEdit_4.text()
        ebill = self.lineEdit_5.text()
        water = self.lineEdit_6.text()
        rent_start = self.lineEdit_7.text()
        rent_end = self.lineEdit_8.text()
        
        self.get_r_number = self.comboBox_7.currentText()  # 房間號
        print("房東ID 租客ID 房子地址 房號 租金 電費 水費 租期開始 租期結束")
        print(self.get_ID, self.get_ID2, self.get_h_address,self.get_r_number, rent, ebill, water, rent_start, rent_end)
        
        sql = "INSERT INTO 合約(每月電費, 每月水費, 每月租金, 租期開始, 租期結束, 合約.房東身分證, 合約.租客身分證, 合約.房子地址, 合約.房號) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
              % (ebill, water, rent, rent_start, rent_end, self.get_ID, self.get_ID2, self.get_h_address, self.get_r_number)
              
        try:
            # 執行sql命令
            self.cursor.execute(sql)
            # 提交到數據庫執行
            self.db.commit()
            self.label_20.setText('新增完成!')
        except:
            # 如果發生錯誤回滾
            print("Insert error")
            self.db.rollback()
            self.label_20.setText('未填寫完整')
        
        # 清空新增區的內容值
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.label_16.clear()
        self.label_17.clear()
        
    # 新增合約-下拉選項
    def add_name(self):
        get_tenant_name = """
            SELECT 租客姓名
            FROM 租客
        """
        get_landlord_name = """
            SELECT 房東姓名
            FROM 房東
        """
        get_house_address = """
            SELECT 房子地址
            FROM 房子
        """
        self.comboBox_5.addItem('')
        self.comboBox_4.addItem('')
        self.comboBox_6.addItem('')
        self.cursor.execute(get_tenant_name)  # 執行select命令
        tenant_name = self.cursor.fetchall()   
        self.cursor.execute(get_landlord_name)  # 執行select命令
        landlord_name = self.cursor.fetchall() 
        self.cursor.execute(get_house_address)  # 執行select命令
        house_address = self.cursor.fetchall()
        
        for i in range(len(tenant_name)):
            self.comboBox_5.addItem(tenant_name[i][0])  # 插入租客姓名    
        for i in range(len(landlord_name)):
            self.comboBox_4.addItem(landlord_name[i][0])  # 插入房東姓名
        for i in range(len(house_address)):
            self.comboBox_6.addItem(house_address[i][0])  # 插入房子地址
            
    # 顯示房東身分證
    def show_ID(self):
        self.label_20.clear()  # 清除新增結果提示
        get_name = self.comboBox_4.currentText()  # 租客
        sql = """
            SELECT 房東身分證
            FROM 房東
            WHERE 房東.房東姓名 = '%s'
        """ %(get_name)

        self.cursor.execute(sql)  # 執行select命令
        self.get_ID = self.cursor.fetchall()  # 使用self來共用變數
        self.get_ID = self.get_ID[0][0]
        self.label_16.setText(self.get_ID)
        
        
    # 顯示租客身分證
    def show_ID2(self):
        get_name2 = self.comboBox_5.currentText()  # 房東
        sql2 = """
            SELECT 租客身分證
            FROM 租客
            WHERE 租客.租客姓名 = '%s'
        """ %(get_name2)
        
        self.cursor.execute(sql2)  # 執行select命令
        self.get_ID2 = self.cursor.fetchall()
        self.get_ID2 = self.get_ID2[0][0]
        self.label_17.setText(self.get_ID2)
        
    # 新增合約-房子連結房間
    def show_room_number(self):
        self.comboBox_7.clear()  # 清除上一次切換
        self.get_h_address = self.comboBox_6.currentText()  # 房子地址
        sql3 = """
            SELECT 房間.房號
            FROM 房子, 房間
            WHERE 房子.房子地址 = 房間.房子地址 and 房子.房子地址 = '%s'
        """ %(self.get_h_address)
        self.cursor.execute(sql3)  # 執行select命令
        get_all_room = self.cursor.fetchall()  # 房間根據此變數來插入相對應選項
        
        for i in range(len(get_all_room)):
            print(get_all_room[i][0])
            self.comboBox_7.addItem(get_all_room[i][0])
        
        
            
            

    #%% ------------------------------------Tab1: 查詢------------------------------------------------------
    # 請選擇->"租客"、"房東"，並印出
    def comboBox_change(self):
        self.comboBox_text = self.comboBox.currentText()  # 目前選擇的對象(房東/租客)，內容由UI創建
        if self.comboBox_text != '合約':
            self.label.setText(self.comboBox_text)  # 印出label
            self.label_3.setText(self.comboBox_text)
            self.label_5.setText(self.comboBox_text)
    
        
        # 指定條件-更改下拉選項
        self.comboBox_2.clear()  # 清空過去插入
        self.comboBox_3.clear()
        #self.comboBox_4.clear()
        #self.comboBox_5.clear()
        #self.comboBox_6.clear()
        #self.comboBox_7.clear()
        self.comboBox_9.clear()  # 租客姓名限定功能
        if self.comboBox.currentText() == '租客':
            self.comboBox_2.addItem('')
            self.comboBox_2.addItem('未繳')
            self.comboBox_2.addItem('已繳')
            self.comboBox_3.addItem('')
            self.comboBox_3.addItem('全部')
            self.comboBox_3.addItem('租金')
            self.comboBox_3.addItem('水費')
            self.comboBox_3.addItem('電費')
            self.comboBox_9.addItem('')
            self.comboBox_9.addItem('IN')
            self.comboBox_9.addItem('NOT IN')
            self.comboBox_9.addItem('EXISTS')
            self.comboBox_9.addItem('NOT EXISTS')
            
        elif self.comboBox.currentText() == '房東':
            self.comboBox_2.addItem('')
            self.comboBox_2.addItem('每月可收入')
            self.comboBox_2.addItem('平均租金')
            self.comboBox_2.addItem('最高租金')
            self.comboBox_2.addItem('最低租金')
            self.comboBox_2.addItem('空房數量')
            self.comboBox_2.addItem('租兩間以上租客')
            self.comboBox_3.addItem('')
         
    # 房東-指定條件查詢
    def lendlord_condition(self):
        condition = self.comboBox_2.currentText()
        print(condition)
        if condition == '每月可收入':
            function = 'SUM'
            new_name = '每月總收入'
        elif condition == '平均租金':
            function = 'AVG'
            new_name = '平均租金'
        elif condition == '最高租金':
            function = 'MAX'
            new_name = '最高租金'
        elif condition == '最低租金':
            function = 'MIN'
            new_name = '最低租金'
        else:
            function = ''
            new_name = ''
            
        sql = """
            SELECT 房東.房東身分證, 房東姓名, %s(每月租金) AS %s
            FROM 房東, 合約
            WHERE 房東.房東身分證 = 合約.房東身分證
            GROUP BY 房東.房東身分證
        """ %(function, new_name)
        
        # 有GROUP才能做SUM、MAX等運算
        if condition == '空房數量':
            sql = """
                SELECT 房東.房東身分證, 房東姓名, COUNT(*) AS 空房數量
                FROM 房東, 提供房, 房間
                WHERE 房東.房東身分證 = 提供房.房東身分證 and 提供房.房子地址 = 房間.房子地址 and 房間.出租狀態='空房'
                GROUP BY 房東.房東身分證
            """
        # 找出不只租一間的租客，顯示個人資料
        if condition =='租兩間以上租客':
            sql = """
                SELECT 租客姓名, 租客身分證
                FROM 租客
                WHERE 租客.租客身分證 IN (
                	SELECT 合約.租客身分證
                	FROM 合約
                	GROUP BY 合約.租客身分證
                	HAVING COUNT(*)>1);
            """
            
        self.cursor.execute(sql)  # 執行select命令
        results = self.cursor.fetchall()
        self.show_tabelWidget(results)  # 顯示表格查詢結果 
         
            
    # ------------------------按下"查詢"時進入---------------------------------------------------
    def Query(self):
        people = self.comboBox.currentText()  # 目前選擇的對象(房東/租客)
        condition = self.comboBox_2.currentText()  # 目前選擇的指定條件1(已繳/未繳)
        condition2 = self.comboBox_3.currentText()  # 目前選擇的指定條件2(租金/水費/電費)
        nested = self.comboBox_9.currentText()  # IN/NOT IN/EXISTS/NOT EXISTS (針對租客姓名做關聯)
        
        
        print(condition2)
        if condition == '未繳':
            pay_state = 'X'
        elif condition == '已繳':
            pay_state = 'O'
        
        name = self.lineEdit.text()  # 姓名
        ID = self.lineEdit_2.text()  # 身分證
        phone = self.lineEdit_3.text()  # 電話
        
        # SQL指令
        if people == '房東':
            if name == '' and ID == '' and phone == '':
                sql = """
                    SELECT 房東.房東身分證, 房東姓名, 房東電話, 提供房.房子地址, 房子名稱
                    FROM 房東, 提供房, 房子
                    WHERE 房東.房東身分證 = 提供房.房東身分證 and 提供房.房子地址 = 房子.房子地址
                """
            elif name != '':
                sql = """
                    SELECT 房東.房東身分證, 房東姓名, 房東電話, 提供房.房子地址, 房子名稱
                    FROM 房東, 提供房, 房子
                    WHERE 房東.房東身分證 = 提供房.房東身分證 and 提供房.房子地址 = 房子.房子地址
                          and 房東.房東姓名 = '%s'
                """ %(name)
                
            elif ID != '':
                sql = """
                    SELECT 房東.房東身分證, 房東姓名, 房東電話, 提供房.房子地址, 房子名稱
                    FROM 房東, 提供房, 房子
                    WHERE 房東.房東身分證 = 提供房.房東身分證 and 提供房.房子地址 = 房子.房子地址
                          and 房東.房東身分證 = '%s'
                """ %(ID)
                
            elif phone != '':
                sql = """
                    SELECT 房東.房東身分證, 房東姓名, 房東電話, 提供房.房子地址, 房子名稱
                    FROM 房東, 提供房, 房子
                    WHERE 房東.房東身分證 = 提供房.房東身分證 and 提供房.房子地址 = 房子.房子地址
                          and 房東.房東電話 = '%s'
                """ %(phone)
                
        elif people == '租客':
            # 都不填
            if name == '' and ID == '' and phone == '':
                sql = """
                    SELECT 租客.租客身分證, 租客姓名, 合約.合約編號, 租客電話, 繳費.繳租金, 繳費.繳水費, 繳費.繳電費, 合約.房子地址, 合約.房號
                    FROM 租客, 合約, 繳費
                    WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                """
                
                # 指定條件(未繳/已繳 -> 租金/水費/電費)
                if condition != '' and condition2 != '':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳%s, 合約.每月%s
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and 繳費.繳%s = '%s'
                    """ %(condition2, condition2, condition2, pay_state)
                    
                if condition == '未繳' and condition2 == '全部':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳租金, 繳費.繳電費, 繳費.繳水費
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and (繳費.繳租金 ='X' or 繳費.繳水費='X' or 繳費.繳電費='X')
                    """ 
                elif condition == '已繳' and condition2 == '全部':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳租金, 繳費.繳電費, 繳費.繳水費
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and 繳費.繳租金 ='O' and 繳費.繳水費='O' and 繳費.繳電費='O'
                    """ 
            # 有填名子        
            elif name != '':
                sql = """
                    SELECT 租客.租客身分證, 租客姓名, 合約.合約編號, 租客電話, 繳費.繳租金, 繳費.繳水費, 繳費.繳電費, 合約.房子地址, 合約.房號
                    FROM 租客, 合約, 繳費
                    WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                          and 租客.租客姓名 ='%s'
                """ %(name)
                
                # IN/EXIST條件 -> 只針對 已繳/未繳選項-----------------------------------------------
                if condition == '未繳':
                    if nested == 'IN' or nested == 'NOT IN':
                        sql = """
                            SELECT 租客.租客身分證 AS 有未繳_租客身分證, 租客姓名, 租客電話
                            FROM 租客
                            WHERE 租客.租客身分證 %s (
                                SELECT 合約.租客身分證
                                FROM 合約, 繳費
                                WHERE 合約.合約編號 = 繳費.合約編號
                                      and (繳費.繳租金 ='X' or 繳費.繳水費='X' or 繳費.繳電費='X')
                                      and 租客.租客姓名='%s')
                        """ %(nested, name)
                    elif nested == 'EXISTS' or nested == 'NOT EXISTS':
                        sql = """
                            SELECT 租客.租客身分證 AS 部分未繳_租客身分證, 租客姓名, 租客電話
                            FROM 租客
                            WHERE %s (
                                SELECT *
                                FROM 合約, 繳費
                                WHERE 合約.合約編號 = 繳費.合約編號
                                      and (繳費.繳租金 ='X' or 繳費.繳水費='X' or 繳費.繳電費='X')
                                      and 租客.租客姓名='%s')
                        """ %(nested, name)

                elif condition == '已繳':
                    if nested == 'IN' or nested == 'NOT IN':
                        sql = """
                            SELECT 租客.租客身分證 AS 繳清_租客身分證, 租客姓名, 租客電話
                            FROM 租客
                            WHERE 租客.租客身分證 %s (
                                SELECT 合約.租客身分證
                                FROM 合約, 繳費
                                WHERE 合約.合約編號 = 繳費.合約編號
                                      and 繳費.繳租金 ='O' and 繳費.繳水費='O' and 繳費.繳電費='O'
                                      and 租客.租客姓名='%s')
                        """ %(nested, name)
                    elif nested == 'EXISTS' or nested == 'NOT EXISTS':
                        sql = """
                            SELECT 租客.租客身分證 AS 部分已繳_租客身分證, 租客姓名, 租客電話
                            FROM 租客
                            WHERE %s (
                                SELECT *
                                FROM 合約, 繳費
                                WHERE 合約.合約編號 = 繳費.合約編號
                                      and 繳費.繳租金 ='O' and 繳費.繳水費='O' and 繳費.繳電費='O'
                                      and 租客.租客姓名 = '%s')
                        """ %(nested, name)
                # ---------------------------------------------------------------------------------
                
                # 指定條件(未繳/已繳 -> 租金/水費/電費)
                if condition != '' and condition2 != '':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳%s, 合約.每月%s
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and 繳費.繳%s = '%s' and 租客.租客姓名 ='%s'
                    """ %(condition2, condition2, condition2, pay_state, name)
                    

                    
                if condition == '未繳' and condition2 == '全部':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳租金, 繳費.繳電費, 繳費.繳水費
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and (繳費.繳租金 ='X' or 繳費.繳水費='X' or 繳費.繳電費='X')
                              and 租客.租客姓名 ='%s'
                    """ %(name)
                    
                elif condition == '已繳' and condition2 == '全部':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳租金, 繳費.繳電費, 繳費.繳水費
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and 繳費.繳租金 ='O' and 繳費.繳水費='O' and 繳費.繳電費='O'
                              and 租客.租客姓名 ='%s'
                    """  %(name)
                    
                    
            # 有填ID  
            elif ID != '':
                sql = """
                    SELECT 租客.租客身分證, 租客姓名, 合約.合約編號, 租客電話, 繳費.繳租金, 繳費.繳水費, 繳費.繳電費, 合約.房子地址, 合約.房號
                    FROM 租客, 合約, 繳費
                    WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                          and 租客.租客身分證 ='%s'
                """ %(ID)
                
                # 指定條件(未繳/已繳 -> 租金/水費/電費)
                if condition != '' and condition2 != '':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳%s, 合約.每月%s
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and 繳費.繳%s = '%s' and 租客.租客身分證 ='%s'
                    """ %(condition2, condition2, condition2, pay_state, ID)
                    
                if condition == '未繳' and condition2 == '全部':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳租金, 繳費.繳電費, 繳費.繳水費
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and (繳費.繳租金 ='X' or 繳費.繳水費 ='X' or 繳費.繳電費='X')
                              and 租客.租客身分證 ='%s'
                    """ %(ID)
                elif condition == '已繳' and condition2 == '全部':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳租金, 繳費.繳電費, 繳費.繳水費
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and 繳費.繳租金 ='O' and 繳費.繳水費 ='O' and 繳費.繳電費='O'
                              and 租客.租客身分證 ='%s'
                    """  %(ID)
            # 有填手機
            elif phone != '':
                sql = """
                    SELECT 租客.租客身分證, 租客姓名, 合約.合約編號, 租客電話, 繳費.繳租金, 繳費.繳水費, 繳費.繳電費, 合約.房子地址, 合約.房號
                    FROM 租客, 合約, 繳費
                    WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                          and 租客.租客電話 ='%s'
                """ %(phone)
                
                # 指定條件(未繳/已繳 -> 租金/水費/電費)
                if condition != '' and condition2 != '':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳%s, 合約.每月%s
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and 繳費.繳%s = '%s' and 租客.租客電話 ='%s'
                    """ %(condition2, condition2, condition2, pay_state, phone)
                    
                if condition == '未繳' and condition2 == '全部':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳租金, 繳費.繳電費, 繳費.繳水費
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and (繳費.繳租金 ='X' or 繳費.繳水費 ='X' or 繳費.繳電費='X')
                              and 租客.租客電話 ='%s'
                    """ %(phone)
                elif condition == '已繳' and condition2 == '全部':
                    sql = """
                        SELECT 租客.租客身分證, 租客姓名, 合約.房子地址, 合約.房號, 繳費.繳租金, 繳費.繳電費, 繳費.繳水費
                        FROM 租客, 合約, 繳費
                        WHERE 租客.租客身分證 = 合約.租客身分證 and 合約.合約編號 = 繳費.合約編號
                              and 繳費.繳租金 ='O' and 繳費.繳水費 ='O' and 繳費.繳電費='O'
                              and 租客.租客電話 ='%s'
                    """  %(phone)
        
        # 獲取所有紀錄列表
        try:
            # fetchone(): 獲取單條數據 (若為單變數，需加%(,))
            # fetchall(): 獲取全部數據
            self.cursor.execute(sql)  # 執行select命令

            results = self.cursor.fetchall()
            print("資料列數:", len(results))
            print("Result=%s" %(results,), '\n')
            
        except:
            print("Select Error")            
            
        self.show_tabelWidget(results)  # 顯示表格搜尋結果
    # ------------------------------------------------------------------------------------------------------
            
    def shut_down(self):
        print("--資料庫結束連線--")
        self.db.close()

    #%% -------------------------------TableWidget (顯示查詢結果)---------------------------------------
    def show_tabelWidget(self, results):
        try:
            self.tableWidget.setRowCount(0)  # 清除前一次查詢的表格
            # 抓出想要的select值
            for row in results:
                
                # 抓出Table屬性attribute--------------------
                columns = []  # Title of attribute
                items = []  # All values of attribute
                
                for i in range(len(row)):
                    columns.append(self.cursor.description[i][0])  # 抓取欄位屬性名稱
                #print("屬性名稱:", columns)       
                
                self.tableWidget.setColumnCount(len(row))  # QTableWidget: 設置欄位的"長度"
                self.tableWidget.setHorizontalHeaderLabels(columns)  # 設定欄位"Title"
                #print("查詢Table屬性個數:", len(row), "\n")
                
                self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)  # 自適應表格寬度
                #self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 設置表格不可更改(預設:可以更改)
                
                for i in range(len(row)):  # 抓取attribute (寫一個可調變的items空間)
                    items.append(row[i])  # 添加attribute
                    self.tableWidget.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)  # 最佳化表格寬度
                items = [items]
                
                # 在表格中添加內容-屬性插入表格
                for i in range(len(items)):
                    item = items[i]
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    #print("item=",item)
                    for j in range(len(item)):
                        item = QtWidgets.QTableWidgetItem(str(items[i][j]))
                        self.tableWidget.setItem(row,j,item)
        except:
            print("Show Error")