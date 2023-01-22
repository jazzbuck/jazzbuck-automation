# utf-8

import pytest
from ..retrieve_pocket import *


class TestWritePocketDataToMarkdown:
    @pytest.fixture
    def pocket_dict(self):
        return {
            "balthazar": {
                "resolved_title": "resolved",
                "title": "title",
                "given_title": "given title",
                "time_added": "1674386246",
                "resolved_url": "https://dis.repair",
                "excerpt": "this is an excerpt",
            },
            "balthazar2": {
                "resolved_title": "resolved2",
                "title": "title2",
                "given_title": "given_title2",
                "time_added": "1674386247",
                "resolved_url": "https://google.com",
                "excerpt": "this is not an excerpt",
            },
        }

    def test_full(self, pocket_dict):
        list_of_markdown = write_pocket_data_to_markdown(pocket_dict=pocket_dict)

        assert list_of_markdown[0][0] == "202301221117-Resolved"
        assert (
            list_of_markdown[0][1]
            == """---
id: 202301221117
aliases: ["202301221117","resolved"]
---
#reading-inbox

# resolved

https://dis.repair

this is an excerpt"""
        )
        assert len(list_of_markdown) == 2
        assert len(list_of_markdown[1]) == 2
        assert type(list_of_markdown[1]) == tuple

    def test_no_resolved_title(self, pocket_dict):
        no_rt = pocket_dict
        no_rt["balthazar"].pop("resolved_title")

        list_of_markdown = write_pocket_data_to_markdown(no_rt)

        assert list_of_markdown[0][0] == "202301221117-GivenTitle"
        assert (
            list_of_markdown[0][1]
            == """---
id: 202301221117
aliases: ["202301221117","given title"]
---
#reading-inbox

# given title

https://dis.repair

this is an excerpt"""
        )
        assert len(list_of_markdown) == 2

    def test_no_titles(self, pocket_dict):
        no_tit = pocket_dict
        no_tit["balthazar"].pop("resolved_title")
        no_tit["balthazar"].pop("given_title")

        try:
            list_of_markdown = write_pocket_data_to_markdown(no_tit)
        except KeyError as exc:
            assert False, f"no title raised an exception {exc}"

    def test_no_date(self, pocket_dict):
        no_date = pocket_dict
        no_date["balthazar"].pop("time_added")

        try:
            list_of_markdown = write_pocket_data_to_markdown(no_date)
        except KeyError as exc:
            assert False, f"no date raised an exception {exc}"

        assert len(list_of_markdown) == 2
