from rest_framework import serializers
from tasks_app.models import Task, Comment
from auth_app.api.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for task display
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
    Serializer for task creation and updating
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
        """Validation of task data"""
        board = attrs.get('board')
        
        # Validate assignee
        assignee_id = attrs.get('assignee_id')
        if assignee_id:
            try:
                assignee = User.objects.get(id=assignee_id)
                if not (board.members.filter(id=assignee.id).exists() or board.owner == assignee):
                    raise serializers.ValidationError(
                        {'assignee_id': 'Assignee must be a member of the board.'}
                    )
                attrs['assignee'] = assignee
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {'assignee_id': 'Assignee does not exist.'}
                )
        
        # Validate reviewer
        reviewer_id = attrs.get('reviewer_id')
        if reviewer_id:
            try:
                reviewer = User.objects.get(id=reviewer_id)
                if not (board.members.filter(id=reviewer.id).exists() or board.owner == reviewer):
                    raise serializers.ValidationError(
                        {'reviewer_id': 'Reviewer must be a member of the board.'}
                    )
                attrs['reviewer'] = reviewer
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {'reviewer_id': 'Reviewer does not exist.'}
                )
        
        return attrs
    
    def create(self, validated_data):
        """Create task"""
        # Set assignee and reviewer from IDs
        validated_data.pop('assignee_id', None)
        validated_data.pop('reviewer_id', None)
        
        # Created_by setzen
        validated_data['created_by'] = self.context['request'].user
        
        return Task.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Update task"""
        # Board ID cannot be changed
        validated_data.pop('board', None)
        validated_data.pop('assignee_id', None)
        validated_data.pop('reviewer_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments
    """
    author = serializers.CharField(source='author.fullname', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
    
    def create(self, validated_data):
        """Create comment"""
        validated_data['author'] = self.context['request'].user
        return Comment.objects.create(**validated_data)
    
