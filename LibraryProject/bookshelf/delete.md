## 📂 `delete.md`

```markdown
# Delete Operation

```python
from bookshelf.models import Book

# Get the book again
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete it
book.delete()
# (1, {'bookshelf.Book': 1})

# Confirm deletion
Book.objects.all()
# <QuerySet []>