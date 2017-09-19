import json
import threading
import urllib
from urllib import request
from urllib.error import HTTPError
import queue
import socket
import os.path

import time

id = 2800

baseUrl = "http://img1.mm131.com/pic/"


def saveImg(imgUrl, fileName):
    pass


class ThreadCrawl(threading.Thread):
    def __init__(self, url, tasks, out_queue):
        threading.Thread.__init__(self)
        self.url = url
        self.out_queue = out_queue
        self.tasks = tasks

    def run(self):
        while True:
            if not self.tasks.empty():
                saveImg(self.tasks.get(), )

            for j in range(100):
                count = 1
                for i in range(100):
                    jpg_link = "http://img1.mm131.com/pic/%d/%d.jpg" % (id, count)
                    saving_path = "Images" + "/" + "%d" % id
                    path = saving_path + "/" + str(count) + ".jpg"
                    if os.path.exists(saving_path):
                        pass
                    else:
                        os.mkdir(saving_path)
                    try:
                        if not os.path.exists(path):
                            request.urlretrieve(jpg_link, path)
                        print(jpg_link + " Success\n")
                    except HTTPError as httpErrpr:
                        print(httpErrpr.reason)
                        if httpErrpr.code == 404:
                            break
                    except BaseException as exception:
                        print(jpg_link + " Failed\n")
                        print(exception.args)
                        pass

                    count += 1

                id += 1


exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, imgQueue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.imgQueue = imgQueue

    def run(self):
        print("Starting " + self.name)
        save_img(self.name, self.imgQueue)
        print("Exiting " + self.name)


def save_img(thread_name, q):
    if changingTasks:
        return
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print("%s processing %s" % (thread_name, data))
            saving_path = "Images" + "/" + "%s" % data[0]
            path = saving_path + "/" + str(data[1]) + ".jpg"
            jpg_link = baseUrl + data[0] + '/' + data[1] + ".jpg"
            if os.path.exists(saving_path):
                pass
            else:
                os.mkdir(saving_path)
            try:
                if not os.path.exists(path):
                    request.urlretrieve(jpg_link, path)
                print(jpg_link + " Success\n")
            except HTTPError as httpErrpr:
                print(jpg_link + " " + httpErrpr.reason)
                if httpErrpr.code == 404:
                    # changeTasksLock.acquire()
                    # changeTasks = True
                    # changeTasksLock.release()
                    queueLock.acquire()
                    while not workQueue.empty():
                        workQueue.get()
                    queueLock.release()

                    global changingTasks
                    changeTasksLock.acquire()
                    changingTasks = True
                    changeTasksLock.release()
                    break
            except BaseException as exception:
                print(jpg_link + " Failed\n")
                print(exception.args)
                pass
        else:
            queueLock.release()

        time.sleep(0.1)


threadList = ["Thread-1", "Thread-2", "Thread-3"]

img_list = [[str(id), str(i)] for i in range(100)]

queueLock = threading.Lock()
changeTasksLock = threading.Lock()
workQueue = queue.Queue(100)
changingTasks = False
threads = []
threadID = 1

# 创建新线程
for tName in range(20):
    thread = myThread(threadID, "thread" + str(tName), workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for word in img_list:
    workQueue.put(word)
queueLock.release()

# 等待队列清空
while id < 3000:
    while not workQueue.empty():
        pass
    id += 1
    img_list = [[str(id), str(i)] for i in range(1,100)]
    queueLock.acquire()
    for word in img_list:
        workQueue.put(word)
    queueLock.release()
    threads.clear()
    changingTasks = False
    for tName in range(20):
        thread = myThread(threadID, "thread" + str(tName), workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print("Exiting Main Thread")
