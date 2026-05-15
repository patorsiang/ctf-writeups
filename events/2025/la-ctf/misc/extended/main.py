# Function to reverse the extended flag transformation
def reverse_extended_flag(extended_flag):
    original_flag = ""

    for c in extended_flag:
        o = bin(ord(c))[2:].zfill(8)  # Convert to 8-bit binary

        # Replace the first '1' with '0' to reverse the transformation
        for i in range(8):
            if o[i] == "1":
                o = o[:i] + "0" + o[i + 1:]
                break

        original_flag += chr(int(o, 2))  # Convert back to character

    return original_flag

# Load the encoded flag from chall.txt
file_path = "chall.txt"
with open(file_path, "rb") as f:
    extended_flag = f.read().decode("iso8859-1")

# Recover the original flag
recovered_flag = reverse_extended_flag(extended_flag)
print(recovered_flag)
