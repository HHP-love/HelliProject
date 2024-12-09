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
    


from django.shortcuts import render

def redoc_view(request):
    return render(request, 'redoc.html')
