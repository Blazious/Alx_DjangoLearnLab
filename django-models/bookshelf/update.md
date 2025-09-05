
## 📂 `update.md`

```markdown
# Update Operation

```python
from bookshelf.models import Book

# Get the existing book
book = Book.objects.get(title="1984")

# Update its title
book.title = "Nineteen Eighty-Four"
book.save()

book.title
# 'Nineteen Eighty-Four'