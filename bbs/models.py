from django.db import models

# Create your models here.
class Topic(models.Model):

	class Meta:
		db_table = "topic"

	comment		= models.CharField(verbose_name="comment", max_length=2000)

	def __str__(self):
		return self.comment
