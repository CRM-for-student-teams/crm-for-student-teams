import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from settings.config import ENV_ID, ENV_POSSIBLE_OPTIONS
import apps.chat.routing  # correct websocket routes

# Ensure correct environment
assert (
    ENV_ID in ENV_POSSIBLE_OPTIONS
), f"Set correct DJANGO_ENV_ID env var. Possible options: {ENV_POSSIBLE_OPTIONS}"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"settings.env.{ENV_ID}")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(apps.chat.routing.websocket_urlpatterns)
        ),
    }
)
