from django import forms
from .models import MyUser,Profile
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator
from .models import USERNAME_REGEX
from django.contrib.auth.models import User
from django.contrib.auth import authenticate # for username and password authentication
from django.db.models import Q

class UserCreationForm(forms.ModelForm):  # for creating the new user
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username','password1','password1','is_staff','email','is_admin','is_active')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active=False
        if commit:
            user.save()
        return user

class LoginUser(forms.Form):
    # username = forms.CharField(max_length=255, validators=[
    #                                              RegexValidator(
    #                                                    regex = USERNAME_REGEX,
    #                                                    message = 'username must be AlphaNumeric',
    #                                                    code = 'Invalid username'
    #                                                )] , 
    #                                             # unique = True,
    #                                           ) 
    query = forms.CharField(label="Username/Email",max_length=255) # getting the field
    password = forms.CharField(label="Password",widget=forms.PasswordInput)

    # username and password validation for login
    #This method fetch data from database
    def clean(self,*args,**kwargs):
        query = self.cleaned_data.get("query")
        password = self.cleaned_data.get("password") #This take query set value
        # user_qs1 = MyUser.objects.filter(username__iexact=query) # get if username
        # user_qs2 = MyUser.objects.filter(email__iexact=query)     # get if email
        # user_qs_final = (user_qs1 | user_qs2).distinct() # it combine together and avoid duplicate if it have
        # dummy1 = MyUser.objects.filter(username__iexact=query)
        # print("The dummy data for username", dummy1) # None
        # dummy2 = MyUser.objects.filter(email__iexact=query)
        # print("The dummy data for email", dummy2) #
        user_qs_final = MyUser.objects.filter( #This take specific vlaue
            Q(username__iexact=query) |       # This django @ lookup used to hit DB 
            Q(email__iexact=query)            # for multiple query only once it optimize performance
        ).distinct()
        for i in user_qs_final:
            print("The user_final data ",i) #The user_final data  rushi@gmail.com
        dum1 = MyUser.objects.filter(Q(username__iexact=query))
        dum2 = MyUser.objects.filter(Q(email__iexact=query))
        print("The username is",dum1)
        print("The email is",dum2)
        # user_obj = User.objects.get(username=username)
        # print("data is",user_obj)  # it return None if no record there
        # the_user = authenticate(username=username,password=password)
        # if not the_user:
        #     raise forms.ValidationError("Invalid credential plz correct")
        if not user_qs_final.exists() and user_qs_final.count() !=1: # cheching user exists or not
            raise forms.ValidationError("Invalid credential-- no record")
        user_obj = user_qs_final.first() #The first method means only object for 
                                         #perticular method and we already check username is exists
        # The get method will ensure that there is exactly one row in the database that matches the query.
        # The helper.first() method will silently eat all but the first matching row
        print("The data is",user_obj) #The data is rushi@gmail.com
        if not user_obj:
            raise forms.ValidationError("Invalid credential-- username error")
        else:    
            if not user_obj.check_password(password):
                raise forms.ValidationError("Invalid credential-- password error")
            if not user_obj.is_active:
                raise forms.ValidationError("Inactive user.Please verify email address")
            #This is done to varification process get done like activate your accounts
            self.cleaned_data["user_obj"]=user_obj # assign first name(data) to this new created field
            my_data = self.cleaned_data.get("user_obj")
            print("The data of my field is",my_data) # aaa@gmail.com .if you log with mail
                                                     # aaa .if you log with username
        return super(LoginUser,self).clean(*args,**kwargs)
    

    # filter the username data using clean method

    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     user_qs = MyUser.objects.filter(username=username)
    #     user_exists=user_qs.exists()
    #     if not user_exists and user_qs.count()!=1: # user not exits and it count to zero
    #         forms.ValidationError("Invalid credential--username error")
    #     return username
class ProfileForm(forms.ModelForm):  # for creating the new user
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('user','city','content','integer')

class UserChangeForm(forms.ModelForm):          # for chaning the user form
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username','email', 'password', 'is_staff', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

