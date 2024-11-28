from django.http import JsonResponse

from django.core.mail import send_mail
def send_email_view(request):
    try:
        subject = 'Hello from Django!'
        message = 'This is a test email sent via Django.'
        sender = 'mahdiyar.mahdi31313@gmail.com'
        recipient_list = ['hadhey0121@gmail.com', 'mahdiyar.mahdi31313@gmail.com']
        send_mail(subject, message, sender, recipient_list)
        return JsonResponse({"status": "success", "message": "Email sent successfully."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    



#     message1 = (
#     "Subject here",
#     "Here is the message",
#     "from@example.com",
#     ["first@example.com", "other@example.com"],
# )

# message2 = (
#     "Another Subject",
#     "Here is another message",
#     "from@example.com",
#     ["second@test.com"],
# )

# send_mass_mail((message1, message2), fail_silently=False)