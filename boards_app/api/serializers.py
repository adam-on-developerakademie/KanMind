from rest_framework import serializers
from boards_app.models import Board
from auth_app.api.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class BoardListSerializer(serializers.ModelSerializer):
    """
    Serializer for board list (GET /api/boards/)
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
    Serializer for board details (GET /api/boards/{id}/)
    """
    members = UserSerializer(many=True, read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']
    
    def get_tasks(self, obj):
        """Tasks with details for board"""
        from tasks_app.api.serializers import TaskSerializer
        tasks = obj.tasks.all()
        return TaskSerializer(tasks, many=True).data

class BoardCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for board creation and updating
    """
    members = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    # Read-only fields for the response
    member_count = serializers.IntegerField(read_only=True)
    ticket_count = serializers.IntegerField(read_only=True) 
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'member_count', 'ticket_count', 
                 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id']
    
    def create(self, validated_data):
        """Create board with members"""
        members_ids = validated_data.pop('members', [])
        
        # Owner is set from request user
        validated_data['owner'] = self.context['request'].user
        
        board = Board.objects.create(**validated_data)
        
        # Add members
        if members_ids:
            members = User.objects.filter(id__in=members_ids)
            board.members.set(members)
        
        return board
    
    def update(self, instance, validated_data):
        """Update board"""
        members_ids = validated_data.pop('members', None)
        
        # Update title
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        
        # Update members
        if members_ids is not None:
            members = User.objects.filter(id__in=members_ids)
            instance.members.set(members)
        
        return instance


class BoardUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for board updates (PATCH/PUT) with complete user data
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
    
    def update(self, instance, validated_data):
        """Update board"""
        members_ids = validated_data.pop('members', None)
        
        # Update title
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        
        # Update members
        if members_ids is not None:
            members = User.objects.filter(id__in=members_ids)
            instance.members.set(members)
        
        return instance
