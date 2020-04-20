# -*- coding: utf-8 -*-
import os,time,pymysql
import schedule
import zipfile
import oss2

ip = input("Enter your ip: ");
user=input("Enter your user: ");
pwd=input("Enter your pwd: ");
task_time = input("Enter your task_time（--:--）: ");
oosyes = input("Enable OSS or not(y/n): ");
if oosyes == 'y':
    endpoint = input("Enter your endpoint: ");
    accessKeyID = input("Enter your accessKeyID: ");
    accessKeySecret = input("Enter your accessKeySecret: ");
    bucketStr = input("Enter your bucket: ");

#检索数据库
def getDatabaseNames():
    conn = pymysql.connect(ip, user, pwd, use_unicode=True, charset="utf8")
    cur = conn.cursor()
    cur.execute('show databases;')
    dbs = cur.fetchall()
    cur.close()
    conn.close()
    return dbs

#path trim一下然后创建
def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False
#文件压缩
def zip_ya(startdir,file_news):
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
    z.close()
    time.sleep(60)
    if oosyes == "y":
        auth = oss2.Auth(accessKeyID, accessKeySecret)
        bucket = oss2.Bucket(auth, "http://"+endpoint, bucketStr)
        timestrName = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        path = os.path.split(os.path.realpath(__file__))
        objectPath = path[0]+"\\"+file_news
        replacePath = objectPath.replace("\\","/")#路径修正
        result = bucket.put_object_from_file('sql/'+timestrName+".zip",replacePath)
        print('http status: {0}'.format(result.status))
        print('request_link:'+"https://"+bucketStr+"."+endpoint+"/sql/"+timestrName+".zip")
        os.remove(replacePath)

def mainfunation():
    timestr = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    folder = "mysql_data_bak/" + timestr
    mkdir(folder)

    dbs = getDatabaseNames()
    print(dbs)
    for db in dbs:
        try:
            dbname = db[0]
            # 排除自带的db
            if dbname == "mysql" or dbname == "performance_schema" or dbname == "information_schema" or dbname == "sys":
                continue
            # 导出db
            cmd = "mysqldump -h" + ip + " -u%s -p%s %s > %s/%s.sql" % (user, pwd, dbname, folder, dbname)
            print(cmd)
            os.system(cmd)
        except Exception as e:
            print(e)
    zip_ya(folder, folder +'.zip' )

schedule.every().day.at(task_time).do(mainfunation)
while True:
    schedule.run_pending()
    time.sleep(1)

