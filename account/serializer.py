from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'tc', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }


    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('passwod and confirm password does not match')
        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class  UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ['email', 'password']
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

    
class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=225, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=225, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password and confirm Password does not match')
        
        user.set_password(password)
        user.save()
        return data



    
class UserEmailSendResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=225)
    class Meta:
        fields = ['email']
    

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('user id is:', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('user token is ', token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('user link is ', link)
            # use Send Email
            body = 'Click Following Link To Reset Your Password '+link
            data = {
                'subject':'Reset Your Password',
                'body': body,
                'to_email':user.email
            }
            Util.send_email(data)
      
            return data
        else:
            raise serializers.ValidationError('You are not a Register User')
        


class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=225, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=225, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']


    def validate(self, data):
        try:
            password = data.get('password')
            password2 = data.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError('Password and confirm Password does not match')
            
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not valid Or Expired')
            
            user.set_password(password)
            user.save()
            return data
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not valid or Expired')

        