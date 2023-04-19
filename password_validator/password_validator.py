# Gooeypie import to allow windows to pop up
import gooeypie as gp
# Pwned Passwords API
import pyhibp
from pyhibp import pwnedpasswords as pw
# List of strings, characters, digits, and the capablilites to randomise them for password generator
import string
import random

# Revealing password with a checkbox event
def toggle_mask(event):
    pass_inp.toggle()


def login(event):

    # Error message if no input
    if len(pass_inp.text) < 1:
        app.alert("ERROR", "Please type a password", "warning")
        return
        
    
    # Checking Password Input Length
    length_detection = False
    if len(pass_inp.text) > 8:
        length_detection = True
    else:
        length_detection = False
    
    if length_detection == True:
        length_check.text = '✅ Length is greater than 8'
    else:
        length_check.text = '❌ Length is less than 8'

    # Checking if Numbers in Password
    pass_has_numbers = False
    for i in pass_inp.text:
        if i.isdigit():
            pass_has_numbers = True

    if pass_has_numbers == True:
        number_check.text = '✅ Has Numbers'
    else:
        number_check.text = "❌ Doesn't have Numbers"
    
    # Checking if there are uppercase letters in Password
    pass_is_capital = False
    for i in pass_inp.text:
        if i.isupper():
            pass_is_capital = True 
        
    if pass_is_capital == True:
        upper_check.text = '✅ Has Capitals'
    else:
        upper_check.text = "❌ Doesn't have Capitals"

    # Checking if there are characters in Password
    character_detection = False
    symbols = string.punctuation
    for i in pass_inp.text:
            if i in symbols:
                character_detection = True

    if character_detection == True:
        character_check.text = '✅ Has Characters'
    else:
        character_check.text = "❌ Doesn't have Characters"

    
    # Checking if password is in the blacklist
    with open('blacklisted_words.txt') as blacklisted_words:
        breached = False
        for line in blacklisted_words:
            if line.strip() == str(pass_inp.text):
                breached = True
        if breached == True:
            blacklist_check.text = "❌ In Blacklist"
        if breached == False:
            blacklist_check.text = "✅ Not in Blacklist"

    # Checking if password has been publicly breached using pwned API
    try:
        
        pyhibp.set_user_agent(ua="Pwned Application")

        resp = pw.is_password_breached(password=str(pass_inp.text))
        if resp:
            pwned_detector = True
        else:
            pwned_detector = False    
            
        if pwned_detector == True:
            pwned_check.text = '❌ Has been breached'
        else:
            pwned_check.text = "✅ Hasn't been breached"
    
    except:
        app.alert("ERROR", "Error accessing pwned API at this moment. Please try again later", "error")
        pwned_check.text = 'Cannot access pwned API'


    # Star Rating
    
    star_rating = 0
        
    if length_detection == True:
        star_rating = star_rating + 1
    else:
        pass
    if character_detection == True:
        star_rating = star_rating + 1
    else:
        pass
    if pass_has_numbers == True:
        star_rating = star_rating + 1
    else:
        pass
    if pass_is_capital == True:
        star_rating = star_rating + 1
    else:
        pass
    if breached == False:
        star_rating = star_rating + 1
    else:
        pass

    # Takes value of star_rating and multiplies it by a star. Outcome will produce 0-5 stars / 5 stars
    star_check.text = "⭐"*star_rating + ' / 5 Stars'


app = gp.GooeyPieApp('Password Strength Checker')

# Event to reveal the criteria window when the criteria button is pressed
def show_criteria_window(event):
    criteria_window.show()



criteria_window = gp.Window(app, 'Password Criteria')
criteria_window.width = 350
criteria_window.height = 250

# Criteria Window Labels
length_tip_lbl = gp.Label(criteria_window, 'Is your password at least 8 digits long? (1 star)')
number_tip_lbl = gp.Label(criteria_window, 'Have you included numbers/digits within your password? (1 star)')
capitals_tip_lbl = gp.Label(criteria_window, 'Have you included capital/uppercase letters in your password? (1 star)')
character_tip_lbl = gp.Label(criteria_window, 'Have you included special characters (!, @, #, etc.) in your password? (1 star)')
blacklist_tip_lbl = gp.Label(criteria_window, 'Is your password in the blacklist (ie. uses common phrases, letters or names)? (1 star)')
pwned_tip_lbl = gp.Label(criteria_window, 'Has your password been publicly breached (pwned) at least once?')
pwned_hyperlink = gp.Hyperlink(criteria_window, 'Have I Been Pwned Website', 'https://haveibeenpwned.com/Passwords')
suggestion_lbl = gp.StyleLabel(criteria_window, 'Struggling to make a strong password? Try our password generator using the button on the previous page!')
suggestion_lbl.font_style = 'italic'

# Criteria Window Grid Layout
criteria_window.set_grid(8, 1)
criteria_window.add(length_tip_lbl, 1, 1)
criteria_window.add(number_tip_lbl, 2, 1)
criteria_window.add(capitals_tip_lbl, 3, 1)
criteria_window.add(character_tip_lbl, 4, 1)
criteria_window.add(blacklist_tip_lbl, 5, 1)
criteria_window.add(pwned_tip_lbl, 6, 1)
criteria_window.add(pwned_hyperlink, 7, 1)
criteria_window.add(suggestion_lbl, 8, 1)

# Event to reveal the password generator window when the password generator button is pressed
def show_generator_window(event):
    generator_app.show()

