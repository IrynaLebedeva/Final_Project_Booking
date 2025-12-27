from rest_framework.permissions import BasePermission


class IsLandlord(BasePermission):
    message = 'Only landlords are allowed.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'landlord'
        )


class IsHost(BasePermission):
    message = 'Only hosts are allowed.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'host'
        )


class IsGuest(BasePermission):
    message = 'Only guests are allowed.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'guest'
        )


class IsHostOrLandlord(BasePermission):
    message = 'Only host or landlord can create listings.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['host', 'landlord']

class IsReviewOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
