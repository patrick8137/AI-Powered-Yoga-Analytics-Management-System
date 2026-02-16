from django.apps import AppConfig

class AiEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_engine'

    def ready(self):
        import ai_engine.signals
        import students.signals
        import os
        from django.contrib.auth import get_user_model

        if os.environ.get("RAILWAY_ENVIRONMENT"):
            User = get_user_model()

            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="admin123"
                )
