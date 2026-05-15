from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

# Load the ciphertext
file_path = "ct.txt"  # Update with the actual path if needed
with open(file_path, "r") as file:
    ciphertext = file.read()

# Remove known words like "LACTF" and extra spaces
ciphertext = ciphertext.replace("LACTF", "").strip()

# Count letter frequencies
letter_frequencies = Counter(ciphertext)

# Convert to DataFrame
df = pd.DataFrame(letter_frequencies.items(), columns=["Character", "Frequency"])
df = df.sort_values(by="Frequency", ascending=False)

# Print the frequency table
print(df)

# Plot the frequency analysis
df.plot(kind="bar", x="Character", y="Frequency")
plt.title("Character Frequency Analysis")
plt.show()
