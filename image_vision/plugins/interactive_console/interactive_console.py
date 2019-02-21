import code


class InteractiveConsole(code.InteractiveConsole):
    def __init__(self, namespace):
        super().__init__(namespace)

    '''
    def write(self, data: str):
        # print(data)
        print('MY write METHOD:', data)
    '''
