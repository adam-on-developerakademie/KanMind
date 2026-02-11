from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


User = get_user_model()

class Board(models.Model):
    """
    Board Model für Kanban-Boards
    """
    title = models.CharField(max_length=200, verbose_name="Titel")
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="owned_boards",
        verbose_name="Besitzer"
    )
    members = models.ManyToManyField(
        User,
        related_name="board_memberships",
        blank=True,
        verbose_name="Mitglieder"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    
    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def member_count(self):
        """Anzahl der Mitglieder"""
        return self.members.count()
    
    @property
    def ticket_count(self):
        """Gesamtanzahl der Tasks"""
        return self.tasks.count()
    
    @property
    def tasks_to_do_count(self):
        """Anzahl der To-Do Tasks"""
        return self.tasks.filter(status='to-do').count()
    
    @property
    def tasks_high_prio_count(self):
        """Anzahl der High-Priority Tasks"""
        return self.tasks.filter(priority='high').count()
