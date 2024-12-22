# Your provided numbers (the indices) of the theaters you want to add
numbers_to_add = []  # Example, you can change this as needed

# Dictionary of all available theaters
theaters_dict = {
    1: "GS Cinemas", 
    2: "V Celluloid Bhaskar Cinemas", 
    3: "Cine Prime Cinema", 
    4: "Pallavi Keerthana Complex", 
    5: "Hollywood Bollywood Theaters",
    6: "Naaz Cinemas",
    7: "Mythri Cinemas Phoenix Mall",
    8: "Plateno Cinemas Dolby Atmos 4K Barco Projection",
    9: "PVR Guntur",
    10: "Cine Square Dolby Atmos A/C",
    11: "JLE Cinemas",
    12: "Sri Saraswathi Picture Palace A/C Christie Laser Projection",
    13: "Krishna Mahal",
    14: "Venkata Krishna Theatre",
    15: "KKR Sai Nivya A/C Dts"
}

# Initialize an empty set to store unique theater names
theater_set = set()

# Add the selected theaters to the theater_set based on the provided numbers
for num in numbers_to_add:
    if num in theaters_dict:  # Check if the number exists in the dictionary
        theater_set.add(theaters_dict[num])

# Convert the set back to a list (optional if you need a list)
theater_list = list(theater_set)
