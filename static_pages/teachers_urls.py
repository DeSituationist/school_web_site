from django.urls import path
from django.views.generic import TemplateView

app_name='static_pages'

urlpatterns = [
    path(
        'английский/',
        TemplateView.as_view(template_name='static_pages/teachers/teachers_english.html'),
        name='teachers_english'
    ),
    path(
        'информатика/',
        TemplateView.as_view(template_name='static_pages/teachers/teachers_computer_science.html'),
        name='teachers_computer_science'
    ),
    path(
        'история-и-обществознание/',
        TemplateView.as_view(template_name='static_pages/teachers/teachers_social_science.html'),
        name='teachers_social_science'
    ),
    path(
        'математика/',
        TemplateView.as_view(template_name='static_pages/teachers/teachers_math.html'),
        name='teachers_math'
    ),
    path(
        'русский-язык-и-литература/',
        TemplateView.as_view(template_name='static_pages/teachers/teachers_russian.html'),
        name='teachers_russian'
    ),
    path(
        'сайты-учителей/',
        TemplateView.as_view(template_name='static_pages/teachers/teachers_personal_sites.html'),
        name='teachers_personal'
    ),
    path(
        'физическая-культура/',
        TemplateView.as_view(template_name='static_pages/teachers/teachers_PE.html'),
        name='teachers_PE'
    ),
]