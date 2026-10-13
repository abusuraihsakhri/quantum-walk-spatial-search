"""Regression tests for the exact complete-graph continuous-time search model."""
import math

import pytest

from quantum_walk.search import simulate_complete_graph, main


@pytest.mark.parametrize('nodes', [2, 3, 16, 64, 256, 1000])
def test_optimal_search_exact(nodes):
    result = simulate_complete_graph(node_count=nodes, marked_vertex=nodes - 1)
    assert result['initial_probability'] == pytest.approx(1 / nodes)
    assert result['series'][0]['success_probability'] == pytest.approx(1 / nodes)
    assert result['peak_time'] == pytest.approx(math.pi * math.sqrt(nodes) / 2)
    assert result['peak_success_probability'] == pytest.approx(1, abs=1e-12)
    assert all(0 <= x['success_probability'] <= 1 for x in result['series'])


def test_detuned_gamma_decreases_success():
    assert simulate_complete_graph(16, gamma=0.2)['peak_success_probability'] < 0.5


@pytest.mark.parametrize('kwargs', [
    {'node_count': 1}, {'node_count': 2.5}, {'node_count': True},
    {'node_count': 4, 'marked_vertex': 4}, {'marked_vertex': -1},
    {'gamma': 0}, {'gamma': float('nan')}, {'gamma': float('inf')},
    {'max_time': -1}, {'max_time': float('nan')}, {'max_time': 100001},
    {'samples': 1}, {'samples': 2002},
])
def test_invalid_parameters(kwargs):
    with pytest.raises(ValueError):
        simulate_complete_graph(**kwargs)


def test_csv_and_cli(tmp_path):
    path = tmp_path / 'probabilities.csv'
    assert main(['--nodes', '4', '--marked', '3', '--samples', '3', '--csv', str(path)]) == 0
    lines = path.read_text().strip().splitlines()
    assert len(lines) == 4
    assert lines[0] == 'time,success_probability'


def test_api(app_client):
    response = app_client.post('/api/quantum/search', json={'node_count':16, 'marked_vertex': 0, 'samples': 5})
    assert response.status_code == 200
    assert response.json()['peak_success_probability'] == pytest.approx(1)
    assert len(response.json()['series']) == 5
    assert app_client.post('/api/quantum/search', json={'node_count':1}).status_code == 422


@pytest.fixture
def app_client():
    from fastapi.testclient import TestClient
    from agents.api import app
    return TestClient(app)
