from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_groups_and_permissions(apps, schema_editor):
    # Get the content type for the Book model
    Book = apps.get_model('bookshelf', 'Book')
    book_content_type = ContentType.objects.get_for_model(Book)
    
    # Create permissions (they should already exist from model definition)
    permissions = {
        'can_view': Permission.objects.get(codename='can_view', content_type=book_content_type),
        'can_create': Permission.objects.get(codename='can_create', content_type=book_content_type),
        'can_edit': Permission.objects.get(codename='can_edit', content_type=book_content_type),
        'can_delete': Permission.objects.get(codename='can_delete', content_type=book_content_type),
    }
    
    # Create Viewers group
    viewers_group, _ = Group.objects.get_or_create(name='Viewers')
    viewers_group.permissions.add(permissions['can_view'])
    
    # Create Editors group
    editors_group, _ = Group.objects.get_or_create(name='Editors')
    editors_group.permissions.add(
        permissions['can_view'],
        permissions['can_create'],
        permissions['can_edit']
    )
    
    # Create Admins group
    admins_group, _ = Group.objects.get_or_create(name='Admins')
    admins_group.permissions.add(
        permissions['can_view'],
        permissions['can_create'],
        permissions['can_edit'],
        permissions['can_delete']
    )

class Migration(migrations.Migration):
    dependencies = [
        ('bookshelf', '0001_initial'),  # Update this to match your last migration
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions),
    ]