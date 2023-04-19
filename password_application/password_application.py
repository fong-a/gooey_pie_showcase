# Extensions/Imports Used for Password Application:
import gooeypie as gp
import string
import random

# For password breach checker:
import pyhibp
from pyhibp import pwnedpasswords as pw

# checkbox for "Show Password"
def toggle_mask_main(event):
    pass_inp.toggle()

# opens generator window
def open_generator_window(event):
    generator_window.show_on_top()

# Main Window -> Each process contributes to the strength of the User's Password
def password_check(event):
    # Defining default values for password strength
    # not_blacklisted = False
    pass_length_valid = False
    pass_cap_valid = False
    pass_symbols_valid = False
    pass_nums_valid = False

    # Compulsory checks - > determines if User has entered a valid (not blank) username and/or password
    with open('Blacklisted_words.txt', 'r') as file:
        if user_inp.text == '':
            app.alert("Invalid Username", "Please Enter a Username", "warning")
            return
        else:
            pass
        
        if pass_inp.text == '':
            app.alert("Invalid Password", "Please enter a Password", "warning")
            return
        else:
            pass

        # 1st strength check -> determines if the password the user entered is contained within the "Blacklisted_words.txt" text file
        blacklisted = False
        output = [ line.strip().split(' ') for line in file.readlines()]
        # ^^^ places all words inside the text file into a list using the '.split()' function
        for i in output:
            if i[0] == pass_inp.text:
                # checks if the user's password is the currently-focused blacklisted word
                blacklisted = True
            else:
                pass
        
        if blacklisted == True:
            # not_blacklisted = False 
            # if password entered is blacklisted, open a pop-up window alerting the user
            app.alert("Password Blacklisted", "Password is blacklisted, please try again", 'warning')
            # also re-sets the star rating to 0, and with the "return" function, skips/ignores the rest of the def function
            stars = 0
            return
        else:
            pass

    # 2nd strength check -> determines if user's password is 8 characters or more and update variables/labels accordingly
    if len(pass_inp.text) >= 8:
        pass_length_valid = True
        length_check.text = '✔️'
    else:
        pass_length_valid = False
        length_check.text = '❌'

    # 3rd strength check -> determines if user's password contains at least 1 capital letter using the ".isupper()" function
    contains_cap = False
    for i in pass_inp.text:
        if i.isupper() == True:
            contains_cap = True
        else:
            pass
            
    # updates the label depending on whether the password has capitals or not
    if contains_cap == True:
        pass_cap_valid = True 
        caps_check.text = '✔️'
    else:
        pass_cap_valid = False
        caps_check.text = '❌'

    # 4th strength check -> determines if user's password contains at least 1 symbol/special character using a set symbols list, "s"
    contains_symbols = False
    # List of all 'detectable' symbols
    symbols = '!@#$%^&*()_+-=[]}{<,>.?/`~\|;:'
 
    for i in pass_inp.text:
        if i in symbols:
            contains_symbols = True

    # updates the label depending on whether the password has symbols or not
    if contains_symbols == True:
        pass_symbols_valid = True
        symbols_check.text = '✔️'

    else:
        pass_symbols_valid = False
        symbols_check.text = '❌'

    # 5th strength check -> determines if user's password contains at least 1 digit using the ".isdigit" function
    contains_digits = False
    for i in pass_inp.text:
        if i.isdigit() == True:
            contains_digits = True
    
    # updates the label depending on whether the password has digits or not
    if contains_digits == True:
        pass_nums_valid = True
        nums_check.text = '✔️'

    else:
        pass_nums_valid = False
        nums_check.text = '❌'

    # Beginning of the star-rating process:
    # sets default star-rating to 0
    stars = 0
    # goes through every previous function, if the strength check's value is true, increase the star-rating by 1 star
    if pass_length_valid == True:
        stars = stars + 1
    else:
        pass
    if pass_cap_valid == True:
        stars = stars + 1
    else:
        pass
    if pass_symbols_valid == True:
        stars = stars + 1
    else:
        pass
    if pass_nums_valid == True:
        stars = stars + 1
    else:
        pass
    # if user's password is blacklisted, reset the star-rating to 0
    if blacklisted == True:
        stars = 0
    else:
        stars = stars + 1
    
    # updates the "star-rating" label to display strength of user's password in the form of stars
    # "stars" is a counter, so when this label-update occurs it will display the single-character string "⭐", 
    # multiplied by the counter's value, a.k.a the user's password strength 
    star_rating_lbl.text = "⭐"*stars

