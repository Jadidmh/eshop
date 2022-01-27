from rest_framework import generics
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ClientRegisterSerializer, GetTokenForLoginSerializer, ClientProfileSerializer, LoginUserWithOtpSerializer, GenerateOtpLoginSerializer 
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
import base64
import pyotp
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from aiohttp import ClientSession
import asyncio

# Create your viewApis here.

class ClientRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ClientRegisterSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response({"موفقیت": "ثبت نام شما با موفقیت انجام شد"}, status=status.HTTP_201_CREATED)

class GetTokenForLoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = GetTokenForLoginSerializer
    parser_classes = (MultiPartParser, FormParser)

class ClientProfileView(generics.RetrieveUpdateAPIView):
    http_method_names = ['put', 'get']
    permission_classes = (IsAuthenticated,)
    serializer_class = ClientProfileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)



#-----------------------------------------------------------------------

async def send_otp(phone, otp):
    async with ClientSession() as session:
        unit_url = "https://RestfulSms.com/api/Token"
        validation_headers = {'content-type': 'application/json'}
        validation_body = {"SecretKey": (
            'SECURITY_CODE'), "UserApiKey": ('API_KEY')}
        response = await session.post(unit_url, json=validation_body, headers=validation_headers)
        if response.status != 201:
            return False
        data1 = await response.json()
        if response.status != 201:
            return False
        return await response.json()


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.now()) + pyotp.random_hex()


class generationOtp:
    def create_otp(self, phone):
        keygen = pyotp.random_hex()
        key = base64.b32encode(keygen.encode())
        self.totp = pyotp.TOTP(key, interval=300)
        return self.totp.now()


sample = generationOtp()

#-----------------------------------------------------------------------------------------------

class GenerateOtpForLogin(APIView):
    serializer_class = GenerateOtpLoginSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if 'phone' in request.data:
            serializer = GenerateOtpLoginSerializer(data=request.data)
            isvalid = serializer.is_valid(raise_exception=True)
            if isvalid:
                user_obj = get_object_or_404(
                    User, phone=request.data["phone"])
                totp = sample.create_otp(user_obj.phone)
                loop = asyncio.new_event_loop()
                data = loop.run_until_complete(send_otp(user_obj.phone, totp))
                if data:
                    return Response({"Success": "user successfuly registered.", "otp": totp}, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)

class LoginWithOtp(APIView):
    serializer_class = LoginUserWithOtpSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if 'phone' not in request.data or 'otp' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoginUserWithOtpSerializer(data=request.data)
        isvalid = serializer.is_valid(raise_exception=True)
        if isvalid:
            user_obj = get_object_or_404(
                User, phone=request.data["phone"])
            if user_obj and sample.totp.verify(request.data["otp"]) and user_obj.is_register==True:
                refresh = RefreshToken.for_user(user_obj)

                return Response({'msg': 'Login Success', 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'you dont hav permision to login please register your phone '}, status=status.HTTP_200_OK)

        return Response({"message": "your field is worng."}, status=status.HTTP_400_BAD_REQUEST)

#------------------------------------------------------------------------------------------------------------------------

class GenerateOtpForActivate(APIView):
    serializer_class = GenerateOtpLoginSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if 'phone' not in request.data:
            return Response({'msg': 'phone required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GenerateOtpLoginSerializer(data=request.data)
        isvalid = serializer.is_valid(raise_exception=True)
        if isvalid:
            user_obj = get_object_or_404(
                User, phone=request.data["phone"])
            totp = sample.create_otp(user_obj.phone)
            loop = asyncio.new_event_loop()
            data = loop.run_until_complete(send_otp(user_obj.phone, totp))
            if data:
                return Response({"Success": "user successfuly registered.", "otp": totp}, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)

class ActivateUserPhone(APIView):

    serializer_class = LoginUserWithOtpSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        if 'phone' not in request.data or 'otp' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
            print('faz1')
        user = get_object_or_404(User, phone=request.data["phone"])
        try:
            if sample.totp.verify(request.data["otp"]):

                user_obj = get_object_or_404(User, phone=user.phone)
                if user_obj.is_register:
                    return Response({'msg': 'user already registered'}, status=status.HTTP_403_FORBIDDEN)
                user_obj.is_register = True
                user_obj.save()
                return Response({'msg': 'user successfuly registered'}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'OTP Wrong !'}, status=status.HTTP_400_BAD_REQUEST)