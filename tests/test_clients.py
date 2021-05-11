from unittest import mock

import pytest

from dps_optimizer.clients import RaiderIoClient
from dps_optimizer.exceptions import ParseError

pytestmark = pytest.mark.asyncio


@pytest.fixture
def raiderio_client_params():
    return {
        "url": "https://raider.io/{class_}",
        "timeout": 10,
        "headers": {},
    }


@mock.patch("aiohttp.client.ClientSession.get")
async def test_raiderio_client_get_top_scores_successful(
    mocked_get_request,
    raiderio_client_params,
):
    def parse(content):
        return f"parsed: {content}"

    mocked_get_request.return_value.__aenter__.return_value.read.return_value = (
        b"raider.io response content"
    )

    raiderio_client = RaiderIoClient(parse_function=parse, **raiderio_client_params)
    process_result = await raiderio_client.get_top_scores(class_="rogue")
    assert process_result == "parsed: raider.io response content"
    mocked_get_request.assert_called_once_with(
        "https://raider.io/rogue",
        headers={},
    )


@mock.patch("aiohttp.client.ClientSession.get")
async def test_raiderio_client_get_top_scores_with_some_parse_fail(
    mocked_get_request,
    raiderio_client_params,
):
    def parse_with_fail(content: str) -> str:
        raise TypeError("deu ruim!")

    mocked_get_request.return_value.__aenter__.return_value.read.return_value = (
        b"raider.io response content"
    )

    raiderio_client = RaiderIoClient(
        parse_function=parse_with_fail, **raiderio_client_params
    )

    with pytest.raises(ParseError):
        await raiderio_client.get_top_scores(class_="rogue")


@mock.patch("aiohttp.client.ClientSession.get")
async def test_raiderio_client_get_top_scores_with_some_http_error(
    mocked_get_request,
    raiderio_client_params,
):
    def parse(content):
        return f"parsed: {content}"

    mocked_get_request.return_value.__aenter__.side_effect = TimeoutError
    tj_client = RaiderIoClient(parse_function=parse, **raiderio_client_params)

    with pytest.raises(TimeoutError):
        await tj_client.get_top_scores(class_="rogue")
