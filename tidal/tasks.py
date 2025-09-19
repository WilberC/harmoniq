def sync_playlists(user):
    """
    Sync playlists for the given user.
    """
    from tidal.api import TidalAPI
    from tidal.models import Playlist, SyncStatus

    api = TidalAPI()
    limit = 50
    offset = 0
    while True:
        playlists_data = api.get_user_playlists(user, limit=limit, offset=offset)
        items = playlists_data.get("items", [])
        if not items:
            break

        for item in items:
            playlist, created = Playlist.objects.update_or_create(
                tidal_id=item["uuid"],
                defaults={
                    "name": item["title"],
                    "sync_status": SyncStatus.PENDING,
                },
            )
            # Here you might want to trigger a task to sync songs in the playlist
            # e.g., sync_playlist_songs.delay(playlist.id)

        offset += limit
        if offset >= playlists_data.get("totalNumberOfItems", 0):
            break
