这是一个刷课的项目，现在它可以刷运动与健康这门课程。
issus：1、还在不具有足够的通用性
2、It makes mistakes when the network is bad
3、在网络不好的时候需要一些直接的延时操作，导致有很多地方有根据经验得出的延时值(time.sleep())


---
# 多线程版本

```python
from xuetangzaixian import xuetangzaixian
#账号和密码，用于登录
loginurl = 'https://next.xuetangx.com/'
username = 'Your nuser name'
password = 'Your password'
coursename = '要刷的正在进行的课程名称'
thread1 = xuetangzaixian(loginurl,username,password,coursename,True,begin=18)
thread2 = xuetangzaixian(loginurl,username,password,coursename,True,begin=20)
# 开启新线程
thread1.start()
thread2.start()

threads = []
# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)

# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")
```

