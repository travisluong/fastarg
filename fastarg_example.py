from src import fastarg

app = fastarg.Fastarg(description="My App", help="app1 help")

app2 = fastarg.Fastarg(description="My App 2", help="app2 help")

app3 = fastarg.Fastarg(description="My App 3", help="app3 help")

@app2.command()
def foo(foo: str):
    """app2 foo"""
    print("foo")

@app3.command()
def bar():
    print("bar")

@app3.command()
def corge(name: str = "corge"):
    print(f"corge {name}")

app.add_fastarg(app2, name="apptwo")
app2.add_fastarg(app3, name="appthree")

@app.command()
def baz(name: str):
    """hello world"""
    print("hello " + name)

@app.command()
def qux(num: int = fastarg.Option(None, help="the default qux num"), name: str = fastarg.Argument("quxx", help="quxx")):
    print(num)
    print(name)

# @app.command()
# def apptwo():
#     print("app two")

if __name__ == "__main__":
    app.run()