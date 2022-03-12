# Fastarg

Fastarg is a command line argument parser utility that is built on Python's standard argparse library.

## Installation

```
pip3 install fastarg
```

## Getting started

main.py

```
import fastarg

app = fastarg.Fastarg(description="hello world")

@app.command()
def hello_world(name: str):
    """hello world"""
    print("hello " + name)

if __name__ == "__main__":
    app.run()
```

Run command:

    $ python3 main.py hello_world foo

Show help text:

    $ python3 main.py -h

## Subcommands

Create arbitrarily large trees of subcommands.

```
import fastarg

app = fastarg.Fastarg(description="productivity app", prog="todo")
app2 = fastarg.Fastarg(description="to do", help="manage todos")
app3 = fastarg.Fastarg(description="user", help="manage users")
app4 = fastarg.Fastarg(description="address", help="manage addresses")

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
    id: int = fastarg.Argument(help="the primary key of todo"), 
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
```

### Example usage

Run hello world:
    
    $ python3 main.py hello_world foo

Show help text for todo subcommand:
    
    $ python3 main.py todo -h
    
Show help text for a subcommand:

    $ python3 main.py todo update_todo -h

Run create_todo subcommand:

    $ python3 main.py todo create_todo "drink water"

Run create_todo with optional completed flag:

    $ python3 main.py todo create_todo "drink water" --completed
    $ python3 main.py todo create_todo "drink water" --no-completed

Run the nested create_address command:

    $ python3 main.py user address create_address 123 "456 main st" --city bellevue --state wa --zip 98004

## Arguments

Positional arguments are required. For example, the create_todo command takes a positional argument of title.

## Options

Options are optional. For example, the create_address command takes an optional argument of city, state, and zip.

## Subcommands in multiple files

main.py

```
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
```

commands/todo.py

```
import fastarg

app = fastarg.Fastarg(description="to do", help="manage todos")

@app.command()
def create_todo(title: str, completed: bool = False):
    """create a todo"""
    print(f"create todo: {title} - {completed}")

@app.command()
def update_todo(
    id: int = fastarg.Argument(help="the primary key of todo"), 
    completed: bool = fastarg.Option(False, help="completed status")
    ):
    """update a todo"""
    print(f"update todo: {id} - {completed}")
```

commands/user.py

```
import fastarg
import commands.address as address

app = fastarg.Fastarg(description="user", help="manage users")

@app.command()
def create_user(email: str, password: str, gold: float):
    """create a user"""
    print(f"creating {email}/{password} with {gold} gold")

@app.command()
def delete_user(email: str):
    """delete a user"""
    print(f"deleting user {email}")

app.add_fastarg(address.app, name="address")
```

## Examples

https://github.com/travisluong/fastarg/tree/main/examples

## Author

Travis Luong