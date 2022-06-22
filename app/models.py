from django.urls import reverse
from django.db import models
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey

class Category(models.Model):
    # VIEW_TYPE = (
    #     (1,'Post'),
    #     (2,'Mahsulot'),
    #     (3,'Rahbariyat')
    # )
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    # view_type = models.IntegerField(choices=VIEW_TYPE, default=1)
    # style_view (post, maxsulot, rahbariyat)
   
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField()
    body = RichTextUploadingField()
    slug = models.SlugField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    views_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)

    
    def get_absolute_url(self):
        return reverse('blog-details', kwargs={'slug':self.url})

class Comment(models.Model):
    fio = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    comment = models.TextField(default='', null=True, blank=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.fio

class Menu(MPTTModel):
    MENU_TYPE = (
        (1,'Page'),
        (2,'Category'),
        (3,'Link')
    )
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(  'self',
                                    null=True, blank=True,
                                    related_name='children', 
                                    on_delete=models.CASCADE, db_index=True,
                                    default=''
                                )
    menu_type = models.IntegerField(choices=MENU_TYPE, default=1)
    link = models.SlugField(null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'link',))
        verbose_name_plural = 'menus'

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.link for i in ancestors]
            slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.link = slugify(self.name)

        super(Menu, self).save(*args, **kwargs)
       
class Page(models.Model):
    title = models.CharField(max_length=100)
    body = RichTextUploadingField()
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Page, self).save(*args, **kwargs)

    def get_absolute_url(self):
      kwargs = {
        'slug': self.slug
      }
      return reverse('page', kwargs=kwargs)


class Setting(models.Model):
    # NAME_TYPE = (
    #     (1,''),
    # )
    section = models.CharField(max_length=200, default='')
    name = models.CharField( max_length=100)
    config = models.CharField(max_length=255)


    def __str__(self):
        return self.name

