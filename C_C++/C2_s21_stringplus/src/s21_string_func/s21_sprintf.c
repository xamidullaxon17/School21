#include "s21_string.h"

// Helper function to parse format specifier
int parse_format_specifier(const char *format, int *pos,
                           FormatSpecifier *spec) {
  int i = *pos + 1;  // Skip the '%'

  // Initialize format specifier
  spec->minus_flag = 0;
  spec->plus_flag = 0;
  spec->space_flag = 0;
  spec->width = 0;
  spec->precision = 0;
  spec->precision_set = 0;
  spec->length_h = 0;
  spec->length_l = 0;

  // Parse flags
  int parsing_flags = 1;
  while (parsing_flags && format[i]) {
    switch (format[i]) {
      case '-':
        spec->minus_flag = 1;
        i++;
        break;
      case '+':
        spec->plus_flag = 1;
        i++;
        break;
      case ' ':
        spec->space_flag = 1;
        i++;
        break;
      default:
        parsing_flags = 0;
        break;
    }
  }

  // Parse width
  while (isdigit(format[i])) {
    spec->width = spec->width * 10 + (format[i] - '0');
    i++;
  }

  // Parse precision
  if (format[i] == '.') {
    i++;
    spec->precision_set = 1;
    while (isdigit(format[i])) {
      spec->precision = spec->precision * 10 + (format[i] - '0');
      i++;
    }
  }

  // Parse length
  if (format[i] == 'h') {
    spec->length_h = 1;
    i++;
  } else if (format[i] == 'l') {
    spec->length_l = 1;
    i++;
  }

  // Check if we have a valid specifier at the end
  char specifier = format[i];
  if (specifier == 'd' || specifier == 'f' || specifier == 'c' ||
      specifier == 's' || specifier == 'u' || specifier == '%') {  // Added 'u'
    *pos = i;  // Update position to the specifier
    return specifier;
  }

  return 0;  // Invalid specifier
}

// Process integer (%d) with formatting
int process_int(char *str, int *length, va_list args, FormatSpecifier *spec) {
  // Get the value based on length modifier
  long value;
  if (spec->length_h) {
    value = (short)va_arg(args, int);
  } else if (spec->length_l) {
    value = va_arg(args, long);
  } else {
    value = va_arg(args, int);
  }

  // Convert to string
  char buffer[32];
  char sign = 0;

  // Handle sign
  if (value < 0) {
    sign = '-';
    value = -value;
  } else if (spec->plus_flag) {
    sign = '+';
  } else if (spec->space_flag) {
    sign = ' ';
  }

  // Convert value to string (in reverse)
  int digit_count = 0;
  if (value == 0) {
    buffer[digit_count++] = '0';
  } else {
    while (value > 0) {
      buffer[digit_count++] = '0' + (value % 10);
      value /= 10;
    }
  }

  // Apply precision if set (minimum number of digits)
  int min_digits = spec->precision_set ? spec->precision : 1;

  // Calculate total length
  int total_len = (digit_count > min_digits) ? digit_count : min_digits;
  if (sign) total_len++;

  // Handle padding and alignment
  int pad_char = ' ';
  int pad_len = spec->width > total_len ? spec->width - total_len : 0;

  // If right-aligned, add padding first
  if (!spec->minus_flag && pad_len > 0) {
    for (int i = 0; i < pad_len; i++) {
      str[(*length)++] = pad_char;
    }
  }

  // Add sign if needed
  if (sign) {
    str[(*length)++] = sign;
  }

  // Add leading zeros for precision
  int leading_zeros = min_digits - digit_count;
  if (leading_zeros > 0) {
    for (int i = 0; i < leading_zeros; i++) {
      str[(*length)++] = '0';
    }
  }

  // Add digits (in correct order)
  for (int i = digit_count - 1; i >= 0; i--) {
    str[(*length)++] = buffer[i];
  }

  // If left-aligned, add padding after
  if (spec->minus_flag && pad_len > 0) {
    for (int i = 0; i < pad_len; i++) {
      str[(*length)++] = pad_char;
    }
  }

  str[*length] = '\0';
  return 0;
}

