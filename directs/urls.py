from django.urls import path
from . import views

urlpatterns = [
    #client urls
    path('client-unread/', views.clientUnread, name='client-unread'),
    path('client-inbox/', views.clientInbox, name='client-inbox'),
    path('client-chat/<str:pk>/', views.clientChat, name='client-chat'),
    path('client-chat-read/<str:pk>/', views.clientChatRead, name='client-chat-read'),
    path('client-send/', views.clientSend, name='client-logout'),

    
    #manufacturer urls
    path('manufacturer-unread/', views.manufacturerUnread, name='manufacturer-unread'),
    path('manufacturer-inbox/', views.manufacturerInbox, name='manufacturer-inbox'),
    path('manufacturer-chat/<str:pk>/', views.manufacturerChat, name='manufacturer-chat'),
    path('manufacturer-send/', views.manufSend, name='manufacturer-logout'),

    #twilio urls
    path('create-conversation/', views.CreateConversationView, name='create-conversation'),
    path('add-participant/', views.AddParticipantView, name='add-participant'),
    path('send-message/', views.SendMessageView, name='send-message'),
    path('get-messages/', views.GetMessagesView, name='get-messages'),
    path('generate-token/', views.GenerateTokenView, name='generate-token'),
    path('twilio-webhook/', views.TwilioWebhookView.as_view(), name='twilio-webhook'),
    
]