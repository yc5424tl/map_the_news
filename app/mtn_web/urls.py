#from django.conf.urls import url
from django.urls import path, re_path
from mtn_web import views
from mtn_web.forms import UserLoginForm
from mtn_web.models import Category, Language, Country, Source


urlpatterns = [
    re_path(r"^$",                                   views.index,                 name="index"),
    re_path(r"^query/new/$",                         views.new_query,             name="new_query"),
    re_path(r"^query/view/(?P<result_pk>\d+)$",      views.view_result,           name="view_result"),
    re_path(r"^query/delete/(?P<result_pk>\d+)$",    views.delete_result,         name="delete_result"),
    re_path(r"^post/new/$",                          views.new_post,              name="new_post"),
    re_path(r"^post/view/(?P<post_pk>\d+)$",         views.view_post,             name="view_post"),
    re_path(r"^post/update/(?P<post_pk>\d+)$",       views.update_post,           name="update_post"),
    re_path(r"^post/delete/(?P<post_pk>\d+)$",       views.delete_post,           name="delete_post"),
    re_path(r"^post/all/public/$",                   views.view_public_posts,     name="view_public_posts"),
    re_path(r"^comment/new/(?P<post_pk>\d+)$",       views.new_comment,           name="new_comment"),
    re_path(r"^comment/view/(?P<comment_pk>\d+)$",   views.view_comment,          name="view_comment"),
    re_path(r"^comment/delete/(?P<comment_pk>\d+)$", views.delete_comment,        name="delete_comment", ),
    re_path(r"^comment/update/(?P<comment_pk>\d+)$", views.update_comment,        name="update_comment", ),
    re_path(r"^accounts/register/$",                 views.register_user,         name="register_user"),
    re_path(r"^accounts/view/(?P<member_pk>\d+)$",   views.view_user,             name="view_user"),
    re_path(r"^choro/view/(?P<result_pk>\d+)$",      views.view_choro,            name="view_choro"),
    re_path(r"^error/report/$",                      views.report_error,          name="report_error"),
    #re_path(r"^accounts/login/$",                    views.login_user,            name="login_user"),
    re_path(r"^sources/groups/$",                    views.view_source_groups,    name="view_source_groups"),
    path('sources/<str:name>/',                  views.view_source_detail,    name='view_source_detail'),
    path('categories/<str:name>/',               views.view_category_sources, name="view_category_sources"),
    path('countries/<str:alphanum_name>/',       views.view_country_sources,  name="view_country_sources"),
    path('languages/<str:alphanum_name>/',       views.view_language_sources, name="view_language_sources"),

    # path('login/', views.login_user(template_name="registration/login.html", authentication_form=UserLoginForm), name='login')
]


# ----- Generated urls from import django.contrib.auth.views in project.urls -----
# accounts/login/                  [name='login']
# accounts/logout/                 [name='logout']
# accounts/password_change/        [name='password_change']
# accounts/password_change/done/   [name='password_change_done']
# accounts/password_reset/         [name='password_reset']
# accounts/password_reset/done/    [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/             [name='password_reset_complete']
