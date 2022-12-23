# 管理员后台操作调用库
import tkinter as tk
import tkinter.messagebox
import csv
from user import User, UserStock
from entryWindow import center_window
import tkinter.ttk as ttk

# 定义读取用户信息，返回列表
def read_user_w():
    with open("account_waiting.csv", encoding='gbk') as csvfile:      # UTF-8有bug，采用网上建议使用gbk
        csv_reader = csv.reader(csvfile)                              # 使用CSV.reader读取CSV中数据
        user_w_list = []
        for row in csv_reader:
            if row[0] == 'id':
                continue
            user_cur = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            user_w_list.append(user_cur)
    return user_w_list

# 定义读取CSV数据中类型函数，返回字典信息
def read_type_c():
    with open('types.csv', encoding='gbk') as csvfile:         # UTF-8有bug，采用网上建议使用gbk
        csv_reader = csv.reader(csvfile)                              # 使用CSV.reader读取CSV中数据
        type_dict = {}
        for row in csv_reader:
            cha_l = row[1].split(sep='，')
            type_dict[row[0]] = cha_l
    return type_dict


# 定义在t列表中根据用户更新库存情况函数
def update_a(t, Users):

    for child in t.get_children():
        t.delete(child)
    for item in Users.accounts:
        t.insert('', tk.END, values=(item.id, item.account, item.password, item.gender, item.address, item.phonenumber, item.email))

# 定义在t列表中根据类型更新库存情况函数
def update_ty(t, type_dict):
    for child in t.get_children():
        t.delete(child)
    for type in list(type_dict.keys()):
        t.insert('', tk.END, values=(type, type_dict[type]))

# 定义读取csv文件中最后一行id的函数
def read_last_id(filename):
    with open(filename, encoding='gbk') as csvfile:                # UTF-8有bug，采用网上建议使用gbk
        csv_reader = csv.reader(csvfile)                              # 使用CSV.reader读取CSV中数据
        li = []
        for row in csv_reader:
            li.append(row[0])
        if li == ['id']:
            return 0
        else:
            return int(li[-1])

# 定义写入账号信息函数
def write_in_csv(filename, user):
    with open(filename, "a", encoding='gbk') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([read_last_id('account.csv') + 1, user.account, user.password, user.gender, user.address, user.phonenumber, user.email])

# 定义写入产品类型函数
def write_in_type(ty_cur, cha_cur):
    with open('types.csv', "a", encoding='gbk') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([ty_cur, cha_cur])

# 定义删除产品类型函数
def delete_item_csv(item_index, filename):
    r = csv.reader(open(filename, encoding='gbk'))
    lines = list(r)
    for line in lines:
        if line[0] == str(item_index):
            lines.remove(line)
            break
    writer = csv.writer(open(filename, 'w', encoding='gbk'))
    writer.writerows(lines)

# 定义管理员界面函数
def admin():
    adminWindow = tk.Tk()
    adminWindow.title('管理员界面')
    center_window(adminWindow, 880, 700)

# 设置界面
    tk.Label(adminWindow, text='待审核注册用户', font=("微软雅黑",20)).place(x=300,y=28, anchor=tk.CENTER)
    columns = ['ID','用户名','密码','性别','地址','联系电话','电子邮箱']
    tree = ttk.Treeview(adminWindow, show="headings", height=10, columns=columns)
    tree.column('ID', width=30, anchor=tk.CENTER,stretch=False)
    tree.column('用户名', width=100, anchor=tk.CENTER)
    tree.column('密码', width=130, anchor=tk.CENTER)
    tree.column('性别', width=50, anchor=tk.CENTER)
    tree.column('地址', width=150, anchor=tk.CENTER)
    tree.column('联系电话', width=100, anchor=tk.CENTER)
    tree.column('电子邮箱', width=200, anchor=tk.CENTER)
    tree.heading('ID', text='ID')
    tree.heading('用户名', text='用户名')
    tree.heading('密码', text='密码')
    tree.heading('性别', text='性别')
    tree.heading('地址', text='地址')
    tree.heading('联系电话', text='联系电话')
    tree.heading('电子邮箱', text='电子邮箱')
    tree.place(x=51, y=65)

    UserS = UserStock(read_user_w())
    update_a(tree, UserS)
# 定义确认用户注册函数
    def agree_ac():
        res = tk.messagebox.askyesnocancel('警告！', '是否确认该用户注册？')
        if res:
            item_index = tree.item(tree.selection()[0], "values")[0]
            for user_cur in UserS.accounts:
                if user_cur.id == item_index:
                    break
            user_append = user_cur
            UserS.accounts.remove(user_cur)
            update_a(tree, UserS)
            write_in_csv('account.csv', user_append)
            delete_item_csv(item_index, 'account_waiting.csv')

    ag_button = tk.Button(adminWindow, text='确认该用户注册', background='white',command=agree_ac).place(x=50, y=280)

# 定义拒绝用户注册函数
    def refuse_ac():
        res = tk.messagebox.askyesnocancel('警告！', '是否拒绝该用户注册？')
        if res:
            item_index = tree.item(tree.selection()[0], "values")[0]
            for user_cur in UserS.accounts:
                if user_cur.id == item_index:
                    break
            UserS.accounts.remove(user_cur)
            update_a(tree, UserS)
            delete_item_csv(item_index, 'account_waiting.csv')

    refu_button = tk.Button(adminWindow, text='拒绝该用户注册', background='white',command=refuse_ac).place(x=200, y=280) #设置拒绝按钮

