import pytest
from django.forms.utils import ErrorList
from django.template import Context, Template
from django.utils.html import escape as django__escape
from django.utils.safestring import SafeString as django__SafeString

from htpy import div, li, ul

pytestmark = pytest.mark.usefixtures("django_env")


def test_template_injection() -> None:
    t = Template("<ul>{{ stuff }}</ul>")
    result = t.render(Context({"stuff": li["I am safe!"]}))

    assert result == "<ul><li>I am safe!</li></ul>"


def test_SafeString() -> None:
    result = ul[django__SafeString("<li>hello</li>")]
    assert str(result) == "<ul><li>hello</li></ul>"


def test_explicit_escape() -> None:
    result = ul[django__escape("<hello>")]
    assert str(result) == "<ul>&lt;hello&gt;</ul>"


def test_errorlist() -> None:
    result = div[ErrorList(["my error"])]
    assert str(result) == """<div><ul class="errorlist"><li>my error</li></ul></div>"""