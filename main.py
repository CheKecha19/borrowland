# main.py (обрезанный под OKX)
from db.database import engine, SessionLocal
from db.models import Base, BorrowRate, StakingRate
from collectors import okx
from analyzer.analyzer import find_opportunities
from datetime import datetime

def init_db():
    Base.metadata.create_all(bind=engine)

def save_borrow_rates(session, borrow_rows):
    for r in borrow_rows:
        session.add(BorrowRate(
            exchange=r["exchange"],
            asset=r["asset"].upper(),
            apr=r["apr"],
            timestamp=r["timestamp"]
        ))
    session.commit()

def save_staking_rates(session, staking_rows):
    for r in staking_rows:
        session.add(StakingRate(
            source=r["source"],
            asset=r["asset"].upper(),
            apr=r["apr"],
            type=r["type"],
            timestamp=r["timestamp"]
        ))
    session.commit()

def main():
    init_db()
    session = SessionLocal()

    # собираем только OKX
    borrow = okx.get_okx_borrow_rates()
    staking = okx.get_okx_staking_rates()

    if borrow:
        save_borrow_rates(session, borrow)
    if staking:
        save_staking_rates(session, staking)

    # готовим к анализу
    b = [{"exchange": r.exchange, "asset": r.asset, "apr": r.apr} for r in session.query(BorrowRate).all()]
    s = [{"source": r.source, "asset": r.asset, "apr": r.apr, "type": r.type} for r in session.query(StakingRate).all()]

    opps = find_opportunities(b, s, min_net_apr=0.1, fee_estimate=0.2)

    if not opps:
        print("No profitable opportunities found.")
    else:
        print("Opportunities:")
        for o in opps:
            print(o)

if __name__ == "__main__":
    main()
