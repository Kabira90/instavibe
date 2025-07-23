from .models import Profile
from django.contrib import admin
from .models import Profile, Post, Follow, Story, Message,Notification, Highlight # Make sure Follow and Story are imported

 



 


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Follow)  # ✅ This will show Follow in admin
admin.site.register(Story)   # ✅ This will show Story in admin
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Highlight)
