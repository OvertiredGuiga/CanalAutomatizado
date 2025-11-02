# Importar tarefas para registrá-las no Celery
from src.tasks import collect_youtube_videos  # noqa: F401
from src.tasks_download import (  # noqa: F401
    download_youtube_video,
    download_multiple_youtube_videos,
    get_video_info_task,
    get_available_formats_task,
)

__version__ = "1.0.0"
__author__ = "Flamengo AI Creator Team"
