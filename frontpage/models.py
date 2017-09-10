from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone
# User 확장을 위해 필요함
from django.db.models.signals import post_save
from django.dispatch import receiver

class MakeBoard(models.Model) :
    # foreignkey는 일대 다수 관계이다. 다수의 게시물에 하나의 글쓴이가 존재할 수 있으므로 아래와 같은 관계를 정의한다.
    author = models.ForeignKey(User, related_name='author')
    # 문자 200자 제한 타이틀
    title = models.CharField(max_length=200)
    # 자세한 내용은 위지윅으로 작성한다. 나는 summernote를 썼다
    desc = models.TextField()
    # 썸네일을 이용하자.
    photo = models.ImageField(upload_to='photos')
    # 작성 날짜를 적자
    created_date = models.DateTimeField(default=timezone.now)
    # 수정 날짜를 적자
    published_date = models.DateTimeField(blank=True, null=True)
    # Like 기능 만들기
    like = models.ManyToManyField(User, related_name='like', blank=True)

    def __str__(self):
        return self.title

# follower 정의하기
# one to one 관계처럼
class Profile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ManyToManyField(User, blank=True, related_name='follower')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)