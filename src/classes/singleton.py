class SingletonMeta(type):
    _instances = {}  # Dictionary to store instance of each singleton class

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            print("Creating the instance")
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]