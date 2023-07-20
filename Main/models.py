from django.db import models


class TagType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000, blank=True)
    parents = models.ManyToManyField('self', blank=True)
    tag_type = models.ForeignKey(TagType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_all_parents(self):
        """
        Gets all parent tags of this tag recursively.
        """
        parents = set(self.parents.all())
        for parent in self.parents.all():
            parents.update(parent.get_all_parents())

        return parents


class Card(models.Model):
    """
    Or 1 image or 1 video
    """
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    video = models.FileField(upload_to='videos/', blank=True)

    def __str__(self):
        return self.title

    def add_tags_and_parents(self, tags):
        """
        Adds a list of tags and all their parent tags recursively.
        """
        tags_to_add = set(tags)
        for tag in tags:
            tags_to_add.update(tag.get_all_parents())

        self.tags.add(*tags_to_add)


