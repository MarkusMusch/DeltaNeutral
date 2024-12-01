import pytest
from unittest.mock import patch, MagicMock
from dash import dcc
import dash_mantine_components as dmc
from backend.models.models_orm import Symbol

# frontend/src/callbacks/test_load_carousel_callback.py


from frontend.src.callbacks.load_carousel_callback import (
    generate_carousel_strategy,
    update_basis_trade,
    handle_tab_switch_basis_trade
)


@pytest.fixture
def mock_symbol():
    return Symbol.BTCUSDT


@pytest.fixture
def mock_data():
    return {"active_carousel": 0}


@pytest.fixture
def mock_generate_graph():
    with patch('frontend.src.callbacks.load_carousel_callback.generate_graph') as mock_graph:
        yield mock_graph


@pytest.fixture
def mock_load_data_cumulative_funding():
    with patch('frontend.src.callbacks.load_carousel_callback.load_data_cumulative_funding') as mock_load:
        yield mock_load


@pytest.fixture
def mock_load_data_funding_rates():
    with patch('frontend.src.callbacks.load_carousel_callback.load_data_funding_rates') as mock_load:
        yield mock_load


@pytest.fixture
def mock_load_data_cumulative_funding_leveraged():
    with patch('frontend.src.callbacks.load_carousel_callback.load_data_cumulative_funding_leveraged') as mock_load:
        yield mock_load


@pytest.fixture
def mock_load_data_funding_rates_leveraged():
    with patch('frontend.src.callbacks.load_carousel_callback.load_data_funding_rates_leveraged') as mock_load:
        yield mock_load


@pytest.fixture
def mock_load_data_net_income_leveraged():
    with patch('frontend.src.callbacks.load_carousel_callback.load_data_net_income_leveraged') as mock_load:
        yield mock_load


def test_generate_carousel_strategy_regular(
    mock_symbol,
    mock_data,
    mock_generate_graph,
    mock_load_data_cumulative_funding,
    mock_load_data_funding_rates
):
    mock_load_data_cumulative_funding.return_value = ([], [])
    mock_load_data_funding_rates.return_value = ([], [])

    slides, data = generate_carousel_strategy('regular', mock_symbol, 0, mock_data)
    assert len(slides) == 2
    assert isinstance(slides[0], dmc.CarouselSlide)
    assert data['active_carousel'] == 0

    slides, data = generate_carousel_strategy('regular', mock_symbol, 1, mock_data)
    assert len(slides) == 2
    assert isinstance(slides[1], dmc.CarouselSlide)
    assert data['active_carousel'] == 1


def test_generate_carousel_strategy_leveraged(
    mock_symbol,
    mock_data,
    mock_generate_graph,
    mock_load_data_cumulative_funding_leveraged,
    mock_load_data_funding_rates_leveraged,
    mock_load_data_net_income_leveraged
):
    mock_load_data_cumulative_funding_leveraged.return_value = ([], [])
    mock_load_data_funding_rates_leveraged.return_value = ([], [])
    mock_load_data_net_income_leveraged.return_value = ([], [])

    slides, data = generate_carousel_strategy('leveraged', mock_symbol, 0, mock_data)
    assert len(slides) == 3
    assert isinstance(slides[0], dmc.CarouselSlide)
    assert data['active_carousel'] == 0

    slides, data = generate_carousel_strategy('leveraged', mock_symbol, 1, mock_data)
    assert len(slides) == 3
    assert isinstance(slides[1], dmc.CarouselSlide)
    assert data['active_carousel'] == 1

    slides, data = generate_carousel_strategy('leveraged', mock_symbol, 2, mock_data)
    assert len(slides) == 3
    assert isinstance(slides[2], dmc.CarouselSlide)
    assert data['active_carousel'] == 2


def test_update_basis_trade(
    mock_symbol,
    mock_data,
    mock_generate_graph,
    mock_load_data_cumulative_funding,
    mock_load_data_funding_rates,
    mock_load_data_cumulative_funding_leveraged,
    mock_load_data_funding_rates_leveraged,
    mock_load_data_net_income_leveraged
):
    mock_load_data_cumulative_funding.return_value = ([], [])
    mock_load_data_funding_rates.return_value = ([], [])
    mock_load_data_cumulative_funding_leveraged.return_value = ([], [])
    mock_load_data_funding_rates_leveraged.return_value = ([], [])
    mock_load_data_net_income_leveraged.return_value = ([], [])

    slides, data = update_basis_trade(0, mock_data, mock_symbol, {'type': 'regular'})
    assert len(slides) == 2
    assert isinstance(slides[0], dmc.CarouselSlide)
    assert data['active_carousel'] == 0

    slides, data = update_basis_trade(1, mock_data, mock_symbol, {'type': 'leveraged'})
    assert len(slides) == 3
    assert isinstance(slides[1], dmc.CarouselSlide)
    assert data['active_carousel'] == 1


def test_handle_tab_switch_basis_trade(
    mock_symbol,
    mock_data,
    mock_generate_graph,
    mock_load_data_cumulative_funding,
    mock_load_data_funding_rates,
    mock_load_data_cumulative_funding_leveraged,
    mock_load_data_funding_rates_leveraged,
    mock_load_data_net_income_leveraged
):
    mock_load_data_cumulative_funding.return_value = ([], [])
    mock_load_data_funding_rates.return_value = ([], [])
    mock_load_data_cumulative_funding_leveraged.return_value = ([], [])
    mock_load_data_funding_rates_leveraged.return_value = ([], [])
    mock_load_data_net_income_leveraged.return_value = ([], [])

    slides = handle_tab_switch_basis_trade(mock_symbol, mock_data, {'type': 'regular'})
    assert len(slides) == 2
    assert isinstance(slides[0], dmc.CarouselSlide)

    slides = handle_tab_switch_basis_trade(mock_symbol, mock_data, {'type': 'leveraged'})
    assert len(slides) == 3
    assert isinstance(slides[0], dmc.CarouselSlide)