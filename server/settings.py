import os


try:
    import local_settings
except ImportError:
    local_settings = {}


DEFAULT_REDIS_ADDR = getattr(local_settings, "REDIS_ADDR", "127.0.0.1")
DEFAULT_REDIS_PORT = getattr(local_settings, "REDIS_PORT", "6379")
DEFAULT_REDIS_DATABASE = getattr(local_settings, "REDIS_DATABASE", "0")
DEFAULT_API_KEY = getattr(local_settings, "API_KEY", "")
DEFAULT_LOG_LEVEL = getattr(local_settings, "LOG_LEVEL", "INFO")


REDIS_URL = getattr(local_settings, "REDIS_URL", ('redis://'
                                                  + os.getenv("REDIS_PORT_6379_TCP_ADDR", DEFAULT_REDIS_ADDR) + ':'
                                                  + os.getenv("REDIS_PORT_6379_TCP_PORT", DEFAULT_REDIS_PORT) + '/'
                                                  + os.getenv("REDIS_DATABASE", DEFAULT_REDIS_DATABASE)))

API_KEY = os.getenv("API_KEY", DEFAULT_API_KEY)

LOG_LEVEL = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)

ANALYZER_CLASSES = [
    'app.analyzers.skill_champion.AnalyzerSkillChampion',
    'app.analyzers.summoner_history.AnalyzerSummonerHistory',
    'app.analyzers.summoner.AnalyzerSummoner',
]
