from settings_setup import setup_settings

# Project modules read `project_settings` at import time, so configs must be registered
# before any `src.*` import happens inside test modules
setup_settings()
