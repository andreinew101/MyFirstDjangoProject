# Patch Django to allow older MariaDB versions
import django.db.backends.base.base as django_base

original_check = django_base.BaseDatabaseWrapper.check_database_version_supported

def patched_check(self):
    """Skip version check for older MariaDB/MySQL versions"""
    # Comment out the original check
    pass

# Apply the patch
django_base.BaseDatabaseWrapper.check_database_version_supported = patched_check
