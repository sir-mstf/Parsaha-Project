from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from article_module.models import Article, ArticleScore


#class ArticleForm(forms.ModelForm):
#    class Meta:
#        model = Article
#        fields = ['title', 'content']

#class ArticleScoreForm(forms.ModelForm):
#    class Meta:
#        model = ArticleScore
#        fields = ['score', 'comment']

# forms.py

# forms.py

# forms.py

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'file', 'edit_permission']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter article content here...'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article title...'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.docx,.txt'
            }),
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
            'file': 'Upload File (Optional)',
        }



class ArticleScoreProtestForm(forms.ModelForm):
    class Meta:
        model = ArticleScore
        fields = ['student_protest']
        widgets = {
            'student_protest': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'اعتراض خود را وارد کنید...'
            })
        }
        labels = {
            'student_protest': 'متن اعتراض'
        }



# forms.py

class ArticleScoreForm(forms.ModelForm):
    class Meta:
        model = ArticleScore
        fields = ['score_1', 'score_2', 'score_3', 'score_4', 'score', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your comment here...'
            })
        }
        labels = {
            'score_1': 'presentation quality(from 4)',
            'score_2': 'content relevance(from 4)',
            'score_3': 'Up-to-date resources(from 10)',
            'score_4': 'subject adaptation(from 2)',
            'score': 'Total Score',
            'comment': 'Comment'
        }
