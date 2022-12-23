# 程序主体所调用的库
from mainWindow import mainWindow
from entryWindow import enter
from user import User, UserStock
from admin_enter import admin
import csv

# 定义读取用户信息，返回列表
def read_user_w():
    with open("account.csv", encoding='gbk') as csvfile:      # UTF-8有bug，采用网上建议使用gbk
        csv_reader = csv.reader(csvfile)                              # 使用CSV.reader读取CSV中数据
        user_w_list = []
        for row in csv_reader:
            if row[0] == 'id':
                continue
            user_cur = User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            user_w_list.append(user_cur)
    return user_w_list

# 程序主体代码

if __name__ == '__main__':
    UserS = UserStock(read_user_w())
    s, account = enter()

    for users in UserS.accounts:
        if users.account == account:
            break

    if s == 1:
        mainWindow(users)
    elif s == 0:
        admin()

