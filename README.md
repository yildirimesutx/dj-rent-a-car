## User Authentication 



 - ihtiyaclar;

    - Custum Register ,
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

```
from rest_framework.authtoken import views

urlpatterns = [

path('login/', views.obtain_auth_token, name='login')
]

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


 
