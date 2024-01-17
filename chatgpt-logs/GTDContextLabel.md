# GTD Context Label Class

## You
Please write a simple python data class representing a GTD context label, with a name, emoji string, and color

## ChatGPT
Certainly! Here's a simple Python data class representing a GTD (Getting Things Done) context label:

```python
from dataclasses import dataclass

@dataclass
class GTDContextLabel:
    name: str
    emoji: str
    color: str

```

You can use this class to create instances of GTD context labels, providing a name, emoji string, and color for each label. For example:

```python
work_label = GTDContextLabel(name="Work", emoji="💼", color="blue")
home_label = GTDContextLabel(name="Home", emoji="🏠", color="green")

```

Feel free to customize the emoji and color values based on your preferences.

## You
Great, please make emojis plural

## ChatGPT
Certainly! Here's the modified Python data class with pluralized attribute names:

```python
from dataclasses import dataclass

@dataclass
class GTDContextLabel:
    names: str
    emojis: str
    colors: str

```

Now, when creating instances of GTD context labels, you'll use pluralized attribute names:

```python
work_label = GTDContextLabel(names="Work", emojis="💼", colors="blue")
home_label = GTDContextLabel(names="Home", emojis="🏠", colors="green")

```

This allows you to store multiple names, emojis, and colors for a given context label if needed.

## You
But keep name and color singular

## ChatGPT
Certainly! Here's the modified Python data class with only the `name` and `color` attributes in the singular form:

```python
from dataclasses import dataclass

@dataclass
class GTDContextLabel:
    name: str
    emojis: str
    color: str

```

Now, you can create instances of GTD context labels with a singular `name` and `color`:

```python
work_label = GTDContextLabel(name="Work", emojis="💼", color="blue")
home_label = GTDContextLabel(name="Home", emojis="🏠", color="green")

```

Feel free to use this class as a template for your GTD context labels.

## You
Now suppose I have a list of these objects, for each I want to generate a title, which is the emojis plus the name in title case. I also want to generate a “filter” which is a Todoist query that searches for a project with that name, or a label with that name not in the NotNow project. Can you write two member functions?

## ChatGPT
Certainly! Here are two member functions for the `GTDContextLabel` class that fulfill your requirements:

```python
from dataclasses import dataclass

@dataclass
class GTDContextLabel:
    name: str
    emojis: str
    color: str

    def generate_title(self):
        # Combine emojis and name in title case
        title = f"{self.emojis} {self.name.title()}"
        return title

    def generate_filter(self):
        # Generate Todoist filter for the label or project
        filter_query = f"#{self.name} & !#NotNow"
        return filter_query

```

Now, you can use these functions on instances of `GTDContextLabel`:

```python
work_label = GTDContextLabel(name="Work", emojis="💼", color="blue")
home_label = GTDContextLabel(name="Home", emojis="🏠", color="green")

# Generate titles and filters
work_title = work_label.generate_title()
work_filter = work_label.generate_filter()

home_title = home_label.generate_title()
home_filter = home_label.generate_filter()

print("Work Title:", work_title)
print("Work Filter:", work_filter)

print("Home Title:", home_title)
print("Home Filter:", home_filter)

```

This should print the titles and filters for the `Work` and `Home` labels based on your specified criteria.

## You
Filter query needs work, please rewrite it:

Project Name OR (label name and not project NotNow)

## ChatGPT
Certainly! Here's the updated `generate_filter` method to match your requirement:

```python
def generate_filter(self):
    # Generate Todoist filter for the label or project
    filter_query = f"#{self.name} | (@{self.name} & !#NotNow)"
    return filter_query

```

This generates a filter query that searches for either the project with the specified name or the label with the specified name that is not in the `NotNow` project.

## You
Great! Can you please also add 40 repeated spaces immediately before the pipe character?

## ChatGPT
Certainly! Here's the modified `generate_filter` method with 40 repeated spaces before the pipe character:

```python
def generate_filter(self):
    # Generate Todoist filter for the label or project
    filter_query = f"{' ' * 40}#{self.name} | (@{self.name} & !#NotNow)"
    return filter_query

```

Now, there are 40 spaces before the pipe character in the generated filter query.

## You
Almost! Between the first hashtag segment and the pipe character

## ChatGPT
My apologies for the oversight. Here's the corrected `generate_filter` method with 40 repeated spaces between the first hashtag segment and the pipe character:

```python
def generate_filter(self):
    # Generate Todoist filter for the label or project
    filter_query = f"#{self.name}{' ' * 40}| (@{self.name} & !#NotNow)"
    return filter_query

```

This will ensure that there are 40 spaces between the first hashtag segment and the pipe character in the generated filter query.

## You
Perfect!

## ChatGPT
I'm glad it's perfect for you! If you have any more questions or if there's anything else I can help you with, feel free to ask. Happy coding!

## You
Please super me the full class body with the two member functions

## ChatGPT
Certainly! Here's the complete `GTDContextLabel` class with the two member functions:

```python
from dataclasses import dataclass

@dataclass
class GTDContextLabel:
    name: str
    emojis: str
    color: str

    def generate_title(self):
        # Combine emojis and name in title case
        title = f"{self.emojis} {self.name.title()}"
        return title

    def generate_filter(self):
        # Generate Todoist filter for the label or project
        filter_query = f"{' ' * 40}#{self.name}{' ' * 40}| (@{self.name} & !#NotNow)"
        return filter_query

```

Feel free to use this complete class in your project. If you have any more questions or requests, feel free to let me know!

## You
So close! You’ve added back in the 40 spaces at the start of the string, they should only be in the middle

## ChatGPT
My apologies for the oversight. Here's the corrected version with 40 spaces only between the first hashtag segment and the pipe character:

```python
from dataclasses import dataclass

@dataclass
class GTDContextLabel:
    name: str
    emojis: str
    color: str

    def generate_title(self):
        # Combine emojis and name in title case
        title = f"{self.emojis} {self.name.title()}"
        return title

    def generate_filter(self):
        # Generate Todoist filter for the label or project
        filter_query = f"#{self.name}{' ' * 40}| (@{self.name} & !#NotNow)"
        return filter_query

```

Now, the 40 spaces are correctly placed between the first hashtag segment and the pipe character in the `generate_filter` method.

