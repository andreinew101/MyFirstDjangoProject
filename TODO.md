# TODO: Restrict Access to "Add user" and "user list" pages

## Completed Tasks
- [x] Add position field to SystemUser model with choices: Admin, Manager, Employee
- [x] Create @admin_manager_required decorator for access control
- [x] Apply decorator to userlist and adduser views
- [x] Update SystemUserForm to include position field
- [x] Restrict position choices in adduser view: only Admins can set Admin position
- [x] Update admin.py to include position in list_display, list_filter, and fields
- [x] Create context processor to check user position
- [x] Add context processor to settings
- [x] Hide "Add User" and "User List" links from sidebar for non-admin/manager users

## Remaining Tasks
- [ ] Test the sidebar visibility changes
