import re

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"({self.type}, {self.value}, {self.line}, {self.column})"

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[self.position] if self.position < len(self.source_code) else None
        self.line = 1
        self.column = 1

        self.keywords = {'let', 'convert', 'to', 'in', 'print'}
        self.operators = {'+', '-', '*', '/', '='}
        self.predefined_functions = {
            'convert_length', 'convert_mass', 'convert_time', 'convert_temperature',
            'normalize_unit', 'get_conversion_factor', 'is_compatible',
            'miles_to_km', 'km_to_miles', 'meters_to_feet',
            'feet_to_meters', 'inches_to_cm', 'cm_to_inches', 'yards_to_meters', 'meters_to_yards',
            'pounds_to_kg', 'kg_to_pounds', 'ounces_to_grams', 'grams_to_ounces',
            'celsius_to_fahrenheit', 'fahrenheit_to_celsius', 'kelvin_to_celsius', 'celsius_to_kelvin',
            'seconds_to_minutes', 'minutes_to_seconds', 'hours_to_minutes', 'minutes_to_hours',
            'days_to_hours', 'hours_to_days', 'years_to_days', 'days_to_years',
            'currency_convert', 'calculate_min', 'calculate_max', 'calculate_speed',
            'cal_sum', 'calc_diff', 'calc_div', 'calc_mul',
            'radians_to_degrees', 'degrees_to_radians', 'liters_to_gallons', 'gallons_to_liters',
            'pascal_to_psi', 'psi_to_pascal', 'joules_to_calories', 'calories_to_joules',
            'watts_to_horsepower', 'horsepower_to_watts', 'square_meters_to_square_feet', 'square_feet_to_square_meters'
        }
        self.units = {'m', 'km', 'miles', 'kg', 'pounds', '°C', 'Fahrenheit', 's', 'min', 'hour', 'day', 'year', 'm/s'}

    def advance(self):
        self.position += 1
        self.column += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None

    def peek(self, offset=1):
        peek_position = self.position + offset
        if peek_position < len(self.source_code):
            return self.source_code[peek_position]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
                self.column = 0
            self.advance()

    def number(self):
        start_pos = self.position
        start_col = self.column
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        if result.endswith('.'):
            self.error(f"Invalid number format: {result}")
        if self.current_char is not None and self.current_char.isalpha():
            unit = ''
            while self.current_char is not None and self.current_char.isalpha():
                unit += self.current_char
                self.advance()
            return Token('UNIT_VALUE', (float(result), unit), self.line, start_col)
        return Token('NUMBER', float(result) if '.' in result else int(result), self.line, start_col)

    def identifier(self):
        start_col = self.column
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        if result in self.keywords:
            return Token('KEYWORD', result, self.line, start_col)
        elif result in self.predefined_functions:
            return Token('FUNCTION', result, self.line, start_col)
        else:
            return Token('IDENTIFIER', result, self.line, start_col)

    def unit_value(self, number_token):
        start_col = self.column
        unit = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char in ['/', '*']):
            unit += self.current_char
            self.advance()
        if not unit:
            self.error("Expected a unit after the number.")
        if unit not in self.units:
            self.error(f"Invalid unit: {unit}")
        return Token('UNIT_VALUE', (number_token.value, unit), self.line, start_col)

    def get_next_token(self):
        while self.current_char is not None:
            self.skip_whitespace()

            if self.current_char is None:
                break

            start_line = self.line
            start_col = self.column

            if self.current_char.isdigit() or self.current_char == '.':
                number_token = self.number()
                if self.current_char is not None and (self.current_char.isalnum() or self.current_char in ['/', '*']):
                    return self.unit_value(number_token)
                return number_token
            elif self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            elif self.current_char in self.operators:
                token = Token('OPERATOR', self.current_char, self.line, self.column)
                self.advance()
                return token
            elif self.current_char == ';':
                token = Token('SEMICOLON', self.current_char, self.line, self.column)
                self.advance()
                return token
            elif self.current_char == '(':
                token = Token('LPAREN', self.current_char, self.line, self.column)
                self.advance()
                return token
            elif self.current_char == ')':
                token = Token('RPAREN', self.current_char, self.line, self.column)
                self.advance()
                return token
            elif self.current_char == ',':
                token = Token('COMMA', self.current_char, self.line, self.column)
                self.advance()
                return token
            else:
                self.error(f"Invalid character: {self.current_char}")

        return Token('EOF', None, self.line, self.column)

    def error(self, message):
        raise SyntaxError(f"Lexical error at line {self.line}, column {self.column}: {message}")

def scan(source_code, output_file):
    lexer = Lexer(source_code)
    tokens =[]
    while True:
        try:
            token = lexer.get_next_token()
            tokens.append(token)
            if token.type == 'EOF':
                break
        except SyntaxError as e:
            print(e) # Keep printing to console for debugging
            return str(e) # Return the error message as a string
    with open(output_file, 'w') as f:
        for token in tokens:
            f.write(f"<{token.type}, {token.value}, [Ln: {token.line}, Col: {token.column}]>\n")
    return tokens