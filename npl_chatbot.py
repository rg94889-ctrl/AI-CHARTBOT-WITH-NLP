import nltk
import spacy
from nltk.chat.util import Chat, reflections
import random
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Load spaCy English model
try:
    nlp = spacy.load('en_core_web_sm')
except:
    print("spaCy English model not found. Please install with:")
    print("python -m spacy download en_core_web_sm")
    exit()

class NLPChatbot:
    def __init__(self):
        # Initialize patterns for NLTK chat
        self.pairs = [
            [
                r"hi|hello|hey",
                ["Hello! How can I help you today?", "Hi there! What can I do for you?"]
            ],
            [
                r"what is your name?",
                ["I'm an NLP-powered chatbot. You can call me ChatAI!",]
            ],
            [
                r"how are you?",
                ["I'm functioning optimally, thank you!", "I'm a bot, so I'm always good!"]
            ],
            [
                r"(.*) (weather|temperature) (.*)",
                ["I can't check real-time weather, but I can tell you about weather patterns!"]
            ],
            [
                r"quit|bye|exit",
                ["Goodbye! Have a great day!", "It was nice talking to you. Bye!"]
            ],
            [
                r"(.*)",
                ["I'm not sure I understand. Can you rephrase that?", 
                 "Interesting! Tell me more about that.",
                 "I'm still learning. Could you ask me something else?"]
            ]
        ]
        
        # Initialize NLTK chat
        self.chat = Chat(self.pairs, reflections)
        
        # Knowledge base for specific queries
        self.knowledge_base = {
            "nlp": "Natural Language Processing (NLP) is a field of AI that focuses on "
                   "interaction between computers and human language.",
            "spacy": "spaCy is an open-source library for advanced NLP in Python.",
            "nltk": "NLTK (Natural Language Toolkit) is a leading platform for building "
                    "Python programs to work with human language data.",
            "chatbot": "A chatbot is a software application that can conduct conversations "
                       "with humans via text or voice."
        }
        
    def process_input(self, user_input):
        # Basic NLTK response
        response = self.chat.respond(user_input)
        
        # If generic response, try spaCy processing
        if response in ["I'm not sure I understand. Can you rephrase that?", 
                        "Interesting! Tell me more about that.",
                        "I'm still learning. Could you ask me something else?"]:
            
            doc = nlp(user_input.lower())
            
            # Check for knowledge base terms
            for token in doc:
                if token.text in self.knowledge_base:
                    return self.knowledge_base[token.text]
            
            # Check for question patterns
            if any(token.text in ['what', 'how', 'why', 'when'] for token in doc):
                if 'weather' in user_input.lower():
                    return self.generate_weather_response()
                elif 'time' in user_input.lower():
                    return "I don't have access to real-time clock data."
                elif 'date' in user_input.lower():
                    return "I don't have access to calendar data."
            
            # Check for visualization request
            if 'visualize' in user_input.lower() or 'graph' in user_input.lower():
                return self.generate_visualization()
        
        return response
    
    def generate_weather_response(self):
        # Simulate weather data visualization
        plt.figure(figsize=(8, 4))
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        temps = [22, 24, 19, 23, 25]
        plt.plot(days, temps, marker='o')
        plt.title('Weekly Temperature Trend')
        plt.xlabel('Day')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        
        # Save plot to bytes
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        
        # Encode image to base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        
        return {
            "text": "Here's a sample weather visualization:",
            "image": img_base64
        }
    
    def generate_visualization(self):
        # Generate a sample NLP-related visualization
        plt.figure(figsize=(8, 4))
        labels = ['Nouns', 'Verbs', 'Adjectives', 'Others']
        sizes = [35, 25, 15, 25]
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Typical Word Distribution in English Text')
        
        # Save plot to bytes
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        
        # Encode image to base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        
        return {
            "text": "Here's a visualization of word distribution in English text:",
            "image": img_base64
        }
    
    def start_chat(self):
        print("NLP Chatbot: Hello! I'm a chatbot with NLP capabilities. Type 'quit' to exit.")
        
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'bye', 'exit']:
                print("NLP Chatbot: Goodbye!")
                break
                
            response = self.process_input(user_input)
            
            if isinstance(response, dict) and 'image' in response:
                print(f"NLP Chatbot: {response['text']}")
                print("[Image would be displayed here in a GUI application]")
                print(f"(Base64 image data length: {len(response['image'])})")
                # In a real application, you would decode and display the image
            else:
                print(f"NLP Chatbot: {response}")

if __name__ == "__main__":
    chatbot = NLPChatbot()
    chatbot.start_chat()
