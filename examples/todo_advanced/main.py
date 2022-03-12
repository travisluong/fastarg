import fastarg
import commands.todo as todo
import commands.user as user

app = fastarg.Fastarg(description="productivity app", prog="todo")

@app.command()
def hello_world(name: str):
    """hello world"""
    print("hello " + name)

app.add_fastarg(todo.app, name="todo")
app.add_fastarg(user.app, name="user")

if __name__ == "__main__":
    app.run()