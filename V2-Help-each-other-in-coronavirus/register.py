# 注册调用库
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import csv


# 定义窗体居中函数
# root为对象，width宽度 height 高度）

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height  = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screen_width - width) / 2, (screen_height - height) / 2)  # 设置窗口居中
    root.geometry(size)

# 定义读取已审核账号密码函数，返回字典数据
def read_account():
    with open("account.csv", encoding='gbk') as csvfile:           # UTF-8有bug，采用网上建议使用gbk
        csv_reader = csv.reader(csvfile)                           # 使用CSV.reader读取CSV中数据
        account_dict = {}
        for row in csv_reader:
            account_dict[row[1]] = row[2]

    return account_dict


# 读取待审核账号密码数据，返回字典数据
def read_account_waiting():
    with open("account_waiting.csv", encoding='gbk') as csvfile:      # UTF-8有bug，采用网上建议使用gbk
        csv_reader = csv.reader(csvfile)                              # 使用CSV.reader读取CSV中数据
        account_waiting_dict = {}
        for row in csv_reader:
            account_waiting_dict[row[1]] = row[2]

    return account_waiting_dict


#定义读取ID函数
def read_last_id(filename):
    with open(filename, encoding='gbk') as csvfile:                    # UTF-8有bug，采用网上建议使用gbk
        csv_reader = csv.reader(csvfile)                              # 使用CSV.reader读取CSV中数据
        li = []
        for row in csv_reader:
            li.append(row[0])
        if li == ['id']:
            return 0
        else:
            return int(li[-1])

# 定义写入新注册用户信息函数，至待审核账户中
def write_in_csv(filename, account_c, password_c, gender_c, address_c, number_c, email_c):
    with open(filename, "a", encoding='gbk') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([read_last_id('account_waiting.csv') + 1, account_c, password_c, gender_c, address_c, number_c, email_c])

# 定义检查输入内容是否为中文函数，返回True or False
def is_chinese(string):
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':            #中文字符的编码为：u’\u4e00’ <= ch <= u’\u9fff’，其中包括了中文简体和中文繁体字
            return True
    return False

# 定义读取管理员用户账号密码函数，返回字典数据
def read_admin_account():
    with open("admin_account.csv", encoding='gbk') as csvfile:
        csv_reader = csv.reader(csvfile)
        admin_account_dict = {}
        for row in csv_reader:
            if row[1] == "用户名":
                continue
            admin_account_dict[row[1]] = row[2]

    return  admin_account_dict


# 定义注册函数
def register():

    resWindow = tk.Tk()      # 设置登陆注册对象
    resWindow.title('欢迎使用你帮我助物品互换系统')
    center_window(resWindow, 500, 335)
    tk.Label(resWindow, text="你帮我助物品互换系统注册",font=("黑体", 24)).place(x=250, y=50, anchor=tk.CENTER)
    tk.Label(resWindow,text="请输入您的账号：", font=("宋体",14)).place(x=90, y=80)
    tk.Label(resWindow,text="请输入您的密码：", font=("宋体",14)).place(x=90, y=110)
    account_entry = tk.Entry(resWindow,width=21)     # 设置账号输入框
    account_entry.place(x=210, y=80)
    password_entry = tk.Entry(resWindow,width=21)    # 设置密码输入框
    password_entry.place(x=210, y=110)
    tk.Label(resWindow, text="请选择您的性别：", font=("宋体", 14)).place(x=90, y=140)
    genderBox = ttk.Combobox(resWindow, height=3, width=6, state='readonly',font=("宋体", 14), values=['男', '女', '保密'])   # 设置性别
    genderBox.place(x=210,y=140)
    tk.Label(resWindow, text="请输入您的地址：", font=("宋体", 14)).place(x=90, y=170)
    tk.Label(resWindow, text="请输入您的电话：", font=("宋体", 14)).place(x=90, y=200)
    tk.Label(resWindow, text="请输入您的邮箱：", font=("宋体", 14)).place(x=90, y=230)
    address_entry = tk.Entry(resWindow, width=21)  # 设置地址输入
    address_entry.place(x=210, y=170)
    phnumber_entry = tk.Entry(resWindow, width=21)  # 设置密码输入
    phnumber_entry.place(x=210, y=200)
    email_entry = tk.Entry(resWindow, width=21)  # 设置账号输入
    email_entry.place(x=210, y=230)

    account_dict = read_account()
    account_dict_wait = read_account_waiting()

# 定义用户账号目前状态更改函数（账号是否被注册，是否在审核中，是否符合规范）
    def change_state():
        account_cur = account_entry.get()
        password_cur = password_entry.get()
        if account_cur in account_dict.keys():
            tk.messagebox.showerror('账号已被注册', '账号已被注册，请重输您的账号!')
        elif account_cur in account_dict_wait.keys():
            tk.messagebox.showerror('该账号正在审核中', '该账号注册正在审核中，请重新输入您的账号！')
        else:
            if len(password_cur) < 6 or is_chinese(password_cur) or (" " in password_cur):
                tk.messagebox.showerror('密码格式错误', '请使用大于等于6位的英文或数字，且不包含空格的字符串作为密码！')
            else:
                gender_cur = genderBox.get()
                if not gender_cur:
                    tk.messagebox.showerror('选择性别', '请选择您的性别！')
                else:
                    address_cur = address_entry.get()
                    if not address_cur:
                        tk.messagebox.showerror('输入地址', '请输入您的地址！')
                    else:
                        number_cur = phnumber_entry.get()
                        if not number_cur:
                            tk.messagebox.showerror('输入手机', '请输入您的手机号码！')
                        elif not str.isnumeric(number_cur):
                            tk.messagebox.showerror('号码错误', '请输入格式正确的手机号码！')
                        else:
                            email_cur = email_entry.get()
                            if not email_cur:
                                tk.messagebox.showerror('输入邮箱', '请输入您的电子邮箱！')
                            elif '@' not in email_cur:
                                tk.messagebox.showerror('邮箱无效', '请输入有效的邮箱！')
                            else:
                                write_in_csv("account_waiting.csv", account_cur, password_cur, gender_cur, address_cur, number_cur, email_cur)
                                tk.messagebox.showwarning('注册申请成功', '注册申请成功！待管理员审核通过后使用本软件！')
                                resWindow.destroy()

    log_button = tk.Button(resWindow,text='申请注册账号',command=change_state)
    log_button.place(x=250, y=290, anchor=tk.CENTER)
    resWindow.mainloop()                                  # 允许程序循环执行,并进入等待和处理事件


