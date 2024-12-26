from detoxify import Detoxify

def analyze_text(text):
    results = Detoxify('original').predict(text)
    
    print("\nContent categories with scores:")
    for category, score in results.items():
        print(f"{category.capitalize()}: {score:.2f}")

while True:
    text = input("Enter text to analyze (or type 'exit' to quit): ")
    if text.lower() == 'exit':
        break
    analyze_text(text)
