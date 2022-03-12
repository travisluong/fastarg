from src import fastarg
import subprocess

def test_foo():
    assert 'foo'.upper() == 'FOO'

def test_fastarg_no_methods():
    app = fastarg.Fastarg()

    assert len(app.commands) == 0

def test_fastarg_one_method():
    app = fastarg.Fastarg()

    @app.command()
    def foo():
        print("foo")

    assert len(app.commands) == 1

def test_command_get_name():
    app = fastarg.Fastarg()

    @app.command()
    def foo():
        print("foo")

    assert app.commands[0].get_name() == "foo"

def test_hello_world():
    completed_process = subprocess.run("python3 main.py hello_world foo", shell=True, capture_output=True)
    assert completed_process.stdout.decode("utf-8") == "hello foo\n"

def test_create_todo():
    completed_process = subprocess.run("python3 main.py todo create_todo \"drink water\"", shell=True, capture_output=True)
    assert completed_process.stdout.decode("utf-8") == "create todo: drink water - False\n"

def test_create_todo_completed():
    completed_process = subprocess.run("python3 main.py todo create_todo \"drink water\" --completed", shell=True, capture_output=True)
    assert completed_process.stdout.decode("utf-8") == "create todo: drink water - True\n"

def test_create_address():
    completed_process = subprocess.run("python3 main.py user address create_address 123 \"456 main st\" --city bellevue --state wa --zip 98004", shell=True, capture_output=True)
    assert completed_process.stdout.decode("utf-8") == "creating address for user 123\n456 main st bellevue wa 98004\n"