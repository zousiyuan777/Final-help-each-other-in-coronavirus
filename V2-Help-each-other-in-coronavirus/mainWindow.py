# 主窗口调用库
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import csv
import ast
from product import Product
from stock import Stock
from user import User, UserStock

# 读取CSV中数据，返回列表
def read_user_w():
    with open("account.csv", encoding='gbk') as csvfile:     # 使用UTF-8会产生bug，根据网上建议改为gbk
        csv_reader = csv.reader(csvfile)                     # 使用CSV.reader来读取csv文件中的数据
        user_w_list = []
        for row in csv_reader:
            if row[0] == 'id':
                continue
            user_cur = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            user_w_list.append(user_cur)
    return user_w_list

# 定义用户类

class User:
    def __init__(self, id, account, password, gender, address, phonenumber, email):
        self.id = id
        self.account = account
        self.password = password
        self.gender = gender
        self.address = address
        self.phonenumber = phonenumber
        self.email = email

# 定义用户库存类
class UserStock:
    def __init__(self, account_list):
        self.accounts = account_list



# 主窗口所用函数
# root为对象，width宽度 height 高度）
def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height  = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screen_width - width) / 2, (screen_height - height) / 2)  # 使窗口位于中间
    root.geometry(size)

#读取库存信息，返回列表
def read_stock():
    with open("stock.csv", encoding='gbk') as csvfile:                    # 使用UTF-8会产生bug，根据网上建议改为gbk
        csv_reader = csv.reader(csvfile)                                  # 使用CSV.reader来读取csv文件中的数据
        project_list = []
        for row in csv_reader:
            if row[0] == 'id':
                continue
            if row[7]:
                chara = ast.literal_eval(row[7])
            pro_cur = Product(row[0], row[1], row[2], row[3], row[4], row[5], row[6], chara, row[8])
            project_list.append(pro_cur)
    return project_list

# 读取库存信息，返回列表
def read_types():
    with open('types.csv', encoding='gbk') as csvfile:      # 使用UTF-8会产生bug，根据网上建议改为gbk
        csv_reader = csv.reader(csvfile)                    # 使用CSV.reader来读取csv文件中的数据
        type_list = []                                      # 创建列表
        type_dict = {}                                      # 创建字典
        for row in csv_reader:
            type_list.append(row[0])
            type_dict[row[0]] = row[1]
        return type_list, type_dict

# 在相应文档内写入新产品内容
def write_csv(filename, product):
    with open(filename, "a", encoding='gbk') as csvfile:   # a为 append，在原有基础上增加，而非覆盖
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([product.id, product.name, product.intro, product.address, product.phonenumber, product.email, product.type, product.charact, product.master])

# 在目录范围内搜索产品
def search_product(stock, index):
    for pro in stock.goods:
        if pro.id == index:
            goal_pro = pro
            return goal_pro
        else:
            return None

# 在列表t中更新stock的库存信息。
project_list = read_stock()
stockIni = Stock(project_list)
def update_stock(t, stock):

    for child in t.get_children():
        t.delete(child)
    for item in stock.goods:
        t.insert('', tk.END, values=(item.id, item.name, item.intro, item.address,item.type, item.master, item.phonenumber, item.email))