# 设置修改物品类型界面
    tk.Label(adminWindow, text='添加/修改物品类型', font=("微软雅黑",20)).place(x=300,y=340, anchor=tk.CENTER)

    tk.Label(adminWindow,text="新的类型名称：", font=("微软雅黑",14)).place(x=25, y=380)
    type_entry = tk.Entry(adminWindow,width=15)
    type_entry.place(x=160, y=380)

    tk.Label(adminWindow,text="新的类型属性：", font=("微软雅黑",14)).place(x=300, y=380)
    addr = tk.StringVar()
    addr.set("（用'，'区分不同属性）")
    cha_entry = tk.Entry(adminWindow,width=27, textvariable=addr)
    cha_entry.place(x=470, y=380)


    tree2 = ttk.Treeview(adminWindow, show="headings", height=8, columns=['物品类型', '物品属性'])
    tree2.column('物品类型', width=300, anchor=tk.CENTER)
    tree2.column('物品属性', width=360, anchor=tk.CENTER)
    tree2.heading('物品类型', text='物品类型')
    tree2.heading('物品属性', text='物品属性')
    tree2.place(x=50, y=420)
    type_dic_s = read_type_c()
    update_ty(tree2, type_dic_s)

# 定义加入新品类函数
    def add_type():
        ty_cur = type_entry.get()
        char_cur = cha_entry.get()
        if not ty_cur:
            tk.messagebox.showerror('未输入类型', '请输入要添加的物品类型！')
        elif ty_cur in list(type_dic_s.keys()):
            tk.messagebox.showerror('类型已存在', '该物品类型已存在！')
        else:
            if char_cur == "（用'，'区分不同属性）":
                tk.messagebox.showerror('未输入属性', '请输入该类型的属性！')
            elif '。' in char_cur or ',' in char_cur or '.' in char_cur or '？' in char_cur or '!' in char_cur:
                tk.messagebox.showerror('分隔符错误', '请使用中文逗号作为属性间的分隔符！')
            else:
                type_dic_s[ty_cur] = char_cur.split(sep='，')
                write_in_type(ty_cur, char_cur)
                update_ty(tree2, type_dic_s)

    type_e_button = tk.Button(adminWindow, text='确认添加',command=add_type).place(x=715, y=400)

# 定义修改类型提示函数
    def corr_type():
        item_index = tree2.item(tree2.selection()[0], "values")[0]
        newWin =tk.Tk()
        newWin.title('修改 {} 类型'.format(item_index))
        center_window(newWin, 400,200)

        tk.Label(newWin, text="修改后的类型名称：", font=("微软雅黑", 14)).place(x=50, y=40)
        ty_entry = tk.Entry(newWin, width=18)
        ty_entry.place(x=185, y=40)
        tk.Label(newWin, text="修改后的类型属性：", font=("微软雅黑", 14)).place(x=50, y=80)
        c_entry = tk.Entry(newWin, width=18)
        c_entry.place(x=185, y=80)

# 定义检查修改类型函数（如是否输入、是否类型存在、是否规范）
        def return_ty():
            type_n = ty_entry.get()
            c_n = c_entry.get()
            if not type_n:
                tk.messagebox.showerror('未输入类型', '请输入要修改的物品类型！')
            elif type_n in list(type_dic_s.keys()) and type_n != item_index:
                tk.messagebox.showerror('类型已存在', '该物品类型已存在！')
            else:
                if not c_n:
                    tk.messagebox.showerror('未输入属性', '请输入该类型的属性！')
                elif '。' in c_n or ',' in c_n or '.' in c_n or '？' in c_n or '!' in c_n:
                    tk.messagebox.showerror('分隔符错误', '请使用中文逗号作为属性间的分隔符！')
                else:
                    del type_dic_s[item_index]
                    delete_item_csv(item_index, 'types.csv')
                    type_dic_s[type_n] = c_n.split(sep='，')
                    write_in_type(type_n, c_n)
                    update_ty(tree2, type_dic_s)
                    newWin.destroy()

        check_bu = tk.Button(newWin, text='确认修改',command=return_ty).place(x=200,y=150, anchor=tk.CENTER)

    correct_button = tk.Button(adminWindow, text='修改该类型',command=corr_type).place(x=715, y=440)

# 定义删除类型函数
    def delete_type():
        item_index = tree2.item(tree2.selection()[0], "values")[0]
        del type_dic_s[item_index]
        delete_item_csv(item_index, 'types.csv')
        update_ty(tree2, type_dic_s)

    delete_button = tk.Button(adminWindow, text='删除该类型',command=delete_type).place(x=715, y=480)

# 定义退出函数
    def exit_window():
        res = tk.messagebox.askyesnocancel('警告','是否退出软件？')
        if res:
            adminWindow.destroy()

    exit_button = tk.Button(adminWindow, text='退出软件',command=exit_window).place(x=300, y=650, anchor=tk.CENTER)
    adminWindow.mainloop()                                 # 允许程序循环执行,并进入等待和处理事件
