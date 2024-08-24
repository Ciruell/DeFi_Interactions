import requests
import time

def get_saucerswap_price(pair):
    response = requests.get('https://api.saucerswap.finance/pools').json()
    for pool in response:
        if (pool['tokenA']['symbol'] == pair[0] and pool['tokenB']['symbol'] == pair[1]) or \
           (pool['tokenA']['symbol'] == pair[1] and pool['tokenB']['symbol'] == pair[0]):
            # Ottieni le riserve dei token
            reserve_tokenA = int(pool['tokenReserveA']) / (10 ** pool['tokenA']['decimals'])
            reserve_tokenB = int(pool['tokenReserveB']) / (10 ** pool['tokenB']['decimals'])
            
            # Calcola il prezzo corretto
            if pool['tokenA']['symbol'] == pair[0]:
                price = reserve_tokenB / reserve_tokenA
            else:
                price = reserve_tokenA / reserve_tokenB
                
            return price

    return None

def monitor_pairs(pairs):
    try:
        while True:
            for pair in pairs:
                price = get_saucerswap_price(pair)
                if price is not None:
                    print(f"Prezzo di {pair[0]}/{pair[1]} su SaucerSwap: {price}")
                else:
                    print(f"Pool {pair[0]}/{pair[1]} non trovato su SaucerSwap")

        # Attendi 10 secondi prima di ripetere il controllo
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrotto dall'utente.")

# Lista delle coppie di token da monitorare
pairs_to_monitor = [
    ('USDC', 'HBAR'),
    ('SAUCE', 'HBAR'),
    ('USDC', 'SAUCE')
]

monitor_pairs(pairs_to_monitor)
