import string
from random import choice
import gooeypie as gp

import sys

import pygame
from pygame.locals import *
from pygame import mixer

from tkinter import *

from haveibeenpwnd import check_password

import re

app = gp.GooeyPieApp("P.A.I.A - Password Generator")
app.resizable_vertical = False

app.set_icon("../PasswordGenerator/PasswordGeneratorAssets/PAIANewIcon6.png")

#Note: When pasting passwords generated from the password generator into the strength checker,
# password strengths may not be identical as strength values for the password generator is 
# judged by what options are enabled and the password generator may not always produce an output 
# that includes the options it is selected with. 

default_password_length = 8 
score = 4
strength_score = 4
is_window_open_chk = False
is_credits_window_open_chk = False
is_guidelines_window_open_chk = False
is_privacy_window_open_chk = False
is_about_window_open_chk = False
is_submenu_window_open_chk = False

mixer.init()

other_window_music = pygame.mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/PasswordCheckerMusicNew1.mp3")
guidelines_window_music = pygame.mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/GuidelinesMusic1.mp3")
privacy_window_music = pygame.mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/PrivacyPolicyMusic1.mp3")
about_window_music = pygame.mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/AboutMusic1New.mp3")
credits_window_music = pygame.mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/CreditsMusic1.mp3")
submenu_window_music = pygame.mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/SubmenuMusic3.mp3")


def select_image(event):
    global score
    score = 0

    #Password Option Scores
    if letters_chk.checked == True:
        score += 1 
    if capitalletters_chk.checked == True:
        score += 1
    if digits_chk.checked == True:
        score += 1
    if symbols_chk.checked == True:
        score += 1
    
    #Password Length Scores
    if length_sld.value < 3:
        score -= 1
    if length_sld.value >= 7: #Very weak
        score += 1
    if length_sld.value >= 10: #Weak
        score += 1
    if length_sld.value >= 13: #Medium
        score += 1
    if length_sld.value >= 16: #Strong
        score += 1
    if length_sld.value >= 19: #Very Strong
        score += 1

    if length_sld.value > 25: #Extra value to counterbalance single options
        score += 1

    #Password Strength Overall Scores
    if score >= 3:
        password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel0_4.png"
        password_strength_lbl.text = "Critically Weak"
        time_to_crack_lbl.text = "Time to crack: Less than a second"
    if score >= 4:
        password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel1_5.png"
        password_strength_lbl.text = "Very Weak"
        time_to_crack_lbl.text = "Time to crack: Seconds to minutes"
    if score >= 5:
        password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel2_5.png"
        password_strength_lbl.text = "Weak"
        time_to_crack_lbl.text = "Time to crack: Hours to days"
    if score >= 6:
        password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel3_5.png"
        password_strength_lbl.text = "Good"
        time_to_crack_lbl.text = "Time to crack: Months to years"
    if score >= 7:
        password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel4_5.png"
        password_strength_lbl.text = "Strong"
        time_to_crack_lbl.text = "Time to crack: Years"
    if score >= 8:
        password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel5_5.png"
        password_strength_lbl.text = "Very Strong"
        time_to_crack_lbl.text = "Time to crack: Centuries"
    else:
        pass

def generate_password(length, letters, capital_letters, digits, symbols):
    #Set characters from which to choose from
    available_chars = ""
    if letters:
        available_chars += string.ascii_lowercase
    if capital_letters:
        available_chars += string.ascii_uppercase
    if digits:
        available_chars += string.digits
    if symbols:
        available_chars += string.punctuation
    
    #Make the password by choosing from the string above
    new_password = ""
    for count in range(length):
        new_password += choice(available_chars)
    
    return new_password

def show_new_password(event):
    #Populates the password box with a new generated password
    #Check that at least one option is selected
    if letters_chk.checked == False and digits_chk.checked == False and symbols_chk.checked == False and capitalletters_chk.checked == False:
        ErrorSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/ErrorSound1.mp3") 
        ErrorSound.play()
        app.alert("Invalid password options", "Please select at least one option for the password!", "error")
    else:
        #Update length label
        length_lbl.text = f"{length_sld.value} characters"

        #Add password to password input
        password_inp.text = generate_password(length_sld.value, letters_chk.checked, capitalletters_chk.checked, digits_chk.checked, symbols_chk.checked)

