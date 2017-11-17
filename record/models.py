from django.db import models
import uuid

# Create your models here.


class PomeloIndex(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    symbol = models.CharField(max_length=5, default=None)
    description = models.CharField(max_length=512,default=None)
    def __str__(self):
        return self.symbol

class PomeloSubIndex(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    pomelo_index = models.ForeignKey(
        PomeloIndex,
        on_delete=models.CASCADE,
        default=None
    )
    sub_symbol = models.CharField(max_length=5, default=None)
    def __str__(self):
        return self.sub_symbol

class GeneralData(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    pomelo_index = models.ForeignKey(
        PomeloIndex,
        on_delete=models.CASCADE,
        default=None
    )
    temp = models.FloatField(default=None)
    weight = models.FloatField(default=None)
    circum = models.FloatField(default=None)
    date = models.DateField(auto_now=False, auto_now_add=False)
    def __str__(self):
        return self.pomelo_index

class Information(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    pomelo_sub_index = models.ForeignKey(
        PomeloSubIndex,
        on_delete=models.CASCADE,
        default=None
    )
    l = models.FloatField(default=0)
    a = models.FloatField(default=0)
    b = models.FloatField(default=0)
    # gar = gland area ratio
    gar = models.FloatField(default=0)
    picture_name = models.CharField(max_length=64,default=None)
    
    def __str__(self):
        return self.pomelo_sub_index
