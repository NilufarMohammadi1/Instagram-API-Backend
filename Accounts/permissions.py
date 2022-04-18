from rest_framework.response import Response
from rest_framework.permissions import BasePermission

from Accounts.models import Followings, Users


class FollowsUser(BasePermission):

    def has_permission(self, request, view):
        selected_user = view.kwargs.get('pk')
        print(selected_user, request.user.id)

        if not selected_user or str(selected_user) == str(request.user.id):
            return True

        final_user = Users.objects.get(id=selected_user)

        try:
            accepted_follower = Followings.objects.get(user_dest=final_user,
                                                       user_base=request.user.id, pending=False)
            return bool(request.user.id == accepted_follower.user_base_id)
        except Exception as ex:
            # return Response({'error':'You are not allowed to access this user posts'})
            print(ex)

        return False
