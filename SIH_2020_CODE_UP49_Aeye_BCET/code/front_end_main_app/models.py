from django.db import models

# Create your models here.
class dbms1(models.Model):
    pt_id=models.CharField(max_length=100)
    pt_name=models.CharField(max_length=100)
    pt_output=models.CharField(max_length=100)
    created_at = models.DateTimeField()

    class Meta:
        db_table="result_ml"