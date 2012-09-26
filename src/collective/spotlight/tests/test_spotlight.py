# -*- coding: utf-8 -*-

import unittest2 as unittest

from AccessControl import Unauthorized

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import logout
from Products.ATContentTypes.tests.utils import dcEdit

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.interface.verify import verifyObject

from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID

from collective.spotlight.content.spotlightfolder import ISpotlightFolder
from collective.spotlight.content.spotlight import ISpotlight
from collective.spotlight.content.spotlight import Spotlight

from collective.spotlight.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('collective.spotlight.spotlightfolder', 'spotlight-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['spotlight-folder']

    def test_adding(self):
        self.folder.invokeFactory('collective.spotlight.spotlight', 'spotlight')
        spl1 = self.folder['spotlight']
        self.assertTrue(ISpotlight.providedBy(spl1))
        self.assertTrue(verifyObject(ISpotlight, spl1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.spotlight.spotlight')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.spotlight.spotlight')
        schema = fti.lookupSchema()
        self.assertEquals(ISpotlight, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.spotlight.spotlight')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(ISpotlight.providedBy(new_object))

    def _edit_spotlight(self, obj):
        dcEdit(obj)
        obj.setTitle("Spotlight")
        obj.setDescription("Description Spotlight")
        notify(ObjectModifiedEvent(obj))

    def test_edit(self):
        self.folder.invokeFactory('collective.spotlight.spotlight', 'spl1')
        spl1 = self.folder['spl1']
        self._edit_spotlight(spl1)
        #self.assertEqual(new.display_portlet, 1)
