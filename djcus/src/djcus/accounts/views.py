from django.shortcuts import render
from .forms import UserCreationForm, LoginUser, ProfileForm
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import get_user_model, login, logout
from .models import MyUser, Profile, ActivationProfile
from django.shortcuts import redirect
# from django.Http import HttpResponseRedirect
# Create your views here.

User=get_user_model()


# def register(request):
# 	if request.method == "POST":
# 		form  = UserCreationForm(request.POST or None)
# 		if form.is_valid():
# 			form.save()
# 		temp_path = "blog/accounts.html"
# 		context = {"form": form }
#     return render(request,temp_path,context)

def home(request):
	temp_path = "blog/home.html"
	context = {}
	print(request.user.username)
	return render(request, temp_path, context)


def register(request):
	form = UserCreationForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)
		form.save()
		form =UserCreationForm()
		return HttpResponseRedirect("/login")
	temp_path = "blog/accounts.html"
	context={
	  "form":form
	}
	return render(request,temp_path,context)


# def user_login(request):
# 	form  = LoginUser(request.POST or None)
# 	if form.is_valid():
# 		#form.save()
# 		username = form.cleaned_data.get("username")
# 		user_obj = User.objects.get(username_iexact=username)
#         login(request,user_obj)
# 		return HttpResponseRedirect("/home")
# 	temp_path = 'blog/login.html'
# 	context = {
# 	   "form":form
# 	}
# 	return render(request,temp_path,context)	
def profile_view(request):
	form = ProfileForm(request.POST or None)
	if form.is_valid():
		form.save()
		form.ProfileForm()
	temp_path ="blog/profile.html"
	context = {
		"form":form
	}
	return render(request,temp_path,context)



def user_login(request):
	form = LoginUser(request.POST or None)
	if form.is_valid():
		user_obj = form.cleaned_data.get("user_obj") # Taking value from field to whom you login
		# user_obj = User.objects.get(username__iexact=query) #This user can login to admin dashboard
		#This get() method takes query set values
		login(request,user_obj)  #This allow user to login to admin dashboard
		form = LoginUser()       #clear the form after save
		return HttpResponseRedirect("/home")
	temp_path = 'blog/login.html'
	context = {
		"form":form
	}
	return render(request,temp_path,context)

def user_logout(request):
	logout(request)   #This allow user to logout from admin dashboard
	return HttpResponseRedirect("/login")

def activate_user_view(request,code=None,*args,**kwargs):
	if code:
		act_profile_qs = ActivationProfile.objects.filter(key=code) # It access all old and new column value
		print("Fetch data is:",act_profile_qs)
		if act_profile_qs.exists() and act_profile_qs.count() ==1:
			act_obj = act_profile_qs.first() # This will return recent or perfect matching
			print("After first method",act_obj)	
			if not act_obj.exp:
				user_obj1 = act_obj.user
				# print("status of exp before",user_obj1.exp)
				user_obj1.exp = True
				# print("status of exp after",user_obj1.exp)
				user_obj1.save()
				print("expired end")
				user_obj1.is_active = True
				user_obj1.save()
				return HttpResponseRedirect("/login")
	return HttpResponseRedirect('/login')