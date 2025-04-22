from django.db import models
from django.core.validators import MinValueValidator


class Event(models.Model):
    SIGNIFICANCE_LEVELS = [
        ('legendary', 'Легендарный'),
        ('epic', 'Эпический'),
        ('normal', 'Обычный'),
    ]
    EVENT_TYPES = [
        ('competition', 'Соревнование'),
        ('hackathon', 'Хакатон'),
        ('meetup', 'Встреча'),
        ('lecture', 'Лекция'),
        ('workshop', 'Мастер-класс'),
        ('conference', 'Конференция'),
        ('cultural', 'Культурное мероприятие'),
        ('sport', 'Спортивное событие'),
    ]
    ACTIVITY_TYPES = [
        ('professional', 'Профессионально-ориентированная деятельность'),
        ('scientific', 'Научно-образовательная деятельность'),
        ('patriotic', 'Патриотическая и гражданско-правовая деятельность'),
        ('cultural_creative', 'Культурно-творческая деятельность'),
        ('spiritual', 'Духовно-нравственная деятельность'),
        ('sports_health', 'Физкультурно-оздоровительная деятельность и воспитание здорового образа жизни'),
        ('student_government', 'Развитие студенческого самоуправления'),
        ('volunteering', 'Поддержка и развитие волонтёрской деятельности'),
        ('ecological', 'Экологическая деятельность'),
        ('tolerance', 'Воспитание толерантности'),
    ]
    title = models.CharField(max_length=200, verbose_name='Название')
    short_description = models.TextField(max_length=300, verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание')
    image = models.ImageField(upload_to='events/images/', verbose_name='Изображение')
    target_audience = models.CharField(max_length=200, verbose_name='Для кого')
    date = models.DateTimeField(verbose_name='Дата и время')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    coins_reward = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='ЛЭТИ-коины'
    )
    type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default='meetup',
        verbose_name='Тип мероприятия'
    )
    significance_level = models.CharField(
        max_length=10,
        choices=SIGNIFICANCE_LEVELS,
        default='normal',
        verbose_name='Уровень значимости'
    )
    organizer = models.CharField(max_length=200, verbose_name='Организатор')
    organizer_link = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Ссылка на организатора'
    )
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPES,
        default='scientific',
        verbose_name='Вид деятельности'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-date']

    def get_significance_color(self):
        colors = {
            'legendary': 'linear-gradient(90deg, #ff8a00, #ffc400)',
            'epic': 'linear-gradient(90deg, #6a00f4, #a100f2)',
            'normal': 'linear-gradient(90deg, #0061ff, #00c3ff)',
        }
        return colors.get(self.significance_level, '#0061ff')