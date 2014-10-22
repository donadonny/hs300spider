def f(i):
    def p():
        print i
    return p



x=f(1)
x()