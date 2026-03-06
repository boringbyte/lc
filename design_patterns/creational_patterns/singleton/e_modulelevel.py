class ConfigManager:

    def __init__(self):
        self.settings = {}

    def load_config(self, file_path):
        self.settings = {"db_host": "localhost", "db_port": 5462}

    def get(self, key):
        return self.settings.get(key)


config_manager = ConfigManager()


if __name__ == '__main__':
    config_manager.load_config("config.json")
    print(config_manager.settings)

    # If we download config_manager instance in another module.py
    # It will return the same configuration
