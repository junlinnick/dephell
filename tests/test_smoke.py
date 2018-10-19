# project
from dephell.converters.pip import PIPConverter


loader = PIPConverter(lock=False)


def test_one():
    resolver = loader.loads_resolver(content='Django<=1.11')
    resolved = resolver.resolve()
    assert resolved is True
    assert 'django' in resolver.graph


def test_two_different():
    resolver = loader.load_resolver(path='./tests/requirements/django-deal.txt')
    resolved = resolver.resolve()
    assert resolved is True
    assert 'django' in resolver.graph
    assert 'deal' in resolver.graph


def test_unresolved():
    resolver = loader.load_resolver(path='./tests/requirements/django-django.txt')
    resolved = resolver.resolve()
    assert resolved is False


def test_resolution():
    resolver = loader.load_resolver(path='./tests/requirements/scipy-pandas-numpy.txt')
    resolved = resolver.resolve()
    assert resolved is True
    assert 'pandas' in resolver.graph
    assert 'scipy' in resolver.graph
    assert 'numpy' in resolver.graph

    assert str(resolver.graph.get('numpy').group.best_release.version) == '1.15.1'
    print(resolver.graph.get('scipy').group.releases)
    assert str(resolver.graph.get('scipy').group.best_release.version) == '0.19.1'
    assert str(resolver.graph.get('pandas').group.best_release.version) > '0.20.3'


def test_unlocked():
    resolver = loader.load_resolver(path='./tests/requirements/attrs-requests.txt')
    resolved = resolver.resolve()
    assert resolved is True
    assert 'attrs' in resolver.graph
    assert 'requests' in resolver.graph


def test_subpackages():
    # https://github.com/sdispater/poetry#dependency-resolution
    resolver = loader.loads_resolver(content='oslo.utils==1.4.0')
    resolved = resolver.resolve()
    assert resolved is True
    assert 'oslo-utils' in resolver.graph
    assert 'pbr' in resolver.graph
    # assert str(resolver.graph.get('oslo-i18n').group.best_release.version) == '2.1.0'
