from five import grok
from zope import schema
from plone.directives import form
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.spotlight import _

styles = SimpleVocabulary(
    [SimpleTerm(value=u'0', title=_(u'Display with image and title')),
     SimpleTerm(value=u'1', title=_(u'Display with title')),
     SimpleTerm(value=u'2', title=_(u'Display with image and title and description'))]
    )


class ISpotlightFolder(form.Schema):
    """A container for spotlight
    """

    display = schema.Choice(
            title=_(u"Display the box"),
            description=_(u"Choose which display box fits the content that will be inserted."),
            vocabulary=styles,
            required=True,
    )
