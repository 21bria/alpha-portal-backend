from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import json

class LoginSerializer(TokenObtainPairSerializer):
    """
    Login pakai username/password bawaan AbstractUser.
    Bisa kamu ubah kalau mau login via email.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Optional: taruh claim role biar FE gampang baca (tidak wajib)
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Extra info buat FE
        data["user"] = {
            "id": user.id,
            "username": user.get_username(),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": f"{user.first_name} {user.last_name}".strip() or user.get_username(),
            "role": user.role,
            "is_superuser": user.is_superuser,
            "is_system": user.is_system,
            "is_global_viewer": user.is_global_viewer,
            "is_admin_user": user.is_admin_user,
        }

        return data
