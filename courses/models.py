from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview_image = models.ImageField(upload_to='courses/previews/')
    description = models.TextField()

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='lessons/previews/')
    video_link = models.URLField()

    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
