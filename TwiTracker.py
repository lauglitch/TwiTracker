import pygame
import tkinter as tk
from tkinter import Label, filedialog, ttk
import zipfile
from PIL import ImageTk, Image


window = tk.Tk()
width = 800
height = 600
hexaColor = '#00acee'   #Twitter blue color in hexadecimal format
followerFile = None
followingFile = None

# 1- Set window's properties
##### SOFTWARE UI #####
def set_window():
    window.geometry(f"{width}x{height}")
    window.title("TwiTracker")
    window.resizable(False, False)
    window.configure(bg=hexaColor)

    # Set window icon
    icon = tk.PhotoImage(file="Assets/twitterLogo.png")
    window.iconphoto(True, icon)
       
# 2- Set instructions' text and its properties
##### SOFTWARE UI #####
def set_instructions():
    instructions = Label(window, text="1- Inicia sesión en tu cuenta de Twitter y ve a Más > Ajustes y Soporte > \n    Ajustes y privacidad > Tu cuenta > Descargar un archivo de tus datos. \n2- Cuando recibas el fichero en tu correo, descárgalo.\n3- Pulsa el botón 'EXPORTAR DATOS' y selecciona el fichero descargado.\n4- Archivo listo en la carpeta de TwiTracker con el nombre 'exportedData.txt'.",
                         font=("Arial", 16),
                         bg=hexaColor,
                         fg="white",
                         justify=tk.LEFT)
    
    instructions.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

# 4- Method called when "EXPORTAR DATOS" button is pressed
##### SOFTWARE LOGIC #####
def find_files():
    show_error(False)

    # Open file explorer and get .zip path
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivo ZIP", "*.zip")])

    if ruta_archivo:
        try:
            with zipfile.ZipFile(ruta_archivo, 'r') as zip_ref:
                # Check if folder "data" exists inside .zip
                carpetas = [nombre for nombre in zip_ref.namelist() if nombre.endswith('/')]
                if 'data/' in carpetas:
                    # Check if files "follower.js" and "following.js" exist inside "data" folder
                    archivos = zip_ref.namelist()
                    if 'data/follower.js' in archivos and 'data/following.js' in archivos:
                        # Extract data and save it inside variables
                        global followerFile 
                        followerFile = zip_ref.read('data/follower.js')
                        global followingFile 
                        followingFile = zip_ref.read('data/following.js')
                        print("'follower.js' and 'following.js' files found.")
                        export_data()
                    else:
                        print("'follower.js' and 'following.js' files not found inside .zip/data.")
                        show_error(True)
                        play_sound(False)
                else:
                    print("'data' folder not found inside .zip.")
                    show_error(True)
                    play_sound(False)
        except zipfile.BadZipFile:
            print("Selected ZIP is not valid.")
            show_error(True)
            play_sound(False)
    else:
        print("ZIP not selected.")

# 5- Method called after "follower.js" and "following.js" are found
##### SOFTWARE LOGIC #####
# TODO:
def export_data():
    lines1 = followerFile.splitlines() #Split text into lines
    indexToStart = 4  # Index of the first line to extract
    firstChar = 20 # Start character on each line

    # Extract lines starting at line 5 and every 6 consecutive lines
    followerID = lines1[indexToStart::6]
    # Select line from the 20th character, and not counting the last character
    followerID = [line[firstChar:-1] for line in followerID]
    #print(ids)   

    lines2 = followingFile.splitlines() #Split text into lines
    indexToStart = 4  # Index of the first line to extract 
    firstChar = 20 # Start character on each line

    # Extract lines starting at line 5 and every 6 consecutive lines
    followingID = lines2[indexToStart::6]
    # Select line from the 20th character, and not counting the last character
    followingID = [line[firstChar:-1] for line in followingID]
    #print(ids)                        

    # Math Calculation -> Result = B - (B ∩ A)
        # Intersection1: intersection = list(set(followerID).difference(followingID)) 
        # Intersection2: intersection = list(set(lista1).intersection(lista2))
    intersection = list(set(followingID) & set(followerID))
    result = [x for x in followingID if x not in intersection]
    #print("Longitud del resultado: ", len(result))

    show_info(len(followerID), len(followingID), len(result))

    # Export text file on software's root
    try:
        play_sound(True)
        with open("exportedData.txt", 'w') as file:
            for linea in result:
                linea = linea = linea.decode("utf-8")
                file.writelines(linea + "\n" )
    except: 
        play_sound(False)
        print("Data couldn't be saved.")

# 6- Method called after "exportedData.txt" exportation failed or "EXPORTAR DATOS" is pressed, that shows or hides error label
##### SOFTWARE UI #####
def show_error(showError):
    if showError:
        errorText.config(text="Archivo no válido")
    else:
        errorText.config(text="")

# 7- Method called after "exportedData.txt" exportation succeed 
##### SOFTWARE UI #####
# It adds 3 visible variables to the UI that shows follower, following and unmutal counts
def show_info(followerCount, followingCount, unmutualCount):
    followerText = Label(window, text=("follower: " + str(followerCount)), font=("Arial", 16), bg=hexaColor, fg="white")
    followerText.place(x=125, y=500)

    followingText = Label(window, text=("following: " + str(followingCount)), font=("Arial", 16), bg=hexaColor, fg="white")
    followingText.place(x=325, y=500)
    
    unmutualText = Label(window, text=("unmutual: " + str(unmutualCount)), font=("Arial", 16), bg=hexaColor, fg="white")
    unmutualText.place(x=525, y=500)

# 8 - Method called after "exportedData.txt" exportation succeed or failed to play a different sound
def play_sound(succeed):
    if succeed:
        pygame.mixer.music.load("Assets/successAudio.mp3")  # Ruta del archivo de sonido
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.load("Assets/failureAudio.mp3")  # Ruta del archivo de sonido
        pygame.mixer.music.play()


# DEBUG: Paint line guides to help the programmer create the UI
def paint_guides():
    canvas = tk.Canvas(window, width=800, height=600)
    canvas.pack()

    # Pintar líneas de guía horizontal
    for i in range(0, 600, 20):
        canvas.create_line(0, i, 800, i, fill="red", dash=(4, 4))

    # Pintar líneas de guía vertical
    for i in range(0, 800, 20):
        canvas.create_line(i, 0, i, 600, fill="red", dash=(4, 4))

# Run all graphic methods
#paint_guides()
set_window()
set_instructions()

# Set title
titlePNG = Image.open("Assets/twitrackerTitle.png").convert("RGBA")
image_tk = ImageTk.PhotoImage(titlePNG)
titleImage = tk.Label(window, image=image_tk, bg=hexaColor,)
titleImage.pack()

# Set buttons and its properties
btnImage = Image.open("Assets/exportButtonPNG.png")
btnImage_tk = ImageTk.PhotoImage(btnImage)
exportButton = ttk.Button(window, image =btnImage_tk, command=find_files, style="TButton")
styles = ttk.Style()
styles.configure('TButton', borderwidth=0, relief="flat", borderradius=8)
posX = (height / 2 - 30)
posY = (width / 2 - 30)
exportButton.place(x= posX, y = posY)

# Set error Label
showErrorText = tk.BooleanVar()
showErrorText.set(False) #mostrar_texto
errorText = tk.Label(window, textvariable="", bg = hexaColor, font=("Arial", 16), fg="white")
errorText.place(x=320, y=450)

# Init mixer
pygame.mixer.init()

window.mainloop()