int process_float(char *str, int *length, va_list args, FormatSpecifier *spec) {
  double value = va_arg(args, double);

  // Default precision is 6 if not specified
  int precision = spec->precision_set ? spec->precision : 6;

  // Handle special cases (NaN, inf)
  if (isnan(value)) {
    const char *nan_str = "nan";
    for (int i = 0; nan_str[i]; i++) {
      str[(*length)++] = nan_str[i];
    }
    str[*length] = '\0';
    return 0;
  } else if (isinf(value)) {
    char sign_char = 0;
    if (value < 0) {
      sign_char = '-';
    } else if (spec->plus_flag) {
      sign_char = '+';
    } else if (spec->space_flag) {
      sign_char = ' ';
    }

    if (sign_char) {
      str[(*length)++] = sign_char;
    }

    const char *inf_str = "inf";
    for (int i = 0; inf_str[i]; i++) {
      str[(*length)++] = inf_str[i];
    }
    str[*length] = '\0';
    return 0;
  }

  // Handle sign
  int negative = signbit(value);
  if (negative) {
    value = -value;
  }

  // Extract integer part
  long long int_part = (long long)value;

  // Extract and round fractional part
  double frac_value = value - (double)int_part;

  // Calculate scaling factor for precision
  double scale = 1.0;
  for (int i = 0; i < precision; i++) {
    scale *= 10.0;
  }

  // Scale and round the fractional part
  long long frac_part = (long long)round(frac_value * scale);

  // Handle carry if rounding causes overflow
  if (frac_part >= (long long)scale) {
    int_part++;
    frac_part = 0;
  }

  // Convert integer part to string (reversed)
  char int_str[64] = {0};
  int int_len = 0;

  if (int_part == 0) {
    int_str[int_len++] = '0';
  } else {
    while (int_part > 0) {
      int_str[int_len++] = '0' + (int_part % 10);
      int_part /= 10;
    }
  }

  // Convert fractional part to string with leading zeros
  char frac_str[64] = {0};
  int frac_digits = 0;

  // Initialize with zeros for all decimal places
  for (int i = 0; i < precision; i++) {
    frac_str[i] = '0';
  }
  frac_digits = precision;

  // Fill in the actual digits
  if (frac_part > 0) {
    int idx = precision - 1;
    while (frac_part > 0 && idx >= 0) {
      frac_str[idx--] = '0' + (frac_part % 10);
      frac_part /= 10;
    }
  }

  // Calculate total length
  int total_length = int_len;
  if (negative || spec->plus_flag || spec->space_flag) total_length++;
  if (precision > 0)
    total_length += 1 + precision;  // For decimal point and fractional digits

  // Calculate padding
  int padding = (spec->width > total_length) ? (spec->width - total_length) : 0;

  // Add padding if right-aligned
  if (!spec->minus_flag && padding > 0) {
    for (int i = 0; i < padding; i++) {
      str[(*length)++] = ' ';
    }
  }

  // Add sign if needed
  if (negative) {
    str[(*length)++] = '-';
  } else if (spec->plus_flag) {
    str[(*length)++] = '+';
  } else if (spec->space_flag) {
    str[(*length)++] = ' ';
  }

  // Add integer part in correct order
  for (int i = int_len - 1; i >= 0; i--) {
    str[(*length)++] = int_str[i];
  }

  // Add decimal point and fractional part if needed
  if (precision > 0) {
    str[(*length)++] = '.';
    for (int i = 0; i < frac_digits; i++) {
      str[(*length)++] = frac_str[i];
    }
  }

  // Add padding if left-aligned
  if (spec->minus_flag && padding > 0) {
    for (int i = 0; i < padding; i++) {
      str[(*length)++] = ' ';
    }
  }

  str[*length] = '\0';
  return 0;
}

// Process character (%c) with formatting
int process_char(char *str, int *length, va_list args, FormatSpecifier *spec) {
  char value = (char)va_arg(args, int);

  // Handle width padding
  int pad_len = spec->width > 1 ? spec->width - 1 : 0;

  // If right-aligned, add padding first
  if (!spec->minus_flag && pad_len > 0) {
    for (int i = 0; i < pad_len; i++) {
      str[(*length)++] = ' ';
    }
  }

  // Add the character
  str[(*length)++] = value;

  // If left-aligned, add padding after
  if (spec->minus_flag && pad_len > 0) {
    for (int i = 0; i < pad_len; i++) {
      str[(*length)++] = ' ';
    }
  }

  str[*length] = '\0';
  return 0;
}

