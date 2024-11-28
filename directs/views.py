from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ManufacturerMessage, ClientMessage, Client, Manufacturer
from .serializers import ManufacturerMessageSerializer, ClientMessageSerializer
from .serializers import CreateConversationSerializer, AddParticipantSerializer, SendMessageSerializer
from django.db.models import Max
from twilio.rest import Client
from decouple import config
from rest_framework.permissions import AllowAny
from twilio.request_validator import RequestValidator
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
import json

# Create your views here.
# @api_view(['GET'])
# def clientUnread(request):
#     messages = ManufacturerMessage.get_message(user=request.user)

#     serializer = ManufacturerMessageSerializer(messages, many=True)

#     return Response(serializer.data)

@api_view(['POST'])
def clientUnread(request):
    id = request.data['id']
    client = Client.objects.filter(id=id).first()
    messages = ManufacturerMessage.get_message(user=client)
    serializer = ManufacturerMessageSerializer(messages, many=True)

    return Response(serializer.data)






# @api_view(['GET'])
# def clientInbox(request):
#     #messages = ManufacturerMessage.objects.filter(client_user=request.user, read=True).annotate(last=Max('created')).order_by('-last')
#     messages = ManufacturerMessage.objects.filter(client_user=request.user).annotate(last=Max('created')).order_by('-last')

#     serializer = ManufacturerMessageSerializer(messages, many=True)

#     return Response(serializer.data)

@api_view(['POST'])
def clientInbox(request):
    id = request.data['id']
    client = Client.objects.filter(id=id).first()
    messages = ManufacturerMessage.objects.filter(client_user=client, read=True).annotate(last=Max('created')).order_by('-last')

    serializer = ManufacturerMessageSerializer(messages, many=True)

    return Response(serializer.data)




@api_view(['PUT'])
def clientChatRead(request, pk):
    manufacturer = Manufacturer.objects.get(id = pk)
    id = request.data['id']
    client = Client.objects.filter(id=id).first()
    messages = ManufacturerMessage.objects.filter(client_user=client, sender=manufacturer).annotate(last=Max('created')).order_by('-last')
    for message in messages:
        message.read = True
        message.save()
    serializer = ManufacturerMessageSerializer(messages, many=True)

    return Response(serializer.data)




@api_view(['POST'])
def clientChat(request, pk):
    manufacturer = Manufacturer.objects.get(id = pk)
    id = request.data['id']
    client = Client.objects.filter(id=id).first()
    messages = ManufacturerMessage.objects.filter(client_user=client, sender=manufacturer).annotate(last=Max('created')).order_by('-last')
    # for message in messages:
    #     message.read = True
    #     message.save()
    serializer = ManufacturerMessageSerializer(messages, many=True)

    return Response(serializer.data)



'''
#get user from request
@api_view(['POST'])
def clientSend(request):
    user = request.user.email
    from_user = Client.objects.filter(email= user ).first()
    data = request.data
    manufacturer = data['manufacturer']
    to_user = Manufacturer.objects.filter(email = manufacturer).first()
    body = data['body']
    message = ClientMessage.send(from_user=from_user, to_user=to_user, body=body)

    serializer = ClientMessageSerializer(message)
    return Response(serializer.data)
'''
#getting user from request body
@api_view(['POST'])
def clientSend(request):
    data = request.data
    manufacturer = data['manufacturer']
    to_user = Manufacturer.objects.filter(id = manufacturer).first()
    body = data['body']
    user = data['client_id']
    from_user = Client.objects.filter(id= user ).first()
    message = ClientMessage.send(from_user=from_user, to_user=to_user, body=body)

    serializer = ClientMessageSerializer(message)

    return Response(serializer.data)









#Manufacturer directs views

# @api_view(['GET'])
# def manufacturerUnread(request):
#     messages = ClientMessage.get_message(user=request.user)

#     serializer = ClientMessageSerializer(messages, many=True)

#     return Response(serializer.data)
@api_view(['POST'])
def manufacturerUnread(request):
    id = request.data['id']
    manufacturer = Manufacturer.objects.filter(id=id).first()
    messages = ClientMessage.get_message(user=manufacturer)

    serializer = ClientMessageSerializer(messages, many=True)

    return Response(serializer.data)





# @api_view(['GET'])
# def manufacturerInbox(request):
#     messages = ClientMessage.objects.filter(manufacturer_user=request.user).annotate(last=Max('created')).order_by('-last')
#     #messages = ClientMessage.objects.filter(manufacturer_user=request.user, read=True).annotate(last=Max('created')).order_by('-last')

#     serializer = ClientMessageSerializer(messages, many=True)

#     return Response(serializer.data)
@api_view(['POST'])
def manufacturerInbox(request):
    id = request.data['id']
    manufacturer = Manufacturer.objects.filter(id=id).first()
    messages = ClientMessage.objects.filter(manufacturer_user=manufacturer, read=True).annotate(last=Max('created')).order_by('-last')
    #messages = ClientMessage.objects.filter(manufacturer_user=request.user, read=True).annotate(last=Max('created')).order_by('-last')

    serializer = ClientMessageSerializer(messages, many=True)

    return Response(serializer.data)




# @api_view(['GET'])
# def manufacturerChat(request, pk):
#     client = Client.objects.get(id = pk)
#     messages = ClientMessage.objects.filter(manufacturer_user=request.user, sender=client).annotate(last=Max('created')).order_by('-last')

#     serializer = ClientMessageSerializer(messages, many=True)

