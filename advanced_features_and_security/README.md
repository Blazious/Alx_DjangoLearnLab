# Permissions and Groups System

This document outlines the permissions and groups system implemented in the Library Project.

## Custom Permissions

The system implements the following custom permissions on the Book model:

- `can_view`: Permission to view book details
- `can_create`: Permission to create new books
- `can_edit`: Permission to edit existing books
- `can_delete`: Permission to delete books

## User Groups

Three user groups are defined with specific permissions:

1. **Viewers**
   - Permissions: `can_view`
   - Can only view book information

2. **Editors**
   - Permissions: `can_view`, `can_create`, `can_edit`
   - Can view, create, and edit books
   - Cannot delete books

3. **Admins**
   - Permissions: `can_view`, `can_create`, `can_edit`, `can_delete`
   - Full access to all book operations

## Implementation Details

### Models

The permissions are defined in the Book model's Meta class:

```python
class Meta:
    permissions = [
        ("can_view", "Can view books"),
        ("can_create", "Can create books"),
        ("can_edit", "Can edit books"),
        ("can_delete", "Can delete books"),
    ]
```

### Views

All views are protected with the `@permission_required` decorator:

```python
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # View implementation
```

### Groups

Groups are created and permissions are assigned through a migration:

```python
# migrations/0002_create_groups_and_permissions.py
```

## Usage

To assign a user to a group:

1. Access the Django admin interface
2. Go to Users
3. Select a user
4. In the Groups section, assign the appropriate group

## Security Notes

- Users without proper permissions will receive a 403 Forbidden response
- All views are protected with permission checks
- Group permissions are additive (users in multiple groups get all permissions)