// Process string (%s) with formatting
int process_string(char *str, int *length, va_list args,
                   FormatSpecifier *spec) {
  char *value = va_arg(args, char *);
  if (value == NULL) {
    value = "(null)";
  }

  int str_len = strlen(value);

  // Apply precision limitation if set
  if (spec->precision_set && str_len > spec->precision) {
    str_len = spec->precision;
  }

  // Handle width padding
  int pad_len = spec->width > str_len ? spec->width - str_len : 0;

  // If right-aligned, add padding first
  if (!spec->minus_flag && pad_len > 0) {
    for (int i = 0; i < pad_len; i++) {
      str[(*length)++] = ' ';
    }
  }

  // Add the string with precision limit
  for (int i = 0; i < str_len; i++) {
    str[(*length)++] = value[i];
  }

  // If left-aligned, add padding after
  if (spec->minus_flag && pad_len > 0) {
    for (int i = 0; i < pad_len; i++) {
      str[(*length)++] = ' ';
    }
  }

  str[*length] = '\0';
  return 0;
}

// Process unsigned integer (%u) with formatting
int process_unsigned(char *str, int *length, va_list args,
                     FormatSpecifier *spec) {
  // Get the value based on length modifier
  unsigned long value;
  if (spec->length_h) {
    value = (unsigned short)va_arg(args, unsigned int);
  } else if (spec->length_l) {
    value = va_arg(args, unsigned long);
  } else {
    value = va_arg(args, unsigned int);
  }

  // Convert to string
  char buffer[32];

  // Convert value to string (in reverse)
  int digit_count = 0;
  if (value == 0) {
    buffer[digit_count++] = '0';
  } else {
    while (value > 0) {
      buffer[digit_count++] = '0' + (value % 10);
      value /= 10;
    }
  }

  // Apply precision if set (minimum number of digits)
  int min_digits = spec->precision_set ? spec->precision : 1;

  // Calculate total length
  int total_len = (digit_count > min_digits) ? digit_count : min_digits;

  // Handle padding and alignment
  int pad_char = ' ';
  int pad_len = spec->width > total_len ? spec->width - total_len : 0;

  // If right-aligned, add padding first
  if (!spec->minus_flag && pad_len > 0) {
    for (int i = 0; i < pad_len; i++) {
      str[(*length)++] = pad_char;
    }
  }

  // Add leading zeros for precision
  int leading_zeros = min_digits - digit_count;
  if (leading_zeros > 0) {
    for (int i = 0; i < leading_zeros; i++) {
      str[(*length)++] = '0';
    }
  }

  // Add digits (in correct order)
  for (int i = digit_count - 1; i >= 0; i--) {
    str[(*length)++] = buffer[i];
  }

  // If left-aligned, add padding after
  if (spec->minus_flag && pad_len > 0) {
    for (int i = 0; i < pad_len; i++) {
      str[(*length)++] = pad_char;
    }
  }

  str[*length] = '\0';
  return 0;
}

int s21_sprintf(char *str, const char *format, ...) {
  if (str == NULL || format == NULL) {
    return -1;
  }

  // Initialize string
  str[0] = '\0';

  va_list args;
  va_start(args, format);

  int length = 0;

  for (int i = 0; format[i] != '\0'; i++) {
    if (format[i] == '%') {
      FormatSpecifier spec;
      char specifier = parse_format_specifier(format, &i, &spec);

      // Check if the specifier is valid
      if (specifier == 'd' || specifier == 'f' || specifier == 'c' ||
          specifier == 's' || specifier == 'u' || specifier == '%') {
        // Handle valid specifiers
        switch (specifier) {
          case 'd':
            process_int(str, &length, args, &spec);
            break;
          case 'f':
            process_float(str, &length, args, &spec);
            break;
          case 'c':
            process_char(str, &length, args, &spec);
            break;
          case 's':
            process_string(str, &length, args, &spec);
            break;
          case 'u':
            process_unsigned(str, &length, args, &spec);
            break;
          case '%':
            str[length++] = '%';
            str[length] = '\0';
            break;
        }
      } else {
        length = 0;  // Reset the length to clear the existing string
        const char error_msg[] = "Unknown spec: ";

        // Add error message
        for (int j = 0; error_msg[j] != '\0'; j++) {
          str[length++] = error_msg[j];
        }
        str[length] = '\0';

        // Stop processing after encountering invalid format and return error
        // code
        va_end(args);
        return -1;
      }
    } else {
      // Regular character
      str[length++] = format[i];
      str[length] = '\0';
    }
  }

  va_end(args);
  return length;
}