# defines the main app's window AND the main password input from the user
app = gp.GooeyPieApp('Password')
pass_inp = gp.Secret(app)

# defines the "Have I Been Pwned" window, including title and dimensions
# also defines pwned window's widgets
pwned_top_window = gp.Window(app, 'Have I Been Pwned?')
pwned_top_window.width = 350
pwned_top_window.height = 150
pwned_number = gp.Label(pwned_top_window, '')
pass_inp = gp.Secret(app)
pwned_top_message = gp.Label(pwned_top_window, 'How many times your password has been breached:')
pwned_top_window.set_grid(2, 1)
pwned_top_window.add(pwned_top_message, 1, 1)
pwned_top_window.add(pwned_number, 2, 1)

# main process of pwned window -> determines how many times the user's password has been breached
def have_i_been_pwned_window(event):
    # Try statement: fancy elif statement; states that if the 'try' code cannot be applied, run the 'except' code instead.
    try:
        pyhibp.set_user_agent(ua="Password Application")
        if pass_inp.text == '':
            app.alert("Invalid Password", "Please enter a Password", "warning")
            return
        else:
            pass
        resp = pw.is_password_breached(password=pass_inp.text)
        if resp:
            pwned_number.text = f"This password has been used online {resp} time(s) before"
        else:
            pwned_number.text = "Your password has not been breached!"

        # opens the new window on-top of main
        pwned_top_window.show_on_top()
    except:
        app.alert("Cannot Access API", "Cannot access Pwned API at this moment, please try again later.", "warning")

# defines Main window's widgets, e.g. labels, buttons, etc
user_lbl = gp.Label(app, "Enter a Username:")
user_inp = gp.Input(app)
pass_lbl = gp.Label(app, "Enter a Password:")
check_btn = gp.Button(app, 'Check Password', password_check)
open_password_generator = gp.Button(app, 'Create New Password', open_generator_window)
open_breach_checker = gp.Button(app, 'Have I Been Pwned?', have_i_been_pwned_window)
pass_length = gp.Label(app, "8 or More Characters?")
length_check = gp.Label(app, "")
pass_cap = gp.Label(app, "Contains Capital Letter?")
caps_check = gp.Label(app, "")
pass_symbols = gp.Label(app, "Contains Symbol?")
symbols_check = gp.Label(app, "")
pass_nums = gp.Label(app, "Contains Number?")
nums_check = gp.Label(app, "")
star_rating_lbl = gp.Label(app, '')
password_rating = gp.Label(app, 'Password Rating:')
styled_label = gp.StyleLabel(app, 'Password Application')
styled_label.font_size = 12
styled_label.font_weight = 'bold'
styled_label.underline = 'underline'

# Checkbox used for hiding/un-hiding the user's input password
checkbox = gp.Checkbox(app, 'Show Password')
checkbox.add_event_listener('change', toggle_mask_main)

# main window's dimensions and title
app.title = 'Password Application'
app.width = 320
app.height = 400

# adds all previously defined (main application, or 'app') widgets into the main password application window via the grid
app.set_grid(11, 2)
app.add(styled_label, 1, 1, column_span=2)
app.add(user_lbl, 2, 1)
app.add(user_inp, 2, 2)
app.add(pass_lbl, 3, 1)
app.add(pass_inp, 3, 2)
app.add(check_btn, 4,1)
app.add(checkbox, 4, 2)
app.add(pass_length, 5, 1)
app.add(length_check, 5, 2)
app.add(pass_cap, 6, 1)
app.add(caps_check, 6, 2)
app.add(pass_symbols, 7, 1)
app.add(symbols_check, 7, 2)
app.add(pass_nums, 8, 1)
app.add(nums_check, 8, 2)
app.add(password_rating, 9, 1)
app.add(star_rating_lbl, 9, 2)
app.add(open_password_generator, 10, 2)
app.add(open_breach_checker, 10, 1)

