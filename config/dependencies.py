from config.app_container import AppContainer


container = AppContainer()

container.core.config.waha.base_url.from_env('WAHA_BASE_URL', '')  # type: ignore
