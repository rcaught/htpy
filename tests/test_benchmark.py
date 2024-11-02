from pathlib import Path
from typing import Any

import pytest
from django.template import Context
from django.template import Template as DjangoTemplate
from jinja2 import Template as JinjaTemplate

from htpy import table, tbody, td, th, thead, tr

django_jinja_template = (
    "<table><thead><tr><th>Row #</th></tr></thead><tbody>"
    "{% for row in rows %}<tr><td>{{ row }}</td></tr>{% endfor %}"
    "</tbody></table>"
)

benchmarks_output_50_000: str = (
    Path(__file__).parent.joinpath("fixtures/output_50_000.html").read_text()
)

ROWS = list(range(50_000))


@pytest.mark.benchmark(cprofile=True, group=__file__)
def test_benchmark_htpy(benchmark: Any) -> None:
    def run(rows: list[int]) -> str:
        return str(table[thead[tr[th["Row #"]]], tbody[(tr[td[str(row)]] for row in rows)]])

    result = benchmark(run, ROWS)

    assert result == benchmarks_output_50_000


@pytest.mark.third_party
@pytest.mark.benchmark(group=__file__)
def test_benchmark_django(benchmark: Any, django_env: Any) -> None:
    result = benchmark(
        DjangoTemplate(django_jinja_template).render,
        Context({"rows": ROWS}),
    )

    assert result == benchmarks_output_50_000


@pytest.mark.third_party
@pytest.mark.benchmark(group=__file__)
def test_benchmark_jinja2(benchmark: Any) -> None:
    result = benchmark(
        JinjaTemplate(django_jinja_template).render,
        rows=ROWS,
    )

    assert result == benchmarks_output_50_000
