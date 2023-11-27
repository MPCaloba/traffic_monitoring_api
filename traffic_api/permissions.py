from rest_framework.permissions import BasePermission, SAFE_METHODS

# Global permission check for the presence of a valid API key.
class HasAPIKey(BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-KEY')
        expected_api_key = '23231c7a-80a7-4810-93b3-98a18ecfbc42'

        #print(f"api_key: {api_key}")
        #print(f"expected_api_key: {expected_api_key}")

        return api_key == expected_api_key

# Class to allow admin users to perform any action, while it allows all other users to perform read-only actions
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access to all users
        if request.method in SAFE_METHODS:
            return True

        # Allow admin users to perform any action
        return request.user and request.user.is_staff

# Class to allow read-only actions to all users, including anonymous users
class IsAnonymousReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access to all users
        if request.method in SAFE_METHODS:
            return True
        return False