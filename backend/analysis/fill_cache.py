from sentiment_analyzer import analyze_sentiment
from cache_manager import CacheManager
import pandas as pd
import time

DATA_PATH = "../../data"
BATCH_SIZE = 500

cache = CacheManager()
df = pd.read_csv(f"{DATA_PATH}/books_clean.csv")
titles = df['book_title'].dropna().unique().tolist()

print(f"Total de libros: {len(titles)}")
print(f"Total de lotes: {(len(titles) + BATCH_SIZE - 1) // BATCH_SIZE}")

for batch_start in range(0, len(titles), BATCH_SIZE):
    batch = titles[batch_start:batch_start + BATCH_SIZE]
    batch_num = batch_start // BATCH_SIZE
    
    print(f"\n=== Lote {batch_num}: libros {batch_start+1} al {batch_start+len(batch)} ===")
    
    for i, title in enumerate(batch):
        global_i = batch_start + i + 1
        if cache.get_sentiment_profile(title):
            print(f"[{global_i}/{len(titles)}] ⏭️  '{title}' ya está en caché")
            continue
        try:
            print(f"[{global_i}/{len(titles)}] ⏳ Analizando '{title}'...")
            analyze_sentiment(title)
        except ValueError as e:
            print(f"[{global_i}/{len(titles)}] ⚠️  Saltando '{title}': {e}")
        except Exception as e:
            print(f"[{global_i}/{len(titles)}] ❌ Error inesperado en '{title}': {e}")
    
    # Pausa entre lotes (excepto tras el último)
    if batch_start + BATCH_SIZE < len(titles):
        print(f"⏸️  Pausa de 2s antes del siguiente lote...")
        time.sleep(2)

print("\n✅ ¡Todos los lotes completados!")