def refresh_new_password(event):
    #Populates the password box with a new generated password
    #Check that at least one option is selected
    if letters_chk.checked == False and digits_chk.checked == False and symbols_chk.checked == False and capitalletters_chk.checked == False:
        ErrorSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/ErrorSound1.mp3") 
        ErrorSound.play()
        app.alert("Invalid password options", "Please select at least one option for the password!", "error")
    else:
        #Update length label
        length_lbl.text = f"{length_sld.value} characters"

        #Add password to password input
        password_inp.text = generate_password(length_sld.value, letters_chk.checked, capitalletters_chk.checked, digits_chk.checked, symbols_chk.checked)
        RefreshSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/RefreshSound2.mp3")
        RefreshSound.play()

def show_guidelines(event):
    GuidelinesOpenSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/ExitConfirmationSound1.mp3")
    GuidelinesOpenSound.play()
    other_window.alert("Note", "Time to crack values are estimations by Bitwarden. PAIA produces password breach data from the online “HaveIBeenPwned?” (HIBP) database.", "question")
    GuidelinesCloseSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/QuitCancel2.mp3")
    GuidelinesCloseSound.play()

def copy_password(event):
    #Copies the generated password to the clipboard
    app.copy_to_clipboard(password_inp.text)
    ClipboardSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/ClipboardSound2.mp3")
    ClipboardSound.play()

def strength_copy_password(event):
    #Copies the strength checker password to the clipboard
    app.copy_to_clipboard(strength_password_inp.text)
    ClipboardSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/ClipboardSound2.mp3")
    ClipboardSound.play()

def strength_select_image(event):
    global strength_score
    strength_score = 0

    #Password Option Scores
    if any(l.islower() for l in strength_password_inp.text) == True:
        strength_score += 1 
    if any(c.isupper() for c in strength_password_inp.text) == True:
        strength_score += 1
    if any(d.isdigit() for d in strength_password_inp.text) == True:
        strength_score += 1
    if any(not s.isalnum() for s in strength_password_inp.text.replace(" ", "")) == True:
        strength_score += 1
    
    #Password Length Scores
    if len(strength_password_inp.text.replace(" ", "")) < 3:
        strength_score -= 1
    if len(strength_password_inp.text.replace(" ", "")) >= 7: #Very weak
        strength_score += 1
    if len(strength_password_inp.text.replace(" ", "")) >= 10: #Weak
        strength_score += 1
    if len(strength_password_inp.text.replace(" ", "")) >= 13: #Medium
        strength_score += 1
    if len(strength_password_inp.text.replace(" ", "")) >= 16: #Strong
        strength_score += 1
    if len(strength_password_inp.text.replace(" ", "")) >= 19: #Very Strong
        strength_score += 1

    if len(strength_password_inp.text) > 25: #Extra value to counterbalance single options
        strength_score += 1

    #Password Strength Overall Scores
    if strength_score < 3:
        strength_password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel0_4.png"
        strength_password_strength_lbl.text = "Critically Weak"
        strength_time_to_crack_lbl.text = "Time to crack: Less than a second"
    if strength_score >= 3:
        strength_password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel0_4.png"
        strength_password_strength_lbl.text = "Critically Weak"
        strength_time_to_crack_lbl.text = "Time to crack: Less than a second"
    if strength_score >= 4:
        strength_password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel1_5.png"
        strength_password_strength_lbl.text = "Very Weak"
        strength_time_to_crack_lbl.text = "Time to crack: Seconds to minutes"
    if strength_score >= 5:
        strength_password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel2_5.png"
        strength_password_strength_lbl.text = "Weak"
        strength_time_to_crack_lbl.text = "Time to crack: Hours to days"
    if strength_score >= 6:
        strength_password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel3_5.png"
        strength_password_strength_lbl.text = "Good"
        strength_time_to_crack_lbl.text = "Time to crack: Months to years"
    if strength_score >= 7:
        strength_password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel4_5.png"
        strength_password_strength_lbl.text = "Strong"
        strength_time_to_crack_lbl.text = "Time to crack: Years"
    if strength_score >= 8:
        strength_password_lvl.image = "../PasswordGenerator/PasswordLevelAssets/passwordlevel5_5.png"
        strength_password_strength_lbl.text = "Very Strong"
        strength_time_to_crack_lbl.text = "Time to crack: Centuries"
    else:
        pass

