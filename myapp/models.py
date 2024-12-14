from django.db import models

class ProcessData(models.Model):
    system_name = models.CharField(max_length=255)
    process_name = models.CharField(max_length=255, null=True, blank=True)  # Allow empty or None
    username = models.CharField(max_length=255, null=True, blank=True)  # Allow empty or None
    pid = models.IntegerField()
    create_time = models.DateTimeField()
    timestamp = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['system_name', 'timestamp']),
            models.Index(fields=['pid']),
        ]

    def __str__(self):
        return f"{self.system_name} - {self.process_name} ({self.pid})"



