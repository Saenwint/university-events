from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from events.models import Event
from analytics.models import EventStats
from tickets.models import Ticket
from users.models import User

class Command(BaseCommand):
    help = 'Generates test data for events and statistics'

    def handle(self, *args, **options):
        # Создаем тестовых пользователей
        users = []
        for i in range(1, 21):
            user = User.objects.create(
                first_name=f'User{i}',
                last_name=f'Test{i}',
                email=f'user{i}@test.com',
                is_confirmed=True
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.email}'))

        # Создаем прошедшие мероприятия с разными типами деятельности
        past_events = []
        activity_types = [choice[0] for choice in Event.ACTIVITY_TYPES]
        
        for i, activity_type in enumerate(activity_types[:5]):  # Создаем 5 мероприятий
            event = Event.objects.create(
                title=f'Прошедшее мероприятие {i+1} ({activity_type})',
                short_description=f'Тестовое мероприятие {i+1}',
                full_description='Полное описание тестового мероприятия',
                target_audience='Студенты',
                date=timezone.now() - timedelta(days=random.randint(1, 30)),
                location='Аудитория 101',
                coins_reward=random.randint(10, 50),
                type=random.choice([choice[0] for choice in Event.EVENT_TYPES]),
                significance_level=random.choice(['normal', 'epic', 'legendary']),
                organizer='Тестовая организация',
                activity_type=activity_type
            )
            past_events.append(event)
            self.stdout.write(self.style.SUCCESS(f'Created past event: {event.title}'))

        # Создаем билеты и статистику для прошедших мероприятий
        for event in past_events:
            # Случайное количество регистраций (10-20)
            num_registrations = random.randint(10, 20)
            registered_users = random.sample(users, num_registrations)
            
            # Создаем билеты
            for user in registered_users:
                ticket = Ticket.objects.create(
                    user=user,
                    event=event,
                    is_used=random.choice([True, False])  # Примерно 50% посетили
                )
                if ticket.is_used:
                    ticket.mark_as_used()  # Обновляем статистику использования
            
            # Создаем статистику мероприятия
            stats = EventStats.objects.create(
                event=event,
                period='all',
                total_registered=num_registrations,
                total_attended=Ticket.objects.filter(event=event, is_used=True).count()
            )
            self.stdout.write(self.style.SUCCESS(
                f'Stats for {event.title}: '
                f'{stats.total_attended}/{stats.total_registered} attended'
            ))

        self.stdout.write(self.style.SUCCESS('Successfully generated test data'))