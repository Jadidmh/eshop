from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q

class AuthBackend(ModelBackend):
    
    def authenticate(self, request, phone=None, password=None, **kwargs):
        
        try:
            user = User.objects.get(Q(username__iexact=phone) | Q(email__iexact=phone) | Q(phone__iexact=phone))
        except User.DoesNotExist:
            User().set_password(password)
            return
        except User.MultipleObjectsReturned:
            user = User.objects.filter(Q(username__iexact=phone) | Q(email__iexact=phone) | Q(phone__iexact=phone)).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
