import re

import mysql
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.app import MDApp
import webbrowser
from kivy.uix.screenmanager import Screen

from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window
import mysql.connector
import bcrypt
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.banner import MDBanner
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDTextButton
from kivymd.uix.dialog import MDDialog
from kivy_garden.mapview import MapView, MapMarkerPopup, MapSource
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from twilio.rest import Client
import random
import mysql.connector
from kivy.storage.jsonstore import JsonStore

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, MDExpansionPanelTwoLine, \
    MDExpansionPanelThreeLine

from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDIconButton

from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

database = mysql.connector.Connect(host="localhost", user="root", password="bytecode@357crafters",
                                   database="bytecodecrafters")

session_store = JsonStore('session.json')


class LoginPage(Screen):
    def on_sign_in(self, email, password):
        if self.check_credentials(email, password):
            # Store session data
            session_store.put('user', email=email)

            # Access session data
            user_email = session_store.get('user')['email']

            # Use the user_email variable as needed
            print(f"Logged in user email: {user_email}")

            self.manager.current = 'home'
            self.ids.email.text = ""
            self.ids.psswrd.text = ""
        else:
            self.show_error_dialog()

    def check_credentials(self, email, password):
        cursor = database.cursor()
        # Retrieve the hashed password from the database based on the email
        cursor.execute('SELECT password FROM logindata WHERE email=%s', (email,))
        stored_hashed_password = cursor.fetchone()

        if stored_hashed_password:
            # Compare the entered password's hash with the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password[0].encode('utf-8')):
                return True  # Passwords match, login successful

        return False

    def show_error_dialog(self):
        # Display an error dialog for unsuccessful login
        dialog = MDDialog(
            title="Login Error",
            text="Invalid username or password.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    my_text = "Details here"

    def on_pressbutton(self):
        self.my_text = "secondpage"
        self.manager.current = "second"

    def sendotp(self):
        self.manager.current= "forgot"




class SignupPage(Screen):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    database = mysql.connector.connect(host="localhost", user="root", password="bytecode@357crafters", database="bytecodecrafters")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.country_codes = [
            {"text": f"{country['text']} {country['code']}", "viewclass": "OneLineListItem",
             "on_release": lambda x=country['code']: self.set_country_code(x)} for country in [
                {"text": "Afghanistan", "code": "+93"},
                {"text": "Albania", "code": "+355"},
                {"text": "Algeria", "code": "+213"},
                {"text": "Andorra", "code": "+376"},
                {"text": "Angola", "code": "+244"},
                {"text": "Argentina", "code": "+54"},
                {"text": "Armenia", "code": "+374"},
                {"text": "Australia", "code": "+61"},
                {"text": "Austria", "code": "+43"},
                {"text": "Azerbaijan", "code": "+994"},
                {"text": "Bahamas", "code": "+1-242"},
                {"text": "Bahrain", "code": "+973"},
                {"text": "Bangladesh", "code": "+880"},
                {"text": "Barbados", "code": "+1-246"},
                {"text": "Belarus", "code": "+375"},
                {"text": "Belgium", "code": "+32"},
                {"text": "Belize", "code": "+501"},
                {"text": "Benin", "code": "+229"},
                {"text": "Bhutan", "code": "+975"},
                {"text": "Bolivia", "code": "+591"},
                {"text": "Bosnia and Herzegovina", "code": "+387"},
                {"text": "Botswana", "code": "+267"},
                {"text": "Brazil", "code": "+55"},
                {"text": "Brunei", "code": "+673"},
                {"text": "Bulgaria", "code": "+359"},
                {"text": "Burkina Faso", "code": "+226"},
                {"text": "Burundi", "code": "+257"},
                {"text": "Cambodia", "code": "+855"},
                {"text": "Cameroon", "code": "+237"},
                {"text": "Canada", "code": "+1"},
                {"text": "Cape Verde", "code": "+238"},
                {"text": "Central African Republic", "code": "+236"},
                {"text": "Chad", "code": "+235"},
                {"text": "Chile", "code": "+56"},
                {"text": "China", "code": "+86"},
                {"text": "Colombia", "code": "+57"},
                {"text": "Comoros", "code": "+269"},
                {"text": "Congo", "code": "+242"},
                {"text": "Congo, Democratic Republic of the", "code": "+243"},
                {"text": "Costa Rica", "code": "+506"},
                {"text": "Croatia", "code": "+385"},
                {"text": "Cuba", "code": "+53"},
                {"text": "Cyprus", "code": "+357"},
                {"text": "Czech Republic", "code": "+420"},
                {"text": "Denmark", "code": "+45"},
                {"text": "Djibouti", "code": "+253"},
                {"text": "Dominica", "code": "+1-767"},
                {"text": "Dominican Republic", "code": "+1-809"},
                {"text": "Ecuador", "code": "+593"},
                {"text": "Egypt", "code": "+20"},
                {"text": "El Salvador", "code": "+503"},
                {"text": "Equatorial Guinea", "code": "+240"},
                {"text": "Eritrea", "code": "+291"},
                {"text": "Estonia", "code": "+372"},
                {"text": "Eswatini", "code": "+268"},
                {"text": "Ethiopia", "code": "+251"},
                {"text": "Fiji", "code": "+679"},
                {"text": "Finland", "code": "+358"},
                {"text": "France", "code": "+33"},
                {"text": "Gabon", "code": "+241"},
                {"text": "Gambia", "code": "+220"},
                {"text": "Georgia", "code": "+995"},
                {"text": "Germany", "code": "+49"},
                {"text": "Ghana", "code": "+233"},
                {"text": "Greece", "code": "+30"},
                {"text": "Grenada", "code": "+1-473"},
                {"text": "Guatemala", "code": "+502"},
                {"text": "Guinea", "code": "+224"},
                {"text": "Guinea-Bissau", "code": "+245"},
                {"text": "Guyana", "code": "+592"},
                {"text": "Haiti", "code": "+509"},
                {"text": "Honduras", "code": "+504"},
                {"text": "Hungary", "code": "+36"},
                {"text": "Iceland", "code": "+354"},
                {"text": "India", "code": "+91"},
                {"text": "Indonesia", "code": "+62"},
                {"text": "Iran", "code": "+98"},
                {"text": "Iraq", "code": "+964"},
                {"text": "Ireland", "code": "+353"},
                {"text": "Israel", "code": "+972"},
                {"text": "Italy", "code": "+39"},
                {"text": "Jamaica", "code": "+1-876"},
                {"text": "Japan", "code": "+81"},
                {"text": "Jordan", "code": "+962"},
                {"text": "Kazakhstan", "code": "+7"},
                {"text": "Kenya", "code": "+254"},
                {"text": "Kiribati", "code": "+686"},
                {"text": "Korea, North", "code": "+850"},
                {"text": "Korea, South", "code": "+82"},
                {"text": "Kuwait", "code": "+965"},
                {"text": "Kyrgyzstan", "code": "+996"},
                {"text": "Laos", "code": "+856"},
                {"text": "Latvia", "code": "+371"},
                {"text": "Lebanon", "code": "+961"},
                {"text": "Lesotho", "code": "+266"},
                {"text": "Liberia", "code": "+231"},
                {"text": "Libya", "code": "+218"},
                {"text": "Liechtenstein", "code": "+423"},
                {"text": "Lithuania", "code": "+370"},
                {"text": "Luxembourg", "code": "+352"},
                {"text": "Madagascar", "code": "+261"},
                {"text": "Malawi", "code": "+265"},
                {"text": "Malaysia", "code": "+60"},
                {"text": "Maldives", "code": "+960"},
                {"text": "Mali", "code": "+223"},
                {"text": "Malta", "code": "+356"},
                {"text": "Marshall Islands", "code": "+692"},
                {"text": "Mauritania", "code": "+222"},
                {"text": "Mauritius", "code": "+230"},
                {"text": "Mexico", "code": "+52"},
                {"text": "Micronesia", "code": "+691"},
                {"text": "Moldova", "code": "+373"},
                {"text": "Monaco", "code": "+377"},
                {"text": "Mongolia", "code": "+976"},
                {"text": "Montenegro", "code": "+382"},
                {"text": "Morocco", "code": "+212"},
                {"text": "Mozambique", "code": "+258"},
                {"text": "Myanmar", "code": "+95"},
                {"text": "Namibia", "code": "+264"},
                {"text": "Nauru", "code": "+674"},
                {"text": "Nepal", "code": "+977"},
                {"text": "Netherlands", "code": "+31"},
                {"text": "New Zealand", "code": "+64"},
                {"text": "Nicaragua", "code": "+505"},
                {"text": "Niger", "code": "+227"},
                {"text": "Nigeria", "code": "+234"},
                {"text": "North Macedonia", "code": "+389"},
                {"text": "Norway", "code": "+47"},
                {"text": "Oman", "code": "+968"},
                {"text": "Pakistan", "code": "+92"},
                {"text": "Palau", "code": "+680"},
                {"text": "Palestine", "code": "+970"},
                {"text": "Panama", "code": "+507"},
                {"text": "Papua New Guinea", "code": "+675"},
                {"text": "Paraguay", "code": "+595"},
                {"text": "Peru", "code": "+51"},
                {"text": "Philippines", "code": "+63"},
                {"text": "Poland", "code": "+48"},
                {"text": "Portugal", "code": "+351"},
                {"text": "Qatar", "code": "+974"},
                {"text": "Romania", "code": "+40"},
                {"text": "Russia", "code": "+7"},
                {"text": "Rwanda", "code": "+250"},
                {"text": "Saint Kitts and Nevis", "code": "+1-869"},
                {"text": "Saint Lucia", "code": "+1-758"},
                {"text": "Saint Vincent and the Grenadines", "code": "+1-784"},
                {"text": "Samoa", "code": "+685"},
                {"text": "San Marino", "code": "+378"},
                {"text": "Sao Tome and Principe", "code": "+239"},
                {"text": "Saudi Arabia", "code": "+966"},
                {"text": "Senegal", "code": "+221"},
                {"text": "Serbia", "code": "+381"},
                {"text": "Seychelles", "code": "+248"},
                {"text": "Sierra Leone", "code": "+232"},
                {"text": "Singapore", "code": "+65"},
                {"text": "Slovakia", "code": "+421"},
                {"text": "Slovenia", "code": "+386"},
                {"text": "Solomon Islands", "code": "+677"},
                {"text": "Somalia", "code": "+252"},
                {"text": "South Africa", "code": "+27"},
                {"text": "South Sudan", "code": "+211"},
                {"text": "Spain", "code": "+34"},
                {"text": "Sri Lanka", "code": "+94"},
                {"text": "Sudan", "code": "+249"},
                {"text": "Suriname", "code": "+597"},
                {"text": "Sweden", "code": "+46"},
                {"text": "Switzerland", "code": "+41"},
                {"text": "Syria", "code": "+963"},
                {"text": "Taiwan", "code": "+886"},
                {"text": "Tajikistan", "code": "+992"},
                {"text": "Tanzania", "code": "+255"},
                {"text": "Thailand", "code": "+66"},
                {"text": "Timor-Leste", "code": "+670"},
                {"text": "Togo", "code": "+228"},
                {"text": "Tonga", "code": "+676"},
                {"text": "Trinidad and Tobago", "code": "+1-868"},
                {"text": "Tunisia", "code": "+216"},
                {"text": "Turkey", "code": "+90"},
                {"text": "Turkmenistan", "code": "+993"},
                {"text": "Tuvalu", "code": "+688"},
                {"text": "Uganda", "code": "+256"},
                {"text": "Ukraine", "code": "+380"},
                {"text": "United Arab Emirates", "code": "+971"},
                {"text": "United Kingdom", "code": "+44"},
                {"text": "United States", "code": "+1"},
                {"text": "Uruguay", "code": "+598"},
                {"text": "Uzbekistan", "code": "+998"},
                {"text": "Vanuatu", "code": "+678"},
                {"text": "Vatican City", "code": "+379"},
                {"text": "Venezuela", "code": "+58"},
                {"text": "Vietnam", "code": "+84"},
                {"text": "Yemen", "code": "+967"},
                {"text": "Zambia", "code": "+260"},
                {"text": "Zimbabwe", "code": "+263"},
                # Add more countries if necessary
            ]
        ]
        self.menu = None

    def on_kv_post(self, base_widget):
        self.menu = MDDropdownMenu(
            caller=self.ids.mobilenumber,
            items=self.country_codes,
            width_mult=4,
            max_height=200,
            position="bottom"
        )

    def custom_input_filter(self, text, from_undo=False, *args):
        allowed_chars = "0123456789+ "
        return ''.join([c for c in text if c in allowed_chars])

    def set_country_code(self, code):
        self.ids.mobilenumber.text = code
        self.menu.dismiss()

    def hash_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password

    def validate_password(self, password):
        return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password))

    def validate_mobile_number(self, mobile_number):
        return bool(re.match(r'^\+[1-9]\d{1,14}$', mobile_number))

    def validate_username(self, username):
        return len(username) >= 4

    def receive_data(self, username, mobilenumber, email, psswrd):
        if re.fullmatch(self.regex, email.text) and self.validate_password(psswrd.text) and self.validate_mobile_number(mobilenumber.text) and self.validate_username(username.text):
            try:
                with self.database.cursor() as cursor:
                    hashed_password = self.hash_password(psswrd.text)
                    cursor.execute(
                        "INSERT INTO logindata (email, username, mobilenumber, password) VALUES (%s, %s, %s, %s)",
                        (email.text, username.text, mobilenumber.text, hashed_password))
                    self.database.commit()

                    # Store session data
                    session_store.put('user', email=email.text, username=username.text)

                    print("Data inserted successfully!")
                    user_email = session_store.get('user')['email']
                    user_username = session_store.get('user')['username']
                    print(f"Logged in user email: {user_email}")
                    self.manager.current = "home"
                    self.ids.username.text = ""
                    self.ids.mobilenumber.text = ""
                    self.ids.email.text = ""
                    self.ids.psswrd.text = ""
            except mysql.connector.Error as e:
                print(f"Error during insertion: {e}")
                error_msg = str(e)
                if "1062" in error_msg:
                    if "PRIMARY" in error_msg:
                        dialog_text = "Email already exists. Please enter a different email."
                    elif "mobilenumber" in error_msg:
                        dialog_text = "Mobile number already exists. Please enter a different mobile number."
                    else:
                        dialog_text = "Duplicate entry error. Please check your input and try again."
                else:
                    dialog_text = f"Error during update/insertion: {error_msg}"

                dialog = MDDialog(
                    title="Error",
                    text=dialog_text,
                    buttons=[MDFlatButton(text="OK", on_release=lambda *args: dialog.dismiss())]
                )
                dialog.open()
        else:
            if not re.fullmatch(self.regex, email.text):
                dialog = MDDialog(
                    title="Invalid Email",
                    text="Enter a valid email",
                    buttons=[MDFlatButton(text="OK", on_release=lambda *args: dialog.dismiss())]
                )
                dialog.open()
            elif not self.validate_password(psswrd.text):
                dialog = MDDialog(
                    title="Invalid Password",
                    text="Enter a password with at least 8 characters, including both letters and numbers",
                    buttons=[MDFlatButton(text="OK", on_release=lambda *args: dialog.dismiss())]
                )
                dialog.open()
            elif not self.validate_mobile_number(mobilenumber.text):
                dialog = MDDialog(
                    title="Invalid Mobile Number",
                    text="Enter a valid mobile number with country code",
                    buttons=[MDFlatButton(text="OK", on_release=lambda *args: dialog.dismiss())]
                )
                dialog.open()
            elif not self.validate_username(username.text):
                dialog = MDDialog(
                    title="Invalid Username",
                    text="Enter a username with at least 4 characters",
                    buttons=[MDFlatButton(text="OK", on_release=lambda *args: dialog.dismiss())]
                )
                dialog.open()


class HomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None

    def drpmenu(self, instance):
        self.menu_list = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'ACCOUNT',
                'on_release': lambda x=None: self.addbtn('account', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'LOGOUT',
                'on_release': lambda x=None: self.logout()
            }
        ]
        self.menu = MDDropdownMenu(items=self.menu_list, width_mult=4)
        self.menu.caller = instance
        self.menu.open()

    def dropmenu(self, instance):
        self.menu_lists = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'HOME',
                'on_release': lambda x=None: self.addbtn('home', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'SERVICES',
                'on_release': lambda x=None: self.addbtn('service', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'JOURNALS',
                'on_release': lambda x=None: self.addbtn('journal', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'CONTACT',
                'on_release': lambda x=None: self.addbtn('contact', x)
            },
        ]
        self.menus = MDDropdownMenu(items=self.menu_lists, width_mult=4)
        self.menus.caller = instance
        self.menus.open()

    def addbtn(self, screen_name, x):
        if self.screen_manager:
            self.screen_manager.current = screen_name

    def logout(self):
        user_email = session_store.get('user')['email']

        # Use the user_email variable as needed
        print(f"Logged out user email: {user_email}")
        session_store.clear()
        self.manager.current = "first"


class ServicePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None

    def drpmenu(self, instance):
        self.menu_list = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'ACCOUNT',
                'on_release': lambda x=None: self.addbtn('account', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'LOGOUT',
                'on_release': lambda x=None: self.logout()
            }
        ]
        self.menu = MDDropdownMenu(items=self.menu_list, width_mult=4)
        self.menu.caller = instance
        self.menu.open()

    def dropmenu(self, instance):
        self.menu_lists = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'HOME',
                'on_release': lambda x=None: self.addbtn('home', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'SERVICES',
                'on_release': lambda x=None: self.addbtn('service', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'JOURNALS',
                'on_release': lambda x=None: self.addbtn('journal', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'CONTACT',
                'on_release': lambda x=None: self.addbtn('contact', x)
            },
        ]
        self.menus = MDDropdownMenu(items=self.menu_lists, width_mult=4)
        self.menus.caller = instance
        self.menus.open()

    def addbtn(self, screen_name, x):
        if self.screen_manager:
            self.screen_manager.current = screen_name

    def logout(self):
        session_store.clear()
        self.manager.current = "first"

    def open_url(self):
        url = "https://docs.google.com/forms/d/e/1FAIpQLSfLP9HXJ3vTzTJwz6XyEn7KR8WCOcJL5cRnZhv_7aeiER-eyw/viewform?usp=share_link"
        webbrowser.open(url)

    def open_url2(self):
        url = "https://docs.google.com/forms/d/e/1FAIpQLScGfrnOivoahtTrcJnpbXVTEwqSqCIV646q0qltCmpUvI-TxA/viewform?vc=0&c=0&w=1&flr=0&usp=mail_form_link"
        webbrowser.open(url)

    def open_url3(self):
        url = "https://docs.google.com/forms/d/1vV_JO5V4VUPMeYG-gB-ePK6BB-CEZDaqNHQM12DohAQ/edit"
        webbrowser.open(url)


class JournalPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None

    def drpmenu(self, instance):
        self.menu_list = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'ACCOUNT',
                'on_release': lambda x=None: self.addbtn('account', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'LOGOUT',
                'on_release': lambda x=None: self.logout()
            }
        ]
        self.menu = MDDropdownMenu(items=self.menu_list, width_mult=4)
        self.menu.caller = instance
        self.menu.open()

    def dropmenu(self, instance):
        self.menu_lists = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'HOME',
                'on_release': lambda x=None: self.addbtn('home', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'SERVICES',
                'on_release': lambda x=None: self.addbtn('service', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'JOURNALS',
                'on_release': lambda x=None: self.addbtn('journal', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'CONTACT',
                'on_release': lambda x=None: self.addbtn('contact', x)
            },
        ]
        self.menus = MDDropdownMenu(items=self.menu_lists, width_mult=4)
        self.menus.caller = instance
        self.menus.open()

    def addbtn(self, screen_name, x):
        if self.screen_manager:
            self.screen_manager.current = screen_name

    def logout(self):
        session_store.clear()
        self.manager.current = "first"


class GoogleMapsTileProvider(ObjectProperty):
    url_template = "https://mt{0}.google.com/vt/lyrs=s&x={tx}&y={ty}&z={z}"

    def get_tile_url(self, x, y, z):
        server_num = (x + y + z) % 4
        return self.url_template.format(server_num, tx=x, ty=y, z=z)


class ContactPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None

    map_view = ObjectProperty(None)

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Create a MapView and set the custom tile provider
        self.map_view = MapView(
            zoom=14,
            lat=9.9312,  # Latitude for Kochi
            lon=76.2673,  # Longitude for Kochi
            map_source=GoogleMapsTileProvider(),
            double_tap_zoom=False,  # Enable double-tap zoom
            touch_zoom=True,  # Enable touch zoom
        )
        layout.add_widget(self.map_view)

        # Add control bar (optional)
        control_bar = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        zoom_in_button = Button(text="+", on_release=lambda x: setattr(self.map_view, 'zoom', self.map_view.zoom + 1))

        zoom_out_button = Button(text="-", on_release=lambda x: setattr(self.map_view, 'zoom', self.map_view.zoom - 1))

        control_bar.add_widget(zoom_in_button)
        control_bar.add_widget(zoom_out_button)
        layout.add_widget(control_bar)

        return layout

    def map(self):
        map_url = f"https://www.google.com/maps/embed?pb=!1m18!1m12!1mf{self.lat},{self.lon}!2m3!1f0!2f0!3f0!3m3!1m2!1s0xd78963c158c280f:0x390320c9971e0000!4f14.6081076!5d76.27933159999995!h=760!w=1366!z=14!ie=UTF8&output=svembed"  # URL format for satellite view
        return map_url

    def drpmenu(self, instance):
        self.menu_list = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'ACCOUNT',
                'on_release': lambda x=None: self.addbtn('account', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'LOGOUT',
                'on_release': lambda x=None: self.logout()
            }
        ]
        self.menu = MDDropdownMenu(items=self.menu_list, width_mult=4)
        self.menu.caller = instance
        self.menu.open()

    def dropmenu(self, instance):
        self.menu_lists = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'HOME',
                'on_release': lambda x=None: self.addbtn('home', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'SERVICES',
                'on_release': lambda x=None: self.addbtn('service', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'JOURNALS',
                'on_release': lambda x=None: self.addbtn('journal', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'CONTACT',
                'on_release': lambda x=None: self.addbtn('contact', x)
            },
        ]
        self.menus = MDDropdownMenu(items=self.menu_lists, width_mult=4)
        self.menus.caller = instance
        self.menus.open()

    def addbtn(self, screen_name, x):
        if self.screen_manager:
            self.screen_manager.current = screen_name

    def whatsapp(self):
        # Phone number to open a WhatsApp chat
        phone_number = "+918714045374"  # Replace with the desired phone number

        # Construct the WhatsApp chat URL with the phone number
        url = f"https://wa.me/{phone_number}"

        # Open the WhatsApp chat URL in the default web browser
        webbrowser.open(url)

    def instagram(self):
        webbrowser.open("https://www.instagram.com/bytecodecrafters?igsh=MTBra3hjbTNrcGJ4dw==")

    def logout(self):
        session_store.clear()
        self.manager.current = "first"


class AccountPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None
        self.username()

    def username(self):
        # Fetch user email from session
        user_email = session_store.get('user')['email']

        # Establish database connection
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bytecode@357crafters",
            database="bytecodecrafters"
        )

        if user_email:
            try:
                cursor = self.database.cursor(dictionary=True)
                print(f"Session user data found for: {user_email}")

                # Execute query to fetch user data
                cursor.execute("SELECT username, email, mobilenumber FROM logindata WHERE email = %s", (user_email,))
                user_data = cursor.fetchone()

                if user_data:
                    print(f"Data found for: {user_data['mobilenumber']}")
                    # Access the username widget by its id
                    self.ids.username.text = user_data['username']
                else:
                    print(f"No user data found for: {user_email}")

                cursor.close()
            except Exception as e:
                print(f"Error fetching user data: {e}")

    def drpmenu(self, instance):
        self.menu_list = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'ACCOUNT',
                'on_release': lambda x=None: self.addbtn('account', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'LOGOUT',
                'on_release': lambda x=None: self.logout()
            }
        ]
        self.menu = MDDropdownMenu(items=self.menu_list, width_mult=4)
        self.menu.caller = instance
        self.menu.open()

    def dropmenu(self, instance):
        self.menu_lists = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'HOME',
                'on_release': lambda x=None: self.addbtn('home', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'SERVICES',
                'on_release': lambda x=None: self.addbtn('service', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'JOURNALS',
                'on_release': lambda x=None: self.addbtn('journal', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'CONTACT',
                'on_release': lambda x=None: self.addbtn('contact', x)
            },
        ]
        self.menus = MDDropdownMenu(items=self.menu_lists, width_mult=4)
        self.menus.caller = instance
        self.menus.open()

    def addbtn(self, screen_name, x):
        if self.screen_manager:
            self.screen_manager.current = screen_name

    def whatsapp(self):
        # Phone number to open a WhatsApp chat
        phone_number = "+918714045374"  # Replace with the desired phone number

        # Construct the WhatsApp chat URL with the phone number
        url = f"https://wa.me/{phone_number}"

        # Open the WhatsApp chat URL in the default web browser
        webbrowser.open(url)

    def instagram(self):
        webbrowser.open("https://www.instagram.com/bytecodecrafters?igsh=MTBra3hjbTNrcGJ4dw==")

    def logout(self):
        session_store.clear()
        self.manager.current = "first"

    def accountdetail(self):
        self.manager.current = "account detail"

    def changepassword(self):
        self.manager.current = "password"

    def deleteaccount(self):
        self.manager.current = "delete account"


class AccountDetailPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.screen_manager = None
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bytecode@357crafters",
            database="bytecodecrafters"
        )

    def on_kv_post(self, base_widget):
        self.menu = None
        self.country_codes = [
            {"text": f"{country['text']} {country['code']}", "viewclass": "OneLineListItem",
             "on_release": lambda x=country['code']: self.set_country_code(x)} for country in [
                {"text": "Afghanistan", "code": "+93"},
                {"text": "Albania", "code": "+355"},
                {"text": "Algeria", "code": "+213"},
                {"text": "Andorra", "code": "+376"},
                {"text": "Angola", "code": "+244"},
                {"text": "Argentina", "code": "+54"},
                {"text": "Armenia", "code": "+374"},
                {"text": "Australia", "code": "+61"},
                {"text": "Austria", "code": "+43"},
                {"text": "Azerbaijan", "code": "+994"},
                {"text": "Bahamas", "code": "+1-242"},
                {"text": "Bahrain", "code": "+973"},
                {"text": "Bangladesh", "code": "+880"},
                {"text": "Barbados", "code": "+1-246"},
                {"text": "Belarus", "code": "+375"},
                {"text": "Belgium", "code": "+32"},
                {"text": "Belize", "code": "+501"},
                {"text": "Benin", "code": "+229"},
                {"text": "Bhutan", "code": "+975"},
                {"text": "Bolivia", "code": "+591"},
                {"text": "Bosnia and Herzegovina", "code": "+387"},
                {"text": "Botswana", "code": "+267"},
                {"text": "Brazil", "code": "+55"},
                {"text": "Brunei", "code": "+673"},
                {"text": "Bulgaria", "code": "+359"},
                {"text": "Burkina Faso", "code": "+226"},
                {"text": "Burundi", "code": "+257"},
                {"text": "Cambodia", "code": "+855"},
                {"text": "Cameroon", "code": "+237"},
                {"text": "Canada", "code": "+1"},
                {"text": "Cape Verde", "code": "+238"},
                {"text": "Central African Republic", "code": "+236"},
                {"text": "Chad", "code": "+235"},
                {"text": "Chile", "code": "+56"},
                {"text": "China", "code": "+86"},
                {"text": "Colombia", "code": "+57"},
                {"text": "Comoros", "code": "+269"},
                {"text": "Congo", "code": "+242"},
                {"text": "Congo, Democratic Republic of the", "code": "+243"},
                {"text": "Costa Rica", "code": "+506"},
                {"text": "Croatia", "code": "+385"},
                {"text": "Cuba", "code": "+53"},
                {"text": "Cyprus", "code": "+357"},
                {"text": "Czech Republic", "code": "+420"},
                {"text": "Denmark", "code": "+45"},
                {"text": "Djibouti", "code": "+253"},
                {"text": "Dominica", "code": "+1-767"},
                {"text": "Dominican Republic", "code": "+1-809"},
                {"text": "Ecuador", "code": "+593"},
                {"text": "Egypt", "code": "+20"},
                {"text": "El Salvador", "code": "+503"},
                {"text": "Equatorial Guinea", "code": "+240"},
                {"text": "Eritrea", "code": "+291"},
                {"text": "Estonia", "code": "+372"},
                {"text": "Eswatini", "code": "+268"},
                {"text": "Ethiopia", "code": "+251"},
                {"text": "Fiji", "code": "+679"},
                {"text": "Finland", "code": "+358"},
                {"text": "France", "code": "+33"},
                {"text": "Gabon", "code": "+241"},
                {"text": "Gambia", "code": "+220"},
                {"text": "Georgia", "code": "+995"},
                {"text": "Germany", "code": "+49"},
                {"text": "Ghana", "code": "+233"},
                {"text": "Greece", "code": "+30"},
                {"text": "Grenada", "code": "+1-473"},
                {"text": "Guatemala", "code": "+502"},
                {"text": "Guinea", "code": "+224"},
                {"text": "Guinea-Bissau", "code": "+245"},
                {"text": "Guyana", "code": "+592"},
                {"text": "Haiti", "code": "+509"},
                {"text": "Honduras", "code": "+504"},
                {"text": "Hungary", "code": "+36"},
                {"text": "Iceland", "code": "+354"},
                {"text": "India", "code": "+91"},
                {"text": "Indonesia", "code": "+62"},
                {"text": "Iran", "code": "+98"},
                {"text": "Iraq", "code": "+964"},
                {"text": "Ireland", "code": "+353"},
                {"text": "Israel", "code": "+972"},
                {"text": "Italy", "code": "+39"},
                {"text": "Jamaica", "code": "+1-876"},
                {"text": "Japan", "code": "+81"},
                {"text": "Jordan", "code": "+962"},
                {"text": "Kazakhstan", "code": "+7"},
                {"text": "Kenya", "code": "+254"},
                {"text": "Kiribati", "code": "+686"},
                {"text": "Korea, North", "code": "+850"},
                {"text": "Korea, South", "code": "+82"},
                {"text": "Kuwait", "code": "+965"},
                {"text": "Kyrgyzstan", "code": "+996"},
                {"text": "Laos", "code": "+856"},
                {"text": "Latvia", "code": "+371"},
                {"text": "Lebanon", "code": "+961"},
                {"text": "Lesotho", "code": "+266"},
                {"text": "Liberia", "code": "+231"},
                {"text": "Libya", "code": "+218"},
                {"text": "Liechtenstein", "code": "+423"},
                {"text": "Lithuania", "code": "+370"},
                {"text": "Luxembourg", "code": "+352"},
                {"text": "Madagascar", "code": "+261"},
                {"text": "Malawi", "code": "+265"},
                {"text": "Malaysia", "code": "+60"},
                {"text": "Maldives", "code": "+960"},
                {"text": "Mali", "code": "+223"},
                {"text": "Malta", "code": "+356"},
                {"text": "Marshall Islands", "code": "+692"},
                {"text": "Mauritania", "code": "+222"},
                {"text": "Mauritius", "code": "+230"},
                {"text": "Mexico", "code": "+52"},
                {"text": "Micronesia", "code": "+691"},
                {"text": "Moldova", "code": "+373"},
                {"text": "Monaco", "code": "+377"},
                {"text": "Mongolia", "code": "+976"},
                {"text": "Montenegro", "code": "+382"},
                {"text": "Morocco", "code": "+212"},
                {"text": "Mozambique", "code": "+258"},
                {"text": "Myanmar", "code": "+95"},
                {"text": "Namibia", "code": "+264"},
                {"text": "Nauru", "code": "+674"},
                {"text": "Nepal", "code": "+977"},
                {"text": "Netherlands", "code": "+31"},
                {"text": "New Zealand", "code": "+64"},
                {"text": "Nicaragua", "code": "+505"},
                {"text": "Niger", "code": "+227"},
                {"text": "Nigeria", "code": "+234"},
                {"text": "North Macedonia", "code": "+389"},
                {"text": "Norway", "code": "+47"},
                {"text": "Oman", "code": "+968"},
                {"text": "Pakistan", "code": "+92"},
                {"text": "Palau", "code": "+680"},
                {"text": "Palestine", "code": "+970"},
                {"text": "Panama", "code": "+507"},
                {"text": "Papua New Guinea", "code": "+675"},
                {"text": "Paraguay", "code": "+595"},
                {"text": "Peru", "code": "+51"},
                {"text": "Philippines", "code": "+63"},
                {"text": "Poland", "code": "+48"},
                {"text": "Portugal", "code": "+351"},
                {"text": "Qatar", "code": "+974"},
                {"text": "Romania", "code": "+40"},
                {"text": "Russia", "code": "+7"},
                {"text": "Rwanda", "code": "+250"},
                {"text": "Saint Kitts and Nevis", "code": "+1-869"},
                {"text": "Saint Lucia", "code": "+1-758"},
                {"text": "Saint Vincent and the Grenadines", "code": "+1-784"},
                {"text": "Samoa", "code": "+685"},
                {"text": "San Marino", "code": "+378"},
                {"text": "Sao Tome and Principe", "code": "+239"},
                {"text": "Saudi Arabia", "code": "+966"},
                {"text": "Senegal", "code": "+221"},
                {"text": "Serbia", "code": "+381"},
                {"text": "Seychelles", "code": "+248"},
                {"text": "Sierra Leone", "code": "+232"},
                {"text": "Singapore", "code": "+65"},
                {"text": "Slovakia", "code": "+421"},
                {"text": "Slovenia", "code": "+386"},
                {"text": "Solomon Islands", "code": "+677"},
                {"text": "Somalia", "code": "+252"},
                {"text": "South Africa", "code": "+27"},
                {"text": "South Sudan", "code": "+211"},
                {"text": "Spain", "code": "+34"},
                {"text": "Sri Lanka", "code": "+94"},
                {"text": "Sudan", "code": "+249"},
                {"text": "Suriname", "code": "+597"},
                {"text": "Sweden", "code": "+46"},
                {"text": "Switzerland", "code": "+41"},
                {"text": "Syria", "code": "+963"},
                {"text": "Taiwan", "code": "+886"},
                {"text": "Tajikistan", "code": "+992"},
                {"text": "Tanzania", "code": "+255"},
                {"text": "Thailand", "code": "+66"},
                {"text": "Timor-Leste", "code": "+670"},
                {"text": "Togo", "code": "+228"},
                {"text": "Tonga", "code": "+676"},
                {"text": "Trinidad and Tobago", "code": "+1-868"},
                {"text": "Tunisia", "code": "+216"},
                {"text": "Turkey", "code": "+90"},
                {"text": "Turkmenistan", "code": "+993"},
                {"text": "Tuvalu", "code": "+688"},
                {"text": "Uganda", "code": "+256"},
                {"text": "Ukraine", "code": "+380"},
                {"text": "United Arab Emirates", "code": "+971"},
                {"text": "United Kingdom", "code": "+44"},
                {"text": "United States", "code": "+1"},
                {"text": "Uruguay", "code": "+598"},
                {"text": "Uzbekistan", "code": "+998"},
                {"text": "Vanuatu", "code": "+678"},
                {"text": "Vatican City", "code": "+379"},
                {"text": "Venezuela", "code": "+58"},
                {"text": "Vietnam", "code": "+84"},
                {"text": "Yemen", "code": "+967"},
                {"text": "Zambia", "code": "+260"},
                {"text": "Zimbabwe", "code": "+263"},
                # Add more countries if necessary
            ]
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.mobilenumber,
            items = self.country_codes ,
            width_mult=4,
            max_height=200,
            position="bottom"
        )

    def open_menu(self):
        self.menu.open()
    def set_country_code(self, code):
        self.ids.mobilenumber.text = code
        self.menu.dismiss()

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    def on_pre_enter(self):
        try:
            cursor = self.database.cursor(dictionary=True)
            user_email = session_store.get('user')['email']
            print(f"session user data found for: {user_email}")

            cursor.execute("SELECT username, email, mobilenumber FROM logindata WHERE email = %s", (user_email,))
            user_data = cursor.fetchone()
            print(f" data found for: {user_data['mobilenumber']}")

            if user_data:
                self.ids.username.text = user_data['username']
                self.ids.email.text = user_data['email']
                self.ids.mobilenumber.text = user_data['mobilenumber']
            else:
                print(f"No user data found for: {user_email}")

            cursor.close()
        except Exception as e:
            print(f"Error fetching user data: {e}")
            dialog = MDDialog(
                title="Error",
                text=f"Error fetching user data: {e}",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda *args: dialog.dismiss()
                    )
                ]
            )
            dialog.open()

    def custom_input_filter(self, text, from_undo=False, *args):
        allowed_chars = "0123456789+ "
        return ''.join([c for c in text if c in allowed_chars])


    def validate_mobile_number(self, mobile_number):
        """
        Validate mobile number with country code.
        Returns True if the mobile number is valid, False otherwise.
        """
        # Add your mobile number validation criteria here
        # For example, requiring a specific country code and format
        return bool(re.match(r'^\+[1-9]\d{1,14}$', mobile_number))

    def validate_username(self, username):
        """
        Validate username.
        Returns True if the username is valid, False otherwise.
        """
        # Add your username validation criteria here
        # For example, requiring at least 4 characters
        return len(username) >= 4

    def update_data(self, username, mobilenumber, email):
        if re.fullmatch(self.regex, email.text) and self.validate_mobile_number(
                mobilenumber.text) and self.validate_username(username.text):
            try:
                with self.database.cursor() as cursor:
                    # Update the existing user's details
                    email_data = session_store.get('user')['email']
                    cursor.execute(
                        "UPDATE logindata SET username = %s, mobilenumber = %s,email =%s WHERE email = %s",
                        (username.text, mobilenumber.text, email.text, email_data)
                    )
                    self.database.commit()

                    # Store session data
                    session_store.clear()
                    session_store.put('user', email=email.text, username=username.text)

                    print("User details updated successfully!")

                    # Store session data
                    session_store.put('user', email=email.text, username=username.text)

                    print("New user data inserted successfully!")
                    self.manager.current = "account"


            except mysql.connector.Error as e:
                print(f"Error during update/insertion: {e}")
                # Handle error as needed
                error_msg = str(e)
                if "1062" in error_msg:  # Check if the error code indicates a duplicate entry
                    if "PRIMARY" in error_msg:
                        dialog_text = "Email already exists. Please enter a different email."
                    elif "mobilenumber" in error_msg:
                        dialog_text = "Mobile number already exists. Please enter a different mobile number."
                    else:
                        dialog_text = "Duplicate entry error. Please check your input and try again."
                else:
                    dialog_text = f"Error during update/insertion: {error_msg}"

                dialog = MDDialog(
                    title="Error",
                    text=dialog_text,
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda *args: dialog.dismiss()
                        )
                    ]
                )
                dialog.open()
        else:
            if not re.fullmatch(self.regex, email.text):
                dialog = MDDialog(
                    title="Invalid Email",
                    text="Enter a valid email",
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda *args: dialog.dismiss()
                        )
                    ]
                )
                dialog.open()

            elif not self.validate_mobile_number(mobilenumber.text):
                dialog = MDDialog(
                    title="Invalid Mobile Number",
                    text="Enter a valid mobile number with country code",
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda *args: dialog.dismiss()
                        )
                    ]
                )
                dialog.open()
            elif not self.validate_username(username.text):
                dialog = MDDialog(
                    title="Invalid Username",
                    text="Enter a username with at least 4 characters",
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda *args: dialog.dismiss()
                        )
                    ]
                )
                dialog.open()

    def drpmenu(self, instance):
        self.menu_list = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'ACCOUNT',
                'on_release': lambda x=None: self.addbtn('account', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'LOGOUT',
                'on_release': lambda x=None: self.logout()
            }
        ]
        self.menu = MDDropdownMenu(items=self.menu_list, width_mult=4)
        self.menu.caller = instance
        self.menu.open()

    def dropmenu(self, instance):
        self.menu_lists = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'HOME',
                'on_release': lambda x=None: self.addbtn('home', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'SERVICES',
                'on_release': lambda x=None: self.addbtn('service', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'JOURNALS',
                'on_release': lambda x=None: self.addbtn('journal', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'CONTACT',
                'on_release': lambda x=None: self.addbtn('contact', x)
            },
        ]
        self.menus = MDDropdownMenu(items=self.menu_lists, width_mult=4)
        self.menus.caller = instance
        self.menus.open()

    def addbtn(self, screen_name, x):
        if self.screen_manager:
            self.screen_manager.current = screen_name

    def whatsapp(self):
        # Phone number to open a WhatsApp chat
        phone_number = "+918714045374"  # Replace with the desired phone number

        # Construct the WhatsApp chat URL with the phone number
        url = f"https://wa.me/{phone_number}"

        # Open the WhatsApp chat URL in the default web browser
        webbrowser.open(url)

    def instagram(self):
        webbrowser.open("https://www.instagram.com/bytecodecrafters?igsh=MTBra3hjbTNrcGJ4dw==")

    def logout(self):
        session_store.clear()
        self.manager.current = "first"

    def on_enter(self, *args):
        self.fetch_user_data()

    def fetch_user_data(self):
        try:
            with self.database.cursor() as cursor:
                # Fetch the email from the session data
                user_email = session_store.get('user')['email']

                # Fetch the user data from the database based on the email
                cursor.execute("SELECT username, email, mobilenumber FROM userdata WHERE email = %s", (user_email,))
                user_data = cursor.fetchone()

                if user_data:
                    username, email, mobilenumber = user_data

                    # Update the UI elements with the fetched data
                    self.ids.username.text = username
                    self.ids.email.text = email
                    self.ids.mobilenumber.text = mobilenumber

        except Exception as e:
            print(f"Error fetching user data: {e}")


class ChangePasswordPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bytecode@357crafters",
            database="bytecodecrafters"
        )

    def toggle_password_visibility(self, textfield, icon_button):
        if textfield.password:
            textfield.password = False
            icon_button.icon = 'eye'
        else:
            textfield.password = True
            icon_button.icon = 'eye-off'

    def validate_password(self, password):
        # Password validation rules
        password_rules = [
            r'^(?=.*[A-Za-z])',  # At least one letter
            r'(?=.*\d)',  # At least one digit
            r'[A-Za-z\d]{8,}$'  # At least 8 characters
        ]

        # Check if the password matches all the rules
        for rule in password_rules:
            if not re.search(rule, password):
                return False

        return True

    def update_password(self):
        current_password = self.ids.currentpassword.text
        new_password = self.ids.newpassword.text
        confirm_password = self.ids.confirmpassword.text

        if new_password != confirm_password:
            # Display an error dialog if the new password and confirm password don't match
            dialog = MDDialog(
                title="Password Mismatch",
                text="The new password and confirm password fields don't match.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda *args: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
            return

        # Validate the new password
        if not self.validate_password(new_password):
            # Display an error dialog if the new password doesn't meet the requirements
            dialog = MDDialog(
                title="Invalid Password",
                text="The new password must be at least 8 characters long and contain at least one letter and one digit.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda *args: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
            return

        try:
            with self.database.cursor() as cursor:
                # Fetch the current password from the database based on the session data
                user_email = session_store.get('user')['email']
                cursor.execute("SELECT password FROM logindata WHERE email = %s", (user_email,))
                result = cursor.fetchone()

                if result:
                    stored_password = result[0]

                    # Verify the current password
                    if self.verify_password(current_password, stored_password):
                        # Update the password in the database
                        hashed_new_password = self.hash_password(new_password)
                        cursor.execute(
                            "UPDATE logindata SET password = %s WHERE email = %s",
                            (hashed_new_password, user_email)
                        )
                        self.database.commit()

                        # Display a success dialog
                        self.manager.current = "account"
                        self.ids.currentpassword.text = ""
                        self.ids.newpassword.text = ""
                        self.ids.confirmpassword.text = ""
                    else:
                        # Display an error dialog if the current password is incorrect
                        dialog = MDDialog(
                            title="Incorrect Password",
                            text="The current password you entered is incorrect.",
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    on_release=lambda *args: dialog.dismiss()
                                )
                            ]
                        )
                        dialog.open()

        except mysql.connector.Error as e:
            print(f"Error updating password: {e}")
            # Handle error as needed

    def verify_password(self, password, hashed_password):
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
        else:
            return False

    def hash_password(self, password):
        # Implement password hashing logic here
        # For example, using bcrypt or another hashing algorithm
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return password

    def drpmenu(self, instance):
        self.menu_list = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'ACCOUNT',
                'on_release': lambda x=None: self.addbtn('account', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'LOGOUT',
                'on_release': lambda x=None: self.logout()
            }
        ]
        self.menu = MDDropdownMenu(items=self.menu_list, width_mult=4)
        self.menu.caller = instance
        self.menu.open()

    def dropmenu(self, instance):
        self.menu_lists = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'HOME',
                'on_release': lambda x=None: self.addbtn('home', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'SERVICES',
                'on_release': lambda x=None: self.addbtn('service', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'JOURNALS',
                'on_release': lambda x=None: self.addbtn('journal', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'CONTACT',
                'on_release': lambda x=None: self.addbtn('contact', x)
            },
        ]
        self.menus = MDDropdownMenu(items=self.menu_lists, width_mult=4)
        self.menus.caller = instance
        self.menus.open()

    def addbtn(self, screen_name, x):
        if self.screen_manager:
            self.screen_manager.current = screen_name

    def whatsapp(self):
        # Phone number to open a WhatsApp chat
        phone_number = "+918714045374"  # Replace with the desired phone number

        # Construct the WhatsApp chat URL with the phone number
        url = f"https://wa.me/{phone_number}"

        # Open the WhatsApp chat URL in the default web browser
        webbrowser.open(url)

    def instagram(self):
        webbrowser.open("https://www.instagram.com/bytecodecrafters?igsh=MTBra3hjbTNrcGJ4dw==")

    def logout(self):
        session_store.clear()
        self.manager.current = "first"


class DeleteAccountPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None
        self.dialog = None
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bytecode@357crafters",
            database="bytecodecrafters"
        )

    def toggle_password_visibility(self, textfield, icon_button):
        if textfield.password:
            textfield.password = False
            icon_button.icon = 'eye'
        else:
            textfield.password = True
            icon_button.icon = 'eye-off'
    def verify_password(self, password, hashed_password):
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
        else:
            return False

    def delete_account(self):
        try:
            with self.database.cursor() as cursor:
                # Fetch the current password from the database based on the session data
                user_email = session_store.get('user')['email']
                cursor.execute("SELECT password FROM logindata WHERE email = %s", (user_email,))
                result = cursor.fetchone()
                password = self.ids.deletepassword.text

                if result:
                    stored_password = result[0]

                    # Verify the current password
                    if self.verify_password(password, stored_password):
                        # Confirm the deletion
                        self.confirm_deletion()


                    else:
                        # Display an error message if the password is incorrect
                        self.dialog = MDDialog(
                            title="Error",
                            text="Incorrect password",
                            buttons=[
                                MDFlatButton(
                                    text="OK",
                                    on_press=lambda x: self.dialog.dismiss(),
                                ),
                            ],
                        )
                        self.dialog.open()
        except Exception as e:
            # Handle any exceptions that may occur
            print(f"Error: {e}")
            self.dialog = MDDialog(
                title="Error",
                text="An error occurred while deleting the account.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_press=lambda x: self.dialog.dismiss(),
                    ),
                ],
            )
            self.dialog.open()

    def confirm_deletion(self):
        # Create a confirmation dialog
        self.dialog = MDDialog(
            title="Confirm Deletion",
            text="Are you sure you want to delete your account?",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_press=lambda x: self.dialog.dismiss(),
                ),
                MDFlatButton(
                    text="Confirm",
                    on_press=lambda x: self.delete_account_confirmed(),
                ),
            ],
        )
        self.dialog.open()

    def delete_account_confirmed(self):
        try:
            with self.database.cursor() as cursor:
                # Fetch the current user's email from the session data
                user_email = session_store.get('user')['email']

                # Delete the user's account from the database
                cursor.execute("DELETE FROM logindata WHERE email = %s", (user_email,))
                self.database.commit()

            # Navigate to the login page
            self.screen_manager.current = "first"
            self.ids.deletepassword.text = ""
        except Exception as e:
            # Handle any exceptions that may occur
            print(f"Error: {e}")
            self.dialog = MDDialog(
                title="Error",
                text="An error occurred while deleting the account.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_press=lambda x: self.dialog.dismiss(),
                    ),
                ],
            )
            self.dialog.open()
        finally:
            # Dismiss the confirmation dialog
            self.dialog.dismiss()

    def drpmenu(self, instance):
        self.menu_list = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'ACCOUNT',
                'on_release': lambda x=None: self.addbtn('account', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'LOGOUT',
                'on_release': lambda x=None: self.logout()
            }
        ]
        self.menu = MDDropdownMenu(items=self.menu_list, width_mult=4)
        self.menu.caller = instance
        self.menu.open()

    def dropmenu(self, instance):
        self.menu_lists = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'HOME',
                'on_release': lambda x=None: self.addbtn('home', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'SERVICES',
                'on_release': lambda x=None: self.addbtn('service', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'JOURNALS',
                'on_release': lambda x=None: self.addbtn('journal', x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'CONTACT',
                'on_release': lambda x=None: self.addbtn('contact', x)
            },
        ]
        self.menus = MDDropdownMenu(items=self.menu_lists, width_mult=4)
        self.menus.caller = instance
        self.menus.open()

    def addbtn(self, screen_name, x):
        if self.screen_manager:
            self.screen_manager.current = screen_name

    def whatsapp(self):
        # Phone number to open a WhatsApp chat
        phone_number = "+918714045374"  # Replace with the desired phone number

        # Construct the WhatsApp chat URL with the phone number
        url = f"https://wa.me/{phone_number}"

        # Open the WhatsApp chat URL in the default web browser
        webbrowser.open(url)

    def instagram(self):
        webbrowser.open("https://www.instagram.com/bytecodecrafters?igsh=MTBra3hjbTNrcGJ4dw==")

    def logout(self):
        session_store.clear()
        self.manager.current = "first"

class ForgotPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bytecode@357crafters",
            database="bytecodecrafters"
        )
        self.data_to_send = None

        # Brevo SMTP configuration
        self.brevo_smtp_server = "smtp-relay.brevo.com"
        self.brevo_smtp_port = 587
        self.brevo_smtp_username = "76486f001@smtp-brevo.com"
        self.brevo_smtp_password = "hJPTnaUtMx1ZgjQz"
        self.from_email = "bytecodeotp@gmail.com"  # Replace with your verified email address
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    def send_otp(self, email):
        try:
            if re.fullmatch(self.regex, email):
                cursor = self.database.cursor(dictionary=True)
                cursor.execute("SELECT COUNT(*) FROM logindata WHERE email = %s", (email,))
                count = cursor.fetchone()['COUNT(*)']


                if count > 0:
                    otp = self.generate_otp(email)

                    # Create a message
                    msg = MIMEMultipart()
                    msg['From'] = self.from_email
                    msg['To'] = email
                    msg['Subject'] = "Your OTP for password reset"

                    # Add the OTP to the message
                    msg.attach(MIMEText(f"Your OTP for password reset is: {otp}", 'plain'))

                    # Send the email
                    server = smtplib.SMTP(self.brevo_smtp_server, self.brevo_smtp_port)
                    server.starttls()
                    server.login(self.brevo_smtp_username, self.brevo_smtp_password)
                    server.sendmail(self.from_email, email, msg.as_string())
                    server.quit()

                    # Display a dialog that OTP has been sent
                    dialog = MDDialog(
                        title="OTP Sent",
                        text="An OTP has been sent to your email.",
                        buttons=[
                            MDFlatButton(
                                text="OK",
                                on_release=lambda x: (self.otpverifypage(email), dialog.dismiss())
                            )
                        ]
                    )
                    dialog.open()
                    self.ids.email.text = ""

                    print(f"OTP sent to {email}: {otp}")

                else:
                    dialog = MDDialog(
                        title="Error",
                        text="No account found for the provided email.",
                        buttons=[
                            MDFlatButton(
                                text="OK",
                                on_release=lambda x: dialog.dismiss()
                            )
                        ]
                    )
                    dialog.open()
            else:
                dialog = MDDialog(
                    title="Invalid Email",
                    text="Enter a valid email",
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda *args: dialog.dismiss()
                        )
                    ]
                )
                dialog.open()
        except mysql.connector.Error as e:
            print(f"Error fetching user data: {e}")
            dialog = MDDialog(
                title="Error",
                text=f"Error fetching user data: {e}",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
        except Exception as e:
            print(f"Error sending OTP: {e}")
            dialog = MDDialog(
                title="Error",
                text=f"Error sending OTP: {e}",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()

    def generate_otp(self, email):
        otp = str(random.randint(100000, 999999))

        try:
            cursor = self.database.cursor(dictionary=True)
            cursor.execute("UPDATE logindata SET otp = %s WHERE email = %s", (otp, email))
            self.database.commit()
            cursor.close()

            self.otp = otp
            return otp
        except mysql.connector.Error as e:
            print(f"Error updating OTP: {e}")
            return None

    def otpverifypage(self,email):
        otp_screen = self.manager.get_screen('otp')
        change_screen = self.manager.get_screen('forgot_change')
        change_screen.email=email
        otp_screen.email = email
        self.manager.current = 'otp'
        otp_screen.start_timer()


class OtpVerifyPage(Screen):
    email =''
    timer_event = None
    countdown = 60
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = None
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bytecode@357crafters",
            database="bytecodecrafters"
        )

    def start_timer(self):
        self.countdown = 60
        self.ids.resend_otp_button.disabled = True
        self.update_timer()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, *args):
        if self.countdown > 0:
            self.countdown -= 1
            self.ids.resend_otp_button.text = f"Resend OTP in {self.countdown}s"
            self.ids.resend_otp_button.text_color = 0.6, 0.6, 0.6, 1
            self.ids.box_layout.pos_hint = {'center_x': 0.46, 'center_y': .4}
        else:
            self.ids.resend_otp_button.disabled = False
            self.ids.resend_otp_button.text = "Resend OTP"
            self.ids.resend_otp_button.text_color = 0.6, 0.6, 0.6, 1
            self.ids.box_layout.pos_hint = {'center_x': 0.5, 'center_y': .4}
            if self.timer_event:
                self.timer_event.cancel()
    def verify_otp(self,otp):
        try:
            print(f"OTP sent to {self.email}: {otp}")
            cursor = self.database.cursor(dictionary=True)
            cursor.execute("SELECT otp FROM logindata WHERE email = %s", (self.email,))
            stored_otp = cursor.fetchone()['otp']
            cursor.close()

            if stored_otp == otp:
                print(f"OTP verified successfully")
                # OTP is valid, proceed to the next screen
                self.manager.current = 'forgot_change'
                self.ids.otp.text = ""
            else:
                # OTP is invalid, display an error message
                dialog = MDDialog(
                    title="Error",
                    text="Invalid OTP",
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda x: dialog.dismiss()
                        )
                    ]
                )
                dialog.open()
        except mysql.connector.Error as e:
            print(f"Error fetching OTP: {e}")
            dialog = MDDialog(
                title="Error",
                text=f"Error fetching OTP: {e}",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
    def resend_otp(self):
        forgot_screen = self.manager.get_screen('forgot')
        forgot_screen.send_otp(self.email)
        self.start_timer()



class ForgotChangePage(Screen):
    email = ""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add your class initialization code here

    def dismiss_dialog_and_navigate(self, dialog):
        self.manager.current = 'first'
        dialog.dismiss()

    def hash_password(self, password):
        # Implement password hashing logic here
        # For example, using bcrypt or another hashing algorithm
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return password

    def validate_password(self, password):
        # Password validation rules
        password_rules = [
            r'^(?=.*[A-Za-z])',  # At least one letter
            r'(?=.*\d)',  # At least one digit
            r'[A-Za-z\d]{8,}$'  # At least 8 characters
        ]

        # Check if the password matches all the rules
        for rule in password_rules:
            if not re.search(rule, password):
                return False

        return True

    def change_password(self):
        new_password = self.ids.newpassword.text
        confirm_password = self.ids.confirmpassword.text

        if new_password == confirm_password:
            if not self.validate_password(new_password):
                # Display an error dialog if the new password doesn't meet the requirements
                dialog = MDDialog(
                    title="Invalid Password",
                    text="Enter a password with at least 8 characters, including both letters and numbers",
                    buttons=[MDFlatButton(text="OK", on_release=lambda *args: dialog.dismiss())]
                )
                dialog.open()
            else:
                # Connect to the database
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="bytecode@357crafters",
                    database="bytecodecrafters"
                )

                # Create a cursor object
                cursor = db.cursor()

                # Update the password for the user with the given email
                cursor.execute("UPDATE logindata SET password = %s WHERE email = %s",
                               (self.hash_password(new_password), self.email))
                db.commit()

                # Close the cursor and database connection
                cursor.close()
                db.close()

                # Display a success message
                dialog = MDDialog(
                    title="Success",
                    text="Password changed successfully",
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda x: dismiss_dialog(self,dialog)
                        )
                    ]
                )
                dialog.open()

                def dismiss_dialog(self,dialog):
                    dialog.dismiss()
                    self.manager.current = "first"
                self.ids.newpassword.text = ""
                self.ids.confirmpassword.text = ""

        else:
            # Display an error message
            dialog = MDDialog(
                title="Error",
                text="New password and confirm password do not match",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()


class YourFirstScreen(Screen):
    pass


class YourThirdScreen(Screen):
    pass


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_page = LoginPage(name='login')
        self.add_widget(self.login_page)

        self.home_page = HomePage(name='home')
        self.home_page.screen_manager = self
        self.add_widget(self.home_page)

        self.service_page = ServicePage(name='service')
        self.service_page.screen_manager = self
        self.add_widget(self.service_page)

        self.journal_page = JournalPage(name='journal')
        self.journal_page.screen_manager = self
        self.add_widget(self.journal_page)

        self.contact_page = ContactPage(name='contact')
        self.contact_page.screen_manager = self
        self.add_widget(self.contact_page)

        self.account_page = AccountPage(name='account')
        self.account_page.screen_manager = self
        self.add_widget(self.account_page)

        self.account_detail_page = AccountDetailPage(name='account detail')
        self.account_detail_page.screen_manager = self
        self.add_widget(self.account_detail_page)

        self.change_password_page = ChangePasswordPage(name='password')
        self.change_password_page.screen_manager = self
        self.add_widget(self.change_password_page)

        self.delete_account_page = DeleteAccountPage(name='delete account')
        self.delete_account_page.screen_manager = self
        self.add_widget(self.delete_account_page)

        self.add_widget(YourFirstScreen(name='first_screen'))
        self.add_widget(YourThirdScreen(name='journals_screen'))
        self.add_widget(YourFirstScreen(name='first_screen'))

        self.current = 'login'


class ScrollableScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ScrollableScreen, self).__init__(**kwargs)
        for i in range(20):
            label = MDLabel(text=f'Text {i}', halign='center')
            self.ids.grid_layout.add_widget(label)


class bytecodecrafters(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file("main.kv")

    def open_url4(self):
        webbrowser.open("https://wa.me/+918714045374")  # Directly call the function with the URL

    def open_url5(self):
        webbrowser.open(
            "https://www.instagram.com/bytecodecrafters?igsh=MTBra3hjbTNrcGJ4dw==")  # Directly call the function with the URL

    def on_start(self):
        self.icon = "bytecodelogo2.png"
        self.title = "BYTECODE CRAFTERS"


if __name__ == "__main__":
    Window.size = (360, 640)
    bytecodecrafters().run()
