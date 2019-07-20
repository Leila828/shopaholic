from django.db import models
from oscar.core.loading import get_class, get_model
PartnerAddress = get_model('partner', 'PartnerAddress')

class PartenaireAdress(PartnerAddress):
    wilay = (('Adrar', 'Adrar'), ('Chlef', 'Chlef'), ('Laghouat', 'Laghouat'), ('Oum EL Bouaghi', 'Oum EL Bouaghi'),
             ('Batna', 'Batna'), ('Béjaia', 'Béjaia'), ('Biskra', 'Biskra'), ('Béchar', 'Béchar'),
             ('Blida', 'Blida'), ('Bouira', 'Bouira'), ('Tamanrasset', 'Tamanrasset'), ('Tébessa', 'Tébessa'),
             ('Tlemcen', 'Tlemcen'), ('Tiaret', 'Tiaret'), ('Tizi Ouzou', 'Tizi Ouzou'), ('Alger', 'Alger'),
             ('Djelfa', 'Djelfa'), ('Jijel', 'Jijel'), ('Sétif', 'Sétif'), ('Saida', 'Saida'),
             ('Skikda', 'Skikda'), ('Sidi Bel Abbès', 'Sidi Bel Abbès'), ('Annaba', 'Annaba'), ('Guelma', 'Guelma'),
             ('Constantine', 'Constantine'), ('Médéa', 'Médéa'), ('Mostaganem', 'Mostaganem'), ('MSila', 'Msila'),
             ('Mascara', 'Mascara'), ('Ouargla', 'Ouargla'), ('Oran', 'Oran'), ('El Bayadh', 'El Bayadh'),
             ('Illizi', 'Illizi'), ('Bordj Bou Arrerij', 'Bordj Bou Arrerij'), ('Boumerdès', 'Boumerdès'),
             ('El Tarf', 'El Tarf'),
             ('Tindouf', 'Tindouf'), ('Tissemsilt', 'Tissemsilt'), ('El Ouad', 'El Ouad'), ('Khenchla', 'Khenchla'),
             ('Souk Ahras', 'Souk Ahras'), ('Tipaza', 'Tipaza'), ('Mila', 'Mila'), ('Ain Defla', 'Ain Defla'),
             ('Naâma', 'Naâma'), ('Ain Témouchent', 'Ain Témouchent'), ('Ghardaia', 'Ghardaia'),
             ('Relizane', 'Relizane')
             )
    wilaya = models.CharField(max_length=255, blank=True, choices=wilay)


from oscar.apps.partner.models import *