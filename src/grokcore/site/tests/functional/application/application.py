"""
An application is a mixin for grok application objects.

You can get the current application by using the
grok.getApplication() function. Typically this will return the same
object as grok.getSite(), but it is possible to have sub-Site objects
which will be returned for grok.getSite(), where-as grok.getApplication
will walk up the tree until it reaches the top-level site object.

Let's create an application, then get it using grok.getApplication():

  >>> import grokcore.site
  >>> import zope.component.hooks
  >>> root = getRootFolder()

  >>> app = grokcore.site.util.create_application(Cave, root, 'mycave')
  >>> root['cave'] = app
  >>> zope.component.hooks.setSite(app)
  >>> grokcore.site.getApplication()
  <grokcore.site.tests.functional.application.application.Cave object at ...>

Or get it using getSite():

  >>> from zope.component.hooks import getSite
  >>> getSite()
  <grokcore.site.tests.functional.application.application.Cave object at ...>

Now we can create a container with a sub-site. When we call grok.getSite()
we'll get the box:

  >>> root['cave']['box'] = WoodBox()
  >>> zope.component.hooks.setSite(root['cave']['box'])
  >>> getSite()
  <grokcore.site.tests.functional.application.application.WoodBox object at ...>

But when we call grokcore.site.util.getApplication() we get the cave:

  >>> grokcore.site.getApplication()
  <grokcore.site.tests.functional.application.application.Cave object at ...>

If you try to create an application that is not valid it will fail:

  >>> grokcore.site.util.create_application(object(), root, 'myobject')
  Traceback (most recent call last):
    ...
  zope.schema._bootstrapinterfaces.WrongType: ...

"""
import grokcore.content
import grokcore.site


class Cave(grokcore.content.Container, grokcore.site.Application):
    """A shelter for homeless cavemen.
    """


class WoodBox(grokcore.content.Container, grokcore.site.Site):
    """A prehistoric container for holding ZCA registries.
    """
