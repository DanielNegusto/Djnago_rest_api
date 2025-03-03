from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview_image = models.ImageField(upload_to="courses/previews/")
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview_image = models.ImageField(upload_to="lessons/previews/")
    video_link = models.URLField()

    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "course")
