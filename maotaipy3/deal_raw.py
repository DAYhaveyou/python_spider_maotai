import yaml
import pymysql as mdb
import os

def get_rawdata(file_name):
    f = open(file_name, 'r')
    i = 0

    lines = []
    linetemp = ""
    for line in f.readlines():
        line = line.strip()
        if len(line) > 0 and line[-1] == ";":
            linetemp += line
            lines.append(linetemp)
            # print linetemp[:2], "\t"
            # print(linetemp, '\n')
            linetemp = ""
        elif len(line) > 0:
            linetemp += line
        i += 1
        if i > 10:
            break

    dateline = 0
    for i in lines[-2]:
        if i == "[":
            break
        else:
            dateline += 1

    date = lines[-2][dateline:]

    dataline = 0
    for i in lines[-1]:
        if i == "{":
            break
        else:
            dataline += 1

    data = lines[-1][dataline:]

    return date, data


def deal_date(str):
    date = []
    temp = ""
    for i in str:
        if i == "[" or i == "'" or i == "-":
            continue
        if i == ",":
            date.append(int(temp))
            temp = ""
            continue
        if i == "]":
            if len(temp) > 0:
                date.append(int(temp))
            return date
        temp += i

# date1 = deal_date(date)
# print date1[2:6], date1[-2:]


def deal_data(str):
    flag = 0
    dict = {}
    name = ""
    number = ""
    for i in str:
        if flag == 1 and i != ',' and i != ']':
            number += i
            continue
        if i == "," and flag == 1:
            dict[name].append(float(number))
            number = ""
            continue
        if i.isupper() and flag == 0:
            name += i
            continue
        if i == "'" or i == "{":
            continue
        if i == "[":
            dict[name] = []
            # name = ""
            flag = 1
            continue
        if i == "]" and flag == 1:
            if len(number) > 0:
                dict[name].append(float(number))
                number = ""
                name = ""
            flag = 0
    return dict

'''
data1 = deal_data(data)

print data1['PRICE'][-10:]
print len(data1['PRICE'])
print len(data1['PB']), "\t", data1['PB'][-10:]
print len(data1['PE']), "\t", data1['PE'][:10]
'''


def connect_database(message):
    host_id, user_name, password, db_name = message
    conn = mdb.connect(host=host_id, user=user_name, passwd=password, db=db_name)
    return conn


def storage_database(date, data, table, message):
    conn = connect_database(message)
    sql = "insert into %s(date, price, pe, pb)" % table
    sql1 = sql + " values(%s, %s, %s, %s)"
    params = []
    flag = 20000

    length = len(date)
    count = 0

    for i in range(length):
        temp_val = [date[i], data['PRICE'][i], data['PE'][i], data['PB'][i]]
        params.append(temp_val)
        count += 1
        if count >= flag:
            conn = connect_database(message)
            cursor = conn.cursor()
            cursor.executemany(sql1, params)
            conn.commit()
            cursor.close()
            conn.close()
            params = []
            count = 0

    if len(params) > 0:
        conn = connect_database(message)
        cursor = conn.cursor()
        cursor.executemany(sql1, params)
        conn.commit()
        cursor.close()
        conn.close()


def create_maotai(table, message):
    conn = connect_database(message)
    sql = "create table %s(id int not null AUTO_INCREMENT," \
          "date int not null," \
          "price float not null," \
          "pe float not null," \
          "pb float not null," \
          "PRIMARY KEY (id))" % table
    sql1 = "select count(1) from %s" % table
    cursor = conn.cursor()
    cursor.execute(sql)
    # raw_value = cursor.fetchone()
    # val = raw_value[0]
    # print(val)
    conn.commit()
    conn.close()


def make_result(file_name):
    r = get_rawdata(file_name)
    date = deal_date(r[0])
    data = deal_data(r[1])
    pwd = os.getcwd()
    file1 = pwd + "/" + "t1.yaml"
    file2 = pwd + "/" + "t2.yaml"
    f1 = open(file1, 'w')
    f2 = open(file2, 'w')
    yaml.dump(date, f1)
    yaml.dump(data, f2)
    f1.close()
    f1.close()
    table = "maotai"
    message_new = ["192.168.1.2", "root", "rootKa$QZ", "LI_DataBase_spider"]
    delete_table(table, message_new)
    create_maotai(table, message_new)
    storage_database(date, data, table, message_new)
    if os.path.exists(file1):
        os.remove(file1)
    if os.path.exists(file2):
        os.remove(file2)


def delete_table(table, message):
    sql = "drop table %s" % table
    conn = connect_database(message)
    cursor = conn.cursor()
    cursor.execute(sql)
    # raw_value = cursor.fetchone()
    # val = raw_value[0]
    # print(val)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    message_new3 = ["192.168.1.2", "root", "rootKa$QZ", "LI_DataBase_spider"]
    create_maotai('maotai1', message_new3)
