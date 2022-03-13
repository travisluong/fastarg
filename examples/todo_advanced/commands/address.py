import fastarg

app = fastarg.Fastarg(description="address", help="manage addresses")

@app.command()
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