# 创建主窗口
def mainWindow(user):
    mainWindow = tk.Tk()                     #窗口初始化
    mainWindow.title("欢迎使用你帮我助物品互换系统")
    center_window(mainWindow, 880, 570)

    columns = ['物品id','物品名称','物品说明','物品地址','物品类型','联系人账户','联系人号码','联系人邮箱']
    tree = ttk.Treeview(mainWindow, show="headings", height=18, columns=columns)
    tree.column('物品id', width=40, anchor=tk.CENTER,stretch=False)
    tree.column('物品名称', width=60, anchor=tk.CENTER)
    tree.column('物品说明', width=100, anchor=tk.CENTER)
    tree.column('物品地址', width=80, anchor=tk.CENTER)
    tree.column('物品类型', width=80, anchor=tk.CENTER)
    tree.column('联系人账户', width=80, anchor=tk.CENTER)
    tree.column('联系人号码', width=120, anchor=tk.CENTER)
    tree.column('联系人邮箱', width=210, anchor=tk.CENTER)

    tree.heading('物品id', text='ID')
    tree.heading('物品名称', text='物品名称')
    tree.heading('物品说明', text='说明')
    tree.heading('物品地址', text='物品地址')
    tree.heading('物品类型', text='物品类型')
    tree.heading('联系人账户', text='联系人账户')
    tree.heading('联系人号码', text='联系人号码')
    tree.heading('联系人邮箱', text='联系人邮箱')
    update_stock(tree, stockIni)

    tree.place(x=50, y=180)

    tk.Label(mainWindow,text="物品名称：", font=("微软雅黑",14)).place(x=30, y=60)               # 标签
    tk.Label(mainWindow,text="物品描述：", font=("微软雅黑",14)).place(x=280, y=90)
    tk.Label(mainWindow, text="物品所在地：", font=("微软雅黑", 14)).place(x=30, y=90)
    v1 = tk.StringVar()                                                                  # Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符
    v2 = tk.StringVar()
    v3 = tk.StringVar()
    v4 = tk.StringVar()
    name_entry = tk.Entry(mainWindow,width=15,textvariable=v1)                          # entry函数获取用户的输入文本
    name_entry.place(x=120, y=60)
    dri_entry = tk.Entry(mainWindow,width=25,textvariable=v2)
    dri_entry.place(x=370, y=90)
    add_entry = tk.Entry(mainWindow, width=13,textvariable=v3)
    add_entry.place(x=137.5, y=90)

    type_list, type_dict = read_types()
    tk.Label(mainWindow, text="物品类型：", font=("微软雅黑", 14)).place(x=30, y=30)
    type_Box = ttk.Combobox(mainWindow, height=5, width=13, state='readonly', font=("微软雅黑", 14),
                              values=type_list)                                                  #  产生的效果是一个下拉列表框产生一个名为<<ComboboxSelected>>的虚拟事件
    type_Box.place(x=110, y=30)
    # 添加商品信息
    chara_dic = {}



# 定义刷新库存函数
    def upda():
        update_stock(tree,stockIni)
        v1.set("")
        v2.set("")
        v3.set("")
        v4.set("")

    updatee_Button = tk.Button(mainWindow, text='刷新列表',command=upda).place(x=660, y=60)   # 设计刷新按钮


    def fill_chara():
        chara_dic.clear()                                          # 初始化
        if not type_Box.get():
            tk.messagebox.showerror('未选择物品类型', '请选择物品类型！')      # 在未选择物品类型时报错

        else:
            new_win = tk.Tk()                                         # 初始化
            new_win.title('填写物品属性')
            chara_l = type_dict[type_Box.get()].split(sep='，')       #得到物品信息

            center_window(new_win, 310, 30*len(chara_l)+100)
            entry_list = []
            for i in range(len(chara_l)):
                tk.Label(new_win, text="{}：".format(chara_l[i]), font=("微软雅黑", 14)).place(x=50, y=20+30*i)
                ch_entry = tk.Entry(new_win, width=15)
                ch_entry.place(x=120, y=20+30*i)
                entry_list.append(ch_entry)                            # 加入属性函数

            # 定义检查属性函数
            def check():
                j = 0
                for char in chara_l:
                    if not entry_list[j].get():
                        tk.messagebox.showwarning('属性未填', '请填写该物品的{}属性'.format(chara_l[j]))
                        fill_chara()
                        break
                    else:
                        chara_dic[char] = entry_list[j].get()
                        j = j + 1
                new_win.destroy()                         # 完成后删除内容

            en_button = tk.Button(new_win, text='确认', command=check)
            en_button.place(x=155, y=80+30*i, anchor=tk.CENTER)
    element_button = tk.Button(mainWindow, text='填写物品属性',command=fill_chara)
    element_button.place(x=660, y=100)



