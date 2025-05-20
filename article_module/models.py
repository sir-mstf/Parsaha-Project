from django.db import models
from account_module.models import Student, Proff
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.OneToOneField(Student, on_delete=models.CASCADE)
    professors = models.ManyToManyField(Proff, through='ArticleScore', related_name='article_professors')
    file = models.FileField(upload_to='files/articles/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(Proff, on_delete=models.CASCADE, null=True, blank=True, related_name='article_manager')
    edit_permission = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f'{self.title}  {str(self.author)}'


class ArticleScore(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    professor = models.ForeignKey(Proff, on_delete=models.CASCADE)
    score = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2,
                                validators=[MaxValueValidator(20), MinValueValidator(0)])
    score_1 = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(4), MinValueValidator(0)])
    score_2 = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(4), MinValueValidator(0)])
    score_3 = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(10), MinValueValidator(0)])
    score_4 = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(2), MinValueValidator(0)])
    prof_role = models.CharField(max_length=50, choices=[('referee', 'Referee'),
                                                        ('advisor', 'Advisor'),])
    comment = models.TextField(blank=True, null=True)
    student_protest = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    scoring_permission = models.BooleanField(default=False, null=True, blank=True)


    class Meta:
        unique_together = ('article', 'professor')

    def __str__(self):
        return f'{self.professor}  {self.score}'



