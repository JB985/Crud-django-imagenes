from django.apps import AppConfig

class CrudAppImgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crud_app_img'

    def ready(self):
        from . import signals