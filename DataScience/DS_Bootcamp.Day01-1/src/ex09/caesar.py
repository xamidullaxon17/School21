from sys import argv

def caesar_cipher(text, shift, mode):
    """
    Caesar cipherni ishlatib matnni kodlaydi yoki dekodlaydi.
    """
    if not text.isascii():
        raise ValueError("The script does not support your language yet.")

    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            if mode == "encode":
                result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            elif mode == "decode":
                result += chr((ord(char) - shift_base - shift) % 26 + shift_base)
        else:
            result += char
    return result

def main():
    if len(argv) != 4:
        raise ValueError("Incorrect number of arguments. Usage: python3 caesar.py <mode> <text> <shift>")
    
    mode = argv[1].lower()
    text = argv[2]
    try:
        shift = int(argv[3])
    except ValueError:
        raise ValueError("Shift value must be an integer.")
    
    if mode not in ["encode", "decode"]:
        raise ValueError("Mode must be either 'encode' or 'decode'.")
    
    result = caesar_cipher(text, shift, mode)
    print(result)

if __name__ == "__main__":
    main()
