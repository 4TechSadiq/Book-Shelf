# from django.contrib.auth.models import BaseUserManager
# from django.utils.translation import gettext_lazy as _

# class CustomClassManager(BaseUserManager):
#     def create_user(self, email, password,**extras):
#         if not email:
#             raise ValueError("The email must be fill")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extras)
#         user.set_password(password)
#         user.save()

#         return user
    
#     def create_superuser(self, email, password, **extras):
#         extras.setdefault("is_staff", True)
#         extras.setdefault("is_super", True)
#         extras.setdefault("is_active", True)

#         if extras.get("is_staff") is not True:
#             raise ValueError(_("superuser must have is_staff.True"))
#         if extras.get("is_superuser") is not True:
#             raise ValueError(_("superuser must have is_superuser=True."))
#         return self.create_user(email, password, **extras)
