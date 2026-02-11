from rest_framework import serializers
from boards_app.models import Board
from auth_app.api.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class BoardListSerializer(serializers.ModelSerializer):
    """
    Serializer für Board-Liste (GET /api/boards/)
    """
    member_count = serializers.IntegerField(read_only=True)
    ticket_count = serializers.IntegerField(read_only=True) 
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 
                 'tasks_high_prio_count', 'owner_id']

class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Serializer für Board-Details (GET /api/boards/{id}/)
    """
    members = UserSerializer(many=True, read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']
    
    def get_tasks(self, obj):
        """Tasks mit Details für Board"""
        from tasks_app.api.serializers import TaskSerializer
        tasks = obj.tasks.all()
        return TaskSerializer(tasks, many=True).data

class BoardCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer für Board-Erstellung und -Aktualisierung
    """
    members = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    owner_data = UserSerializer(source='owner', read_only=True)
    members_data = UserSerializer(source='members', many=True, read_only=True)
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'owner_data', 'members_data']
    
    def create(self, validated_data):
        """Board erstellen mit Mitgliedern"""
        members_ids = validated_data.pop('members', [])
        
        # Owner wird aus dem Request-User gesetzt
        validated_data['owner'] = self.context['request'].user
        
        board = Board.objects.create(**validated_data)
        
        # Mitglieder hinzufügen
        if members_ids:
            members = User.objects.filter(id__in=members_ids)
            board.members.set(members)
        
        return board
    
    def update(self, instance, validated_data):
        """Board aktualisieren"""
        members_ids = validated_data.pop('members', None)
        
        # Titel aktualisieren
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        
        # Mitglieder aktualisieren
        if members_ids is not None:
            members = User.objects.filter(id__in=members_ids)
            instance.members.set(members)
        
        return instance
    