def common_breached_password(event):
    common_passwords = ["123456", "123456789", "12345", "qwerty", "password", "12345678", "111111", "123123", "1234567890", "1234567", "qwerty123", "000000", "1q2w3e", "aa12345678", "abc123", "password1", "1234", "qwertyuiop", "123321", "password123", "password"]

    if strength_password_inp.text.lower().replace(" ", "") in common_passwords:
        # common_breached_password_lbl.text = "Common Password Checker: Your password is one of the most commonly used."
        common_breached_password_lbl.text = """(!) - This password is part of the top breached passwords."""
    else:
        common_breached_password_lbl.text = "(/) - Not part of the top breached passwords."

def breached_password(event):
    try:
        count = ((check_password(strength_password_inp.text))["count"])
        breached_password_lbl.text = f"""Breach Total: {count:,}"""
        ScanSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/PasswordBreach3.mp3")
        ScanSound.play()
        if count > 1:
            breach_advice_lbl.text = """This password has previously appeared in a data breach. Immediate change of password 
recommended."""
        else:
            breach_advice_lbl.text = "This password wasn't found in any of the passwords loaded into HIBP."
    except:
        breached_password_lbl.text = f"""Breach Total: 0"""
        breach_advice_lbl.text = """(ERROR): Unable to connect to HIBP database due to blocked connection. Cannot provide 
information regarding password breaches at this time."""

def blacklisted_passwords(event):
    with open("BlacklistedPasswords.txt") as file:
        contents = file.read().split()
        if strength_password_inp.text.lower().replace(" ", "") in contents:
            blacklisted_passwords_lbl.text = """(!) - Contains a dictionary or blacklisted word."""
        else:
            blacklisted_passwords_lbl.text = """(/) - Does not contain a dictionary or blacklisted word."""
    pass

def blanket_strength_function(event):
    strength_select_image(event)

def breach_detection(event):
    breached_password(event)
    common_breached_password(event)
    blacklisted_passwords(event)

#Password Checker Window

def open_other_window(event):
    global other_window_music
    global is_window_open_chk
    global is_credits_window_open_chk

    if is_window_open_chk == False and is_credits_window_open_chk == False and is_submenu_window_open_chk == False:
        is_window_open_chk = True
        NewWindowSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/SidebarOpen1.mp3")
        NewWindowSound.play()
        pygame.mixer.music.pause()
        other_window_music.play(-1)
        other_window.show()
    else:
        pass

other_window = gp.Window(app, 'P.A.I.A - Password Strength Checker')
other_window.resizable_vertical = False

def music_close_other_window():
    global other_window_music
    global is_window_open_chk
    is_window_open_chk = False
    close_other_window = True
    other_window_music.stop()
    ExitConfirmationSound2 = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/QuitCancel2.mp3")
    ExitConfirmationSound2.play()
    pygame.mixer.music.unpause()
    return close_other_window

#Label Containers for Password Checker

password_strength_inp_container = gp.LabelContainer(other_window, "Input Password:")
password_strength_lvl_container = gp.LabelContainer(other_window, "Password Strength:")
password_strength_breach_container = gp.LabelContainer(other_window, "Breach Detection:")

#Strength Checker widgets
strength_password_inp = gp.Input(password_strength_inp_container)
strength_password_inp.width = 40
strength_copy_btn = gp.Button(password_strength_inp_container, "Copy to clipboard!", strength_copy_password)
strength_password_lvl = gp.Image(password_strength_lvl_container, "../PasswordGenerator/PasswordLevelAssets/passwordlevel0_4.png")
strength_password_strength_lbl = gp.Label(password_strength_lvl_container, "Critically Weak")
strength_time_to_crack_lbl = gp.Label(password_strength_lvl_container, "Time to crack: Less than a second")
common_breached_password_lbl = gp.Label(password_strength_breach_container, "(/) - Not part of the top breached passwords.")
breached_password_lbl = gp.Label(password_strength_breach_container, "Breach Total: 0")
password_breach_btn = gp.Button(password_strength_breach_container, "Check for breaches", breach_detection)
breach_advice_lbl = gp.Label(password_strength_breach_container, "This password wasn't found in any of the passwords loaded into HIBP.")
blacklisted_passwords_lbl = gp.Label(password_strength_breach_container, "(/) - Does not contain a dictionary or blacklisted word.")
strength_question_btn = gp.ImageButton(other_window, "../PasswordGenerator/PasswordGeneratorAssets/PAIAQuestionMark6.png", show_guidelines)

