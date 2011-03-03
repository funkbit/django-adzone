# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from adzone.managers import AdManager

class Advertiser(models.Model):
    """
    A Model for our Advertiser.
    """
    company_name = models.CharField(_('Company Name'), max_length=255)
    website = models.URLField(_('Company Site'), verify_exists=(settings.DEBUG==False))
    user = models.ForeignKey(User, verbose_name=_('User'))

    class Meta:
        verbose_name = _('Ad Provider')
        verbose_name_plural = _('Advertisers')
        ordering = ('company_name',)

    def __unicode__(self):
        return self.company_name

    def get_website_url(self):
        return self.website

class AdCategory(models.Model):
    """
    a Model to hold the different Categories for adverts
    """
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), unique=True)
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('title',)

    def __unicode__(self):
        return self.title

class AdZone(models.Model):
    """
    a Model that describes the attributes and behaviours of ad zones
    """
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'))
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        verbose_name = _('Zone')
        verbose_name_plural = _('Zones')
        ordering = ('title',)

    def __unicode__(self):
        return self.title

class AdBase(models.Model):
    """
    This is our base model, from which all ads will inherit.
    The manager methods for this model will determine which ads to
    display return etc.
    """
    title = models.CharField(_('Title'), max_length=255)
    url = models.URLField(_('Advertised URL'), verify_exists=(settings.DEBUG==False))
    enabled = models.BooleanField(_('Enabled'), default=False)
    since = models.DateTimeField(_('Since'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    # Relations
    advertiser = models.ForeignKey(Advertiser, verbose_name=_('Ad Provider'))
    category = models.ForeignKey(AdCategory, verbose_name=_('Category'))
    zone = models.ForeignKey(AdZone, verbose_name=_('Zone'))

    # Our Custom Manager
    objects = AdManager()

    class Meta:
        verbose_name = _('Ad Base')
        verbose_name_plural = _('Ad Bases')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('adzone_ad_view', [self.id])

class AdImpression(models.Model):
    """
    The AdImpression Model will record every time the ad is loaded on a page
    """
    impression_date = models.DateTimeField(_('When'), auto_now_add=True)
    source_ip = models.IPAddressField(_('Who'), null=True, blank=True)
    ad = models.ForeignKey(AdBase, verbose_name=_('Ad'))

    class Meta:
        verbose_name = _('Ad Impression')
        verbose_name_plural = _('Ad Impressions')

class AdClick(models.Model):
    """
    The AdClick model will record every click that a add gets
    """
    click_date = models.DateTimeField(_('When'), auto_now_add=True)
    source_ip = models.IPAddressField(_('Who'), null=True, blank=True)
    ad = models.ForeignKey(AdBase, verbose_name=_('Ad'))

    class Meta:
        verbose_name = _('Ad Click')
        verbose_name_plural = _('Ad Clicks')

# Example Ad Types
class TextAd(AdBase):
    """ A most basic, text based advert """
    content = models.TextField(_('Content'))
    
    class Meta:
        verbose_name = _('Text Ad')
        verbose_name_plural = _('Text Ads')

class BannerAd(AdBase):
    """ A standard banner Ad """
    content = models.ImageField(_('Content'), upload_to='adzone/bannerads/')
    
    class Meta:
        verbose_name = _('Banner Ad')
        verbose_name_plural = _('Banner Ads')
