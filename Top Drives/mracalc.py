from math import floor, log10

def mra_calc():
    """
    Calculates the MRA with uncertainty.
    MRA = (0-60) / (60-100) * 100
    """
    # 0-60 time
    accel_60 = float(input("Enter 0-60 time:\n"))
    accel_60_unc = 0.05
    accel_60_unc_rel = accel_60_unc / accel_60
    # 0-100 time
    accel_100 = float(input("Enter 0-100 time:\n"))
    accel_100_unc = 0.005
    # 60-100 time
    accel_60_100 = accel_100 - accel_60
    accel_60_100_unc = accel_60_unc + accel_100_unc
    accel_60_100_unc_rel = accel_60_100_unc / accel_60_100
    # MRA
    mra = accel_60 / accel_60_100 * 100
    mra_unc_rel = accel_60_unc_rel + accel_60_100_unc_rel
    mra_unc = mra_unc_rel * mra
    # The uncertainty must only have one SF
    # Find which decimal place to round the values to
    place = -int(floor(log10(abs(mra_unc))))
    mra_rounded = round(mra, place)
    mra_unc_rounded = round(mra_unc, place)
    # Display as integer if applicable
    # Positive place values correspond to decimal places
    if place <= 0:
        mra_rounded = int(mra_rounded)
        mra_unc_rounded = int(mra_unc_rounded)
    print(f"MRA: {mra_rounded} ± {mra_unc_rounded}")


mra_calc()
