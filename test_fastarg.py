import fastarg

app = fastarg.Fastarg()

app2 = fastarg.Fastarg()

@app2.command()
def foo():
    print("foo")

app.add_fastarg(app2, name="foo")

@app.command()
def hello(name: str):
    """hello world"""
    print("hello " + name)

@app.command()
def goodbye(num: int):
    print(num)

if __name__ == "__main__":
    app.run()