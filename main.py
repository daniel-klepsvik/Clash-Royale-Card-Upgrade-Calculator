import requests

# --- 1. USER CONFIGURATION ---
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImNlZjI4ZjFjLTgyMTUtNDY1MC1hMDRmLTBmZDI2ZjZlMDJjMCIsImlhdCI6MTc3NDg2MTE4OCwic3ViIjoiZGV2ZWxvcGVyL2QzNDBlZTllLThhMDEtODIzOC02NDY0LTQzOTIyMWUxOWRkNSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxOTMuMTAuMTkxLjEyMiJdLCJ0eXBlIjoiY2xpZW50In1dfQ.6qRaHDsH0IZhK8d4RiOm1C9yBK-yyZV1H315lza6tjaky5-F6hWeDg9uBMj_XrVGETTa1RYIAWuBIS-OpemzYQ"  
PLAYER_TAG = "%238GU9LJGG"     
CARD_TO_CHECK = "Giant Skeleton" 

# --- 2. 2026 UPGRADE DATA ---
UPGRADE_DATA = {
    "COMMON": {
        2:(2,5), 3:(4,20), 4:(10,50), 5:(20,150), 6:(50,400), 7:(100,1000), 
        8:(200,2000), 9:(400,4000), 10:(800,8000), 11:(1000,15000), 
        12:(1500,25000), 13:(2500,40000), 14:(3500,60000), 15:(5500,90000), 16:(7500,120000)
    },
    "RARE": {
        4:(2,50), 5:(4,150), 6:(10,400), 7:(20,1000), 8:(50,2000), 9:(100,4000), 
        10:(200,8000), 11:(300,15000), 12:(400,25000), 13:(550,40000), 
        14:(750,60000), 15:(1000,90000), 16:(1400,120000)
    },
    "EPIC": {
        7:(2,1000), 8:(4,2000), 9:(10,4000), 10:(20,8000), 11:(30,15000), 
        12:(50,25000), 13:(70,40000), 14:(100,60000), 15:(130,90000), 16:(180,120000)
    },
    "LEGENDARY": {
        10:(2,5000), 11:(4,15000), 12:(6,25000), 13:(9,40000), 
        14:(12,60000), 15:(14,90000), 16:(20,120000)
    },
    "CHAMPION": {
        12:(2,25000), 13:(5,40000), 14:(8,60000), 15:(11,90000), 16:(15,120000)
    }
}

def run_calculator():
    url = f"https://api.clashroyale.com/v1/players/{PLAYER_TAG}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error {response.status_code}: Check API Key/IP.")
            return
        
        data = response.json()
        cards = data.get("cards", [])
        card = next((c for c in cards if c["name"].lower() == CARD_TO_CHECK.lower()), None)
        
        if not card:
            print(f"Card '{CARD_TO_CHECK}' not found.")
            return

        # Normalize Level
        rarity_max_map = {"COMMON": 14, "RARE": 12, "EPIC": 9, "LEGENDARY": 6, "CHAMPION": 4}
        rarity = card["rarity"].upper()
        current_level = card["level"] + (14 - rarity_max_map[rarity])
        
        inventory = card["count"]
        target_level = current_level
        total_gold_needed = 0
        temp_inventory = inventory

        # --- CALCULATE UPGRADES ---
        for lv in range(current_level + 1, 17):
            if lv not in UPGRADE_DATA[rarity]: break
            req_cards, req_gold = UPGRADE_DATA[rarity][lv]
            
            if temp_inventory >= req_cards:
                temp_inventory -= req_cards
                total_gold_needed += req_gold
                target_level = lv
            else:
                break

        # --- FINAL FORMATTED OUTPUT ---
        print("-" * 45)
        print(f"CARD: {card['name']} ({rarity})")
        print("-" * 45)
        
        if target_level > current_level:
            # You can jump one or more levels
            print(f"Current Level: {current_level}")
            print(f"Max Reachable Level: {target_level}")
            
            # Find the requirement for the NEXT level after the jump
            next_step_lv = target_level + 1
            if next_step_lv in UPGRADE_DATA[rarity]:
                goal_cards, _ = UPGRADE_DATA[rarity][next_step_lv]
                print(f"Remaining {card['name']} Cards: {temp_inventory} / {goal_cards}")
            else:
                print(f"Remaining {card['name']} Cards: {temp_inventory} (Max Level)")
                
            print(f"Total Gold Cost: {total_gold_needed:,} Gold")
        
        else:
            # You are stuck at current level
            print(f"Current Level: {current_level}")
            next_lv = current_level + 1
            if next_lv in UPGRADE_DATA[rarity]:
                req_cards, next_gold = UPGRADE_DATA[rarity][next_lv]
                print(f"Next Level ({next_lv}) Progress: {inventory} / {req_cards} cards")
                print(f"Total Gold Cost: {next_gold:,} Gold")
            else:
                print("Status: Max Level (16) Reached!")
        print("-" * 45)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_calculator()