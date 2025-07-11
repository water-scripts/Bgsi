import sys
import math
import random

# Constants for End City generation
CHUNK_STEP = 20  # End Cities generate every 20 chunks (320 blocks)
CHUNK_SIZE = 16
CITY_RADIUS = 250_000  # Default search radius in blocks


def get_end_city_candidates(seed, center_x, center_z, radius=CITY_RADIUS):
    """
    Returns a list of (x, z) coordinates for possible End City locations within the given radius.
    This matches the logic of Chunkbase/Seed Map with 'Show All' enabled (no biome checks).
    """
    candidates = []
    # Convert block coordinates to chunk coordinates
    min_chunk_x = (center_x - radius) // CHUNK_SIZE
    max_chunk_x = (center_x + radius) // CHUNK_SIZE
    min_chunk_z = (center_z - radius) // CHUNK_SIZE
    max_chunk_z = (center_z + radius) // CHUNK_SIZE

    for chunk_x in range(min_chunk_x, max_chunk_x + 1):
        for chunk_z in range(min_chunk_z, max_chunk_z + 1):
            # Only check chunks that are multiples of 20
            if chunk_x % CHUNK_STEP != 0 or chunk_z % CHUNK_STEP != 0:
                continue
            # End City placement uses a random offset within the 20x20 chunk region
            region_x = chunk_x // CHUNK_STEP
            region_z = chunk_z // CHUNK_STEP
            rnd = random.Random()
            rnd.seed((region_x * 341873128712 + region_z * 132897987541) ^ seed)
            offset_x = rnd.randint(0, 8)
            offset_z = rnd.randint(0, 8)
            city_chunk_x = region_x * CHUNK_STEP + 8 + offset_x
            city_chunk_z = region_z * CHUNK_STEP + 8 + offset_z
            city_x = city_chunk_x * CHUNK_SIZE + 9
            city_z = city_chunk_z * CHUNK_SIZE + 9
            # Only include if within radius
            dx = city_x - center_x
            dz = city_z - center_z
            if dx * dx + dz * dz <= radius * radius:
                candidates.append((city_x, city_z))
    return candidates


def main():
    print("Input seed:", end=' ')
    seed = int(input().strip())
    print("Input X:", end=' ')
    center_x = int(input().strip())
    print("Input Z:", end=' ')
    center_z = int(input().strip())
    radius = CITY_RADIUS

    print(f"Finding End Cities for seed {seed} within {radius} blocks of ({center_x}, {center_z})...")
    cities = get_end_city_candidates(seed, center_x, center_z, radius)
    print(f"Found {len(cities)} possible End City locations:")
    for x, z in cities:
        print(f"End City at X: {x}, Z: {z}")

if __name__ == "__main__":
    main()