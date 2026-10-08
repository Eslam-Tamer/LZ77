import sys
from dataclasses import dataclass

@dataclass
class Tag:
    offset: int = 0
    length_of_match: int = 0
    next_symbol: str = ''
    
def lz77_compress(input_str, search_buffer, look_ahead_buffer):
    compressed = []

    input_length = len(input_str)
    index = 0

    while index < input_length:
        # Initialization and default settings for a new Tag
        new_tag = Tag()
        new_tag.offset = 0
        new_tag.length_of_match = 0
        new_tag.next_symbol = input_str[index]

        # Check max offset
        max_offset = index if index < search_buffer else search_buffer

        # Check max match length
        max_search_length = (
            input_length - index
            if (index + look_ahead_buffer) > input_length
            else look_ahead_buffer
        )

        # Loop to check for matches
        for offset in range(1, max_offset + 1):
            length = 0

            # Checking the match length based on the maximum match length
            while (length < max_search_length and input_str[index - offset + length] == input_str[index + length]):
                length += 1

            # Update the Tag if a better match is found
            if length > new_tag.length_of_match:
                new_tag.offset = offset
                new_tag.length_of_match = length
                new_tag.next_symbol = input_str[index + length] if (index + length) < input_length else ''

        compressed.append(new_tag)
        index += new_tag.length_of_match + 1

    return compressed

def lz77_decompress(compressed):
    decompressedText = ""
    # tag[0] = offset, tag[1] = length, tag[2] = next_symbol

    for tag in compressed:
        if tag[0] == 0 and tag[1] == 0:
            decompressedText += tag[2]
        else:
            offset = len(decompressedText) - tag[0]
            for i in range(tag[1]):
                decompressedText += decompressedText[offset]
                offset += 1

            decompressedText += tag[2]

    return decompressedText


def menu():
    # Display the main program menu
    print("===================================")
    print("          LZ77 Compression         ")
    print("===================================")
    print("1. Compress Text")
    print("2. Decompress Text")
    print("3. Exit")
    print("===================================")


def get_number_of_tags():
    """Get a valid number of tags from the user."""

    while True:
        try:
            number_of_tags = int(input("Enter number of tags: "))

            if number_of_tags < 0:
                print("Invalid input! Number of tags cannot be negative.\n")
                continue

            return number_of_tags

        except ValueError:
            print("Invalid input! Please enter a valid number.\n")


def get_tag():
    """Get and validate one LZ77 tag."""

    while True:
        try:
            user_input = input(
                "Enter offset, length, and next symbol "
                "(use 'space' for a space character): "
            )

            parts = user_input.split()

            # A tag must contain exactly 3 values
            if len(parts) != 3:
                print(
                    "Invalid tag! Please enter exactly "
                    "3 values: offset length next_symbol.\n"
                )
                continue

            offset = int(parts[0])
            length = int(parts[1])
            next_symbol = parts[2]

            # Offset and length cannot be negative
            if offset < 0:
                print("Invalid offset! Offset cannot be negative.\n")
                continue

            if length < 0:
                print("Invalid length! Length cannot be negative.\n")
                continue

            # Convert "space" into an actual space character
            if next_symbol.lower() == "space":
                next_symbol = " "
            elif next_symbol.lower() == "null":
                next_symbol = ""

            return offset, length, next_symbol

        except ValueError:
            print(
                "Invalid input! Offset and length must be numbers.\n"
            )


def main():
    while True:

        menu()

        # Get user choice
        try:
            choice = int(input("Enter your choice: "))

        except ValueError:
            print("Invalid input! Please enter a number.\n")
            continue

        # ==============================
        # Compress
        # ==============================
        if choice == 1:

            text = input("Enter the text: ")

            if text == "":
                print("Invalid input! Text cannot be empty.\n")
                continue

            # Get Search Buffer Size
            while True:
                try:
                    search_buffer_size = int(
                        input("Enter search buffer size: ")
                    )

                    if search_buffer_size <= 0:
                        print("Size must be greater than 0.\n")
                        continue

                    break

                except ValueError:
                    print("Invalid input! Please enter a positive integer.\n")

            # Get Lookahead Buffer Size
            while True:
                try:
                    lookahead_buffer_size = int(
                        input("Enter lookahead buffer size: ")
                    )

                    if lookahead_buffer_size <= 0:
                        print("Size must be greater than 0.\n")
                        continue

                    break

                except ValueError:
                    print("Invalid input! Please enter a positive integer.\n")

            for tag in lz77_compress(text,search_buffer_size,lookahead_buffer_size):
                    print(f"<{tag.offset},{tag.length_of_match},{tag.next_symbol}>")

        # ==============================
        # Decompress
        # ==============================
        elif choice == 2:

            number_of_tags = get_number_of_tags()

            tags = []

            for i in range(number_of_tags):
                print(f"\nTag {i + 1}:")

                offset, length, next_symbol = get_tag()

                tags.append(
                    (offset, length, next_symbol)
                )

            decompressed_data = lz77_decompress(tags)

            print(f"\nDecompressed data: {decompressed_data}\n")

        # ==============================
        # Exit
        # ==============================
        elif choice == 3:

            print("\nExiting program. Goodbye!")

            sys.exit(0)

        # ==============================
        # Invalid menu choice
        # ==============================
        else:

            print(
                "Invalid choice! Please choose "
                "1, 2, or 3.\n"
            )


if __name__ == "__main__":
    main()
