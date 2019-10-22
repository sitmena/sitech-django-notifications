from sitech_notifications.core.channels.base_channel import BaseChannel


class MailChannel(BaseChannel):

    def send(self, notifiable, notification):
        print('The notification sent via MailChannel')
