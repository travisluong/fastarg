import fastarg

app = fastarg.Fastarg(description="to do", help="manage todos")

@app.command()
def create_todo(title: str, completed: bool = False):
    """create a todo"""
    print(f"create todo: {title} - {completed}")

@app.command()
def update_todo(
    id: int = fastarg.Argument(-1, help="the primary key of todo"), 
    completed: bool = fastarg.Option(False, help="completed status")
    ):
    """update a todo"""
    print(f"update todo: {id} - {completed}")