import assert from 'node:assert/strict';
import test from 'node:test';
import { simulateCompleteGraph, resultsCsv } from '../web/app.mjs';

test('uniform initial probability and optimal search on K_N', () => {
  for (const n of [2, 3, 16, 64, 1000]) {
    const result = simulateCompleteGraph(n, n - 1);
    assert.ok(Math.abs(result.initial_probability - 1/n) < 1e-12);
    assert.ok(Math.abs(result.series[0].success_probability - 1/n) < 1e-12);
    assert.ok(Math.abs(result.peak_success_probability - 1) < 1e-12);
    assert.ok(Math.abs(result.peak_time - Math.PI*Math.sqrt(n)/2) < 1e-10);
    assert.ok(result.series.every(p => p.success_probability >= 0 && p.success_probability <= 1));
  }
});

test('hopping-rate perturbation changes output', () => {
  const optimal = simulateCompleteGraph(16);
  const detuned = simulateCompleteGraph(16, 0, 0.2);
  assert.ok(detuned.peak_success_probability < optimal.peak_success_probability);
});

test('rejects invalid inputs and exports valid CSV', () => {
  for (const args of [[1], [2, 2], [16, 0, 0], [16, 0, 1e308], [16, 0, Infinity], [16, 0, null, -1], [16, 0, null, null, 1]]) {
    assert.throws(() => simulateCompleteGraph(...args), RangeError);
  }
  const csv = resultsCsv(simulateCompleteGraph(4, 1, null, null, 3));
  assert.equal(csv.trim().split('\n').length, 4);
  assert.match(csv, /^time,success_probability\n/);
});
