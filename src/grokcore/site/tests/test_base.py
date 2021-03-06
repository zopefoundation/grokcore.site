import doctest
import re
import unittest
from pkg_resources import resource_listdir

from zope.testing import cleanup, renormalizing
import zope.component.eventtesting

checker = renormalizing.RENormalizing([
    # str(Exception) has changed from Python 2.4 to 2.5 (due to
    # Exception now being a new-style class).  This changes the way
    # exceptions appear in traceback printouts.
    (re.compile(
        r"ConfigurationExecutionError: <class '([\w.]+)'>:"),
        r'ConfigurationExecutionError: \1:')])


def setUpZope(test):
    zope.component.eventtesting.setUp(test)


def cleanUpZope(test):
    cleanup.cleanUp()


def suiteFromPackage(name):
    layer_dir = 'base'
    files = resource_listdir(__name__, '{}/{}'.format(layer_dir, name))
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename.endswith('_fixture.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'grokcore.site.tests.%s.%s.%s' % (
            layer_dir, name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            setUp=setUpZope,
            tearDown=cleanUpZope,
            checker=checker,
            optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)

        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ['utility', 'application']:
        suite.addTest(suiteFromPackage(name))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
