from django.conf.urls import url
from django.urls import path, re_path
from mtn_web import views
from mtn_web.forms import UserLoginForm
from mtn_web.models import Category, Language, Country, Source
from mtn_web.views import CountryList, LanguageList, CategoryList

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^query/new/$", views.new_query, name="new_query"),
    url(r"^query/view/(?P<result_pk>\d+)$", views.view_result, name="view_result"),
    url(r"^query/delete/(?P<result_pk>\d+)$", views.delete_result, name="delete_result"),
    url(r"^post/new/$", views.new_post, name="new_post"),
    url(r"^post/view/(?P<post_pk>\d+)$", views.view_post, name="view_post"),
    url(r"^post/update/(?P<post_pk>\d+)$", views.update_post, name="update_post"),
    url(r"^post/delete/(?P<post_pk>\d+)$", views.delete_post, name="delete_post"),
    url(r"^post/all/public/$", views.view_public_posts, name="view_public_posts"),
    url(r"^comment/new/(?P<post_pk>\d+)$", views.new_comment, name="new_comment"),
    url(r"^comment/view/(?P<comment_pk>\d+)$", views.view_comment, name="view_comment"),
    url(r"^comment/delete/(?P<comment_pk>\d+)$", views.delete_comment, name="delete_comment", ),
    url(r"^comment/update/(?P<comment_pk>\d+)$", views.update_comment, name="update_comment", ),
    url(r"^accounts/register/$", views.register_user, name="register_user"),
    url(r"^accounts/view/(?P<member_pk>\d+)$", views.view_user, name="view_user"),
    url(r"^sources/category/$", views.view_category_sources, name="view_category_sources"),
    url(r"^sources/country/publisher/$", views.view_country_publisher_sources, name="view_country_publisher_sources"),
    url(r"^sources/language/$", views.view_language_sources, name="view_language_sources"),
    url(r"^choro/view/(?P<result_pk>\d+)$", views.view_choro, name="view_choro"),
    url(r"^error/report/$", views.report_error, name="report_error"),
    url(r"^accounts/login/$", views.login_user, name="login_user"),
    path('categories/', CategoryList.as_view(), name="category_list"),
    path('countries/', CountryList.as_view(), name="country_list"),
    path('languages/', LanguageList.as_view(), name="language_list"),

    # url(r"^category/view/(?P<category_pk>\d+)$", view.view_category, name="view_category"),
    # url(r"^language/view/(?P<language_pk>\d+)$", views.view_language, name="view_language"),
    # url(r"^country/view/(?P<country_pk>\d+)$", views.view_country, name="view_country"),

    # url(r'all-categories', views.ListView.as_view(model=Category)),
    # url(r'all-languages', views.ListView.as_view(model=Language)),
    # url(r'all-countries', views.ListView.as_view(model=Country)),
    # path('login/', views.login_user(template_name="registration/login.hmtl", authentication_form=UserLoginForm), name='login')
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
