# Sitech Notifications
Notifying users of various things that happen in your application is super easy to implement. Sitech notifications allow you to send a message to any user via Email, Datbase, and many other channels.

## Installation

Run the [pip](https://pip.pypa.io/en/stable/) command to install the latest version:

```bash
 pip install git+https://github.com/sitmena/sitech-notifications.git@v1.0
```

Add `sitech_notifications` to your `INSTALLED_APPS` in settings.py:
```bash
 INSTALLED_APPS = (
    ...
    'sitech_notifications',
 )
```

## Creating Notifications

In Sitech Notifications, each notification is represented by a single class, and to create a new notification you can run the following manage.py command:
```bash
 python manage.py createnotification TestNotification
 ```   
 
And this will place a fresh notification class with the below contents. Each notification class contains a `via` method and a variable number of message building methods (such as `to_mail` or `to_database`) that convert the notification to a message optimized for that particular channel.

```python
from sitech_notifications.core import Notification  
from sitech_notifications.core.channels import DatabaseChannel  
  
  
class TestNotification(Notification):  
  
  # Get the notification's delivery channels.  
  def via(self, notifiable):  
        return [DatabaseChannel]  
  
  # Get the dict representation of the notification.  
  def to_database(self, notifiable):  
        pass
```

## Sending  Notifications

###  # Using The Notifiable Mixin
Notifications may be sent in two ways: using the notify method of the Notifiable mixin or using the NotificationSender . First, let's explore using the mixin:

```python
 from sitech_notifications.core import Notifiable
 from django.db import models

 class Profile(models.Model, Notifiable):  
	phone = models.CharField(max_length=255, verbose_name='Phone')
	address = models.TextField(max_length=512,verbose_name='Address')
	
```
Adding `Notifiable` mixin in your  `Profile` model will allow you to easily send notifications to profiles using `notify` method. The `notify` method expects to receive a notification instance:
```python
 profile = Profile.objects.get(pk=1)
 profile.notify(TestNotification());
```

**Remember ,** you may use the `sitech_notifications.core.Notifiable` mixin on any of your models. You are not limited to only including it on your `Profile`model.


###  # Using The NotificationSender:
Alternatively, you may send notifications via the `NotificationSender` . This is useful primarily when you need to send a notification to multiple notifiable entities such as a list of profiles. To send notifications using the NotificationSender, pass all of the notifiable entities and the notification instance to the `send` method:

```python
 from sitech_notifications.core import NotificationSender
 
 profiles = Profile.objects.all()
 NotificationSender.send(profiles, TestNotification())
 
```

###  # Specifying Delivery Channels:
Every notification class has a `via` method that determines on which channels the notification will be delivered. Notifications may be sent on the `database`, `mail`,  `unifonc` channels.

The `via` method receives a `notifiable` instance, which will be an instance of the class to which the notification is being sent. You may use `notifiable` to determine which channels the notification should be delivered on:

```python

 #Get the notification's delivery channels.
 def via(notifiable):
	 if notifiable.prefers_sms:
		return [UnifonicChannel]
	 return	[DatabaseChannel]
	 	     
```
Let's quickly go through the different notification channels supported by Sitech Notifications.

-   **Database:** This option allows you to store notifications in a database should you wish to build a custom UI to display it.
-  **Mail:** The notifications will be sent in the form of email to users.
-  **Unifonic:** As the name suggests, users will receive SMS notifications on their phone.
