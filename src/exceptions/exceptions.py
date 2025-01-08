class DataFrameError(ValueError):
    def __init__(self, message="Dataframe not provide"):
        self.message = message
        super().__init__(self.message)


class AssetError(ValueError):
    def __init__(self, message="Asset not computable"):
        self.message = message
        super().__init__(self.message)