from django.http import HttpResponse
from django.shortcuts import redirect
from operator import attrgetter


def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('profile')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group_names = set([])
			if request.user.groups.exists():
				all_groups = request.user.groups.all()
				group_names = set([group.name for group in all_groups])
			if len(group_names.intersection(allowed_roles)) > 0:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator
