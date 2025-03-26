import customtkinter as ctk
from tkinter import END
import threading
import pyttsx3
from chatbot import chatbot_response

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Set global styling for CustomTkinter
ctk.set_appearance_mode("dark")  # "dark", "light", or "system"
ctk.set_default_color_theme("blue")  # You can choose your theme

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Assistant Chatbot")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        # Chat Display Area (Scrollable Textbox)
        self.chat_display = ctk.CTkTextbox(self.root, width=500, height=350, corner_radius=10)
        self.chat_display.pack(pady=10, padx=10)
        self.chat_display.insert(END, "🤖 Chatbot: Hello! How can I assist you?\n\n")
        self.chat_display.configure(state="disabled")  # Make it read-only

        # User Input Field
        self.user_input = ctk.CTkEntry(self.root, width=400, height=40, placeholder_text="Type your message...", corner_radius=10)
        self.user_input.pack(pady=5)

        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.button_frame.pack(pady=10)

        # Send Button
        self.send_button = ctk.CTkButton(self.button_frame, text="Send", command=self.send_message, width=100, height=40, corner_radius=10)
        self.send_button.pack(side="left", padx=5)

        # Clear Chat Button
        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear Chat", fg_color="red", command=self.clear_chat, width=100, height=40, corner_radius=10)
        self.clear_button.pack(side="left", padx=5)

    def send_message(self):
        user_message = self.user_input.get().strip()
        if user_message:
            self.chat_display.configure(state="normal")
            self.chat_display.insert(END, f"🧑‍💼 You: {user_message}\n")
            response = chatbot_response("P001", user_message)
            self.chat_display.insert(END, f"🤖 Chatbot: {response}\n\n")
            self.chat_display.configure(state="disabled")
            self.user_input.delete(0, END)
            
            # Optionally, speak the response using text-to-speech
            threading.Thread(target=speak, args=(response,), daemon=True).start()

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", END)
        self.chat_display.insert(END, "🤖 Chatbot: Hello! How can I assist you?\n\n")
        self.chat_display.configure(state="disabled")

if __name__ == "__main__":
    root = ctk.CTk()
    app = ChatbotGUI(root)
    root.mainloop()


