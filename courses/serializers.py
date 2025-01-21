from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(required=False, validators=[validate_video_url])
    course = serializers.PrimaryKeyRelatedField(required=False, queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ['id', 'owner', 'title', 'description', 'video_link', 'course']

    def create(self, validated_data):
        return Lesson.objects.create(**validated_data)

    def update(self, instance, validated_data):
        course = validated_data.pop('course', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if course is not None:
            instance.course = course

        instance.save()
        return instance


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'owner', 'title', 'description', 'lessons', 'lesson_count', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    def get_lesson_count(self, obj):
        return obj.lessons.count()



