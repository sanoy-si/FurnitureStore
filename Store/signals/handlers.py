from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import BadHeaderError
from Store.models import CustomOrder, Customer, Order
from django.core.mail import send_mail
from templated_mail.mail import BaseEmailMessage

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
  # print(kwargs)
  if kwargs['created']:
    user=kwargs['instance']
    # print(user.first_name,user.email)
    Customer.objects.create(user=user)
    try:
      message = BaseEmailMessage(
        template_name='emails\welcome.html',
        context={'name':user.first_name}
      )
      message.send([user.email])
    except BadHeaderError:
      pass
    except:
      pass
    # send_mail('Success','User Created Successfully','settings.EMAIL_HOST_USER',,fail_silently=False)

@receiver(post_save, sender = Order)
def send_success_email(sender, **kwargs):
  if kwargs['created']:
    order = kwargs['instance']
    user = order.customer.user
    try:
      message = BaseEmailMessage(
        template_name='emails\success.html',
        context={'name':user.first_name}
      )
      message.send([user.email])
    except BadHeaderError:
      pass
    except:
      pass
    
@receiver(post_save, sender = CustomOrder)
def send_wait_email(sender, **kwargs):
  if kwargs['created']:
    order = kwargs['instance']
    user = order.customer.user
    try:
      message = BaseEmailMessage(
        template_name='emails\wait.html',
        context={'name':user.first_name}
      )
      message.send([user.email])
    except BadHeaderError:
      pass
    except:
      pass
    