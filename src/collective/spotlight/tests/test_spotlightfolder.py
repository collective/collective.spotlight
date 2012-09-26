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
        self.assertTrue(ISpotlightFolder.providedBy(self.folder))
        self.assertTrue(verifyObject(ISpotlightFolder, self.folder))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.spotlight.spotlightfolder')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.spotlight.spotlightfolder')
        schema = fti.lookupSchema()
        self.assertEquals(ISpotlightFolder, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.spotlight.spotlightfolder')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(ISpotlightFolder.providedBy(new_object))

    def _edit_spotlightfolder(self, obj):
        dcEdit(obj)
        obj.setTitle("Spotlight folder")
        obj.setDescription("Description Spotlight folder")
        obj.display_portlet = 1
        notify(ObjectModifiedEvent(obj))

    def test_edit(self):
        new = self.folder
        self._edit_spotlightfolder(new)
        self.assertEqual(new.display_portlet, 1)
