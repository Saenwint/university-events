import os
import secrets
from django.db import connection
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from datetime import datetime, timedelta

from tickets.models import Ticket
from events.models import Event
from users.models import User 


def reset_autoincrement(model):
    with connection.cursor() as cursor:
        table_name = model._meta.db_table
        cursor.execute(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1;")

class Command(BaseCommand):
    help = 'Fill the database with initial users data'

    def handle(self, *args, **options):
        reset_autoincrement(User)
        fake = Faker('ru_RU')
        
        admin_data = settings.ADMIN_LIST[0]
        if not User.objects.filter(email=admin_data).exists():
            User.objects.create_superuser(
                email=admin_data,
                password=settings.ADMIN_PASS,
                first_name='Александр',
                last_name='Дудин',
                is_admin=True,
                is_staff=True,
                is_confirmed=True,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin: {admin_data}'))
        
        for i in range(30):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f'user{i}@example.com'
            
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    email=email,
                    password='defaultpassword',
                    first_name=first_name,
                    last_name=last_name,
                    is_admin=False,
                    is_staff=False,
                    is_confirmed=True,
                    is_active=True
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully filled the database with users'))

        reset_autoincrement(Event)
        fake = Faker('ru_RU')
        
        images_dir = os.path.join(settings.BASE_DIR, 'analytics', 'management', 'commands', 'media', 'events')
        
        if not os.path.exists(images_dir):
            self.stdout.write(self.style.ERROR(f'Directory {images_dir} does not exist'))
            return
        
        image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            self.stdout.write(self.style.ERROR('No image files found in the directory'))
            return
        
        for i in range(10):
            image_file = image_files[i % len(image_files)]
            image_path = os.path.join(images_dir, image_file)
            
            event = Event(
                title=fake.sentence(nb_words=4),
                short_description=fake.text(max_nb_chars=300),
                full_description=fake.text(max_nb_chars=1000),
                target_audience="Студенты, преподаватели",
                date=datetime.now() + timedelta(days=(i*3) - 9),
                location=fake.address(),
                coins_reward=fake.random_int(min=0, max=10),
                type=fake.random_element(Event.EVENT_TYPES)[0],
                significance_level=fake.random_element(Event.SIGNIFICANCE_LEVELS)[0],
                organizer=fake.company(),
                activity_type=fake.random_element(Event.ACTIVITY_TYPES)[0],
            )
            
            with open(image_path, 'rb') as img:
                event.image.save(image_file, img, save=True)
            
            self.stdout.write(self.style.SUCCESS(f'Created event: {event.title} with image {image_file}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully created events with images'))

        reset_autoincrement(Ticket)
        event_ids = range(1, 10)
        user_ids = range(1, 30)
        
        created_count = 0
        
        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'User with id {user_id} does not exist'))
                continue
                
            # Выбираем 5 случайных мероприятий для пользователя
            selected_events = Event.objects.filter(id__in=event_ids).order_by('?')[:5]
            
            if not selected_events:
                self.stdout.write(self.style.WARNING('No events found in specified range'))
                continue
                
            for i, event in enumerate(selected_events):
                # Для первых 2 билетов устанавливаем is_used=True
                is_used = i < 2
                used_at = datetime.now() - timedelta(days=1) if is_used else None
                
                ticket = Ticket(
                    user=user,
                    event=event,
                    is_used=is_used,
                    used_at=used_at,
                    # qr_code_image останется None (не создаем)
                )
                
                # Генерируем unique_code перед сохранением
                ticket.unique_code = f"EV-{event.id}-US-{user.id}-{secrets.token_urlsafe(8)}"
                ticket.save()
                created_count += 1
                
                self.stdout.write(self.style.SUCCESS(
                    f'Created ticket for user {user.id} on event {event.id} (used: {is_used})'
                ))
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {created_count} tickets for {len(user_ids)} users'
        ))