class CommandLineInterface:

    def __init__(self, \
        errmsg='USAGE: python example.py <command> [<key>=<value>]*'):
        self.functions = {}
        self.errmsg = errmsg

    def command(self, f):
        import inspect
        self.functions[f.__name__] = (inspect.getfullargspec(f).args, f)
        return f

    def main(self):
        import sys
        if len(sys.argv) == 1 or sys.argv[1] not in self.functions.keys():
            print(self.errmsg)
            sys.exit(1)
        kwargs = {}
        for parameter in sys.argv[2:]:
            partitioned_parameter = parameter.partition('=')
            if not partitioned_parameter[1]:
                print(self.errmsg)
                sys.exit(1)
            if partitioned_parameter[0] not in self.functions[sys.argv[1]][0]:
                print(self.errmsg)
                sys.exit(1)
            kwargs[partitioned_parameter[0]] = partitioned_parameter[2]
        sys.exit(self.functions[sys.argv[1]][1](**kwargs))
