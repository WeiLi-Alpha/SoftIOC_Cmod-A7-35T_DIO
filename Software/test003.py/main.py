# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import math

class People(object):
    total = 0
    name = 'Sam'
    age = 100

    def __init__(self,name,age):
        super(People,self).__init__()
#        import math

        name = name
        age = age
        #self
        self.eat(name,age)

        print('Initialization, name:%s, age:%s' %(name, age))

    def eat(self,name,age):
        print('%s eat food at age of %s...' %(name, age))
        print('%s eat food at age of %s...' %(self.name, self.age))

    def eat2(self,name,age):
        print('-----------------')
        self.eat(name,age+1)
        print('-----------------')

    @classmethod
    def work(cls,name, time, *args, **kwargs):
        print(cls)
        print('%s work %s mins' %(name,time))

    @classmethod
    def sleep(cls):
        print('ever function should add a @classmethod')

    @staticmethod
    def run(time):
        print('run for %s mins, sin(time)=%s' %(time,math.sin(time)))

People.work('Jim',10)

p1 = People('Sam',22)
p1.eat2('w',172)

p2 = People()

p1.work(10)
People.run(100)
