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
        return self.config.get("OPENAI", "api_key")

    @property
    def OPENAI_BASE_URL(self):
        return self._get_optional("OPENAI", "base_url")

    @property
    def OPENAI_CHAT_MODEL(self):
        return self.config.get("OPENAI", "chat_model", fallback="gpt-4o-mini")

    @property
    def OPENAI_EMBEDDING_MODEL(self):
        return self.config.get(
            "OPENAI",
            "embedding_model",
            fallback="text-embedding-3-small"
        )

    @property
    def OPENAI_CLIENT_KWARGS(self):
        client_kwargs = {"api_key": self.OPENAI_API_KEY}

        if self.OPENAI_BASE_URL:
            client_kwargs["base_url"] = self.OPENAI_BASE_URL

        return client_kwargs

    @property
    def OPENAI_EMBEDDING_KWARGS(self):
        embedding_kwargs = {
            "openai_api_key": self.OPENAI_API_KEY,
            "model": self.OPENAI_EMBEDDING_MODEL,
            "tiktoken_enabled": self.OPENAI_EMBEDDING_TIKTOKEN_ENABLED,
        }

        if self.OPENAI_BASE_URL:
            embedding_kwargs["openai_api_base"] = self.OPENAI_BASE_URL

        return embedding_kwargs

    @property
    def OPENAI_EMBEDDING_TIKTOKEN_ENABLED(self):
        return self.config.getboolean(
            "OPENAI",
            "embedding_tiktoken_enabled",
            fallback=False
        )

    @property
    def DB_HOST(self):
        return self.config.get("DATABASE", "host")

    @property
    def DB_USER(self):
        return self.config.get("DATABASE", "user")

    @property
    def DB_PASS(self):
        return self.config.get("DATABASE", "password")

    @property
    def DB_NAME(self):
        return self.config.get("DATABASE", "database")

    @property
    def ENV(self):
        return self.config.get("SERVER", "environment", fallback="production")

    @property
    def RELOAD_VECTORSTORE(self):
        return self.config.getboolean("SERVER", "reload_vectorstore_on_startup", fallback=False)


# ✅ Global configuration instance
settings = Config()
