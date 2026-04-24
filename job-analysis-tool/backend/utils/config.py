import configparser
import os


class Config:
    def __init__(self, file_path="config.ini"):
        self.config = configparser.ConfigParser()
        resolved_path = file_path

        if not os.path.isabs(resolved_path):
            resolved_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                file_path
            )

        if not os.path.exists(resolved_path):
            raise FileNotFoundError(f"Configuration file not found: {resolved_path}")

        self.config.read(resolved_path)

    def _get_optional(self, section, option, fallback=None):
        value = self.config.get(section, option, fallback=fallback)
        if value is None:
            return None

        value = value.strip()
        return value or fallback

    @property
    def OPENAI_API_KEY(self):
        return self.config.get("OPENAI", "api_key", fallback="").strip()

    @property
    def OPENAI_BASE_URL(self):
        return self._get_optional("OPENAI", "base_url")

    @property
    def OPENAI_ENABLED(self):
        return bool(self.OPENAI_API_KEY)

    @property
    def OPENAI_CHAT_MODEL(self):
        return self.config.get("OPENAI", "chat_model", fallback="gpt-4o-mini")

    @property
    def OPENAI_CLIENT_KWARGS(self):
        client_kwargs = {"api_key": self.OPENAI_API_KEY}

        if self.OPENAI_BASE_URL:
            client_kwargs["base_url"] = self.OPENAI_BASE_URL

        return client_kwargs

    @property
    def ENV(self):
        return self.config.get("SERVER", "environment", fallback="production")

    @property
    def ALLOWED_ORIGINS(self):
        raw_value = self.config.get("SERVER", "allowed_origins", fallback="http://localhost:5173")
        return [origin.strip() for origin in raw_value.split(",") if origin.strip()]

    @property
    def MAX_UPLOAD_SIZE_MB(self):
        return self.config.getint("SERVER", "max_upload_size_mb", fallback=8)

    @property
    def DB_ENABLED(self):
        return self.config.getboolean("DATABASE", "enabled", fallback=False)

    @property
    def DB_HOST(self):
        return self.config.get("DATABASE", "host", fallback="localhost")

    @property
    def DB_PORT(self):
        return self.config.getint("DATABASE", "port", fallback=3306)

    @property
    def DB_USER(self):
        return self.config.get("DATABASE", "user", fallback="")

    @property
    def DB_PASS(self):
        return self.config.get("DATABASE", "password", fallback="")

    @property
    def DB_NAME(self):
        return self.config.get("DATABASE", "database", fallback="")

    @property
    def DB_CONFIGURED(self):
        return self.DB_ENABLED and all((self.DB_HOST, self.DB_PORT, self.DB_USER, self.DB_NAME))


settings = Config()
