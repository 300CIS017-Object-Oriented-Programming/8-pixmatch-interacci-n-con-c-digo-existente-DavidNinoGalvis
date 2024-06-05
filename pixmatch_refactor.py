import streamlit as st
import os
import time as tm
import random
import base64
import json
from PIL import Image
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="PixMatch", page_icon="🕹️", layout="wide", initial_sidebar_state="expanded")

# Set the path for resources based on the current working directory
vDrive = os.path.splitdrive(os.getcwd())[0]
vpth = "./"

# Styling variables
sbe = """<span style='font-size: 140px; border-radius: 7px; text-align: center; display:inline; padding: 3px 0.4em;'>|fill_variable|</span>"""
pressed_emoji = """<span style='font-size: 24px; border-radius: 7px; text-align: center; display:inline; padding: 3px 0.2em;'>|fill_variable|</span>"""
horizontal_bar = "<hr style='margin: 0; height: 1px; border: 1px solid #635985;'><br>"
purple_btn_colour = """
    <style>
        div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
        div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
        div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
    </style>
"""

# Initialize session state variables
mystate = st.session_state
if "expired_cells" not in mystate: mystate.expired_cells = []
if "myscore" not in mystate: mystate.myscore = 0
if "plyrbtns" not in mystate: mystate.plyrbtns = {}
if "sidebar_emoji" not in mystate: mystate.sidebar_emoji = ''
if "emoji_bank" not in mystate: mystate.emoji_bank = []
if "GameDetails" not in mystate: mystate.GameDetails = ['Medium', 6, 7, '']

def adjust_page_padding(section='main'):
    """
    Adjust the top padding of specific sections of the Streamlit page.
    """
    padding_style = {
        'main': " <style> div[class^='block-container'] { padding-top: 2rem; } </style> ",
        'sidebar': " <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ",
        'all': " <style> div[class^='block-container'] { padding-top: 2rem; } </style> <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> "
    }
    st.markdown(padding_style[section], True)

def manage_leaderboard(action):
    """
    Manage the leaderboard: create, write, and read.
    """
    if action == 'create' and mystate.GameDetails[3]:
        if not os.path.isfile(vpth + 'leaderboard.json'):
            json.dump({}, open(vpth + 'leaderboard.json', 'w'))

    elif action == 'write' and mystate.GameDetails[3]:
        if os.path.isfile(vpth + 'leaderboard.json'):
            leaderboard = json.load(open(vpth + 'leaderboard.json'))
            leaderboard[len(leaderboard) + 1] = {'NameCountry': mystate.GameDetails[3], 'HighestScore': mystate.myscore}
            leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))
            leaderboard = dict(list(leaderboard.items())[:4])
            json.dump(leaderboard, open(vpth + 'leaderboard.json', 'w'))

    elif action == 'read' and mystate.GameDetails[3]:
        if os.path.isfile(vpth + 'leaderboard.json'):
            leaderboard = json.load(open(vpth + 'leaderboard.json'))
            leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))
            display_leaderboard(leaderboard)

def display_leaderboard(leaderboard):
    """
    Display the leaderboard in the sidebar.
    """
    sc0, sc1, sc2, sc3, sc4 = st.columns((2, 3, 3, 3, 3))
    for rank, (key, data) in enumerate(leaderboard.items(), start=1):
        if rank == 1:
            sc0.write('🏆 Past Winners:')
            sc1.write(f"🥇 | {data['NameCountry']}: :red[{data['HighestScore']}]")
        elif rank == 2:
            sc2.write(f"🥈 | {data['NameCountry']}: :red[{data['HighestScore']}]")
        elif rank == 3:
            sc3.write(f"🥉 | {data['NameCountry']}: :red[{data['HighestScore']}]")
        elif rank == 4:
            sc4.write(f"🏅 | {data['NameCountry']}: {data['HighestScore']}")

