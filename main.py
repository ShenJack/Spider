from urllib import request
from urllib.error import HTTPError
import socket
import os.path
socket.setdefaulttimeout(30)

id = 2800

for j in range(100):
    count = 1
    for i in range(100):
        jpg_link = "http://img1.mm131.com/pic/%d/%d.jpg" % (id, count)
        saving_path = "%d" % id
        path = saving_path + "/" + str(count) + ".jpg"
        if os.path.exists(saving_path):
            pass
        else:
            os.mkdir(saving_path)
        try:
            request.urlretrieve(jpg_link, path)
            print(jpg_link+" Success\n")
        except HTTPError as httpErrpr:
            if httpErrpr.code == 404:
                break
        except BaseException as exception:
            print(jpg_link+" Failed\n")
            print(exception.args)
            pass

        count += 1

    id += 1