#Add Strength Checker widgets to their containers
password_strength_inp_container.set_grid(2, 2)
password_strength_inp_container.set_column_weights(1, 0)
password_strength_inp_container.add(strength_password_inp, 1, 1, stretch=True, fill=True)
password_strength_inp_container.add(strength_copy_btn, 2, 1)

password_strength_lvl_container.set_grid(5, 1)
password_strength_lvl_container.add(strength_password_strength_lbl, 1, 1, fill=True)
password_strength_lvl_container.add(strength_password_lvl, 2, 1, fill=True)
password_strength_lvl_container.add(strength_time_to_crack_lbl, 3, 1, fill=True)

password_strength_breach_container.set_grid(5, 1)
password_strength_breach_container.add(password_breach_btn, 1, 1)
password_strength_breach_container.add(breached_password_lbl, 2, 1, fill=True)
password_strength_breach_container.add(breach_advice_lbl, 3, 1, fill=True)
password_strength_breach_container.add(blacklisted_passwords_lbl, 4, 1, fill=True)
password_strength_breach_container.add(common_breached_password_lbl, 5, 1, fill=True)

#Main Second Window

other_window.set_grid(4, 1)
other_window.add(password_strength_inp_container, 1, 1, fill=True)
other_window.add(password_strength_breach_container, 2, 1, fill=True)
other_window.add(password_strength_lvl_container, 3, 1, fill=True)
other_window.add(strength_question_btn, 4, 1, align="right")

strength_password_inp.add_event_listener("change", blanket_strength_function)

other_window.on_close(music_close_other_window)

#Credits Window

def open_credits_window(event):
    global credits_window_music
    global is_credits_window_open_chk
    global is_window_open_chk

    if is_credits_window_open_chk == False and is_window_open_chk == False and is_guidelines_window_open_chk == False and is_privacy_window_open_chk == False and is_about_window_open_chk == False:
        is_credits_window_open_chk = True
        creditsWindowSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/SidebarOpen1.mp3")
        creditsWindowSound.play()
        submenu_window_music.stop()
        credits_window_music.play(-1)
        credits_window.show()
    else:
        pass

credits_window = gp.Window(app, "P.A.I.A - Credits")
credits_window.resizable_vertical = False

def music_close_credits_window():
    global credits_window_music
    global is_credits_window_open_chk
    is_credits_window_open_chk = False
    close_credits_window = True
    credits_window_music.stop()
    ExitConfirmationSound3 = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/QuitCancel2.mp3")
    ExitConfirmationSound3.play()
    submenu_window_music.play(-1)
    return close_credits_window

#Label containers for credits window

credits_container = gp.LabelContainer(credits_window, "Credits:")
composers_container = gp.LabelContainer(credits_window, "Composers:")
sounddesign_container = gp.LabelContainer(credits_window, "Sound Design:")

#Add credits widgets

credits = gp.Label(credits_container, """Developer: Devon Kawaguchi                              """)

composer1 = gp.Label(composers_container, """Daisuke Matsuoka - Nintendo""")
composer2 = gp.Label(composers_container, """Asuka Ito - Nintendo""")
composer3 = gp.Label(composers_container, """Kazumi Totaka - Nintendo""")

sounddesign1 = gp.Label(sounddesign_container, """Pascal Michael Stiefel""")

#Add credits widgets to their containers

credits_container.set_grid(1, 1)
credits_container.add(credits, 1, 1, fill=True)

composers_container.set_grid(3, 1)
composers_container.add(composer1, 1, 1, fill=True)
composers_container.add(composer2, 2, 1, fill=True)
composers_container.add(composer3, 3, 1, fill=True)

sounddesign_container.set_grid(1, 1)
sounddesign_container.add(sounddesign1, 1, 1, fill=True)

#Set grid for credits window

credits_window.set_grid(3,1)
credits_window.add(credits_container, 1, 1, fill=True)
credits_window.add(composers_container, 2, 1, fill=True)
credits_window.add(sounddesign_container, 3, 1, fill=True)

#Credits window event listeners

credits_window.on_close(music_close_credits_window)

#Guidelines Window

def open_guidelines_window(event):
    global guidelines_window_music
    global is_guidelines_window_open_chk
    global is_window_open_chk

    if is_guidelines_window_open_chk == False and is_window_open_chk == False and is_credits_window_open_chk == False and is_privacy_window_open_chk == False and is_about_window_open_chk == False:
        is_guidelines_window_open_chk = True
        GuidelinesWindowSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/SidebarOpen1.mp3")
        GuidelinesWindowSound.play()
        pygame.mixer.music.pause()
        submenu_window_music.stop()
        guidelines_window_music.play(-1)
        guidelines_window.show()
    else:
        pass

