import random
import string

def generate_garbage_text(length=100):
    characters = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choice(characters) for _ in range(length))

def test_text_classifier(classify_func):
    # Test with random garbage text
    garbage = generate_garbage_text()
    try:
        result = classify_func(garbage)
        print(f"Classification result for garbage text: {result}")
    except Exception as e:
        print(f"Handled text classification exception: {e}")

    # Test with empty string
    try:
        result = classify_func('')
        print(f"Classification result for empty string: {result}")
    except Exception as e:
        print(f"Handled empty string exception: {e}")

    # Test with very long input
    long_text = generate_garbage_text(10000)
    try:
        result = classify_func(long_text)
        print(f"Classification result for very long text: {result}")
    except Exception as e:
        print(f"Handled long text exception: {e}")