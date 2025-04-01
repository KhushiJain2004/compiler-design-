from units import get_conversion_factor, normalize_to_base, convert_from_base, is_compatible

# Length conversion functions
def miles_to_km(value):
    return value * 1.60934

def km_to_miles(value):
    return value / 1.60934

def meters_to_feet(value):
    return value * 3.28084

def feet_to_meters(value):
    return value / 3.28084

# Mass conversion functions
def kg_to_pounds(value):
    return value * 2.20462

def pounds_to_kg(value):
    return value / 2.20462

def grams_to_ounces(value):
    return value * 0.035274

def ounces_to_grams(value):
    return value / 0.035274

# Time conversion functions
def hours_to_minutes(value):
    return value * 60

def minutes_to_seconds(value):
    return value * 60

def days_to_hours(value):
    return value * 24

# Temperature conversion functions
def celsius_to_fahrenheit(value):
    return (value * 9/5) + 32

def fahrenheit_to_celsius(value):
    return (value - 32) * 5/9

def celsius_to_kelvin(value):
    return value + 273.15

def kelvin_to_celsius(value):
    return value - 273.15

# Speed conversion functions
def kmh_to_ms(value):
    return value * 0.277778

def ms_to_kmh(value):
    return value / 0.277778

def mph_to_kmh(value):
    return value * 1.60934

def kmh_to_mph(value):
    return value / 1.60934

# General conversion functions
def convert_length(value, from_unit, to_unit):
    factor = get_conversion_factor(from_unit, to_unit)
    if isinstance(factor, tuple):
        # Temperature-like conversion needed
        base_value = normalize_to_base(value, from_unit)
        return convert_from_base(base_value, to_unit)
    return value * factor

def convert_mass(value, from_unit, to_unit):
    return convert_length(value, from_unit, to_unit)  # Same logic

def convert_time(value, from_unit, to_unit):
    return convert_length(value, from_unit, to_unit)  # Same logic

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    
    # Convert to kelvin first
    if from_unit != 'kelvin':
        value = normalize_to_base(value, from_unit)
    
    # Convert from kelvin to target
    if to_unit != 'kelvin':
        value = convert_from_base(value, to_unit)
    
    return value

def normalize_unit(value, unit):
    """Convert value to SI unit"""
    return normalize_to_base(value, unit)

def get_conversion_factor(from_unit, to_unit):
    """Wrapper around the units module function"""
    return get_conversion_factor(from_unit, to_unit)

def is_compatible(unit1, unit2):
    """Wrapper around the units module function"""
    return is_compatible(unit1, unit2)

# Utility functions
def currency_convert(amount, rate):
    return amount * rate

def calculate_min(a, b):
    return min(a, b)

def calculate_max(a, b):
    return max(a, b)

def calculate_speed(distance, time):
    return distance / time

def calculate_sum(*args):
    return sum(args)

def calculate_diff(a, b):
    return a - b

def calculate_mul(a, b):
    return a * b

def calculate_div(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

# Dictionary of all available functions
FUNCTIONS = {
    # Length conversions
    'miles_to_km': miles_to_km,
    'km_to_miles': km_to_miles,
    'meters_to_feet': meters_to_feet,
    'feet_to_meters': feet_to_meters,
    
    # Mass conversions
    'kg_to_pounds': kg_to_pounds,
    'pounds_to_kg': pounds_to_kg,
    'grams_to_ounces': grams_to_ounces,
    'ounces_to_grams': ounces_to_grams,
    
    # Time conversions
    'hours_to_minutes': hours_to_minutes,
    'minutes_to_seconds': minutes_to_seconds,
    'days_to_hours': days_to_hours,
    
    # Temperature conversions
    'celsius_to_fahrenheit': celsius_to_fahrenheit,
    'fahrenheit_to_celsius': fahrenheit_to_celsius,
    'celsius_to_kelvin': celsius_to_kelvin,
    'kelvin_to_celsius': kelvin_to_celsius,
    
    # Speed conversions
    'kmh_to_ms': kmh_to_ms,
    'ms_to_kmh': ms_to_kmh,
    'mph_to_kmh': mph_to_kmh,
    'kmh_to_mph': kmh_to_mph,
    
    # General conversion functions
    'convert_length': convert_length,
    'convert_mass': convert_mass,
    'convert_time': convert_time,
    'convert_temperature': convert_temperature,
    'normalize_unit': normalize_unit,
    'get_conversion_factor': get_conversion_factor,
    'is_compatible': is_compatible,
    
    # Utility functions
    'currency_convert': currency_convert,
    'calculate_min': calculate_min,
    'calculate_max': calculate_max,
    'calculate_speed': calculate_speed,
    'calculate_sum': calculate_sum,
    'calculate_diff': calculate_diff,
    'calculate_mul': calculate_mul,
    'calculate_div': calculate_div
}