guidelines_window = gp.Window(app, "P.A.I.A - Guidelines")
guidelines_window.resizable_vertical = False

def music_close_guidelines_window():
    global guidelines_window_music
    global is_guidelines_window_open_chk
    is_guidelines_window_open_chk = False
    close_guidelines_window = True
    guidelines_window_music.stop()
    ExitConfirmationSound3 = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/QuitCancel2.mp3")
    ExitConfirmationSound3.play()
    submenu_window_music.play(-1)
    return close_guidelines_window

#Label containers for guidelines window

guidelines_container = gp.LabelContainer(guidelines_window, "Password Strength - Criteria:")
guidelines2_container = gp.LabelContainer(guidelines_window, "Password Score - Criteria:")

#Add guidelines widgets

guidelines1 = gp.Label(guidelines_container, """Password strength is measured in terms of the password length and complexity, as determined 
by the inclusion of lowercase, uppercase, digits, or symbol characters in the password. """)
                       
guidelines2 = gp.Label(guidelines_container, """Each inclusion of one of these password complexity criteria tallies one point to the password’s 
cumulative strength score. """)
                       
guidelines3 = gp.Label(guidelines_container, """A point is also tallied each time password length exceeds certain thresholds, as demonstrated 
by the chart below:""")

strength_chart_img = gp.Image(guidelines_container, "../PasswordGenerator/PasswordGeneratorAssets/PAIAStrengthChartResized5.png")

guidelines4 = gp.Label(guidelines2_container, """Once the total strength score of a password is tallied, the application displays its overall 
grade per the following criteria:""")
                       
guidelines5 = gp.Label(guidelines2_container, """A score of 3 and under is critically weak, 4 is very weak, 5 is weak, 6 is good, 7 is strong, 
and 8 is very strong.""")

guidelines6 = gp.Label(guidelines2_container, """This methodology applies to the password checker as well.""")

#Add guidelines widgets to their containers

guidelines_container.set_grid(6, 1)
guidelines_container.add(guidelines1, 1, 1, fill=True)
guidelines_container.add(guidelines2, 2, 1, fill=True)
guidelines_container.add(guidelines3, 3, 1, fill=True)
guidelines_container.add(strength_chart_img, 4, 1, fill=True)

guidelines2_container.set_grid(3, 1)
guidelines2_container.add(guidelines4, 1, 1, fill=True)
guidelines2_container.add(guidelines5, 2, 1, fill=True)
guidelines2_container.add(guidelines6, 3, 1, fill=True)

#Set grid for guidelines window

guidelines_window.set_grid(2,1)
guidelines_window.add(guidelines_container, 1, 1, fill=True)
guidelines_window.add(guidelines2_container, 2, 1, fill=True)

#Guidelines window event listeners

guidelines_window.on_close(music_close_guidelines_window)

#Privacy Policy Window

def open_privacy_window(event):
    global privacy_window_music
    global is_privacy_window_open_chk
    global is_window_open_chk

    if is_privacy_window_open_chk == False and is_window_open_chk == False and is_credits_window_open_chk == False and is_guidelines_window_open_chk == False and is_about_window_open_chk == False:
        is_privacy_window_open_chk = True
        privacyWindowSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/SidebarOpen1.mp3")
        privacyWindowSound.play()
        pygame.mixer.music.pause()
        submenu_window_music.stop()
        privacy_window_music.play(-1)
        privacy_window.show()
    else:
        pass

privacy_window = gp.Window(app, "P.A.I.A - Privacy Policy")
privacy_window.resizable_vertical = False

def music_close_privacy_window():
    global privacy_window_music
    global is_privacy_window_open_chk
    is_privacy_window_open_chk = False
    close_privacy_window = True
    privacy_window_music.stop()
    ExitConfirmationSound3 = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/QuitCancel2.mp3")
    ExitConfirmationSound3.play()
    submenu_window_music.play(-1)
    return close_privacy_window

#Label containers for privacy window

privacy_container = gp.LabelContainer(privacy_window, "Preface:")
privacy_table_container = gp.LabelContainer(privacy_window, "Table of Contents:")

#Add privacy widgets

