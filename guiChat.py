import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import openai
from tkinter import *
from PIL import Image, ImageTk
import requests
import os
import shutil 

API_KEY = "YOUR_KEY_HERE"

# Class containing information about current conversation
class Form:

    questions = []
    answers = []
    template = ""

# Opens downloaded image in screen's canvas
def open_image(path):

    img = Image.open(path)
    img = img.resize((305, 305), Image.ANTIALIAS)
    canvas.configure(bg="black")
    temp = ImageTk.PhotoImage(img)
    images_tk_list.append(temp)
    canvas.create_image((0, 0), anchor="nw", image=temp)

# Writes current convo to the text widget
def write_convo():

    global convo

    print("--------------------\n" + convo + "\n----------------------")

    txt_edit.delete("1.0", tk.END)

    temp = convo.split("\)")
    if len(temp) > 1:
        text = temp[len(temp) - 1]
    else:
        text = convo

    txt_edit.insert(tk.END, text)

# Prompts openai for an image, and saves the image file
def save_image():
    
    openai.api_key = API_KEY
    prompt=tk.simpledialog.askstring("Prompt for Image Generator", "What would you like to make an image of?").lower()

    response = openai.Image.create(
      prompt=prompt,
      n=1,
      size="1024x1024"
    )

    image_url = response['data'][0]['url']

    url = image_url

    if not os.path.exists("AI_images"):
        os.mkdir("AI_images")
    file_name = "AI_images/" + prompt.strip() + ".ppm"

    res = requests.get(url, stream = True)

    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')

    ## img = PhotoImage(file=file_name)
    open_image(file_name)

def keyReleased(event):
    global commandPressed

    if event.keysym == "Meta_L":
        commandPressed = False

def keyPressed(event):

    global commandPressed

    if event.keysym == "Escape":
        window.quit()

    if event.keysym == "Meta_L":
        commandPressed = True

    if commandPressed:
        if event.keysym == "n":
            initiate()
            commandPressed = False
        elif event.keysym == 's':
            save_file()
            commandPressed = False
        elif event.keysym == 'o':
            open_file()
            commandPressed = False
        elif event.keysym == 'm':
            set_mood()
            commandPressed = False

    return

# Asks openai for a completion for the current conversation, plus new user input
def submit_prompt(template = False, moodsetup=False):

    global convo
    prompt = ""
    text = ""

    openai.api_key = API_KEY
    model_engine = "text-davinci-002"

    temperature = 1
    screen = txt_edit.get("1.0", tk.END)

    # grab part of convo which was displayed before
    temp = convo.split("\)")
    if len(temp) > 1:
        text = temp[len(temp) - 1]
    else:
        text = convo

    prompt = screen.replace(text,'') # need to prompt with only new part and add back

    # if len(prompts) > 1:
    #     prompt = prompts[len(prompts) - 1]

    convo += prompt

    response = openai.Completion.create(
        engine=model_engine,
        prompt=convo,
        max_tokens=1000,
        n = 1,            
        temperature = temperature
    ).choices[0].text.strip()

    if moodsetup:
        convo += "\)Prompt: "
    elif template:
        convo += response + "\n\nPrompt: "
    else:
        convo += response + "\n\nPrompt: "

# Opens file into text edit widget
def open_file():
    global convo
    convo = ""
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        convo += input_file.read()
    write_convo()

# Saves current conversation into text file
def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    
# Starts convo with a prompt which sets mood for the rest of the conversation
def set_mood():

    global convo

    mood=tk.simpledialog.askstring("Prompt for Set Mood", "What do you want the AI to pretend to be?").lower()
    convo = f"Please provide an answer to every prompt starting with 'Prompt:', act like like you are {mood} \)Prompt: "

    convo = f"The following is a conversation with an AI assistant. The assistant is feeling very {mood}.\nPrompt: Hello, how are you?\nI am {mood}\)Prompt: "
    
    write_convo()

def email_template():

    global global_form

    global_form.questions = [
        "What is the name of the person you are emailing: ",
        "Why are you emailing today: ",
        "Descriptors for the email: "
    ]

    print_questions()

    global_form.template = "email"

def recipe_template():

    global global_form

    global_form.questions = [
        "What food would you like: "
    ]

    print_questions()

    global_form.template = "recipe"

def advanced_recipe_template():

    global global_form

    global_form.questions = [
        "What ingredients do you have: "
    ]

    print_questions()

    global_form.template = "advanced_recipe"

def prompt_template():

    global global_form

    global_form.questions = [
        "What do you want the story to be about: "
    ]

    print_questions()

    global_form.template = "prompt"
    
