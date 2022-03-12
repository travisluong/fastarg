from src import fastarg

app = fastarg.Fastarg(description="Productivity App", prog="todo")
app2 = fastarg.Fastarg(description="To Do", help="Manage todos")
app3 = fastarg.Fastarg(description="User", help="Manage users")
app4 = fastarg.Fastarg(description="Address", help="Manage addresses")

@app.command()
def hello_world(name: str):
    """hello world"""
    print("hello " + name)

@app2.command()
def create_todo(title: str, completed: bool = False):
    """create a todo"""
    print(f"create todo: {title} - {completed}")

@app2.command()
def update_todo(
    id: int = fastarg.Argument(-1, help="the primary key of todo"), 
    completed: bool = fastarg.Option(False, help="completed status")
    ):
    """update a todo"""
    print(f"update todo: {id} - {completed}")

@app3.command()
def create_user(email: str, password: str, gold: float):
    """create a user"""
    print(f"creating {email}/{password} with {gold} gold")

@app3.command()
def delete_user(email: str):
    """delete a user"""
    print(f"deleting user {email}")

@app4.command()
def create_address(
    user_id: int, 
    address: str, 
    city: str = fastarg.Option("", help="city (e.g. Seattle)"), 
    state: str = fastarg.Option("", help="state (e.g. WA)"), 
    zip: str = fastarg.Option("", help="zip")
    ):
    """create address for user"""
    print(f"creating address for user {user_id}")
    print(f"{address} {city} {state} {zip}")


app.add_fastarg(app2, name="todo")
app.add_fastarg(app3, name="user")
app3.add_fastarg(app4, name="address")

if __name__ == "__main__":
    app.run()