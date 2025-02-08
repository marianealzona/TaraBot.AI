from PIL import Image  # Import PIL for image handling
import customtkinter as CTk  #  Ensure CTk is imported
import google.generativeai as genai

# Set your API key
genai.configure(api_key="ENTER API KEY HERE")

def chat_with_gemini(user_message, chat_history=None):
    model = genai.GenerativeModel("gemini-pro")
    input_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history]) + f"\nuser: {user_message}" if chat_history else user_message
    
    try:
        response = model.generate_content(input_text)
        return response.text.strip() if response.text else "No response."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def open_chatbot_window():
    chatbot_window = CTk.CTk()
    chatbot_window.title("TaraBot.AI")
    chatbot_window.geometry("600x900")
    chatbot_window.minsize(600, 900)

    try:
        image = CTk.CTkImage(
            light_image=Image.open("cute.png"),
            dark_image=Image.open("cute.png"),
            size=(50, 50)
        )
    except Exception as e:
        print(f"Error loading image: {e}")
        image = None

    main_frame = CTk.CTkFrame(chatbot_window, corner_radius=15, fg_color="#1E1E1E")
    main_frame.pack(padx=10, pady=10, fill="both", expand=True)

    title_frame = CTk.CTkFrame(main_frame, fg_color="transparent")
    title_frame.pack(pady=(40, 20), anchor="center")

    if image:
        CTk.CTkLabel(title_frame, image=image, text="").pack(side="left", padx=(0, 10))
    
    CTk.CTkLabel(
        title_frame,
        text="Hi, I'm TaraBot!",
        font=("Roboto", 40, "bold"),
        text_color="white"
    ).pack(side="left", padx=10, fill="x", expand=True)

    # Add a thin line below the title
    CTk.CTkFrame(main_frame, fg_color="#444444", height=1).pack(fill="x", padx=20, pady=(0, 10))

    chat_display = CTk.CTkScrollableFrame(main_frame, fg_color="#1E1E1E", corner_radius=10, height=550)
    chat_display.pack(padx=10, pady=10, fill="both", expand=True)

    chat_display._parent_canvas.configure(bg="#1E1E1E", highlightthickness=0)
    chat_display._scrollbar.configure(
        fg_color="#1E1E1E",  # Darker scrollbar background
        button_color="#1E1E1E",  # Darker scrollbar buttons
        button_hover_color="#555555"  # Improved hover color
    )
    chat_display._scrollbar.pack_forget()  # Initially hide the scrollbar
    
    input_frame = CTk.CTkFrame(main_frame, fg_color="#1E1E1E")
    input_frame.pack(fill="x", padx=10, pady=(5, 10))

    input_field = CTk.CTkEntry(
        input_frame, font=("Roboto Medium", 18), width=300, height=60,
        placeholder_text="Type a message...", fg_color="#121212",
        text_color="white", border_width=2, corner_radius=20
    )
    input_field.pack(side="left", padx=10, fill="x", expand=True)

    send_button = CTk.CTkButton(
        input_frame, text="Send", corner_radius=20, font=("Roboto Medium", 18),
        width=80, height=40, fg_color="#0078D7", hover_color="#005A9E",
        command=lambda: handle_input()
    )
    send_button.pack(side="right")

    chat_log = []
    n_remembered_post = 2

    def create_bubble(text, sender):
        wrapper_frame = CTk.CTkFrame(chat_display, fg_color="transparent")
        wrapper_frame.pack(fill="x", padx=10, pady=5, anchor="w" if sender == "bot" else "e")

        bubble_frame = CTk.CTkFrame(
            wrapper_frame,
            corner_radius=20,
            fg_color="#2E2E2E" if sender == "bot" else "#0078D7",
            bg_color="transparent",
            border_width=0
        )
        bubble_frame.pack(anchor="w" if sender == "bot" else "e", padx=5, pady=2)

        text_widget = CTk.CTkLabel(
            bubble_frame,
            text=text,
            font=("Roboto Medium", 16),
            text_color="light gray",
            wraplength=400,
            justify="left",
            padx=15,
            pady=10
        )
        text_widget.pack(padx=10, pady=5)

        chat_display._parent_canvas.yview_moveto(1)
        chat_display.update_idletasks()

    def handle_input(event=None):
        user_input = input_field.get().strip()
        input_field.delete(0, "end")

        if not user_input:
            return

        if user_input.lower() in ['quit', 'exit', 'bye']:
            create_bubble("Goodbye! 👋", "bot")
            chatbot_window.after(2000, chatbot_window.destroy)
            return

        create_bubble(user_input, "user")
        response = chat_with_gemini(user_input, chat_log[-n_remembered_post * 2:] if chat_log else None)

        # Remove asterisks from the response
        response = response.replace("**", "")

        chat_log.append({"role": "user", "content": user_input})
        chat_log.append({"role": "assistant", "content": response})

        chatbot_window.after(500, lambda: create_bubble(response, "bot"))
    input_field.bind("<Return>", handle_input)
    create_bubble("Hello! How can I assist you today?", "bot")
    chatbot_window.mainloop()

if __name__ == "__main__":
    open_chatbot_window()
