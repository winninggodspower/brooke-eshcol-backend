from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.template.loader import render_to_string
from django.contrib import messages

from django.conf import settings

from django.core.mail import send_mail, BadHeaderError

from .forms import MemberForm
from django.views import View

from .models import Payment
# Create your views here.

class members(View):

    def post(self, request):
        form = MemberForm(request.POST)

        if form.is_valid():
            member = form.save()
            
            # sending email to director notifying him that someone has becomed a member
            username = f"{member.first_name} {member.last_name}"

            subject = f"{username} Became a member in Brookeeshcol"
            email_template_name = "become-member/become-member-email.txt"
            email_content = {
                'username': username,
                "email": member.email,
                'phone': member.phone,
                'site_name': settings.SITE_NAME,
                'member_id': member.id,
                }
            email = render_to_string(email_template_name, email_content)
            try:
                send_mail(subject, email, 'contact@brookeeshcol.com' , settings.ADMIN_EMAILS, fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, "Successfully Becomed a member of Brookeeshcol system limited")
            return redirect("home")
        
        # adding the is-invalid class to field with errors
        for field in form.errors:
            print(field)
            form[field].field.widget.attrs['class'] += ' is-invalid'

        return render(request, 'member.html', {"form": form})


    def get(self, request):
        form = MemberForm()

        # adding the is-invalid class to field with errors
        for field in form.errors:
            print(field)
            form[field].field.widget.attrs['class'] += ' is-invalid'

        return render(request, 'member.html', {'form': form})


# Response blueprint
# message: "Approved"
# redirecturl: "?trxref=2182893&reference=2182893"
# reference: "2182893"
# status: "success"
# trans: "2306170385"
# transaction: "2306170385"
# trxref: "2182893"


def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        payment = Payment(request.POST)
        payment = payment.save()

        if not payment.verify_payment():
            messages.error('payment unverified, please make a valid payment')
            messages.delete()
            return redirect('members')

        else:
            member = MemberForm(request.POST.get('personal_info'))
            member.save()
            messages.success(request, "Successfully Becomed a member of Brookeeshcol system limited")
            return redirect('home')
