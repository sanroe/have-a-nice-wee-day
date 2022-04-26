from cleantext import clean
import secrets
import string

# Function to clean up and replace unwanted characters for slug creation
def clean_up_for_slug(to_name):
    slug_prefix = clean(to_name, lower=True, no_emoji=True)
    # Replacing multiple characters, this method is quicker than declaring a variable for chars
    for char in ["'", '!', '?', ',', '.', '(', ':', ';', '#', '/', '@', '$', '£', '€', '*', '+', '=', '[', ']', '{', '}', '|', '~', '`', '%', '<', '>']:
        if char in slug_prefix:
            slug_prefix = slug_prefix.replace(char, '')
    slug_prefix = slug_prefix.replace(" ", "-")
    return slug_prefix

# Function to create a unique slug
def create_unique_slug(to_name):
    slug_prefix = clean_up_for_slug(to_name)
    slug_suffix = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(20))
    slug = slug_prefix + '-' + slug_suffix
    return slug