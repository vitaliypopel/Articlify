from json import loads
from typing import Any


class Config:

    def __init__(self) -> None:
        with open('config.json', 'r') as file:
            file_read = file.read()

            if not file_read:
                raise ConfigError('Файл config.json пустий. Будь ласка налаштуйте конфігурацію')

            config = loads(file_read)

        self.__config: dict[str] = config['configuration']

    def get(self, key: str) -> Any:
        if key not in self.__config.keys():
            raise ConfigError('Конфіг не знайдено! Перевірте файл config.json')

        return self.__config[str(key)]


class ConfigError(ValueError):
    # Кастомний ConfigError створений спеціально для класу Config

    def __init__(self, error: str):
        self.error = error