#     return Response(serializer.data)
@api_view(['POST'])
def manufacturerChat(request, pk):
    id = request.data['id']
    manufacturer = Manufacturer.objects.filter(id=id).first()
    client = Client.objects.get(id = pk)
    messages = ClientMessage.objects.filter(manufacturer_user=manufacturer, sender=client).annotate(last=Max('created')).order_by('-last')
    # for message in messages:
    #     message.read = True
    #     message.save()
    serializer = ClientMessageSerializer(messages, many=True)

    return Response(serializer.data)





#get chat messages with particular client
'''
#getting user from request
@api_view(['POST'])
def manufSend(request):
    from_user = request.user
    data = request.data
    client = data['client']
    to_user = Client.objects.get(email = client)
    body = data['body']
    message = ManufacturerMessage.send(from_user=from_user, to_user=to_user, body=body)

    serializer = ManufacturerMessageSerializer(message)
    return Response(serializer.data)
'''

#getting user from request body
@api_view(['POST'])
def manufSend(request):
    data = request.data
    client = data['client']
    to_user = Client.objects.filter(id = client).first()
    body = data['body']
    user = data['manufacturer_id']
    from_user = Manufacturer.objects.filter(id= user ).first()
    message = ManufacturerMessage.send(from_user=from_user, to_user=to_user, body=body)

    serializer = ManufacturerMessageSerializer(message)

    return Response(serializer.data)

'''

#login required decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_api_view(request):
    return Response({"message": "Hello, authenticated user!"})
'''


account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# conversation = client.conversations.v1.conversations.create(
#     friendly_name="Friendly Conversation"
# )
conversation_sid = config('TWILIO_CONVERSATION_SID')

#print(conversation_sid)

class TwilioService:
    def __init__(self):
        self.client = Client(account_sid, auth_token)
        self.service_sid = conversation_sid

    def create_conversation(self, friendly_name):
        return self.client.conversations.services(self.service_sid).conversations.create(friendly_name=friendly_name)

    def add_participant(self, conversation_sid, identity):
        return self.client.conversations.services(self.service_sid).conversations(conversation_sid).participants.create(identity=identity)

    def send_message(self, conversation_sid, body, author):
        return self.client.conversations.services(self.service_sid).conversations(conversation_sid).messages.create(body=body, author=author)
    
twilio_service = TwilioService()

@api_view(['POST'])
def CreateConversationView(request):
    serializer = CreateConversationSerializer(data=request.data)
    if serializer.is_valid():
        conversation = twilio_service.create_conversation(serializer.validated_data['friendly_name'])
        return Response({"conversation_sid": conversation.sid})
    return Response(serializer.errors)

@api_view(['POST'])
def AddParticipantView(request):
    serializer = AddParticipantSerializer(data=request.data)
    if serializer.is_valid():
        participant = twilio_service.add_participant(
            serializer.validated_data['conversation_sid'],
            serializer.validated_data['identity']
        )
        return Response({"participant_sid": participant.sid})
    return Response(serializer.errors)

@api_view(['POST'])
def SendMessageView(request):
    serializer = SendMessageSerializer(data=request.data)
    if serializer.is_valid():
        message = twilio_service.send_message(
            serializer.validated_data['conversation_sid'],
            serializer.validated_data['body'],
            serializer.validated_data['author']
        )
        return Response({"message_sid": message.sid})
    return Response(serializer.errors)

@api_view(['GET'])
def GetMessagesView(request):
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    messages = client.conversations.v1.conversations(
        "CH7e4d0171125a4c5bbe4a566cde91ff41"
    ).messages.list(limit=20)

    #return Response(messages)
    def message_to_dict(message):
        return {
            "sid": message.sid,
            "conversation_sid": message.conversation_sid,
            "author": message.author,
            "body": message.body,
            "date_created": message.date_created.isoformat() if message.date_created else None,
            "date_updated": message.date_updated.isoformat() if message.date_updated else None,
            "media": message.media,
            # Add more fields as necessary
        }

    # Convert all messages to a JSON-serializable format
    messages_json = [message_to_dict(message) for message in messages]

    # Serialize to JSON string
    json_output = json.dumps(messages_json, indent=2)

    messages = json.loads(json_output)

    # Extract the body attribute from each message
    extracted_attributes = [
        {"sid": message["sid"], "author": message["author"], "body": message["body"]}
        for message in messages
    ]
    # Print the extracted body attributes
    clean_messages=[]
    print(extracted_attributes)
    return Response(extracted_attributes)

@api_view(['POST'])
def GenerateTokenView(request):
    account_sid = config('TWILIO_ACCOUNT_SID')
    api_key = config('TWILIO_API_KEY_SID')
    api_secret = config('TWILIO_API_SECRET')
    service_sid = config('TWILIO_CONVERSATION_SID')
    identity = request.data['email']

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)
    chat_grant = ChatGrant(service_sid=service_sid)
    token.add_grant(chat_grant)

    return Response({"token": token.to_jwt()})

class TwilioWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Validate the Twilio request
        validator = RequestValidator(auth_token)
        twilio_signature = request.headers.get("X-Twilio-Signature", "")

        # Build the absolute URI for the request
        url = request.build_absolute_uri()
        params = request.POST.dict()

        if not validator.validate(url, params, twilio_signature):
            return Response({"error": "Invalid request signature"})
        
        expected_signature = validator.compute_signature(url, params)
        print(f"Expected: {expected_signature}, Received: {twilio_signature}")

        # Process the webhook event
        event_type = request.data.get("EventType")
        print((f"Received Twilio event: {event_type}"))

        if event_type == "onMessageAdded":
            message_sid = request.data.get("MessageSid")
            message_body = request.data.get("Body")
            # Add logic to handle message here (e.g., save to DB)

        # Handle other event types if needed
        return Response(f"New message received: {message_sid} - {message_body}")
    

