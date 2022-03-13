def deco(func):
    def inner():
        print("running inner()")
        func()
    return inner

def target():
    print('running target()')

target = deco(target)

target()