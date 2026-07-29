from django.urls import path

from . import views

urlpatterns = [

    # ==========================================================
    # HOME
    # ==========================================================

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),


    # ==========================================================
    # AUTHENTICATION
    # ==========================================================

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),


    # ==========================================================
    # POSTS
    # ==========================================================

    path(
        "post/<int:id>/",
        views.post_detail,
        name="post_detail"
    ),

    path(
        "create/",
        views.create_post,
        name="create_post"
    ),

    path(
        "edit/<int:id>/",
        views.edit_post,
        name="edit_post"
    ),

    path(
        "delete/<int:id>/",
        views.delete_post,
        name="delete_post"
    ),

    path(
        "like/<int:pk>/",
        views.like_post,
        name="like_post"
    ),

    path(
        "bookmark/<int:id>/",
        views.bookmark_post,
        name="bookmark_post"
    ),


    # ==========================================================
    # PROFILE
    # ==========================================================

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "profile/edit/",
        views.profile_edit,
        name="profile_edit"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "author/<str:username>/",
        views.author_profile,
        name="author_profile"
    ),


    # ==========================================================
    # NEWSLETTER
    # ==========================================================

    path(
        "newsletter/",
        views.newsletter,
        name="newsletter"
    ),


    # ==========================================================
    # CONTACT FORM
    # ==========================================================

    path(
        "contact/send/",
        views.contact_form,
        name="contact_form"
    ),

]