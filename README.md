## User Authentication 



 - ihtiyaclar;

    - customize Register ,
    - Register olunca login olunması
    - Login olunca token olusması
    - Logout olunca tkenin silinmesi

# I.YOL   

 - https://www.django-rest-framework.org/api-guide/authentication/

 - TokenAuthentication kullanıyoruz,

 settings.py =>

 ```
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]

 ```


 ```
REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'      
    ]
}

 ```


 ```
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],
    style={"input_type": "password"}
    
    )


    password2 = serializers.CharField(write_only=True, required=True,
    style={"input_type": "password"})

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

 ```


 - Yukarıdaki işlemde register islemini dizayn ettik,
   
    - email zorunlu oldu, password kontrolu uygulandı.
    - Token yukarıdaki islenler ile üretilmedi.


- Token üretilmesini views.py da register islemi yapılırken uygulayacagız.



views.py =>
```
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

#yukarıdaki işlem register için yeterli 
#aşağıdaki işlemi register olduktan sonra login olması için yaptık, ayrıca login olurken Tokenda olusturuldu.

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        data = serializer.data
        data['token'] = token.key
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
```

*** LOGIN ***

- obtain_auth_token views i var rest_framework un
db de userin tokeni varsa getiriyor, yoksa yeniden oluşturuyor

```
from rest_framework.authtoken import views

urlpatterns = [

path('login/', views.obtain_auth_token, name='login')
]


http://127.0.0.1:8000/user/login/ browserpi de gözükmez postmanda login olmamız gerekyor.

login olduktan sonra Token oluştu.

```


*** LOGOUT ***

- Logout olduğunda Token silinmesi icinde logout tanımlıyoruz.
- logout işleminde sistemde tanımlı token siliniyor tekrar login olunca yeni token veriyor, güvenlik yöntemi

 ```
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        data = {
            'message': 'logout'
        }
        return Response(data)  
 ```


 # II.YOL


- bu asamada auth icin ek paket kurulumu yapacagiz.

- `dj-rest-auth`  https://dj-rest-auth.readthedocs.io/en/latest/index.html


- `pip install dj-rest-auth`

```
INSTALLED_APPS = (
    ...,
    'rest_framework',
    'rest_framework.authtoken',
    ...,
    'dj_rest_auth'
)
```

- `python manage.py migrate` user tablolarının olusması icin 

urls.py 

```
urlpatterns = [
    ...,
    path('dj-rest-auth/', include('dj_rest_auth.urls'))
]
```

- patterns ne yönlendirme yapıyoruz. aşağıda belirtildiği gibi, ilgili auth işlemlerini seçiyoruz,


```
users/ auth/ password/reset/ [name='rest_password_reset']
users/ auth/ password/reset/confirm/ [name='rest_password_reset_confirm']
users/ auth/ login/ [name='rest_login']
users/ auth/ logout/ [name='rest_logout']
users/ auth/ user/ [name='rest_user_details']
users/ auth/ password/change/ [name='rest_password_change']
```

- bu peketin register işlemleri içinde özelliği bulunmaktada fakat özelleştirilebilirlik açısından biz kendi registerimizi yazdık

***REGISTER***

- User modelinden register işlemini tanımlıyoruz. Burada değiştirmek istediğimiz fields tekrar yazıyoruz.

    - emaili uniq ve zorunlu olması için tekrar tanımladık,
    - password1 ve password2 saglamasını kullanmak icin 


serializers.py

```
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validated_password


class RegisterSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(
        required=True,
 
        # burada dökümantasyondan gelen validatör işlemini kullanıyoruz. User dan mail vardı fakat burada biz required ve uniq olması için validatör işlemi yaptık
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
     ) 
    password = serializers.CharField(
        write_only=True,
        required =True,
        #pass özel hazır validator kullandık
        validators=[validated_password]
        style={"input-type":"password"}
     )
    password2 = serializers.CharField(
        write_only=True,
        required =True,
        #pass özel hazır validator kullandık
        validators=[validated_password]
        style={"input-type":"password"}
     )

     class Meta:
        model=User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2"
        )
    
# create işlemiş yapılma aşamasını dizayn ettik, user ile password aynı anda kayıt için göndermiyoruz. ilk önce pop ile password data dan ayırdık, password haricindeki user i tüm field ları ile çağırdık, ayırıp tanımladığımız password değişkenine atadığımız passwordu set işlemi ile user a eşitledik, 

    def create(self, validate_data):
        password = validated_data.pop("password")
        validated_data.pop("password2")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        if data["password"] != data["password2"]
            raise serializers.ValidationError(
                {"password":"password didn't match..."}
            )
        return data 
```


- register isleminden sonra views ve urls islemleri kaldı


```
views.py

from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
```

```
urls.py 

from django.urls import path, include
from .views import RegisterView


urlpatterns = [
    
    path('auth/', include('dj_rest_auth.urls')),
    path("register/", RegisterView.as_view()),
]
```


settings.py/base.py

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
       
    ]
}
```

- buraya kadar ki islemlerde register olduk, auth paketinden gelen login ile login olunca token üretti.

- Biz register olurken aynı zamanda login ve token olusmasi  için 2 farklı islem ile devam edebiliriz. signals, obtain token

  

```


ilgili app de signals.py da 

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


create_token satırı sabit gelmekte, üzerinde tanımlanan dekoratır önemli, sender in user modeli create olunca token ni kaydet

apps.py da bu yazılan signalin çalışması için 



from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    (bu ifadeyi tanımlıyoruz, bu ifade olmazsa çalışmaz)
    def ready(self):
        import users.signals
    

- register olduktan sonra token da oluştu, fakat bize tokeni filed olarak dönmedi, admin panelden kontrol edilebilir. 
- Bu olusan tokeni frontende gönderilmesi icin view içirisine override islemi yaptık. 

def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
            data["token"] = token.key
        else:
            data["token"] = "No token created for this user.... :))"
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
```


- Olusturduğumuz register isleminde artık frontende sadece token kodu döndü, user ait bilgilerin dönmesi için 

- https://dj-rest-auth.readthedocs.io/en/latest/configuration.html 


```
dokumandan configurationdan tokeni aldık, cource kodundan sadece key döndüğünü gördük ve nested olarak bize bilgileri vermesi icin user serializers olusturduk.
en son dokumanda eger validat yapıldıysa settings.py da bildirilmesi husunu da ekledik.
from dj_rest_auth.serializers import TokenSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email"
        )

class CustomTokenSerializer(TokenSerializer):
    user = UserSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = (
            "key",
            "user"
        ) 



settigns.py

REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'user.serializers.CustomTokenSerializer',

}
```







