from django.db import models
from django.contrib.auth.models import AbstractUser
#from article_module.models import Article, ArticleScore


# Create your models here.

class User(AbstractUser):
    email_active_code = models.CharField(max_length=100)
    about_user = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True, choices=[
        ('proff', 'Professor'),
        ('student', 'student')
    ])
    avatar = models.ImageField(upload_to='images/user_avatar', null=True, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return self.email


class Proff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_num = models.IntegerField()
    field_of_study = models.CharField(max_length=100)
    education_level = models.CharField(max_length=100)

    def __str__(self):
        if self.user.last_name or self.user.first_name:
            return self.user.first_name + self.user.last_name
        else:
            return self.user.email


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_num = models.IntegerField(null=True, blank=True)
    faculty = models.CharField(max_length=100, choices=[
        ('computer_engineering', 'Computer Engineering'),
        ('electrical_engineering', 'Electrical Engineering'),
        ('math', 'Math'),
        ('mechanic_engineering', 'Mechanical Engineering'),
    ])
    #prof = models.ManyToManyField(Proff, blank=True, through='StudentProfessorRelation')
    field_of_study = models.CharField(max_length=100)
    education_level = models.CharField(max_length=100, default='post_gradual', choices=[
        ('phd', 'PhD'),
        ('post_gradual', 'Post Gradual')
    ])

    def __str__(self):
        if self.user.last_name or self.user.first_name:
            return self.user.first_name + self.user.last_name
        else:
            return self.user.email


#class StudentProfessorRelation(models.Model):
#    student = models.ForeignKey(Student, on_delete=models.CASCADE)
#    professor = models.ForeignKey(Proff, on_delete=models.CASCADE)
#    role = models.CharField(max_length=50, choices=[
#        ('advisor', 'Advisor'),
#        ('manager', 'Manager'),
#        ('referee', 'Referee'),
#    ])

#    class Meta:
#        unique_together = ('student', 'professor', 'role')


