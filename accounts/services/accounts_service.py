from accounts.models import CustomUser
from datetime import datetime
from django.db.models import QuerySet



def create_single_user(email:str, nickname:str, password:str,**kwargs: str) -> CustomUser:
    user = CustomUser.objects.create_user(email=email, nickname=nickname, password=password, **kwargs)
    return user

def check_email_duplication(email:str) -> CustomUser:
    return CustomUser.objects.filter(eamil__iexact=email).exists()

# def change_user_profile(user: CustomUser, nickname:str, bio:str, **kwargs: str) -> CustomUser:
#     user.nickname = nickname
#     user.bio = bio
#     # img = kwargs.get('img','')
#     try:        
#         img = kwargs['img']        
#         img_extension = img.name.split(".")[-1]
#         img.name = user.email.split("@")[0] + "-" + datetime.now().strftime("%Y-%m-%d") + "." + img_extension
#         user.img = img
#     except:
#         pass

#     try:        
#         password = kwargs['password']
#         user.set_password(password)
#     except:
#         pass
#     user.save()
#     return user


def get_friend_list(user_id:int) -> QuerySet[CustomUser]:
    user = CustomUser.objects.get(id=user_id)
    friends = user.friends.all()
    return friends