# Defines password generator window's widgets, e.g. inputs and outputs
generator_window = gp.Window(app, 'Password Generator')
generator_inp = gp.Input(generator_window)
generator_output = gp.Input(generator_window)

# Different selections of password contents for the new password through the use of a dropdown menu
selection = ['*Select Option*','Just Letters', 'Letters and Numbers', 'Just Numbers', 'Numbers and Characters', 'Just Characters', 'Letters and Characters', 'Letters, Numbers and Characters']
selection_lbl = gp.Label(generator_window, 'Select Password Contents:')
selection_dropdown = gp.Dropdown(generator_window, selection)
# dropdown dimensions
selection_dropdown.selected_index = 0
selection_dropdown.width = 30

# Main process of generator window
def gen_new_password(event):
    # New password contents
    password_contents = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]}{<,>.?/`~\|;:' # string.punctuation

    # Depending on which dropdown option the User selects, the contents of the new password will change accordingly:
    if selection_dropdown.selected == '*Select Option*':
        # if no option is selected, no letters, numbers, or characters, will be added onto the new password
        password_contents = ' ' 
    elif selection_dropdown.selected == 'Just Letters':
        # if this option is selected, the new generated password will only contain letters, and will exclude numbers and characters
        password_contents = string.ascii_letters
    elif selection_dropdown.selected == 'Letters and Numbers':
        # if this option is selected, the new generated password will only contain letters and numbers
        password_contents = string.ascii_letters + string.digits
    elif selection_dropdown.selected == 'Just Numbers':
        # new password will only contain numbers
        password_contents = string.digits
    elif selection_dropdown.selected == 'Numbers and Characters':
        # new password will only contain numbers and characters
        password_contents = string.digits + '_!#$%^&*?'
    elif selection_dropdown.selected == 'Just Characters':
        # new password will only contain characters
        password_contents = '_!#$%^&*?' 
    elif selection_dropdown.selected == 'Letters and Characters':
        # new password will only contain letters and characters
        password_contents = string.ascii_letters + '_!#$%^&*?'
    elif selection_dropdown.selected == 'Letters, Numbers and Characters':
        # new password will contain letters, numbers and characters
        pass
    
    # user inputs a keyword in which the password generator uses for reference when creating new password.
    keyword = generator_inp.text
    generator_output.text = keyword
    # adds random characters depending on the desired password length set by the slider 
    for n in range(length_slider.value):
        # Creates the new, improved password by adding random characters onto keyword
        generator_output.text += random.choice(password_contents)

# defines the slider as a widget, as well as it's length limits (1 character -> 15 characters)
length_slider = gp.Slider(generator_window, 1, 15)
password_inp = gp.Input(generator_window)
password_inp.justify = 'center'
length_slider.add_event_listener('change', gen_new_password)
length_slider.value = 12

keyword_inp_message = gp.Label(generator_window, 'First, Enter a KEYWORD: ')
length_slider_message = gp.Label(generator_window, 'Set Desired Password Length Using the Slider:')
copied_lbl = gp.Label(generator_window, "")

# This def function copies the password generator's output to the user's clipboard, and updates a label stating: "Copied!"
def copy_password(event):
    app.copy_to_clipboard(generator_output.text)
    copied_lbl.text = "Copied!"

# button that user has to press in order to copy new password to the clipboard
gen_copy_to_clipboard = gp.Button(generator_window, "Copy to Clipboard", copy_password)

# defines generator window's grid + widget layout
generator_window.set_grid(5, 2)
generator_window.add(keyword_inp_message, 1, 1)
generator_window.add(generator_inp, 1, 2)
generator_window.add(selection_lbl, 2, 1)
generator_window.add(selection_dropdown, 2, 2)
generator_window.add(length_slider_message, 3, 1, column_span=2)
generator_window.add(length_slider, 4, 1, fill=True)
generator_window.add(generator_output, 4, 2, fill=True)
generator_window.add(gen_copy_to_clipboard, 5, 1)
generator_window.add(copied_lbl, 5, 2)

# Finally, the main application is run and the app is opened
app.run()