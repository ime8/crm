#-*-coding:utf-8 -*-
# age = 25
# name = 'Swaroop'
# print('{0} is {1} years old'.format(name,age))
# print('why is %s playing with that python' %(name))
#
#
#
# name = 'global'
# def test():
#     name = 'local'
#
#     def inner_test():
#         nonlocal name
#         # global name
#
#         name = name + '变量'
#         return name
#
#     print(name) #'local'+'变量'
#     return inner_test()
#
# print(name) #'global'
# print(test())
# print(name) #'global'
#
#
#
#
# def funX():
#     x =5
#     def funY():
#         nonlocal x
#         x+=1
#         return x
#     return funY
# a = funX()
# print(a()) #6
# print(a()) #7 因为x+=1已经把外部函数的x改成了6
# print(a()) #8
#
# def fn(name):
#     def inner():
#         return name()
#     return inner
#
# @fn # aa = fn(aa)
# def aa():
#     print("aaaaaa")
#
# aa()
#
#
# def count():
#
#     fs = []
#     for i in range(1,4):
#
#         def fn():
#             return i*i
#         fs.append(fn)
#     return fs
# f1,f2,f3 = count()
# print(f1())
# print(f2())
# print(f3())
#
#
# def count():
#     fs = []
#     for i in range(1,4):
#         def fn():
#             return i*i
#         fs.append(fn)
#     return fs
# f1,f2,f3 = count()
# print(f1()) #9
# print(f2()) #9
# print(f3()) #9
#
#
# def count():
#     def f(j):
#         def g():
#             return j*j
#         return g
#     fs = []
#     for i in range(1, 4):
#         fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
#     return fs
#
# f1,f2,f3 = count()
# print(f1()) #1
# print(f2()) #4
# print(f3()) #9

# a = 10
# def bar():
#     global a
#     a = 'in bar'
# bar()
# print(a) #in bar

# def fn():
#     count = 8
#     def inner(dt=0):
#         nonlocal count
#         count =count +dt
#         print(count)
#     return inner
# fn()() #8


field_obj =((0, '转介绍'), (1, 'QQ群'), (2, '官网'), (3, '百度推广'), (4, '51CTO'), (5, '知乎'), (6, '市场推广'))
for choice_item in field_obj:
    print(choice_item[0])
    break



