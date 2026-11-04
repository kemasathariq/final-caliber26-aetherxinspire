"""Own-history resampling. No distribution is fitted, and every sampled quantity or interval exists in the material's own record.

Common random numbers: block draws are the same for every material in a replication, and for Scenarios A and B. Lead draws are
uniform numbers per material and day, mapped onto each view's own intervals, so views and policies share them. Seeds use
numpy SeedSequence with fixed integer keys, independent of PYTHONHASHSEED.
"""
import numpy as np

from src.simulation import settings as cfg

STREAM_BLOCKS, STREAM_LEADS, STREAM_ESTIMATE_BLOCKS, STREAM_ESTIMATE_WINDOWS, STREAM_FORECAST = 1, 2, 3, 4, 5


def generator(stream: int, *key: int, seed: int = cfg.MASTER_SEED) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence(seed, spawn_key=(stream, *key)))


def material_key(material: str) -> int:
    return int(material) if material.isdigit() else sum((i + 1) * ord(c) for i, c in enumerate(material))


def draw_month_sources(reps: int, n_target: int, n_source: int, rng: np.random.Generator, block: int = cfg.BLOCK_MONTHS) -> np.ndarray:
    """Circular block bootstrap of month indices. Returns reps x n_target source month indices."""
    n_blocks = int(np.ceil(n_target / block))
    starts = rng.integers(0, n_source, size=(reps, n_blocks))
    offsets = np.arange(block)
    sources = (starts[:, :, None] + offsets) % n_source
    return sources.reshape(reps, -1)[:, :n_target]


def day_of_month_table(lines, month_lengths: list[int]) -> np.ndarray:
    """source months x 31 issue quantities by day of month. Lines are (absolute day, quantity)."""
    table = np.zeros((len(month_lengths), 31))
    starts = np.cumsum([0, *month_lengths])
    for day, qty in lines:
        m = int(np.searchsorted(starts, day, side="right") - 1)
        table[m, day - starts[m]] += qty
    return table


def build_daily_paths(table: np.ndarray, sources: np.ndarray, target_lengths: list[int]) -> np.ndarray:
    """reps x days demand. A source line keeps its day of month; a day past the target month's end moves to its last day (design 9.3)."""
    reps = sources.shape[0]
    paths = np.zeros((reps, sum(target_lengths)))
    folded = {}
    for n in set(target_lengths):
        f = table[:, :n].copy()
        f[:, n - 1] += table[:, n:].sum(axis=1)
        folded[n] = f
    offset = 0
    for m, n in enumerate(target_lengths):
        paths[:, offset:offset + n] = folded[n][sources[:, m]]
        offset += n
    return paths


def lead_draws(observations: np.ndarray, uniform: np.ndarray) -> np.ndarray:
    """Map uniform numbers onto a material's sorted promised intervals. Whole days, at least 1 (S-14)."""
    index = np.minimum((uniform * len(observations)).astype(int), len(observations) - 1)
    return np.maximum(np.ceil(observations[index]), 1).astype(int)


def lead_time_demand(paths: np.ndarray, leads: np.ndarray, starts: np.ndarray) -> np.ndarray:
    """Demand over a lead window starting on a resampled day, wrapping circularly around the path. paths: reps x days. leads, starts: reps x windows."""
    reps, days = paths.shape
    cum = np.zeros((reps, days + 1))
    cum[:, 1:] = np.cumsum(paths, axis=1)
    total = cum[:, -1][:, None]
    whole, rest = np.divmod(leads, days)
    end = starts + rest
    wrap = end > days
    row = np.arange(reps)[:, None]
    head = cum[row, np.minimum(end, days)] - cum[row, starts]
    tail = np.where(wrap, cum[row, np.maximum(end - days, 0)], 0.0)
    return whole * total + head + tail
