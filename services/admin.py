from django.contrib import admin
from .models import Pathway, ReferralSource, D2A, Discharge, Referral, DischargeService

# Register all of the models in the admin site
admin.site.register(Pathway)
admin.site.register(ReferralSource)
admin.site.register(D2A)
admin.site.register(Discharge)
admin.site.register(Referral)
admin.site.register(DischargeService)
