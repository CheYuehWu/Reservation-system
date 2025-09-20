# orders 顯示空房 的UI







# orders和customers的顯示某日空房
# orders的查詢新增修改刪除
# customer UI
# orders 表格顯示
# 日期用方格找




import pymysql
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,QHBoxLayout
from PyQt5.QtCore import QDate, QDateTime, QTime
from PyQt5.QtWidgets import QDateTimeEdit
# import charts


db_settings={
    "host":"localhost",
    'port':3306,
    "user":"root",
    "password":"password",
    "db":"room_booking",
    "charset":"utf8"
}

class CustomerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Management")  # 設定視窗標題
        self.setGeometry(400, 0, 1000, 800)  # 設定視窗大小與位置
        self.initUI()  # 初始化介面
        self.conn = pymysql.connect(**db_settings)
        self.cursor = self.conn.cursor()
          
         # 載入資料庫中的客戶資料
    """初始化使用者介面"""
    def initUI(self):
        main_layout = QHBoxLayout()  # 使用垂直佈局
        layout = QVBoxLayout()  # 使用垂直佈局
        layout1 = QVBoxLayout()  # 使用垂直佈局
        layout2 = QVBoxLayout()  # 使用垂直佈局

        # 表格元件，用於顯示客戶資料
        self.Cus_table = QTableWidget()
        self.Cus_table.setColumnCount(3)  # 設定表格的列數
        self.Cus_table.setHorizontalHeaderLabels(["cid", "Name", "Phone"])
        layout.addWidget(self.Cus_table)  # 將表格加入佈局

        self.Orders_table = QTableWidget()
        self.Orders_table.setColumnCount(5)
        self.Orders_table.setHorizontalHeaderLabels(["oid", "Check In Date", "Check Out Date", "Number of People", "Customer ID"])
        layout1.addWidget(self.Orders_table)
        # 載入客戶資料

        
        

        # 輸入框：用於輸入客戶姓名
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter Name")  # 提示文字
        layout.addWidget(self.name_input)

        # 輸入框：用於輸入客戶電話
        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Enter Phone")  # 提示文字
        layout.addWidget(self.phone_input)

        # self.check_in_date = QLineEdit(self)
        # self.check_in_date.setPlaceholderText("Enter check in date")  # 提示文字
        # layout1.addWidget(self.check_in_date)

        self.check_in_date = QDateTimeEdit(QDate.currentDate(), self)
        self.check_in_date.setDisplayFormat('yyyy-MM-dd')
        self.check_in_date.setDisplayFormat('yyyy.MM.dd')
        self.check_in_date.setMinimumDate(QDate.currentDate().addDays(-3650))
        self.check_in_date.setMaximumDate(QDate.currentDate().addDays(3650))
        self.check_in_date.setCalendarPopup(True)  # 顯示日曆選擇器
        label = QLabel("Check In Date")
        layout1.addWidget(label)
        layout1.addWidget(self.check_in_date)


        # self.check_out_date = QLineEdit(self)
        # self.check_out_date.setPlaceholderText("Enter check out date")
        # layout1.addWidget(self.check_out_date)
        self.check_out_date = QDateTimeEdit(QDate.currentDate(), self)
        self.check_out_date.setDisplayFormat('yyyy-MM-dd')
        self.check_out_date.setDisplayFormat('yyyy.MM.dd')
        self.check_out_date.setMinimumDate(QDate.currentDate().addDays(-3650))
        self.check_out_date.setMaximumDate(QDate.currentDate().addDays(3650))
        self.check_out_date.setCalendarPopup(True)  # 顯示日曆選擇器
        label = QLabel("Check Out Date")
        layout1.addWidget(label)
        layout1.addWidget(self.check_out_date)

        self.num_of_people = QLineEdit(self)
        self.num_of_people.setPlaceholderText("Enter number of people")
        layout1.addWidget(self.num_of_people)
    
        self.cid = QLineEdit(self)
        self.cid.setPlaceholderText("Enter customer ID")
        layout1.addWidget(self.cid)

        self.eid = QLineEdit(self)
        self.eid.setPlaceholderText("Enter employee ID")
        layout1.addWidget(self.eid)

        self.rid = QLineEdit(self)
        self.rid.setPlaceholderText("Enter room ID")
        layout1.addWidget(self.rid)



        # 按鈕：新增客戶
        self.add_button = QPushButton("Add Customer")
        self.add_button.clicked.connect(self.add_customer)  # 綁定按鈕點擊事件
        layout.addWidget(self.add_button)
        self.add_button1 = QPushButton("Add Orders")
        self.add_button1.clicked.connect(self.add_customer) # 綁定按鈕點擊事件
        layout1.addWidget(self.add_button1)
        print("add button")




        # 按鈕：更新選中的客戶
        self.update_button = QPushButton("Update Selected Customer")
        self.update_button.clicked.connect(self.update_customer)  # 綁定按鈕點擊事件
        layout.addWidget(self.update_button)
        self.update_button1 = QPushButton("Update Selected Order")
        self.update_button1.clicked.connect(self.update_orders)  # 綁定按鈕點擊事件
        layout1.addWidget(self.update_button1)

         # 按鈕：刪除選中的客戶
        self.delete_button = QPushButton("Delete Selected Customer")
        # self.delete_button.clicked.connect(self.delete_customer())  # 綁定按鈕點擊事件
        self.delete_button.clicked.connect(lambda: self.delete_customer(self.Cus_table, "Customer"))
        layout.addWidget(self.delete_button)

        self.delete_button1 = QPushButton("Delete Selected Orders")
        self.delete_button1.clicked.connect(lambda: self.delete_customer(self.Orders_table, "Orders"))
        layout1.addWidget(self.delete_button1)

        

        self.find_button = QPushButton("Find Available Room")
        self.find_button.clicked.connect(self.check_availability)  # 綁定按鈕點擊事件
        layout2.addWidget(self.find_button)

        

        # dateTimeEdit = QDateTimeEdit(self)
        # # 指定当前日期时间为控件的日期时间
        # dateTimeEdit2 = QDateTimeEdit(QDateTime.currentDateTime(), self)
        # 指定当前地日期为控件的日期，注意没有指定时间
        # dateEdit = QDateTimeEdit(QDate.currentDate(), self)
        # 指定当前地时间为控件的时间，注意没有指定日期
        # timeEdit = QDateTimeEdit(QTime.currentTime(), self)
        # dateEdit.setDisplayFormat('yyyy-MM-dd')
        # dateTimeEdit.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        # dateTimeEdit2.setDisplayFormat('yyyy/MM/dd HH-mm-ss')
        # dateEdit.setDisplayFormat('yyyy.MM.dd')
        # timeEdit.setDisplayFormat('HH:mm:ss')
        # dateEdit.setMinimumDate(QDate.currentDate().addDays(-3650))
        # dateEdit.setMaximumDate(QDate.currentDate().addDays(3650))
        # dateEdit.setCalendarPopup(True)  # 顯示日曆選擇器
        # layout1.addWidget(dateEdit)
       
        main_layout.addLayout(layout)  # 將layout加入主佈局
        main_layout.addLayout(layout1)  # 將layout1加入主佈局
        main_layout.addLayout(layout2)
        self.setLayout(main_layout)  # 設定視窗的佈局

    def load_data(self,table,table_UI):
        self.cursor.execute(f"SELECT * FROM {table}")
        result = self.cursor.fetchall()  # 獲取所有客戶資料
        table_UI.setRowCount(len(result))  # 設定表格的行數
        for row_index, row_data in enumerate(result):
            for column_index, column_data in enumerate(row_data):
                item = QTableWidgetItem(str(column_data))
                table_UI.setItem(row_index, column_index, item)  # 設定表格的每個單元格的資料
        table_UI.resizeColumnsToContents()  # 調整列寬以適應內容
        table_UI.resizeRowsToContents()  # 調整行高以適應內容
        table_UI.setSelectionBehavior(QTableWidget.SelectRows)  # 設定選擇行的行為
        table_UI.setSelectionMode(QTableWidget.SingleSelection)  # 設定單選模式
        table_UI.setEditTriggers(QTableWidget.NoEditTriggers)  # 禁止編輯表格
        table_UI.setAlternatingRowColors(True)  # 設定交替行顏色
        table_UI.setSortingEnabled(True)  # 啟用排序功能
        table_UI.setColumnWidth(0, 100)  # 設定第一列的寬度
        table_UI.setColumnWidth(1, 200)  # 設定第二列的寬度
        table_UI.setColumnWidth(2, 150)  # 設定第三列的寬度
        table_UI.setColumnHidden(0, True)  # 隱藏第一列（Customer ID）
        table_UI.setColumnHidden(2, False)  # 顯示第二列（Phone）
        table_UI.setColumnHidden(1, False)  # 顯示第三列（Name）

    def add_customer(self):
            cname = self.name_input.text()
            phone = self.phone_input.text()
            checkinday = self.check_in_date.text()
            checkoutday = self.check_out_date.text()
            num_of_people = self.num_of_people.text()
            cid = self.cid.text()
            eid = self.eid.text()

            if cname and phone:
                self.cursor.execute("INSERT INTO Customer (cname, phone) VALUES (%s, %s)", (cname, phone))
                
                self.conn.commit()  # 提交事務
                self.load_data("Customer",self.Cus_table)  # 重新載入客戶資料
            elif checkinday and checkoutday and num_of_people and cid and eid:
                self.cursor.execute("INSERT INTO Orders (checkinday, checkoutday, num_of_people, cid, eid) VALUES (%s, %s, %s, %s, %s)", (checkinday, checkoutday, num_of_people, cid, eid))
                self.cursor.execute("Select max(oid) from Orders where cid = %s",cid)  # 獲取最新的oid
                # self.cursor.execute("Insert into Service (oid) values (%s)", self.cursor.fetchone()[0])  # 插入服務資料
                oid = self.cursor.fetchall()
                self.cursor.execute("INSERT INTO Service (rid,oid) VALUES (%s,%s)", (self.rid.text(),oid))  # 插入服務資料
                self.conn.commit()  # 提交事務
                self.load_data("Orders",self.Orders_table)  # 重新載入訂單資料
            else:
                QMessageBox.warning(self, "Input Error", "Please enter both name and phone number.")
              # 重新載入資料




    def delete_customer(self,table_UI,table):
        selected_row = table_UI.currentRow()
        if selected_row >= 0:
            id = table_UI.item(selected_row, 0).text()
            header = table_UI.horizontalHeaderItem(0).text()
            self.cursor.execute(f"DELETE FROM {table} WHERE {header} = {id}",)
            self.conn.commit()
            self.load_data(table,table_UI)  # 重新載入客戶資料
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a customer to delete.")
    def update_orders(self):
        selected_row = self.Orders_table.currentRow()
        if selected_row >= 0:
            oid = self.Orders_table.item(selected_row, 0).text()
            checkinday = self.check_in_date.text()
            checkoutday = self.check_out_date.text()
            num_of_people = self.num_of_people.text()
            cid = self.cid.text()
            eid = self.eid.text()
            if checkinday and checkoutday and num_of_people and cid and eid:
                self.cursor.execute("UPDATE Orders SET checkinday = %s, checkoutday = %s, num_of_people = %s, cid = %s, eid = %s WHERE oid = %s", (checkinday, checkoutday, num_of_people, cid, eid, oid))
                self.conn.commit()
                self.load_data("Orders", self.Orders_table)  # 重新載入訂單資料
            else:
                QMessageBox.warning(self, "Input Error", "Please enter correct information")

    def update_customer(self):
        selected_row = self.Cus_table.currentRow()
        if selected_row >= 0:
            cid = self.Cus_table.item(selected_row, 0).text()
            cname = self.name_input.text()
            phone = self.phone_input.text()
            if cname and phone:
                self.cursor.execute("UPDATE Customer SET cname = %s, phone = %s WHERE cid = %s", (cname, phone, cid))
                self.conn.commit()
                self.load_data("Customer", self.Cus_table)  # 重新載入客戶資料
            else:
                QMessageBox.warning(self, "Input Error", "Please enter both name and phone number .")

    def check_availability(self):
        checkinday = self.check_in_date.text()
        checkoutday = self.check_out_date.text()
        #從service裡找到是否有rid再列印出來
        self.cursor.execute("SELECT rid FROM Room where rid NOT IN\
        (SELECT Service.rid FROM Service INNER JOIN Orders ON Service.oid = Orders.oid AND Orders.checkinday <= %s AND Orders.checkoutday >= %s)", (checkinday, checkinday))
        #  query = "SELECT Service.rid FROM Service LEFT JOIN Orders ON Service.oid = Orders.oid AND Orders.checkinday <= %s AND Orders.checkoutday >= %s WHERE Orders.oid IS NULL"
        # cursor.execute(query, (checkinday, checkoutday))
        result = self.cursor.fetchall()
        
        # if result == []:
        #     print("No available room")    
        # else:    
        #    print(result)
        if not result:
            QMessageBox.information(self, "Room Availability", "No available rooms for the selected dates.")
        else:
            available_rooms = ", ".join([str(row[0]) for row in result])
            QMessageBox.information(self, "Room Availability", f"Available rooms: {available_rooms}")
    
    
        

