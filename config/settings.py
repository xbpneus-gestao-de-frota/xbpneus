import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "backend.transportador", # Principal app de transportador
    'backend.jobs',
    'backend.common',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "backend.transportador.dashboard",
    "backend.transportador.empresas",
    
    # 3rd Party
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework_simplejwt.token_blacklist",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "django_rq",
    "axes",
    
    # Transportador - Módulos
    "backend.transportador.frota",
    "backend.transportador.pneus",
    "backend.transportador.manutencao",
    "backend.transportador.estoque",
    "backend.transportador.loja",
    "backend.transportador.motorista_interno",
    "backend.transportador.custos",
    "backend.transportador.combustivel",
    "backend.transportador.multas",
    "backend.transportador.documentos",
    "backend.transportador.viagens",
    "backend.transportador.clientes",
    "backend.transportador.fornecedores",
    "backend.transportador.seguros",
    "backend.transportador.contratos",
    "backend.transportador.faturamento",
    "backend.transportador.pagamentos",
    "backend.transportador.telemetria",
    "backend.transportador.rastreamento",
    "backend.transportador.rotas",
    "backend.transportador.entregas",
    "backend.transportador.dashboards",
    "backend.transportador.notificacoes",
    "backend.transportador.almoxarifado",
    "backend.transportador.relatorios",
    "backend.transportador.cargas",
    "backend.transportador.pecas",
    "backend.transportador.ferramentas",
    "backend.transportador.epis",
    "backend.transportador.treinamentos",
    "backend.transportador.compliance",
    "backend.transportador.alertas",
    "backend.transportador.integracoes",
    "backend.transportador.configuracoes",
    
    # IA - Novo Módulo
    "backend.transportador.ia_pneus",
    
    # Outros Módulos
    "backend.borracharia",
    "backend.motorista",
    "backend.revenda",
    "backend.recapagem",
    "backend.reports",
]

MIDDLEWARE = [
    'backend.common.metrics.MetricsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "frontend" / "dist"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],
    },
}]

WSGI_APPLICATION = "config.wsgi.application"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "frontend" / "public" / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_RATES": {
        "anon": os.environ.get("XBP_THROTTLE_ANON", "100/min"),
        "user": os.getenv("XBP_THROTTLE_USER", "1000/min"),
    },
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_PAGINATION_CLASS": "config.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": int(os.getenv("PAGE_SIZE", "20")),
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

SPECTACULAR_SETTINGS = {"TITLE": "XBPNEUS API", "VERSION": "v1"}

# Redis Queue
RQ_QUEUES = {
    "default": {"URL": os.getenv("REDIS_URL", "redis://localhost:6379/0")}
}

# Configurações de IA
IA_CONFIG = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    "MODEL_PATH": BASE_DIR / "backend" / "transportador" / "ia_pneus" / "models",
    "DATABASE_PATH": BASE_DIR / "backend" / "transportador" / "ia_pneus" / "database",
    "ENABLE_LEARNING": os.getenv("IA_ENABLE_LEARNING", "True") == "True",
    "ENABLE_GAMIFICATION": os.getenv("IA_ENABLE_GAMIFICATION", "True") == "True",
}

# Auth
AUTH_USER_MODEL = "transportador.UsuarioTransportador"

# Axes (Security)
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_LOCK_OUT_AT_FAILURE = True
AXES_LOCKOUT_PARAMETERS = ["username", "ip_address"]

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "json"},
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
    "loggers": {
        "django": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "gunicorn.error": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "gunicorn.access": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
    },
}

# Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(os.getenv("SENTRY_TRACES", "0.0"))
    )

# Security
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True") == "True"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "True") == "True"
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"

# CORS
_cors = os.getenv("CORS_ALLOWED_ORIGINS")
if _cors:
    CORS_ALLOWED_ORIGINS = [x.strip() for x in _cors.split(",") if x.strip()]

# Debug override
if os.environ.get("DJANGO_DEBUG") in {"1", "true", "True"}:
    DEBUG = True

# Audit masking (LGPD/AppSec)
AUDIT_MASK_FIELDS = {
    "password", "token", "access", "refresh", "authorization", "auth", "secret", "cpf", "email"
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

