from django.contrib import admin
from django.urls import path, include

handler404 = 'sudoku.views.error_404'
handler500 = 'sudoku.views.error_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sudoku.urls')),
]
