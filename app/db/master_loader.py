from db.models import Country, Race

def load_master(db):

    if db.query(Country).count() > 0:
        return  # 既にある

    # 国
    jp = Country(name="Japan", climate="temperate", track_bias="speed")
    us = Country(name="USA", climate="dry", track_bias="speed")

    db.add_all([jp, us])
    db.flush()

    # レース
    races = [
        Race(name="Tokyo Cup", country_id=jp.country_id, grade="G1", distance=2400),
        Race(name="Osaka Mile", country_id=jp.country_id, grade="G2", distance=1600),
    ]

    db.add_all(races)