privacy1 = gp.Label(privacy_container, """Although PAIA does not collect, store, or transmit any personal information, as 
the application is processed locally on user devices, PAIA is not required to 
have a privacy policy.""")
                       
privacy2 = gp.Label(privacy_container, """Nevertheless, PAIA employs a privacy policy as a means of clearly communicating to 
users what data the application collects and how it is used, as well as affirming the 
application’s dedication towards ensuring user privacy.""")
                    
privacy3 = gp.Label(privacy_table_container, """Please refer to the full privacy policy document attached in the application folder.""")
                    
privacy4 = gp.Label(privacy_table_container, """1. Security""")

privacy5 = gp.Label(privacy_table_container, """2. Privacy Policy Changes""")

privacy6 = gp.Label(privacy_table_container, """3. Contact Information & Credit""")

#Add privacy widgets to their containers

privacy_container.set_grid(3, 1)
privacy_container.add(privacy1, 1, 1, fill=True)
privacy_container.add(privacy2, 2, 1, fill=True)

privacy_table_container.set_grid(4, 1)
privacy_table_container.add(privacy4, 1, 1, fill=True)
privacy_table_container.add(privacy5, 2, 1, fill=True)
privacy_table_container.add(privacy6, 3, 1, fill=True)
privacy_table_container.add(privacy3, 4, 1, fill=True)

#Set grid for privacy window

privacy_window.set_grid(2,1)
privacy_window.add(privacy_container, 1, 1, fill=True)
privacy_window.add(privacy_table_container, 2, 1, fill=True)

#privacy window event listeners

privacy_window.on_close(music_close_privacy_window)

#About Policy Window

def open_about_window(event):
    global about_window_music
    global is_about_window_open_chk
    global is_window_open_chk

    if is_about_window_open_chk == False and is_window_open_chk == False and is_credits_window_open_chk == False and is_guidelines_window_open_chk == False and is_privacy_window_open_chk == False:
        is_about_window_open_chk = True
        aboutWindowSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/SidebarOpen1.mp3")
        aboutWindowSound.play()
        pygame.mixer.music.pause()
        submenu_window_music.stop()
        about_window_music.play(-1)
        about_window.show()
    else:
        pass

about_window = gp.Window(app, "P.A.I.A - About")
about_window.resizable_vertical = False

def music_close_about_window():
    global about_window_music
    global is_about_window_open_chk
    is_about_window_open_chk = False
    close_about_window = True
    about_window_music.stop()
    ExitConfirmationSound3 = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/QuitCancel2.mp3")
    ExitConfirmationSound3.play()
    submenu_window_music.play(-1)
    return close_about_window

#Label containers for about window

about_container = gp.LabelContainer(about_window, "Description:")
about_img_container = gp.LabelContainer(about_window, "PAIA - Icon:")

#Add about widgets

about1 = gp.Label(about_container, """Aiming to streamline the process of cybersecurity, PAIA, an acronym for 
protect, authenticate, identify, and alert, is a user-friendly password 
generator application that protects users through unique password 
generation, authenticates through password strength evaluation, identifies 
by displaying password breaches, and alerts by informing users of 
compromised passwords.""")
                       
about2 = gp.Label(about_container, """Serving as my Junior Term 1 Software Assessment, PAIA is intended to aid 
audiences of all ages, especially elderly, identify and develop strong 
cybersecurity measures.""")
                  
about_img = gp.Image(about_img_container, "../PasswordGenerator/PasswordGeneratorAssets/PAIANewIcon6.png")

#Add about widgets to their containers

about_container.set_grid(3, 2)
about_container.add(about1, 1, 1, fill=True)
about_container.add(about2, 2, 1, fill=True)

about_img_container.set_grid(1, 1)
about_img_container.add(about_img, 1, 1, fill=True)

#Set grid for about window

about_window.set_grid(2,2)
about_window.add(about_container, 1, 1, fill=True)
about_window.add(about_img_container, 1, 2, fill=True)

#about window event listeners

about_window.on_close(music_close_about_window)

#Submenu Window

def open_submenu_window(event):
    global submenu_window_music
    global is_submenu_window_open_chk
    global is_window_open_chk

    if is_submenu_window_open_chk == False and is_window_open_chk == False:
        is_submenu_window_open_chk = True
        submenuWindowSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/SidebarOpen1.mp3")
        submenuWindowSound.play()
        pygame.mixer.music.pause()
        submenu_window_music.play(-1)
        submenu_window.show()
    else:
        pass

