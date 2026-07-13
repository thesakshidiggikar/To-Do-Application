class DirectoryNotFoundException(Exception):
    def __init__(self):
        self.message = "Directory not found"
        super().__init__(self.message)


class TodoNotFoundException(Exception):
    def __init__(self):
        self.message = "Todo not found"
        super().__init__(self.message)