generator_app = gp.Window(app, 'Password Generator')
generator_app.width = 350
generator_app.height = 200

# Options is the dropdown options which the user will select. The selected option will be the the contents of the password
options = ['Select Option', 'Letters', 'Letters and Numbers', 'Letters, Numbers and Characters', 'Numbers', 'Numbers and Characters', 'Letters and Characters', 'Characters']

# This is the event to process the choice selected into its respective assortment of letters, digits and/or punctuation
def convert(event):
    # Default dropdown option. No output
    if dropdown.selected == 'Select Option':
        choices = ' '
    elif dropdown.selected == 'Letters':
        choices = string.ascii_letters
    elif dropdown.selected == 'Letters and Numbers':
        choices = string.ascii_letters + string.digits
    elif dropdown.selected == 'Letters, Numbers and Characters':
        choices = string.ascii_letters + string.digits + string.punctuation
    elif dropdown.selected == 'Numbers':
        choices = string.digits
    elif dropdown.selected == 'Numbers and Characters':
        choices = string.digits + string.punctuation
    elif dropdown.selected == 'Letters and Characters':
        choices = string.ascii_letters + string.punctuation
    elif dropdown.selected == 'Characters':
        choices = string.punctuation
        
    new_password = ''
    password_output.text = new_password
    # Takes slider value and applies it to length of password
    # Takes choices and randomises its order and gives it the given length
    for n in range(slider.value):
        password_output.text += random.choice(choices)

        
# event to copy password to clipboard when pressing the 'copy to clipboard' button
def copy(event):
    app.copy_to_clipboard(password_output.text)


dropdown_lbl = gp.Label(generator_app, 'Select Password Contents')
slider_lbl = gp.Label(generator_app, 'Set Desired Length')
output_lbl = gp.Label(generator_app, 'Password: ')
slider = gp.Slider(generator_app, 5, 20)
dropdown = gp.Dropdown(generator_app, options)
dropdown.selected_index = 0
dropdown.width = 30
refresh_btn = gp.Button(generator_app, 'Refresh', convert)
refresh_btn.width = 20
password_output = gp.Input(generator_app)
copy_to_clip_btn = gp.Button(generator_app, 'Copy to Clipboard', copy)
copy_to_clip_btn.width = 33
password_output.justify = 'center'


slider.add_event_listener('change', convert)


generator_app.set_grid(4,3)
generator_app.add(dropdown_lbl, 1, 1)
generator_app.add(slider_lbl, 2, 1)
generator_app.add(output_lbl, 3, 1)
generator_app.add(refresh_btn, 4, 1)
generator_app.add(dropdown, 1, 2, column_span = 2)
generator_app.add(slider, 2, 2, fill=True)
generator_app.add(password_output, 3, 2, fill=True)
generator_app.add(copy_to_clip_btn, 4, 2)


slider.value = 8



pass_lbl = gp.StyleLabel(app, "Enter Password:")
pass_lbl.font_size = 11
pass_lbl.font_weight = 'bold'
pass_lbl.underline = 'underline'
pass_inp = gp.Secret(app)
pass_inp.width = 25
test_btn = gp.Button(app, 'Test Password', login)
length_label = gp.Label(app, 'Length: ') 
character_label = gp.Label(app, 'Characters: ') 
length_check = gp.Label(app, '')
character_check = gp.Label(app, '')
character_check.width = 25
number_label = gp.Label(app, 'Numbers: ')
number_check = gp.Label(app, '')
number_check.width = 25
upper_label = gp.Label(app, 'Has Capitals: ')
upper_check = gp.Label(app, '')
blacklist_label = gp.Label(app, 'In Blacklist: ')
blacklist_check = gp.Label(app, '')
pwned_breach = gp.Label(app, 'Publicly Breached: ')
pwned_breach.width = 20
pwned_check = gp.Label(app, '')
star_label = gp.StyleLabel(app, 'Password Rating: ')
star_label.font_style = 'italic'
star_check = gp.Label(app, '')
criteria_btn = gp.Button(app, 'Criteria', show_criteria_window)
criteria_btn.width = 20
pass_generator_btn = gp.Button(app, 'Password Generator', show_generator_window)
pass_generator_btn.width = 25


check = gp.Checkbox(app, 'Show Password')
check.add_event_listener('change', toggle_mask)

app.set_grid(10, 5)
app.add(pass_lbl, 1, 1)
app.add(pass_inp, 1, 2, column_span = 2)
app.add(test_btn, 2, 1)
app.add(check, 2, 2, column_span = 2)
app.add(length_label, 3, 1, column_span = 2)
app.add(length_check, 3, 3, column_span = 2)
app.add(number_label, 4, 1, column_span = 2)
app.add(number_check, 4, 3, column_span = 2)
app.add(upper_label, 5, 1, column_span = 2)
app.add(upper_check, 5, 3, column_span = 2)
app.add(character_label, 6, 1, column_span = 2)
app.add(character_check, 6, 3, column_span = 2)
app.add(blacklist_label, 7, 1, column_span = 2)
app.add(blacklist_check, 7, 3, column_span = 2)
app.add(pwned_breach, 8, 1, column_span = 2)
app.add(pwned_check, 8, 3, column_span = 2)
app.add(star_label, 9, 1)
app.add(star_check, 9, 3)
app.add(criteria_btn, 10, 1)
app.add(pass_generator_btn, 10, 3)


app.run()