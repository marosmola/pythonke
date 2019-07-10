from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from markdown import markdown


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False)


class Post(models.Model):

    COLOR_MODE_CHOICES = [
        ('light', 'light'),
        ('dark', 'dark'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    title_color = models.CharField(max_length=5, choices=COLOR_MODE_CHOICES, default='light')
    slug = models.SlugField(unique=True)
    image = models.FileField(null=True, blank=True)
    description = models.CharField(max_length=100)

    content = models.TextField(blank=True)
    draft = models.BooleanField(default=False)
    # publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    gitlink = models.URLField()

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ["-created"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "{}-{}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_reciever, sender=Post)