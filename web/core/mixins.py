from django.http import Http404


class IsOwnerMixin(object):
    """Ensures the current user owns the item."""

    def _get_owner(self, obj):
        """Checks for different types of 'owners',
        returns the one that exists."""
        if hasattr(obj, 'creator'):
            return obj.creator
        if hasattr(obj, 'owner'):
            return obj.owner
        if hasattr(obj, 'user'):
            return obj.user
        return None

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self._get_owner(obj)

        if user != self.request.user:
            raise Http404()
        return super(IsOwnerMixin, self).dispatch(request, *args, **kwargs)
