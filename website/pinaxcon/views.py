# -*- coding: utf-8 -*-
import datetime
import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.template import Context, loader
from symposion.schedule.models import Slot, Day
from symposion.speakers.models import Speaker

from .forms import BecasForm
from .attendees.models import Attendee



MAP = [
    {
        "name": "Club de emprendedores de Bahía Blanca (Viernes 25)",
        "lat": -38.719668,
        "lng": -62.266995,
        "center": True
    },
    {
        "name": "Salón de los Fundadores de la UNS (Viernes 25)",
        "lat": -38.71971,
        "lng": -62.26782
    },
    {
        "name": "Complejo Palihue - UNS (Sábado 26 y Domingo 27)",
        "lat": -38.694053,
        "lng": -62.249016
    }

]


def becas(request):
    form_class = BecasForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'nombre_completo')
            contact_email = request.POST.get(
                'email')
            form_content = request.POST.get('que_necesitas')

            # Email the profile with the
            # contact information
            template = loader.get_template('becas_email.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                "[BECAS]Nueva beca requerida",
                content,
                "no-reply@python.org.ar",
                ['pyconar@listas.bitson.com.ar'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            messages.add_message(request, messages.INFO, u"""¡Gracias por tu solicitud!, nos pondremos en contacto a la brevedad para
 informarte de los pasos a seguir""")

            return redirect('becas')
        else:
            messages.add_message(request, messages.ERROR, u"""Por favor completa los campos correctamente""")

    return render(request, 'becas.html', {
        'form': form_class,
    })

AUDIENCE_LEVEL = {
    1: 'Inicial',
    2: 'Intermedio',
    3: 'Avanzado'
}

def schedule_json(request):
    slots = Slot.objects.filter(
        day__schedule__published=True,
        day__schedule__hidden=False
    ).order_by("start")

    protocol = request.META.get('HTTP_X_FORWARDED_PROTO', 'http')


    def create_session_slots(hour_slots):
        data = []
        for slot in hour_slots:
            slot_data = {
                "location": ", ".join(room["name"] for room in slot.rooms.values()),
                "timeStart": slot.start_datetime.strftime("%-I:%M %p"),
                "timeEnd": slot.end_datetime.strftime("%-I:%M %p"),
                "kind": slot.kind.label,
                "tags": "",
            }
            if hasattr(slot.content, "proposal"):
                slot_data.update({
                    "name": slot.content.title,
                    "audience_level": AUDIENCE_LEVEL[slot.content.proposal.audience_level],
                    "speakerNames": [s.name for s in slot.content.speakers()],
                    "description": slot.content.description,
                    "idTalk": slot.content.pk,
                    "conf_url": "%s://%s%s" % (
                        protocol,
                        Site.objects.get_current().domain,
                        reverse("schedule_presentation_detail", args=[slot.content.pk])
                    ),
                    "cancelled": slot.content.cancelled,
                })
            else:
                slot_data.update({
                    "name": slot.content_override if slot.content_override else "Slot",
                })

            data.append(slot_data)

        return data

    schedule = []
    for day in Day.objects.all():
        schedule_content = {}
        day_key = day.date.strftime('%Y-%m-%d')
        schedule_content['date'] = day_key
        schedule_content['groups'] = []

        slots_day = slots.filter(day=day)
        hours = [k for k  in set([k[0].strftime("%H")
                                  for k in slots_day.values_list('start')])]
        hours.sort()

        for hour in hours:
            group_content = {}
            h_ini = (datetime.datetime.combine(datetime.date.today(),
                                               datetime.time(int(hour)))
                                                )


            h_ini_rounded = h_ini.strftime('%H:00')

            h_fin_rounded = ((datetime.datetime.combine(datetime.date.today(),
                                                datetime.time(int(hour)))
                                                ) + datetime.timedelta(
                                                    hours=1)).strftime('%H:00')

            hour_slots = slots_day.filter(start__gte=h_ini_rounded,
                                          start__lt=h_fin_rounded)

            group_content['time'] = h_ini.strftime("%-I:%M %p")
            sessions = create_session_slots(hour_slots)
            group_content['sessions'] = sessions
            schedule_content['groups'].append(group_content)
        schedule.append(schedule_content)

    speakers = []

    for speaker in Speaker.objects.filter():
        speaker_data = {}
        speaker_data['name'] = speaker.name
        speaker_data['twitter'] = speaker.twitter_username
        speaker_photo = '' if not speaker.photo else speaker.photo.url
        if speaker_photo:
            speaker_data['profilePic'] = "http://{host}{url}".format(
                                                        host=request.get_host(),
                                                        url=speaker.photo.url)
        else:
            speaker_data['profilePic'] = ''

        speakers.append(speaker_data)


    return HttpResponse(
        json.dumps({"schedule": schedule, "speakers": speakers, "map": MAP}),
        content_type="application/json"
    )


@staff_member_required
def process_acreditation(request):

    if request.method=="POST":
        id_attendee = request.POST.get('id_attendee')
        attendee = Attendee.objects.get(id=id_attendee)
        attendee.is_acredited = True

        require_certificate = request.POST.get('require_certificate')
        wanna_party = request.POST.get('wanna_party')

        attendee.require_certificate = True if require_certificate == 'on' else False
        attendee.wanna_party = True if wanna_party == 'on' else False

        attendee.save()
    else:
        id_attendee = request.GET.get('id_attendee')
        attendee = Attendee.objects.get(id=id_attendee)

    is_speaker = False

    if Speaker.objects.filter(user = attendee.user):
        is_speaker = True

    return render(request, 'acreditation.html', {
        'attendee': attendee,
        'is_speaker': is_speaker
    })
