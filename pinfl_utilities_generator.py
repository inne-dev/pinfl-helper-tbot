"""Random PINFL generation module."""

import random


class PinflUtilitiesGenerator:
    """Random PINFL generation."""

    def generate(self, gender, birth_date):
        """PINFL generation function."""
        return self.generate_custom(gender, birth_date)

    def generate_custom(self, gender, birth_date, area_code=None, serial_number=None):
        """Generate PINFL with optional custom area code and serial number."""
        century = str(self._gender_date_index(gender, birth_date))
        month = str(birth_date.month).zfill(2)
        day = str(birth_date.day).zfill(2)
        decade = str(birth_date.year % 100).zfill(2)

        if area_code is None:
            area_code = random.randint(1, 999)
        if serial_number is None:
            serial_number = random.randint(1, 999)

        area_code_text = self._normalize_three_digit_value(area_code, "area code")
        serial_number_text = self._normalize_three_digit_value(
            serial_number, "serial number"
        )

        digits = [
            str(digit)
            for digit in century + day + month + decade + area_code_text + serial_number_text
        ]

        check_digit = self._calculate_check_digit(digits)
        return "".join(digits) + str(check_digit)

    def generate_pinfl(self, gender, birth_date):
        """Generate PINFL."""

        return self.generate(gender, birth_date)

    def _gender_date_index(self, gender, birth_date):
        gender_shift_number = 1 if gender == "female" else 0
        return (birth_date.year // 100) - 17 + gender_shift_number

    def _calculate_check_digit(self, digits):
        weight_func = [7, 3, 1, 7, 3, 1, 7, 3, 1, 7, 3, 1, 7]
        sum_digits = sum(
            int(digit) * weight for digit, weight in zip(digits, weight_func)
        )
        return sum_digits % 10

    def _normalize_three_digit_value(self, value, field_name):
        text_value = str(value).strip()
        if not text_value.isdigit():
            raise ValueError(f"Invalid {field_name}: {value}")

        number = int(text_value)
        if number < 1 or number > 999:
            raise ValueError(f"Invalid {field_name}: {value}")

        return str(number).zfill(3)