submenu_window = gp.Window(app, "P.A.I.A - Menu")
submenu_window.resizable_vertical = False

def music_close_submenu_window():
    if is_guidelines_window_open_chk == False and is_credits_window_open_chk == False and is_privacy_window_open_chk == False and is_about_window_open_chk == False:
        global submenu_window_music
        global is_submenu_window_open_chk
        is_submenu_window_open_chk = False
        close_submenu_window = True
        submenu_window_music.stop()
        ExitConfirmationSound3 = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/QuitCancel2.mp3")
        ExitConfirmationSound3.play()
        pygame.mixer.music.unpause()
        return close_submenu_window

#Label containers for submenu window

submenu_container = gp.LabelContainer(submenu_window, "Options:")
submenu_img_container = gp.LabelContainer(submenu_window, "Menu:")

#Add submenu widgets

open_guidelines_btn = gp.Button(submenu_container, "  Guidelines  ", open_guidelines_window)
open_privacy_btn = gp.Button(submenu_container, "Privacy Policy", open_privacy_window)
open_about_btn = gp.Button(submenu_container, "About", open_about_window)
open_credits_btn = gp.Button(submenu_container, "Credits", open_credits_window)

paia_menu_img = gp.Image(submenu_img_container, "../PasswordGenerator/PasswordGeneratorAssets/PAIAMenuIcon4.png")

#Add submenu widgets to their containers

submenu_img_container.set_grid(1, 1)
submenu_img_container.add(paia_menu_img, 1, 1, fill=True)

submenu_container.set_grid(2, 2)
submenu_container.set_column_weights(1, 1)
submenu_container.add(open_guidelines_btn, 1, 1, fill=True, column_span=1)
submenu_container.add(open_privacy_btn, 1, 2, fill=True, column_span=1)
submenu_container.add(open_about_btn, 2, 1, fill=True, column_span=1)
submenu_container.add(open_credits_btn, 2, 2, fill=True, column_span=1)

#Set grid for submenu window

submenu_window.set_grid(2,1)
submenu_window.add(submenu_img_container, 1, 1, fill=True)
submenu_window.add(submenu_container, 2, 1, fill=True)

#submenu window event listeners

submenu_window.on_close(music_close_submenu_window)

#Main Window widgets

def check_exit():
    ExitConfirmationSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/ExitConfirmationSound1.mp3")
    ExitConfirmationSound.play()
    ok_to_exit = app.confirm_yesno('Really?', 'Are you sure you want to close?', 'question')
    QuitCancelSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/QuitCancel2.mp3")
    QuitCancelSound.play()
    return ok_to_exit

#SOUNDS AND MUSIC 

def checksound(event):
    if letters_chk.checked == False:
        EnterSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/UncheckSound1.mp3")
        EnterSound.play()
    elif letters_chk.checked == True:
        EnterSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/CheckSound2.mp3")
        EnterSound.play()

def checksound2(event):
    if capitalletters_chk.checked == False:
        EnterSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/UncheckSound1.mp3")
        EnterSound.play()
    elif capitalletters_chk.checked == True:
        EnterSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/CheckSound2.mp3")
        EnterSound.play()

def checksound3(event):
    if digits_chk.checked == False:
        EnterSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/UncheckSound1.mp3")
        EnterSound.play()
    elif digits_chk.checked == True:
        EnterSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/CheckSound2.mp3")
        EnterSound.play()

def checksound4(event):
    if symbols_chk.checked == False:
        EnterSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/UncheckSound1.mp3")
        EnterSound.play()
    elif symbols_chk.checked == True:
        EnterSound = mixer.Sound("../PasswordGenerator/PasswordGeneratorMusic/CheckSound2.mp3")
        EnterSound.play()

#BOTH SOUNDS AND SHOW_NEW_PASSWORD

def sound_and_npassword1(event):
    show_new_password(event)
    checksound(event)
    select_image(event)

def sound_and_npassword2(event):
    show_new_password(event)
    checksound2(event)
    select_image(event)

def sound_and_npassword3(event):
    show_new_password(event)
    checksound3(event)
    select_image(event)

def sound_and_npassword4(event):
    show_new_password(event)
    checksound4(event)
    select_image(event)

#Create label containers

length_cont = gp.LabelContainer(app, "Length:")
options_cont = gp.LabelContainer(app, "Options:")
password_cont = gp.LabelContainer(app, "Password:")
password_strength = gp.LabelContainer(app, "Password Strength:")

