# TODO: Add Delete Button to User List

- [ ] Create `confirm_delete_user.html` template based on `confirm_delete.html`, adapted for users
- [ ] Add `delete_user` view in `views.py` with `@admin_manager_required` decorator
- [ ] Add URL `path('users/delete/<int:pk>/', views.delete_user, name='delete_user')` in `urls.py`
- [ ] Edit `userlist.html`: Fix header to "Email", add "Actions" column, change `<th>` to `<td>` in tbody, add delete button