# 定义展示物品信息函数
    def show_detail():

        try:
            item_index = tree.item(tree.selection()[0], "values")[0]           #对Python窗体(tkinter)获取树状数据(Treeview)，返回字典类型数据
        except IndexError:
            tk.messagebox.showerror('未选择', '请选择要查看详细属性的物品！')
        else:
            stockIni = Stock(read_stock())
            for pro in stockIni.goods:
                if pro.id == item_index:
                    break
            new_win = tk.Tk()
            new_win.title('{} 详细属性'.format(pro.name))
            center_window(new_win, 310, 30 * len(pro.charact) + 50)
            for i in range(len(pro.charact)):
                tk.Label(new_win, text="{}：".format(list(pro.charact.keys())[i]), font=("微软雅黑", 14)).place(x=80, y=20 + 30 * i)
                tk.Label(new_win, text="{}".format(pro.charact[list(pro.charact.keys())[i]]), font=("微软雅黑", 14)).place(x=180, y=20 + 30 * i)
    detail_button = tk.Button(mainWindow, text='查看该物品详细属性',command=show_detail)
    detail_button.place(x=660, y=20)

    # 添加物品函数
    def add_in_stock():
        name_cur = name_entry.get()
        ari_cur = dri_entry.get()
        add_cur = add_entry.get()
        type_cur = type_Box.get()
        if len(stockIni.goods) == 0:
            id_cur = 1
        else:
            id_cur = int(stockIni.goods[-1].id) + 1
        product_cur = Product(id_cur, name_cur, ari_cur, add_cur, user.phonenumber, user.email,type_cur,chara_dic, user.account)
        stockIni.Add(product_cur)                      # 加入新库存
        update_stock(tree, stockIni)                   # 更新库存树状数据
        write_csv('stock.csv', product_cur)            # 写入物品信息
    add_button = tk.Button(mainWindow,text='添加一个物品',command=add_in_stock)
    add_button.place(x=300, y=20)

    # 在csv数据中里删除商品
    def delete_item_csv(item_index, filename):
        r = csv.reader(open(filename, encoding='gbk'))         # UTF-8对于汉字有bug，故使用网上建议的gbk编码
        lines = list(r)
        for line in lines:
            if line[0] == str(item_index):
                lines.remove(line)
                break
        writer = csv.writer(open(filename, 'w', encoding='gbk'))
        writer.writerows(lines)

    # 定义删除库存函数
    def delete_stock():
        try:
            item_index = tree.item(tree.selection()[0], "values")[0]
        except IndexError:
            tk.messagebox.showerror('为选择', '请选择要删除的物品！')
        else:

            for pro in stockIni.goods:
                if pro.id == item_index:
                    break
            if pro.master != user.account:                                    # 判定该物品主人是否为登录用户
                tk.messagebox.showerror('这不是您的物品', '这不是您的物品，无法删除！')
            else:
                res = tk.messagebox.askyesnocancel('警告！','是否删除所选商品？')
                if res:
                    stockIni.goods.remove(pro)
                    update_stock(tree, stockIni)
                    delete_item_csv(item_index, 'stock.csv')

    delete_button = tk.Button(mainWindow,text='删除指定物品',command=delete_stock)
    delete_button.place(x=300, y=58)

    # 定义搜索函数
    def search_in_tree():
        ty_C = type_Box.get()
        if not ty_C:                                                          #判定是否选择了搜索类型
            tk.messagebox.showerror('请选择类型', '请选择需要搜索的物品类型！')
        else:
            charac = search_Box.get()
            if not charac:
                for child in tree.get_children():
                    tree.delete(child)
                infor_cur = search_entry.get()
                for cur_pro in stockIni.goods:
                    if (infor_cur == cur_pro.id or (infor_cur in cur_pro.name) or (infor_cur in cur_pro.intro) or (infor_cur in cur_pro.master) or (infor_cur in cur_pro.address) or (infor_cur in cur_pro.email)) and cur_pro.type == ty_C:
                        tree.insert('', tk.END, values=(cur_pro.id, cur_pro.name, cur_pro.intro, cur_pro.address,cur_pro.type, cur_pro.master, cur_pro.phonenumber,
                            cur_pro.email))         # tk.end表示Text文本缓冲区最后一个字符的下一个位置，在此定位用
            else:
                if charac == '物品ID':
                    for child in tree.get_children():              # 遍历所有树状数据
                        tree.delete(child)
                    infor_cur = search_entry.get()
                    for cur_pro in stockIni.goods:
                        if infor_cur == cur_pro.id and cur_pro.type == ty_C:
                            tree.insert('', tk.END, values=(cur_pro.id, cur_pro.name, cur_pro.intro, cur_pro.address,cur_pro.type, cur_pro.master, cur_pro.phonenumber,
                            cur_pro.email))

                elif charac == '物品名称':
                    for child in tree.get_children():
                        tree.delete(child)
                    infor_cur = search_entry.get()
                    for cur_pro in stockIni.goods:
                        if infor_cur in cur_pro.name and cur_pro.type == ty_C:
                            tree.insert('', tk.END, values=(cur_pro.id, cur_pro.name, cur_pro.intro, cur_pro.address,cur_pro.type, cur_pro.master, cur_pro.phonenumber,
                            cur_pro.email))

                elif charac == '物品说明':
                    for child in tree.get_children():
                        tree.delete(child)
                    infor_cur = search_entry.get()
                    for cur_pro in stockIni.goods:
                        if infor_cur in cur_pro.intro and cur_pro.type == ty_C:
                            tree.insert('', tk.END, values=(
                                cur_pro.id, cur_pro.name, cur_pro.intro, cur_pro.address, cur_pro.type, cur_pro.master,
                                cur_pro.phonenumber,
                                cur_pro.email))

                elif charac == '物品地址':
                    for child in tree.get_children():
                        tree.delete(child)
                    infor_cur = search_entry.get()
                    for cur_pro in stockIni.goods:
                        if infor_cur in cur_pro.address and cur_pro.type == ty_C:
                            tree.insert('', tk.END, values=(cur_pro.id, cur_pro.name, cur_pro.intro, cur_pro.address,cur_pro.type, cur_pro.master, cur_pro.phonenumber,
                            cur_pro.email))

                elif charac == '联系人账户':
                    for child in tree.get_children():
                        tree.delete(child)
                    infor_cur = search_entry.get()
                    for cur_pro in stockIni.goods:
                        if infor_cur in cur_pro.master and cur_pro.type == ty_C:
                            tree.insert('', tk.END, values=(cur_pro.id, cur_pro.name, cur_pro.intro, cur_pro.address,cur_pro.type, cur_pro.master, cur_pro.phonenumber,
                            cur_pro.email))

                elif charac == '联系人号码':
                    for child in tree.get_children():
                        tree.delete(child)
                    infor_cur = search_entry.get()
                    for cur_pro in stockIni.goods:
                        if infor_cur == cur_pro.phonenumber and cur_pro.type == ty_C:
                            tree.insert('', tk.END, values=(cur_pro.id, cur_pro.name, cur_pro.intro, cur_pro.address,cur_pro.type, cur_pro.master, cur_pro.phonenumber,
                            cur_pro.email))

                elif charac == '联系人邮箱':
                    for child in tree.get_children():
                        tree.delete(child)
                    infor_cur = search_entry.get()
                    for cur_pro in stockIni.goods:
                        if infor_cur in cur_pro.email and cur_pro.type == ty_C:
                            tree.insert('', tk.END, values=(cur_pro.id, cur_pro.name, cur_pro.intro, cur_pro.address,cur_pro.type, cur_pro.master, cur_pro.phonenumber,
                            cur_pro.email))