menu = gp.LabelContainer(app, "Menu:") #Menu
submenu = gp.LabelContainer(app, "") #Submenu

img_cont = gp.LabelContainer(app, "")

#Password Strength widgets

password_lvl = gp.Image(password_strength, "../PasswordGenerator/PasswordLevelAssets/testlevel1.png")

#Images

paia_img = gp.Image(img_cont, "../PasswordGenerator/PasswordGeneratorAssets/PAIAIconResizedNew1.png")


# BOTH PASSWORD STRENGTH AND SHOW_NEW_PASSWORD

def strength_and_npassword1(event):
    show_new_password(event)
    select_image(event)

#Create length select widgets
length_lbl = gp.Label(length_cont, f"{default_password_length} characters")
length_sld = gp.Slider(length_cont, 2, 50)

#Password strength label widget

password_strength_header = gp.StyleLabel(password_strength, "Password Strength:")
password_strength_lbl = gp.Label(password_strength, "Your password is:")
time_to_crack_lbl = gp.Label(password_strength, "Time to crack:")

#Create password options widgets
letters_chk = gp.Checkbox(options_cont, "- Lowercase Letters")
capitalletters_chk = gp.Checkbox(options_cont, "- Uppercase Letters")
digits_chk = gp.Checkbox(options_cont, "- Digits")
symbols_chk = gp.Checkbox(options_cont, "- Symbols")
letters_chk.checked = True
capitalletters_chk.checked = True
digits_chk.checked = True
symbols_chk.checked = True

#Create password widgets

password_inp = gp.Input(password_cont)
password_inp.width = 40
reload_btn = gp.ImageButton(password_cont, "../PasswordGenerator/PasswordGeneratorAssets/RefreshIcon.png", refresh_new_password)
copy_btn = gp.Button(password_cont, "Copy to clipboard!", copy_password)
open_other_btn = gp.Button(menu, "Password Checker", open_other_window)

open_submenu_btn = gp.Button(menu, "Menu", open_submenu_window)

# test_btn = gp.Button(menu, "Next", open_other_window)

guidelines_btn = gp.ImageButton(password_strength, "../PasswordGenerator/PasswordGeneratorAssets/RefreshIcon.png", show_guidelines)

#Add all widgets to their containers
length_cont.set_grid(2, 1)
length_cont.add(length_lbl, 1, 1)
length_cont.add(length_sld, 2, 1, fill=True)

options_cont.set_grid(4, 1)
options_cont.add(letters_chk, 1, 1)
options_cont.add(capitalletters_chk, 2, 1)
options_cont.add(digits_chk, 3, 1)
options_cont.add(symbols_chk, 4, 1)

password_cont.set_grid(2, 2)
password_cont.set_column_weights(1, 0)
password_cont.add(password_inp, 1, 1, stretch=True, fill=True)
password_cont.add(reload_btn, 1, 2)
password_cont.add(copy_btn, 2, 1)

password_strength.set_grid(3, 2)
password_strength.add(password_strength_lbl, 1, 1, fill=True)
password_strength.add(password_lvl, 2, 1, fill=True)
password_strength.add(time_to_crack_lbl, 3, 1, fill=True)

menu.set_grid(2, 1)
menu.add(open_other_btn, 1, 1)
menu.add(open_submenu_btn, 2, 1, fill=True)

img_cont.set_grid(1, 1)
img_cont.add(paia_img, 1, 1)

#Add widgets to the main window
app.set_grid(5, 2)
app.add(length_cont, 1, 2, fill=True)
app.add(options_cont, 2, 2, fill=True)
app.add(password_cont, 3, 2, fill=True)
app.add(password_strength, 4, 2, fill=True)

app.add(menu, 1, 1)
app.add(img_cont, 2, 1, fill=True)

#Length slide event listener
length_sld.add_event_listener("change", strength_and_npassword1)

#Add event listeners 
letters_chk.add_event_listener("change", sound_and_npassword1)
capitalletters_chk.add_event_listener("change", sound_and_npassword2)
digits_chk.add_event_listener("change", sound_and_npassword3)
symbols_chk.add_event_listener("change", sound_and_npassword4)

length_sld.value = default_password_length

select_image(None)

mixer.music.load("../PasswordGenerator/PasswordGeneratorMusic/passwordtitlemusic2.mp3")
mixer.music.play(-1)

app.on_close(check_exit)

app.run()

