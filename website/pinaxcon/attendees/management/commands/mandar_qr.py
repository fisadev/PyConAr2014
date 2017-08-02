# -*- coding: utf-8 -*-
import base64

import qrcode
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from pinaxcon.attendees.models import Attendee

import os.path
import re

from email.MIMEBase import MIMEBase

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart



def send_email(to_list, subject, message, url_image, sender='no-reply@python.org.ar'):
	msg = EmailMultiAlternatives(subject, message, sender, to_list)

	html = """
<html>
<body>
<p>
Hola,
</p>
<p>Ya faltan pocas horas para la PyconAr 2016. ¡Te estamos esperando!</p>

<p> Para agilizar el proceso de acreditación, te pedimos por favor que presentés el siguiente código en la entrada, con el mismo te entregaremos las remera/s y/o vianda/s si las compraste en la tienda.</p>
		<img src="{}">
<p>¡Nos vemos en Bahía!</p>
<p> El equipo de PyconAr 2016</p>
</body></html>""".format(url_image)

	msg.attach_alternative(html, 'text/html')
	msg.send()

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        attendees = Attendee.objects.filter()
        for attendee in attendees:
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
            qr.add_data('http://ar.pycon.org/process-acreditation/?id_attendee={}'.format(attendee.id))
            qr.make(fit=True)
            img = qr.make_image()
            url = "/project/pinaxcon/site_media/media/qr/qr{}.png".format(attendee.id)
            img.save(url)

        for attendee in attendees:
            url = "http://ar.pycon.org/site_media/media/qr/qr{}.png".format(attendee.id)
            #encoded_image = base64.b64encode(open(url, "rb").read())
            send_email((attendee.user.email,), 'Importante(fix-webmail): Datos de registro PyconAr2016', 'message', url)

        self.stdout.write(self.style.SUCCESS('Enviados "%s"' % 1))

