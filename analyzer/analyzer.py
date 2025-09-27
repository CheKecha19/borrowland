# analyzer/analyzer.py
def calculate_net_apr(borrow_apr, staking_apr, fees=0.0):
    """
    Все APR — в процентах.
    fees — суммарная оценка годовых потерь в процентах (комиссии, слиппейдж, cost of withdraw)
    """
    return staking_apr - borrow_apr - fees

def find_opportunities(borrow_list, staking_list, min_net_apr=0.0, fee_estimate=0.2):
    """
    borrow_list: [{'exchange','asset','apr',...}, ...]
    staking_list: [{'source','asset','apr','type',...}, ...]
    Возвращает список opportunities с net_apr > min_net_apr
    """
    opps = []
    # index staking by asset for speed
    from collections import defaultdict
    staking_by_asset = defaultdict(list)
    for s in staking_list:
        staking_by_asset[s["asset"].upper()].append(s)

    for b in borrow_list:
        asset = b["asset"].upper()
        if asset not in staking_by_asset:
            continue
        for s in staking_by_asset[asset]:
            net = calculate_net_apr(b.get("apr",0.0), s.get("apr",0.0), fees=fee_estimate)
            if net >= min_net_apr:
                opps.append({
                    "asset": asset,
                    "borrow_source": b.get("exchange"),
                    "borrow_apr": b.get("apr"),
                    "staking_source": s.get("source"),
                    "staking_apr": s.get("apr"),
                    "staking_type": s.get("type"),
                    "net_apr": round(net, 6)
                })
    return sorted(opps, key=lambda x: x["net_apr"], reverse=True)
