# Bookshelf App – Permissions & Groups

## Custom Permissions (in `Book` model)
- `can_view` → allows viewing books.
- `can_create` → allows adding new books.
- `can_edit` → allows editing existing books.
- `can_delete` → allows deleting books.

## Groups
Configured in Django Admin:
- **Readers** → `can_view`
- **Librarians** → `can_view`, `can_create`, `can_edit`
- **Managers** → all permissions

## Views
Protected with `@permission_required`:
- `book_list` → `can_view`
- `book_create` → `can_create`
- `book_edit` → `can_edit`
- `book_delete` → `can_delete`

## Testing
1. Create test users.
2. Assign them to different groups.
3. Log in and verify access:
   - Readers → only view.
   - Librarians → view, create, edit.
   - Managers → all.