def facts_template():

    global global_form

    global_form.questions = [
        "What do you want to receive facts about: "
    ]

    print_questions()

    global_form.template = "facts"

def print_questions():
    
    global global_form

    txt_edit2.delete("1.0", tk.END)
    new_text = ""

    for question in global_form.questions:
        new_text += question + "\n\n"
        
    txt_edit2.insert(tk.END, new_text.strip() + " ")

    global_form.answers = []

def returnPressed(event):

    if "\n\n" in txt_edit2.get("1.0", tk.END)[-2:]:
        returnPressed2()
        return

    submit_prompt()
    write_convo()

# Return pressed in the second text edit widget, which is for submitting info to the templates
def returnPressed2():

    global global_form
    global convo

    text = txt_edit2.get("1.0", tk.END)

    if len(text.split("\n")) == 1:
        return

    for line in text.split("\n"):

        if len(line.split(": ")) == 1:
            continue

        question = line.split(": ")[0] + ": "

        if question in global_form.questions:
            global_form.answers.append(line.split(": ")[1])

    if len(global_form.answers) == len(global_form.questions) and len(global_form.answers) > 0:
        global_form.answers = [x.strip().lower() for x in global_form.answers]
        if global_form.template == "email" and len(global_form.answers) == 3:
            convo = f"Prompt: Please write me a {global_form.answers[2]} email, pretend you are me, and write to {global_form.answers[0]}. I am emailing them because {global_form.answers[1]}.\)"
        elif global_form.template == "recipe":
            convo = f"Prompt: Please give me a recipe for the dish called: {global_form.answers[0]}\)"
        elif global_form.template == "advanced_recipe":
            convo = f"Prompt: Please give me a recipe containing the following foods: {global_form.answers[0]}\)"
        elif global_form.template == "prompt":
            convo = f"Prompt: Please write me a story containing the following: {global_form.answers[0]}\)"
        elif global_form.template == "facts":
            convo = f"Prompt: Please give me 40 facts about the following: {global_form.answers[0]}\)"

        write_convo()
        submit_prompt(template=True)
        write_convo()

    txt_edit2.delete("1.0", tk.END)    
    txt_edit2.insert(tk.END, "Press enter here to retry.")   

def initiate():

    global model_engine
    global convo
    global commandPressed
    commandPressed = False
    txt_edit.delete("1.0", tk.END)
    convo = "Prompt: "

    write_convo()

convo = ""
userHeader = "Prompt:"
images_tk_list = []
commandPressed = False
answer = ""

global_form = Form()

# Initiate Window
window = tk.Tk()
window.title("Chat")

# Initialize Frames, Menu, and Text Window
frm_screen = tk.Frame(window, bd=2) # bd means border
frm_screen.pack(expand=True, fill="both")
frm_screen2 = tk.Frame(window, bd=2) # bd means border
frm_screen2.pack(side="bottom", fill="x")
txt_edit = tk.Text(frm_screen)
txt_edit2 = tk.Text(frm_screen2)

txt_edit.pack(expand=True, fill="both")
txt_edit2.pack(expand=True, side="right", fill="both")

menu = Menu(window)
window.config(menu=menu)

# Bind Events to frames 
window.bind('<Return>',returnPressed)
window.bind('<Key>',keyPressed)
window.bind('<KeyRelease>', keyReleased)

#frm_screen2.bind('<Return>',returnPressed2)

# Configure Canvas
canvas = Canvas(frm_screen2, width=300, height=300)
canvas.pack(side="left")
canvas.configure(bg='white')

# Configure Menu
filemenu = Menu(menu)
menu.add_cascade(label="Options", menu=filemenu)
filemenu.add_command(label="Open (cmd-o)", command=open_file)
filemenu.add_command(label="New (cmd-n)", command=initiate)
filemenu.add_command(label="Save (cmd-s)", command=save_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)

templates = Menu(menu)
menu.add_cascade(label="Templates", menu=templates)
templates.add_command(label="Simple Email", command=email_template)
templates.add_command(label="Recipe for dish", command=recipe_template)
templates.add_command(label="Recipe for Ingredients", command=advanced_recipe_template)
templates.add_command(label="Write a story", command=prompt_template)
templates.add_command(label="List of facts", command=facts_template)


functions = Menu(menu)
menu.add_cascade(label="Functions", menu=functions)
functions.add_command(label="Create Image", command=save_image)
functions.add_command(label="Set Mood (cmd-m)", command=set_mood)

initiate()
window.mainloop()
