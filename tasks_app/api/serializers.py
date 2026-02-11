from rest_framework import serializers
from tasks_app.models import Task, Comment
from auth_app.api.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer für Task-Darstellung
    """
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                 'assignee', 'reviewer', 'due_date', 'comments_count']

class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer für Task-Erstellung und -Aktualisierung
    """
    assignee_id = serializers.IntegerField(required=False, allow_null=True)
    reviewer_id = serializers.IntegerField(required=False, allow_null=True)
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                 'assignee_id', 'reviewer_id', 'assignee', 'reviewer', 'due_date', 'comments_count']
    
    def validate(self, attrs):
        """Validierung der Task-Daten"""
        # Board-Zugehörigkeit prüfen bei Assignee und Reviewer
        board = attrs.get('board')
        assignee_id = attrs.get('assignee_id')
        reviewer_id = attrs.get('reviewer_id')
        
        if assignee_id:
            try:
                assignee = User.objects.get(id=assignee_id)
                if not board.members.filter(id=assignee_id).exists() and board.owner != assignee:
                    raise serializers.ValidationError("Assignee muss Mitglied des Boards sein.")
                attrs['assignee'] = assignee
            except User.DoesNotExist:
                raise serializers.ValidationError("Assignee existiert nicht.")
        
        if reviewer_id:
            try:
                reviewer = User.objects.get(id=reviewer_id)
                if not board.members.filter(id=reviewer_id).exists() and board.owner != reviewer:
                    raise serializers.ValidationError("Reviewer muss Mitglied des Boards sein.")
                attrs['reviewer'] = reviewer
            except User.DoesNotExist:
                raise serializers.ValidationError("Reviewer existiert nicht.")
        
        return attrs
    
    def create(self, validated_data):
        """Task erstellen"""
        # Assignee und Reviewer aus IDs setzen
        validated_data.pop('assignee_id', None)
        validated_data.pop('reviewer_id', None)
        
        # Created_by setzen
        validated_data['created_by'] = self.context['request'].user
        
        return Task.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Task aktualisieren"""
        # Board-ID darf nicht geändert werden
        validated_data.pop('board', None)
        validated_data.pop('assignee_id', None)
        validated_data.pop('reviewer_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer für Kommentare
    """
    author = serializers.CharField(source='author.fullname', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
    
    def create(self, validated_data):
        """Kommentar erstellen"""
        validated_data['author'] = self.context['request'].user
        return Comment.objects.create(**validated_data)
    
