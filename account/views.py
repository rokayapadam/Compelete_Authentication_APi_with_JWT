from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import User
from rest_framework import status
from account.serializer import UserSerializer, UserLoginSerializer, UserProfileSerializer, UserPasswordChangeSerializer,UserEmailSendResetSerializer,UserResetPasswordSerializer
from django.contrib.auth import authenticate
from .renderer import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Custom token generator
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# Create your views here.

# class UserRegistration(APIView):
#     renderer_classes = [UserRenderer]
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.save()
#             token = get_tokens_for_user(user)
#             return Response({ 'tokan':token, 'msz':'Registration Successfull'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#  another method  used and not neccessary if  condition AND it is the best method use 
class UserRegistration(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({ 'tokan':token, 'msz':'Registration Successfull'}, status=status.HTTP_201_CREATED)






class UserLogin(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            print(email, password)
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token, 'msz':'Login success'}, status=status.HTTP_200_OK)
            
            return Response({'errors':{'non_field_errors':[' Email or Password is not valid']}}, 
             status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserPasswordChangeSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msz':'Password Changed Successfull'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)




class UserEmailSendView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=True):
        serializer = UserEmailSendResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msz':'Password Reset link send and please check your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserResetPasswordSerializer(data=request.data, context = {'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msz':'Password Reset Successfull'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

