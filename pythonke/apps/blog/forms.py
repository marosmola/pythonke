from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post

class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = False

    content = forms.CharField(widget=forms.Textarea)
    publish = forms.DateField(widget=forms.SelectDateWidget)
    
    class Meta:
        model = Post
        fields = ( "title", "title_color", "description", "image", "content", "draft", "publish", "gitlink")

