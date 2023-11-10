from django.db import models

# Create your models here.
class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    who = models.CharField(max_length=100)
    action_type = models.CharField(max_length=100)
    object_type = models.CharField(max_length=100)
    object_id = models.IntegerField()


    def to_json(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "who": self.who,
            "action_type": self.action_type,
            "object_type": self.object_type,
            "object_id": self.object_id,
        }