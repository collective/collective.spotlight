from five import grok
from zope import schema
from plone.directives import form
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.spotlight import _

styles_portlet = SimpleVocabulary(
    [SimpleTerm(value=u'0', title=_(u'image and title')),
     SimpleTerm(value=u'1', title=_(u'title')),
     SimpleTerm(value=u'2', title=_(u'image and title and description'))]
    )


class ISpotlightFolder(form.Schema):
    """A container for spotlight
    """

    display_portlet = schema.Choice(
            title=_(u"Display the portlet"),
            description=_(u"Choose which display box fits the content that will be inserted."),
            vocabulary=styles_portlet,
            required=True,
    )
