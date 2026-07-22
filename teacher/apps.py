from django.apps import AppConfig


class TeacherConfig(AppConfig):
    name = 'teacher'

    def ready(self):
        import teacher.signals  # noqa
