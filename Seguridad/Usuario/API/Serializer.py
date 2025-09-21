from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from Seguridad.Usuario.models import Usuario

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        # Se añaden 'is_staff' y 'is_superuser' a la lista de campos.
        # Esto permite que el serializador los acepte en las solicitudes de creación.
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')

    # Valida que ambas contraseñas coincidan
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    # Se sobrescribe el método 'create' para manejar los nuevos campos.
    def create(self, validated_data):
        # Se extraen los campos 'is_staff' y 'is_superuser' del diccionario
        # 'validated_data' usando .pop(). Esto es crucial para que no causen
        # un error al crear la instancia del usuario. Si no se proporcionan en la solicitud,
        # el valor por defecto será False.
        is_staff = validated_data.pop('is_staff', False)
        is_superuser = validated_data.pop('is_superuser', False)

        # Se crea la instancia del usuario con los datos restantes.
        usuario = Usuario(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            # Se asignan los valores de 'is_staff' y 'is_superuser' al nuevo usuario.
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        
        usuario.set_password(validated_data['password'])  # Encripta la contraseña
        usuario.save()
        return usuario
    
# Seguridad/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Llama al método del serializador padre para obtener el token por defecto.
        token = super().get_token(user)

        # Añade la propiedad 'is_superuser' al payload del token.
        token['is_superuser'] = user.is_superuser

        return token