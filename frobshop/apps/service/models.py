from django.db import models
from django.utils.functional import cached_property
from django.conf import settings
from django.db.models import Count, Sum


class category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories', blank=True,
                              null=True, max_length=255)
    description = models.TextField(max_length=1000, blank=True,
                              null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def get_services(self):
        return service.objects.filter(category=self)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

class service(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    UPC = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True,
                              null=True)
    tel = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    ville = models.CharField(max_length=255, null=True, blank=True)
    wilay = (('Adrar','Adrar'),('Chlef','Chlef'),('Laghouat','Laghouat'),('Oum EL Bouaghi','Oum EL Bouaghi'),
             ('Batna','Batna'),('Béjaia','Béjaia'),('Biskra','Biskra'),('Béchar','Béchar'),
             ('Blida', 'Blida'),('Bouira','Bouira'),('Tamanrasset','Tamanrasset'),('Tébessa','Tébessa'),
             ('Tlemcen', 'Tlemcen'),('Tiaret','Tiaret'),('Tizi Ouzou','Tizi Ouzou'),('Alger','Alger'),
             ('Djelfa', 'Djelfa'),('Jijel','Jijel'),('Sétif','Sétif'),('Saida','Saida'),
             ('Skikda', 'Skikda'),('Sidi Bel Abbès','Sidi Bel Abbès'),('Annaba','Annaba'),('Guelma','Guelma'),
             ('Constantine', 'Constantine'),('Médéa','Médéa'),('Mostaganem','Mostaganem'),('MSila','Msila'),
             ('Mascara', 'Mascara'),('Ouargla','Ouargla'),('Oran','Oran'),('El Bayadh','El Bayadh'),
             ('Illizi', 'Illizi'),('Bordj Bou Arrerij','Bordj Bou Arrerij'),('Boumerdès','Boumerdès'),('El Tarf','El Tarf'),
             ('Tindouf', 'Tindouf'),('Tissemsilt','Tissemsilt'),('El Ouad','El Ouad'),('Khenchla','Khenchla'),
             ('Souk Ahras', 'Souk Ahras'),('Tipaza','Tipaza'),('Mila','Mila'),('Ain Defla','Ain Defla'),
             ('Naâma', 'Naâma'),('Ain Témouchent','Ain Témouchent'),('Ghardaia','Ghardaia'),('Relizane','Relizane')
            )
    wilaya = models.CharField(max_length=255, choices=wilay, null=True, blank=True)
    rating = models.FloatField(('Rating'), null=True, editable=False)

    def get_all_images(self):
        return self.images.all()

    def primary_image(self):
        return self.images.order_by('display_order').first()

        # Updating methods

    def update_rating(self):
        self.rating = self.calculate_rating()
        self.save()

    update_rating.alters_data = True

    def calculate_rating(self):
        result = self.avis.filter(
            status=self.avis.approved
        ).aggregate(
            sum=Sum('score'), count=Count('id'))
        reviews_sum = result['sum'] or 0
        reviews_count = result['count'] or 0
        rating = None
        if reviews_count > 0:
            rating = float(reviews_sum) / reviews_count
        return rating

    def has_review_by(self, user):
        if user.is_anonymous:
            return False
        return self.avis.filter(user=user).exists()

    def is_review_permitted(self, user):
        if user.is_authenticated or settings.OSCAR_ALLOW_ANON_REVIEWS:
            return not self.has_review_by(user)
        else:
            return False

    @cached_property
    def num_approved_reviews(self):
        return self.avis.approved().count()



class ServiceImage(models.Model):
    service = models.ForeignKey(service, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='services', blank=True,
                              null=True, max_length=255)
    display_order = models.PositiveIntegerField(
        ("Display order"), default=0, db_index=True)

