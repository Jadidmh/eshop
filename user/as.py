class RegisterAPI(generics.CreateAPIView):
    model = CustomUser

    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        if request.data["password"] == request.data["password2"]:
            if "phone" in request.data and "email" in request.data and "city" in request.data:
                serializer = self.get_serializer(data=request.data)
                isvalid = serializer.is_valid(raise_exception=True)
                if isvalid:
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)

                    totp = sample.create_otp(serializer.data["phone"])
                    loop = asyncio.new_event_loop()
                    data = loop.run_until_complete(
                        send_otp(serializer.data["phone"], totp))
                    if data:
                        return Response({"Success": "user successfuly saved.", "otp": totp}, status=status.HTTP_201_CREATED, headers=headers)
                    else:
                        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({"message": "your field is worng."}, status=status.HTTP_400_BAD_REQUEST)
