from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool (request.user.is_superuser)
        
        
class IsReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self,  request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            print(permissions.SAFE_METHODS)
            return True
        else:
            return obj.review_user == obj.review_user or request.user.superuser
            #return obj.review_user == request.user or request.user.is_superuser  #is_staff
        