from inspect import signature

def cli(func):
    sig = signature(func)
    for name, param in sig.parameters.items():
        print(param.kind, ':', name, '=', param.default)
        annotation = param.annotation
        print(annotation)

@cli
def target(foo: str, bar: int = 1):
    print(f"foo: {foo} bar: {bar}")
