from search.models import Youtube


def like_cancel_youtube(youtube_url: str) -> None:
    Youtube.objects.get(url=youtube_url).delete()
