# Create GTD Instances

## You
suppose I have the following python dataclass:

```
class GTDContextLabel:
    name: str
    emojis: str
    color: str
```

and I want to make a bunch of instances of it with the following data:


🏠🧺🧹🛠️ home orange

🏡🌳🍃 yard lime green

📞🗣️📲 call mint green

✨ 🤳 👀 iphone yellow

📝📊📑 computer sky blue

🗓️🧱⏰⏲️ schedule berry red

🎧🧠💻 focused charcoal

⚡️💻✨ quick charcoal

the colors should be formatted with underscores instead of spaces 

## ChatGPT
You can create instances of the `GTDContextLabel` class with the provided data by defining a list of tuples containing the data and then using a list comprehension to create instances. Here's an example:

```python
from dataclasses import dataclass

@dataclass
class GTDContextLabel:
    name: str
    emojis: str
    color: str

# Data with emojis and color (formatted with underscores)
data = [
    ("home", "🏠🧺🧹🛠️", "orange"),
    ("yard", "🏡🌳🍃", "lime_green"),
    ("call", "📞🗣️📲", "mint_green"),
    ("iphone", "✨ 🤳 👀", "yellow"),
    ("computer", "📝📊📑", "sky_blue"),
    ("schedule", "🗓️🧱⏰⏲️", "berry_red"),
    ("focused", "🎧🧠💻", "charcoal"),
    ("quick", "⚡️💻✨", "charcoal"),
]

# Create instances of GTDContextLabel
instances = [GTDContextLabel(name, emojis, color.replace(' ', '_')) for name, emojis, color in data]

# Print instances
for instance in instances:
    print(instance)

```

This code uses a list comprehension to iterate through the data and create instances of the `GTDContextLabel` class. The `color` values are formatted with underscores using the `replace` method to replace spaces with underscores. The resulting instances are then printed.

## You
can you instead just use the map function and asterisk operator to directly create the list. replace is not necessary since the literal strings are now correctly formatted

## ChatGPT
Certainly! You can use the `map` function along with the asterisk operator to directly create instances of the `GTDContextLabel` class. Here's the modified code:

```python
from dataclasses import dataclass

@dataclass
class GTDContextLabel:
    name: str
    emojis: str
    color: str

# Data with emojis and color (formatted with underscores)
data = [
    ("home", "🏠🧺🧹🛠️", "orange"),
    ("yard", "🏡🌳🍃", "lime_green"),
    ("call", "📞🗣️📲", "mint_green"),
    ("iphone", "✨ 🤳 👀", "yellow"),
    ("computer", "📝📊📑", "sky_blue"),
    ("schedule", "🗓️🧱⏰⏲️", "berry_red"),
    ("focused", "🎧🧠💻", "charcoal"),
    ("quick", "⚡️💻✨", "charcoal"),
]

# Create instances of GTDContextLabel using map and the asterisk operator
instances = list(map(lambda x: GTDContextLabel(*x[:-1], x[-1].replace(' ', '_')), data))

# Print instances
for instance in instances:
    print(instance)

```

In this version, `map` is used with a lambda function to apply the constructor of `GTDContextLabel` to each tuple in the `data` list. The asterisk operator (`*`) is used to unpack the tuple elements into the constructor arguments. The `replace` method is applied only to the last element of the tuple to format the `color` string. The result is then converted to a list.

