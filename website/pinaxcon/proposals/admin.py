from django.contrib import admin

from .models import TalkProposal
from symposion.proposals.models import SupportingDocument

class Inline(admin.StackedInline):
        model = SupportingDocument

class TalkProposalAdmin(admin.ModelAdmin):
        inlines = (Inline,)

admin.site.register(TalkProposal, TalkProposalAdmin)
