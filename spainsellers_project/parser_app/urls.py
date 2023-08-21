from django.urls import path


from parser_app.views import ovisat, lcphones, chipspain, fourphones, repuestosfuentes, preciosadictos, spainsellers


urlpatterns = [
    path('ovisat-json/', ovisat, name='ovisat-json'),
    path('lcphones-json/', lcphones, name='lcphones-json'),
    path('chipspain-json/', chipspain, name='chipspain-json'),
    path('fourphones-json/', fourphones, name='fourphones-json'),
    path('repuestosfuentes-json/', repuestosfuentes, name='repuestosfuentes-json'),
    path('preciosadictos-json/', preciosadictos, name='preciosadictos-json'),
    path('spainsellers-json/', spainsellers, name='spainsellers-json'),
]
