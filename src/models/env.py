from uvicrocketpy import Environment

def build_env():
    env = Environment(
        latitude=48.5,
        longitude=-123.3,
        elevation=0
    )
    env.set_date((2025, 9, 12, 12))  # year, month, day, hour
    return env