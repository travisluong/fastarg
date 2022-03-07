from src import fastarg


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

