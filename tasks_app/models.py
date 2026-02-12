from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


User = get_user_model()

class Task(models.Model):
    """
    Task Model for tasks in boards
    """
    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    board = models.ForeignKey(
        'boards_app.Board',
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="Board"
    )
    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='to-do',
        verbose_name="Status"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name="Priorität"
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name="Zugewiesener Bearbeiter"
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewing_tasks',
        verbose_name="Reviewer"
    )
    due_date = models.DateField(null=True, blank=True, verbose_name="Fälligkeitsdatum")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name="Erstellt von"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    
    class Meta:
        verbose_name = "Aufgabe"
        verbose_name_plural = "Aufgaben"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.board.title})"
    
    @property
    def comments_count(self):
        """Number of comments"""
        return self.comments.count()

class Comment(models.Model):
    """
    Comment Model for task comments
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Task"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Autor"
    )
    content = models.TextField(verbose_name="Inhalt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    
    class Meta:
        verbose_name = "Kommentar"
        verbose_name_plural = "Kommentare"
        ordering = ['created_at']
    
    def __str__(self):
        return f"Kommentar von {self.author.fullname} zu {self.task.title}"
    
