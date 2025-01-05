class DataFrameError(ValueError):
    def __init__(self, menssage="Dataframe not provide!"):
        self.menssage = menssage
        super().__init__(self.menssage)

    def __str__(self):
        return f"{self.menssage}"
