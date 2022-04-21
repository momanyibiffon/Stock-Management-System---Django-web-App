from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from .forms import EditProfileForm, RegistrationForm, ProfileForm
# to ensure the user remains logged in even after changing the password
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .decorators import unauthenticated_user
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# @unauthenticated_user
@login_required
def signup_view(request):
    title = "New User"
    template = "accounts/signup.html"
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # user = form.save()
            # user.refresh_from_db()  # load the profile instance created by the signal
            # user.profile.birth_date = form.cleaned_data.get('birth_date')
            user = form.save()

            group = Group.objects.get(name="employee")
            user.groups.add(group)
            messages.success(request, "Account created successfully")
            return redirect('login')

        else:
            messages.warning(request, "Fix the errors below")

    else:
        form = RegistrationForm()

    context = {
        'title': title,
        'form': form,
    }
    return render(request, template, context)


# @unauthenticated_user
# @login_required()
def login_view(request):
    if not request.user.is_authenticated:
        title = "Login"
        template = "accounts/login.html"

        context = {
            'title': title,
        }
        return render(request, template, context)


@login_required
def profile_view(request):
    title = 'Profile'
    # template = 'accounts/profile.html'
    template = 'accounts/dashboard.html'
    user = request.user
    context = {
        'title': title,
        'user': user,
    }
    return render(request, template, context)


@login_required
def edit_profile_view(request):
    title = "Edit profile"
    template = 'accounts/dashboard.html'
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, "You profile has been updated")
            return redirect('accounts:profile')

    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'form': form,
        'title': title,
        'profile_form': profile_form,
    }
    return render(request, template, context)


@login_required
def change_password_view(request):
    cp_title = 'Change Password'
    template = 'accounts/dashboard.html'

    if request.method == "POST":
        cp_form = PasswordChangeForm(data=request.POST, user=request.user)
        if cp_form.is_valid():
            cp_form.save()
            # this grabs the current user and keeps them logged in
            update_session_auth_hash(request, cp_form.user)
            messages.success(request, "You password has been changed")
            return redirect('accounts:profile')
        # else:
        # messages.error(request, "Incorrect form data, please correct the errors")
        # return redirect('accounts:change_password')
    else:
        cp_form = PasswordChangeForm(user=request.user)

    context = {
        'cp_title': cp_title,
        'cp_form': cp_form,
    }
    return render(request, template, context)


@login_required
def dashboard_view(request, user_id):
    template = 'posts/dashboard.html'
    title = "Dashboard"

    # latest_posts = NewPost.objects.filter(status='published').order_by('-published')[0:3]
    # categories = PostCategory.objects.all()
    user = request.user

    # get_my_posts = NewPost.objects.filter(added_by_id=user_id)

    # pagination
    # paginator = Paginator(get_my_posts, 6)  # Show 6 posts per page.
    # page_number = request.GET.get('page')
    # all_my_posts = paginator.get_page(page_number)
    context = {
        'title': title,
        # 'all_my_posts': all_my_posts,
        # 'latest_posts': latest_posts,
        # 'categories': categories,
        'user': user,
    }
    return render(request, template, context)


@login_required
def users_view(request):
    title = "Users"
    template = "accounts/users.html"
    users = User.objects.all()

    context = {
        'title': title,
        'users': users,
    }
    return render(request, template, context)
