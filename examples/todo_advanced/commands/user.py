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