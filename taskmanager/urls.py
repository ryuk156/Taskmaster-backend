from django.urls import path
from . import views

urlpatterns = [
    path('api/boards/', views.create_board, name='create_board'),
    path('api/viewboards/', views.get_boards, name='get_boards'),
    path('api/viewboard/<int:pk>/', views.get_board, name='get_board'),
    path('api/deleteboard/<int:pk>/', views.delete_board, name='delete_board'),
    path('api/updateboard/<int:pk>/', views.update_board, name='update_board'),
    path('api/boards/<int:board_id>/createcolumn/', views.create_column, name='create_column'),
    path('api/viewcolumns/', views.get_columns, name='get_columns'),
    path('api/viewcolumn/<int:pk>/', views.get_column, name='get_column'),
    path('api/deletecolumn/<int:pk>/', views.delete_column, name='delete_column'),
    path('api/updatecolumn/<int:pk>/', views.update_column, name='update_column'),
    path('api/columns/<int:column_id>/createcard/', views.create_card, name='create_card'),
    path('api/viewcards/', views.get_cards, name='get_cards'),
    path('api/viewcard/<int:pk>/', views.get_card, name='get_card'),
    path('api/deletecard/<int:pk>/', views.delete_card, name='delete_card'),
    path('api/updatecard/<int:pk>/', views.update_card, name='update_card'),
    path('api/swapcard/', views.swap_card, name='swap_card'),
    path('api/userlist/', views.ListUsers, name='ListUsers'),
    path('api/shareboard/<int:board_id>/', views.share_board, name='share_board'),
    path('api/sharedboards/', views.get_shared_boards, name='get_shared_boards'),
]