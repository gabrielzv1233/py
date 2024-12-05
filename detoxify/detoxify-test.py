from detoxify import Detoxify

def analyze_text(text):
    results = Detoxify('original').predict(text)
    
    # Display all content categories with scores, even if they are 0
    print("\nContent categories with scores:")
    for category, score in results.items():
        print(f"{category.capitalize()}: {score:.2f}")

# Main loop to input text and analyze it
while True:
    text = input("Enter text to analyze (or type 'exit' to quit): ")
    if text.lower() == 'exit':
        break
    analyze_text(text)
