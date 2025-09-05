## 📂 `CRUD_operations.md`

This is just a **combined file** with all operations in one place:

```markdown
# CRUD Operations on Book Model

## Create
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# <Book: 1984 by George Orwell (1949)>