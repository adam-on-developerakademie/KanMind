from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer für Benutzerregistrierung
    """
    password = serializers.CharField(write_only=True, min_length=8)
    repeated_password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password', 'token', 'user_id']
    
    def validate(self, attrs):
        """Validierung für Passwort-Wiederholung"""
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError("Passwörter stimmen nicht überein.")
        return attrs
    
    def create(self, validated_data):
        """Erstelle neuen Benutzer mit Token"""
        validated_data.pop('repeated_password')
        
        # Username automatisch aus E-Mail generieren
        validated_data['username'] = validated_data['email']
        
        user = User.objects.create_user(**validated_data)
        
        # Token erstellen
        token, created = Token.objects.get_or_create(user=user)
        user.token = token.key
        
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer für Benutzeranmeldung
    """
    email = serializers.EmailField()
    password = serializers.CharField()
    token = serializers.CharField(read_only=True)
    fullname = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    
    def validate(self, attrs):
        """Validierung der Login-Daten"""
        email, password = self._extract_credentials(attrs)
        user = self._authenticate_user(email, password)
        self._check_user_status(user)
        return self._prepare_response_data(attrs, user)
    
    def _extract_credentials(self, attrs):
        """Extrahiere und validiere Credentials"""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if not email or not password:
            raise serializers.ValidationError("E-Mail und Passwort sind erforderlich.")
        
        return email, password
    
    def _authenticate_user(self, email, password):
        """Authentifiziere Benutzer über E-Mail"""
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            raise serializers.ValidationError("Ungültige Anmeldedaten.")
        
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Ungültige Anmeldedaten.")
        
        return user
    
    def _check_user_status(self, user):
        """Prüfe ob Benutzer aktiv ist"""
        if not user.is_active:
            raise serializers.ValidationError("Benutzerkonto ist deaktiviert.")
    
    def _prepare_response_data(self, attrs, user):
        """Bereite Response-Daten mit Token vor"""
        token, created = Token.objects.get_or_create(user=user)
        
        attrs['user'] = user
        attrs['token'] = token.key
        attrs['fullname'] = user.fullname
        attrs['user_id'] = user.id
        
        return attrs

class UserSerializer(serializers.ModelSerializer):
    """
    Einfacher User Serializer für API-Responses
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']
