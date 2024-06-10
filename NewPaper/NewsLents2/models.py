from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.core.cache import cache

# Create your models here.
class Likeable(models.Model):
    _rating = models.IntegerField(default=0, db_column='rating')

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1 if self._rating > 0 else 0
        self.save()

    class Meta:
        abstract = True
class Author(Likeable):
    user_author = models.ForeignKey(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0, db_column='rating')



    def update_rating(self):
        summa = 0

        list_rating_post = Post.objects.filter(author=self).values('_rating')
        for i in list_rating_post:
            summa = summa + (i['_rating'] * 3)

        list_rating_comment = Comment.objects.filter(user=self.user_author).values('_rating')
        for i in list_rating_comment:
            summa = summa + i['_rating']

        list_rating_comment_post = Comment.objects.filter(post__author=self).values('_rating')
        for i in list_rating_comment_post:
            summa = summa + i['_rating']

        self._rating = summa
        self.save()

    def __str__(self):
        return f'{self.user_author}'
class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories', through='Subscription')

    def __str__(self):
        return f'{self.category}'

class Post(Likeable):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news_or_state = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, unique=True)
    text = models.TextField(unique=True)
    _rating = models.IntegerField(default=0, db_column='rating')

    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return self.text[:124:] + '...'

    def __str__(self):
        return f'''{self.title[:90:]} : {self.text[:200:]}'''

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'''{self.post.title[:40:]} : {self.category}'''

class Comment(Likeable):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    _rating = models.IntegerField(default=0, db_column='rating')

    def __str__(self):
        return f'{self.post.title[:40:]} : {self.text}'

class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

    def __str__(self):
        return f'{self.user} : {self.category}'