def setup_initial_page():
    """
    Configure and display the initial page with sidebar, game instructions, and images.
    """
    with st.sidebar:
        st.subheader("🖼️ Pix Match:")
        st.markdown(horizontal_bar, True)
        sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 390))
        st.image(sidebarlogo, use_column_width='auto')

    hlp_dtl = f"""<span style="font-size: 26px;">
    <ol>
    <li style="font-size:15px";>Game play opens with (a) a sidebar picture and (b) a N x N grid of picture buttons, where N=6:Easy, N=7:Medium, N=8:Hard.</li>
    <li style="font-size:15px";>You need to match the sidebar picture with a grid picture button, by pressing the (matching) button (as quickly as possible).</li>
    <li style="font-size:15px";>Each correct picture match will earn you <strong>+N</strong> points (where N=5:Easy, N=3:Medium, N=1:Hard); each incorrect picture match will earn you <strong>-1</strong> point.</li>
    <li style="font-size:15px";>The sidebar picture and the grid pictures will dynamically regenerate after a fixed seconds interval (Easy=8, Medium=6, Hard=5). Each regeneration will have a penalty of <strong>-1</strong> point</li>
    <li style="font-size:15px";>Each of the grid buttons can only be pressed once during the entire game.</li>
    <li style="font-size:15px";>The game completes when all the grid buttons are pressed.</li>
    <li style="font-size:15px";>At the end of the game, if you have a positive score, you will have <strong>won</strong>; otherwise, you will have <strong>lost</strong>.</li>
    </ol></span>"""

    sc1, sc2 = st.columns(2)
    GameHelpImg = vpth + random.choice(["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
    GameHelpImg = Image.open(GameHelpImg).resize((550, 550))
    sc2.image(GameHelpImg, use_column_width='auto')

    sc1.subheader('Rules | Playing Instructions:')
    sc1.markdown(horizontal_bar, True)
    sc1.markdown(hlp_dtl, unsafe_allow_html=True)
    st.markdown(horizontal_bar, True)

    author_dtl = "<strong>Happy Playing: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>"
    st.markdown(author_dtl, unsafe_allow_html=True)

def load_image_base64(filepath):
    """
    Read an image file and return its base64 encoded string.
    """
    try:
        with open(filepath, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return ""

def check_button_press(cell):
    """
    Evaluate and update the game state when a button is pressed.
    """
    if not mystate.plyrbtns[cell]['isPressed']:
        mystate.plyrbtns[cell]['isPressed'] = True
        mystate.expired_cells.append(cell)

        if mystate.plyrbtns[cell]['eMoji'] == mystate.sidebar_emoji:
            mystate.plyrbtns[cell]['isTrueFalse'] = True
            mystate.myscore += {'Easy': 5, 'Medium': 3, 'Hard': 1}[mystate.GameDetails[0]]
        else:
            mystate.myscore -= 1
            mystate.plyrbtns[cell]['isTrueFalse'] = False
            check_max_errors()

def check_max_errors():
    """
    Check if the player has exceeded the maximum number of allowed errors.
    """
    total_cells = mystate.GameDetails[2] ** 2
    max_errors_allowed = (total_cells // 2) + 1
    current_errors = sum(1 for cell in mystate.plyrbtns if not mystate.plyrbtns[cell]['isTrueFalse'] and mystate.plyrbtns[cell]['isPressed'])
    if current_errors >= max_errors_allowed:
        st.error("You have exceeded the maximum number of allowed errors.")
        tm.sleep(5)
        mystate.runpage = main_page
        st.rerun()

def reset_board():
    """
    Reset the game board by updating the emojis on the buttons and ensuring the sidebar emoji is present.
    """
    total_cells = mystate.GameDetails[2]

    mystate.sidebar_emoji = random.choice(mystate.emoji_bank)
    sidebar_emoji_in_list = False
    for cell in range(1, (total_cells ** 2) + 1):
        if not mystate.plyrbtns[cell]['isPressed']:
            vemoji = random.choice(mystate.emoji_bank)
            mystate.plyrbtns[cell]['eMoji'] = vemoji
            if vemoji == mystate.sidebar_emoji:
                sidebar_emoji_in_list = True

    if not sidebar_emoji_in_list:
        available_cells = [cell for cell in range(1, (total_cells ** 2) + 1) if not mystate.plyrbtns[cell]['isPressed']]
        if available_cells:
            selected_cell = random.choice(available_cells)
            mystate.plyrbtns[selected_cell]['eMoji'] = mystate.sidebar_emoji

def prepare_new_game():
    """
    Prepare the initial state for a new game, resetting scores and selecting a new set of emojis.
    """
    total_cells = mystate.GameDetails[2]
    mystate.expired_cells = []
    mystate.myscore = 0

    emoji_categories = {
        'Easy': ['foods', 'moon', 'animals'],
        'Medium': ['foxes', 'emojis', 'humans', 'vehicles', 'houses', 'hands', 'purple_signs', 'red_signs', 'blue_signs'],
        'Hard': ['foxes', 'emojis', 'humans', 'foods', 'clocks', 'hands', 'animals', 'vehicles', 'houses', 'purple_signs', 'red_signs', 'blue_signs', 'moon']
    }

    chosen_category = random.choice(emoji_categories[mystate.GameDetails[0]])
    mystate.emoji_bank = locals()[chosen_category]

    mystate.plyrbtns = {cell: {'isPressed': False, 'isTrueFalse': False, 'eMoji': ''} for cell in range(1, (total_cells ** 2) + 1)}

def get_score_emoji():
    """
    Return an emoji representing the current score of the player.
    """
    if mystate.myscore == 0:
        return '😐'
    elif -5 <= mystate.myscore <= -1:
        return '😏'
    elif -10 <= mystate.myscore <= -6:
        return '☹️'
    elif mystate.myscore <= -11:
        return '😖'
    elif 1 <= mystate.myscore <= 5:
        return '🙂'
    elif 6 <= mystate.myscore <= 10:
        return '😊'
    elif mystate.myscore > 10:
        return '😁'

def new_game():
    """
    Initialize and start a new game, setting up the board and updating the UI.
    """
    reset_board()
    total_cells = mystate.GameDetails[2]

    adjust_page_padding('sidebar')
    with st.sidebar:
        st.subheader(f"🖼️ Pix Match: {mystate.GameDetails[0]}")
        st.markdown(horizontal_bar, True)

        st.markdown(sbe.replace('|fill_variable|', mystate.sidebar_emoji), True)
        aftimer = st_autorefresh(interval=(mystate.GameDetails[1] * 1000), key="aftmr")
        if aftimer > 0:
            mystate.myscore -= 1

        st.info(f"{get_score_emoji()} Score: {mystate.myscore} | Pending: {(total_cells ** 2) - len(mystate.expired_cells)}")
        st.markdown(horizontal_bar, True)
        if st.button(f"🔙 Return to Main Page", use_container_width=True):
            mystate.runpage = main_page
            st.rerun()

    manage_leaderboard('read')
    st.subheader("Picture Positions:")
    st.markdown(horizontal_bar, True)

    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style>", unsafe_allow_html=True)

    cols = [st.columns([1] * total_cells + [2]) for _ in range(total_cells)]
    for cell in range(1, (total_cells ** 2) + 1):
        row, col = divmod(cell - 1, total_cells)
        if mystate.plyrbtns[cell]['isPressed']:
            emoji = '✅️' if mystate.plyrbtns[cell]['isTrueFalse'] else '❌'
            cols[row][col].markdown(pressed_emoji.replace('|fill_variable|', emoji), True)
        else:
            vemoji = mystate.plyrbtns[cell]['eMoji']
            cols[row][col].button(vemoji, on_click=check_button_press, args=(cell,), key=f"B{cell}")

    st.caption('')
    st.markdown(horizontal_bar, True)

    if len(mystate.expired_cells) == (total_cells ** 2):
        manage_leaderboard('write')
        st.balloons() if mystate.myscore > 0 else st.snow()
        tm.sleep(5)
        mystate.runpage = main_page
        st.rerun()

def main_page():
    """
    Main function to manage the overall game flow, resetting and preparing the board based on user choices.
    """
    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>', unsafe_allow_html=True)
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    setup_initial_page()
    with st.sidebar:
        mystate.GameDetails[0] = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=1, horizontal=True)
        mystate.GameDetails[3] = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India', help='Optional input only for Leaderboard')

        if st.button(f"🕹️ New Game", use_container_width=True):
            difficulty_settings = {'Easy': (8, 6), 'Medium': (6, 7), 'Hard': (5, 8)}
            mystate.GameDetails[1], mystate.GameDetails[2] = difficulty_settings[mystate.GameDetails[0]]

            manage_leaderboard('create')
            prepare_new_game()
            mystate.runpage = new_game
            st.rerun()

        st.markdown(horizontal_bar, True)

if 'runpage' not in mystate: mystate.runpage = main_page
mystate.runpage()
