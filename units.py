from enum import Enum

class UnitType(Enum):
    LENGTH = "length"
    MASS = "mass"
    TIME = "time"
    TEMPERATURE = "temperature"
    SPEED = "speed"
    CURRENCY = "currency"

# Base units (SI units)
BASE_UNITS = {
    UnitType.LENGTH: 'meter',
    UnitType.MASS: 'kilogram',
    UnitType.TIME: 'second',
    UnitType.TEMPERATURE: 'kelvin',
    UnitType.SPEED: 'meter_per_second',
    UnitType.CURRENCY: 'usd'  # Using USD as base currency
}

# Conversion factors to base units
CONVERSION_FACTORS = {
    # Length
    'meter': 1.0,
    'kilometer': 1000.0,
    'centimeter': 0.01,
    'millimeter': 0.001,
    'mile': 1609.344,
    'yard': 0.9144,
    'foot': 0.3048,
    'inch': 0.0254,
    
    # Mass
    'kilogram': 1.0,
    'gram': 0.001,
    'milligram': 0.000001,
    'pound': 0.453592,
    'ounce': 0.0283495,
    'ton': 1000.0,
    
    # Time
    'second': 1.0,
    'minute': 60.0,
    'hour': 3600.0,
    'day': 86400.0,
    'week': 604800.0,
    
    # Temperature (special handling)
    'kelvin': lambda x: x,
    'celsius': lambda x: x + 273.15,
    'fahrenheit': lambda x: (x + 459.67) * 5/9,
    
    # Speed
    'meter_per_second': 1.0,
    'kilometer_per_hour': 0.277778,
    'mile_per_hour': 0.44704,
    
    # Currency (example rates - should be updated dynamically)
    'usd': 1.0,
    'eur': 0.85,
    'gbp': 0.75,
    'jpy': 110.0,
    'inr': 75.0
}

TEMP_REVERSE = {
    'kelvin': {
        'celsius': lambda k: k - 273.15,
        'fahrenheit': lambda k: k * 9/5 - 459.67
    }
}

def is_compatible(unit1, unit2):
    # Implement more sophisticated compatibility checks based on dimensions (length, mass, time, temp)
    # For now, a simple check if they belong to the same general category might suffice initially
    length_units = {'m', 'km', 'miles', 'feet', 'inches', 'cm', 'yards'}
    mass_units = {'kg', 'pounds', 'ounces', 'grams'}
    time_units = {'s', 'min', 'hour', 'day', 'year'}
    temp_units = {'°C', 'Fahrenheit', 'Kelvin'}
    speed_units = {'m/s'}

    if unit1 in length_units and unit2 in length_units:
        return True
    if unit1 in mass_units and unit2 in mass_units:
        return True
    if unit1 in time_units and unit2 in time_units:
        return True
    if unit1 in temp_units and unit2 in temp_units:
        return True
    if unit1 in speed_units and unit2 in speed_units:
        return True
    return False


def get_conversion_factor(from_unit, to_unit):
    """Get the conversion factor between two compatible units"""
    if not is_compatible(from_unit, to_unit):
        raise ValueError(f"Cannot convert between {from_unit} and {to_unit}")
    
    # Handle temperature separately
    if from_unit in ['kelvin', 'celsius', 'fahrenheit']:
        # We need to know we're dealing with temperature
        # This requires special handling in the interpreter
        return (from_unit, to_unit)
    
    # For other units, calculate the factor
    if from_unit == to_unit:
        return 1.0
    
    # Convert from_unit to base unit
    from_factor = CONVERSION_FACTORS[from_unit]
    to_factor = CONVERSION_FACTORS[to_unit]
    
    # If either is a function (like temperature), we need special handling
    if callable(from_factor) or callable(to_factor):
        return (from_unit, to_unit)
    
    return from_factor / to_factor

def normalize_to_base(value, unit):
    """Convert a value to its base unit"""
    if unit in ['celsius', 'fahrenheit']:
        # Convert to kelvin
        return CONVERSION_FACTORS[unit](value)
    elif callable(CONVERSION_FACTORS[unit]):
        # Handle other special cases if any
        return CONVERSION_FACTORS[unit](value)
    else:
        return value * CONVERSION_FACTORS[unit]

def convert_from_base(value, unit):
    """Convert a value from base unit to target unit"""
    if unit in ['celsius', 'fahrenheit']:
        return TEMP_REVERSE['kelvin'][unit](value)
    elif callable(CONVERSION_FACTORS[unit]):
        # Handle other special cases if any
        return CONVERSION_FACTORS[unit](value)
    else:
        return value / CONVERSION_FACTORS[unit]


def convert_value(value, from_unit, to_unit):
    if is_compatible(from_unit, to_unit):
        if from_unit == to_unit:
            return value

        try:
            # Handle temperature conversion
            if from_unit in ['kelvin', 'celsius', 'fahrenheit'] and to_unit in ['kelvin', 'celsius', 'fahrenheit']:
                if from_unit == 'kelvin':
                    kelvin_value = value
                elif from_unit == 'celsius':
                    kelvin_value = normalize_to_base(value, from_unit)
                elif from_unit == 'fahrenheit':
                    kelvin_value = normalize_to_base(value, from_unit)

                if to_unit == 'kelvin':
                    return kelvin_value
                elif to_unit == 'celsius':
                    return convert_from_base(kelvin_value, to_unit)
                elif to_unit == 'fahrenheit':
                    return convert_from_base(kelvin_value, to_unit)
            else:
                # Convert to base unit
                base_value = normalize_to_base(value, from_unit)
                # Convert from base unit to target unit
                return convert_from_base(base_value, to_unit)
        except KeyError:
            print(f"Error: Conversion factor not found for {from_unit} to base or from base to {to_unit}")
            return None
    else:
        print(f"Error: Incompatible units: {from_unit} and {to_unit}")
        return None