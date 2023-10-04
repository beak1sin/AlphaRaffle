from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectStaticCommand
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

class SkipExistingFileStorage(ManifestStaticFilesStorage):
    def _save(self, name, content):
        if self.exists(name):
            return name  # 파일이 이미 존재하면, 저장 작업을 스킵합니다.
        return super()._save(name, content)

class Command(CollectStaticCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = SkipExistingFileStorage(location=self.storage.location)
