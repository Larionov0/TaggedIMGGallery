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
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    video = models.FileField(upload_to='videos/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def get_all_tags_string(self):
        return ', '.join([tag.name for tag in self.tags.all()])


class ImagePart(models.Model):
    """
    A part of an image, like a face or a car.
    """
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    start_x = models.FloatField()  # %
    start_y = models.FloatField()  # %
    width = models.FloatField()  # %
    height = models.FloatField()  # %
    scale = models.FloatField(default=1)  # %
    tags = models.ManyToManyField(Tag, blank=True)
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'start_x': self.start_x,
            'start_y': self.start_y,
            'width': self.width,
            'height': self.height,
            'scale': self.scale,
            'tags': [tag.name for tag in self.tags.all()],
            'name': self.name,
        }
