from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm,PasswordChangeForm,UserRegistrationForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from django.contrib import messages
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password']                                
                                )
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
                    
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request,'account/login.html',{'form':form}) 
    
#def user_logout(request):
#    print(request.method)
#    logout(request) 
#    return render(request,'registration/logged_out.html') 
    

                  
def password_change(request):
    if not request.user.is_authenticated(): 
        return HttpResponseRedirect(reverse("loginerror")) 
    template = {} 
    form = PasswordChangeForm()     
    if request.method=="POST": 
        form = PasswordChangeForm(request.POST.copy()) 
        if form.is_valid(): 
            username = request.user.username 
            oldpassword = form.cleaned_data["old_password"] 
            newpassword = form.cleaned_data["new_password1"] 
            newpassword1 = form.cleaned_data["new_password2"] 
            user = authenticate(username=username,password=oldpassword) 
            if user: #原口令正确 
                if newpassword == newpassword1:#两次新口令一致 
                    user.set_password(newpassword) 
                    user.save() 
                    print('1')
                    return HttpResponseRedirect("/account/password-change/done/")     
                else:#两次新口令不一致 
                    template["word"] = '两次输入口令不一致'   
                    template["form"] = form 
                    print('2') 
                    return render_to_response("account/password_change_form.html",template,context_instance=RequestContext(request))  
            else:  #原口令不正确 
                if newpassword == newpassword1:#两次新口令一致 
                    template["word"] = '原口令不正确'   
                    template["form"] = form 
                    print('3') 
                    return render_to_response("account/password_change_form.html",template,context_instance=RequestContext(request)) 
                else:#两次新口令不一致 
                    template["word"] = '原口令不正确，两次输入口令不一致'   
                    template["form"] = form 
                    print('4') 
                    return render_to_response("account/password_change_form.html",template,context_instance=RequestContext(request))  
    template["form"] = form         
    return render_to_response("account/password_change_form.html",template,context_instance=RequestContext(request)) 
    
def password_change_done(request):
    return render(request,"account/password_change_done.html")    
    
@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section':'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yer
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']            
            )
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request,'account/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form':user_form}
    )
    
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files = request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile updated successfully')
        else:
            messages.error(request,'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})
    
                                       


















































