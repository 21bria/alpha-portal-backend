from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.cms.models.media import Media, MediaAlbumItem


@receiver(post_delete, sender=Media)
def delete_media_file(sender, instance, **kwargs):

    # delete original file
    if instance.file:
        instance.file.delete(save=False)

    # delete thumbnail
    if instance.thumbnail:
        instance.thumbnail.delete(save=False)


@receiver(post_delete, sender=MediaAlbumItem)
def delete_album_item_media(sender, instance, **kwargs):
    if instance.media:
        instance.media.delete()