# 查询结果
    tk.Label(mainWindow,text="查找物品：", font=("微软雅黑",14)).place(x=30, y=120)
    search_entry = tk.Entry(mainWindow,width=15, textvariable=v4)
    search_entry.place(x=120, y=120)
    search_button = tk.Button(mainWindow,text='查找',command=search_in_tree)
    search_button.place(x=560, y=120)
    tk.Label(mainWindow, text="根据该特征查找：", font=("微软雅黑", 14)).place(x=280, y=120)
    search_Box = ttk.Combobox(mainWindow, height=6, width=9, state='readonly', font=("微软雅黑", 14),
                             values=['物品ID','物品名称','物品说明','物品地址','联系人账户','联系人号码','联系人邮箱'])  # 性别选择框
    search_Box.place(x=430, y=123)


#显示我的物品
    def search_in_tree_mine():
        for child in tree.get_children():                                           # 遍历所有树状数据
            tree.delete(child)
        infor_cur = search_entry.get()
        for cur_pro in stockIni.goods:
            if cur_pro.master == user.account:
                tree.insert('', tk.END, values=(cur_pro.id, cur_pro.name, cur_pro.intro, cur_pro.address,cur_pro.type, cur_pro.master, cur_pro.phonenumber,
                        cur_pro.email))
    search_m_button = tk.Button(mainWindow, text='查找我上传的物品', command=search_in_tree_mine)
    search_m_button.place(x=440, y=20)

# 展示所有商品
    def show_all():
        update_stock(tree, stockIni)
    search_button = tk.Button(mainWindow,text='显示全部库存物品',command=show_all)
    search_button.place(x=440, y=58)

    tk.Label(mainWindow, text='当前登录的账户为:{}'.format(user.account), font=('微软雅黑',12)).place(relx=0, rely=0.95)

# 定义关闭窗口提示函数
    def exit_window():
        res = tk.messagebox.askyesnocancel('警告','是否退出软件？')
        if res:
            mainWindow.destroy()                                #停止mainloop
    exit_button = tk.Button(mainWindow, text='退出软件',command=exit_window).place(x=440, y=530, anchor=tk.CENTER)

# 允许程序循环执行,并进入等待和处理事件
    mainWindow.mainloop()