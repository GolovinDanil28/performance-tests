# Импортируем необходимые типы из Pydantic
from pydantic import BaseModel, SecretStr, EmailStr, HttpUrl
# Импортируем базовый класс настроек и конфигурацию из pydantic-settings
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestUser(BaseModel):
    email: EmailStr
    password: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.basics",  # Путь до файла с переменными окружения
        env_file_encoding="utf-8",  # Кодировка .env файла
        env_nested_delimiter=".",  # Разделитель для вложенных структур, например TEST_USER.EMAIL
    )


    base_url: HttpUrl
    test_user: TestUser


print(Settings())