try:
    conn = pymysql.connect(**db_settings)
    with conn.cursor() as cursor:
        # id = 3
        # cursor.execute("SELECT * FROM Customer where cid = %s", id)
        # result = cursor.fetchall()
        # print(result)
    # 插入
        
        # cname = "John"
        # phone = "0934567890"
        # cursor.execute("INSERT INTO Customer (cname, phone) VALUES (%s, %s)", (cname, phone))
        # conn.commit() 
    # 修改
        
            # id = 3
            # cursor.execute("UPDATE Customer SET cname = 'jeff' where cid = %s", id)
            # cursor.execute("UPDATE Customer SET phone = '0987654321' where cid = %s", id)
            # conn.commit()
        # 刪除
        
        # id = 8
        # cursor.execute("DELETE FROM Customer where cid = %s", id)
        # conn.commit()

        checkinday = "2025-03-20"
        checkoutday = "2025-03-28"
        #從service裡找到是否有rid再列印出來
        cursor.execute("SELECT rid FROM Room where rid NOT IN\
        (SELECT Service.rid FROM Service INNER JOIN Orders ON Service.oid = Orders.oid AND Orders.checkinday <= %s AND Orders.checkoutday >= %s)", (checkinday, checkinday))
        #  query = "SELECT Service.rid FROM Service LEFT JOIN Orders ON Service.oid = Orders.oid AND Orders.checkinday <= %s AND Orders.checkoutday >= %s WHERE Orders.oid IS NULL"
        # cursor.execute(query, (checkinday, checkoutday))
        result = cursor.fetchall()
        if result == []:
            print("No available room")    
        else:    
            print(result)
        

        #orders 
        #insert
        # checkinday = "2025-03-21"
        # checkoutday = "2025-03-28"
        # num_of_people = 2
        # cid = 3
        # eid = 1
        # cursor.execute("INSERT INTO Orders (checkinday, checkoutday, num_of_people, cid, eid) VALUES (%s, %s, %s, %s, %s)", (checkinday, checkoutday, num_of_people, cid, eid))
        # conn.commit() 


        #修改
        # checkinday = "2025-03-21"
        # checkoutday = "2025-03-28"
        # num_of_people = 10
        # oid = 9
        # cursor.execute("UPDATE Orders SET checkinday = %s, checkoutday = %s, num_of_people = %s WHERE oid = %s", (checkinday, checkoutday, num_of_people, oid))
        # conn.commit()


        #刪除
        def delete(form,which_id,id):
            cursor.execute(f"DELETE FROM {form} WHERE {which_id}= {id}")
        # delete("Orders","oid",9)
        # delete("Customer","cid",9)
        conn.commit()



except Exception as ex:
    print(ex)

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 建立應用程式
    window = CustomerApp()  # 建立主視窗
    window.show()  # 顯示主視窗
    window.load_data("Customer",window.Cus_table)  # 載入客戶資料
    window.load_data("Orders",window.Orders_table)  # 載入訂單資料
    # conn = pymysql.connect(**db_settings)
    # with conn.cursor() as cursor:
    #     window.add_customer(cursor)


    sys.exit(app.exec_())  # 執行應用程式





