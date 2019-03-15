# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import sys

from copy import copy
import random

from flask import Flask, render_template, request, jsonify
from lifxlan import BLUE, GREEN, LifxLAN, sleep, RED, ORANGE, YELLOW, CYAN, PURPLE, PINK, time, Group, WHITE

BEIGE = [10500, 20000, 65535, 3500]
SADNESS_VIOLET = [46634, 65535, 65535, 3500]
DARK_GREEN = [16173, 65535, 20000, 1500]
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import mido

outport = mido.open_output('To Live Live')

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')


# db = SQLAlchemy(app)



@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


last_enabled = 1
last = 3
mood_lookup = {"happy": 1, "sadness": 2, "angry": 3, "fear": 4, "trust": 5, "amazement": 6,"neutral":7,"rage":3,"ecstasy":10,"musicoff":11,"start":12}

# enabled_channel_disable_map = {1:12}
enabled_channel_disable_map = {1: 10, 2: 12, 3: 11}


# enabled_channel_disable_map = {1:11}




@app.route('/register')
def register():
    print 'changing'
    print request.args
    print request.data
    print request.values
    mood = request.args.get("mood", "")
    if mood:
        control_channel = mood_lookup[mood]
        # Turn off old audio
        outport.send(mido.Message('control_change', control=11, value=70, channel=2))
        # Trigger new scene audio in ableton
        outport.send(mido.Message('control_change', control=control_channel, value=70, channel=2))

        # last_enabled = control_channel
        # last = last_enabled
    try:
        if mood is not "musicoff":
            setWaveformsOnGroup(current_bulb, mood)
        # search_lights(mood)
    except Exception as e:
        print "problms "
        print e

    return jsonify({"hello": "you"})


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/search')
def search():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

mood_light_config = {

    "happy": {
        "light_animation_type": "smooth",
        "default_color": YELLOW,
        "cycle_color": [15500, 30000, 65535, 3500]
    },
    "rage": {
        "light_animation_type": "smooth",
        "default_color": ORANGE,
        "cycle_color": [65535, 65535, 65535, 2000]
    },
    "angry": {
        "light_animation_type": "strobe",
        "default_color": RED,
        "cycle_color": [0,0,0,0]
    },
    "amazement": {
        "light_animation_type": "urgency",
        "default_color": ORANGE,
        "cycle_color": CYAN
    },
    "fear": {
        "light_animation_type": "strobe",
        "default_color": DARK_GREEN,
        "cycle_color": [0, 0, 0, 0]
    },
    "start": {
        "light_animation_type": "start",
        "default_color": GREEN,
        "cycle_color": [0, 0, 0, 0]
    },
    "trust": {
        "light_animation_type": "smooth",
        "default_color": SADNESS_VIOLET,
        "cycle_color": WHITE
    },
    "neutral": {
        "light_animation_type": "smooth",
        "default_color": WHITE,
        "cycle_color": BEIGE
    },
    "ecstasy": {
        "light_animation_type": "dance_party",
        "default_color": WHITE,
        "cycle_color": BEIGE
    },
    "sadness": {
        "light_animation_type": "smooth",
        "default_color": PURPLE,
        "cycle_color": BLUE
    }

}




def setWaveformsOnGroup(bulb_group, mood):
    # Strobe
    # bulb.set_color_all_lights(WHITE)
    # bulb.set_waveform_all_lights(0, [0,0,0,0], 500, 11, 0, 4)#


    # Cycle Colors
    #  bulb.set_color_all_lights(YELLOW)
    # bulb.set_color(BEIGE)
    # bulb.set_waveform_all_lights(1, [15500, 30000, 65535, 3500], 5000, 10, 10000, 3)


    default_color = mood_light_config[mood]["default_color"]
    cycle_color = mood_light_config[mood]["cycle_color"]
    light_animation_type = mood_light_config[mood]["light_animation_type"]

    count = 0;
    if (count <= 2):
        for device in bulb_group.devices:
            device.set_power(65535)

            device.set_color(default_color)

            if light_animation_type == "smooth":
                device.set_waveform(1, cycle_color, 5000, 6, 10000, 3)
            elif light_animation_type == "urgency":
                device.set_waveform(0, cycle_color, 1500, 15, 0, 3)
            elif light_animation_type == "strobe":
                 device.set_waveform(1, [0, 0, 0, 0], 300, 40, 0, 4)
            elif light_animation_type == "single":
                turn_of_all_lights()

                random_light_index = 0
                if len(bulb_group.devices) > 1:
                    random_light_index = random.randint(0, len(bulb_group.devices))

                single_device = bulb_group.devices[random_light_index]
                single_device.set_power(65535)
                single_device.set_color(default_color)
                single_device.set_waveform(1, cycle_color, 5000, 10, 10000, 3)
                break
            elif light_animation_type == "start":
                turn_of_all_lights()

                random_light_index = 0
                if len(bulb_group.devices) > 1:
                    random_light_index = random.randint(0, len(bulb_group.devices))

                single_device = bulb_group.devices[random_light_index]
                single_device.set_power(65535)
                single_device.set_color(default_color)
                device.set_waveform(1, [0, 0, 0, 0], 1000, 10, 0, 4)
                break
            elif light_animation_type == "dance_party":
                trigger_dance_party(bulb_group)
                break


        count+=1
        time.sleep(1)

def trigger_dance_party(bulb_group):
    for i in range(60):
        try:
            print("Here")
            note = random.randint(50, 70)
            bulb_group.set_color([random.randint(10000, 50000), 65535, 65535, 3500])
            outport.send(mido.Message('note_on', note=note, channel=2))
            time.sleep(.3)
            outport.send(mido.Message('note_off', note=note, channel=2))

        except Exception as e:
            print e


def turn_of_all_lights():
    for device in current_bulb.devices:
        device.set_power(0)

def rainbow(bulb, duration_secs=0.5, smooth=False):
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
    colors = [RED, ORANGE]

    transition_time_ms = duration_secs * 1000 if smooth else 0
    rapid = True if duration_secs < 1 else False
    for color in colors:
        bulb.set_color(color, transition_time_ms, rapid)
        sleep(duration_secs)


def toggle_device_power(device, interval=0.5, num_cycles=3):  # TEST
    original_power_state = device.get_power()
    device.set_power("off")
    rapid = True if interval < 1 else False
    for i in range(num_cycles):
        device.set_power("on", rapid)
        sleep(interval)
        device.set_power("off", rapid)
        sleep(interval)
    device.set_power(original_power_state)


def toggle_light_color(light, interval=0.5, num_cycles=3):
    original_color = light.get_color()
    rapid = True if interval < 1 else False
    for i in range(num_cycles):
        light.set_color(BLUE, rapid=rapid)
        sleep(interval)
        light.set_color(GREEN, rapid=rapid)
        sleep(interval)
    light.set_color(original_color)


# original_colors  = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
original_colors = [BLUE, PURPLE, PINK]
anger_colors = [RED, ORANGE, PINK]


def breathe_lights(group):
    half_period_ms = 500
    duration_mins = 20
    duration_secs = duration_mins * 60
    print("Breathing...")
    bulb = group.devices
    start_time = time()
    while True:
        for color in original_colors:
            index = random.randint(0, len(group.devices)) - 1
            dim = list(copy(color))
            half_bright = int(dim[2] / 2)
            dim[2] = half_bright if half_bright >= 1900 else 1900
            bulb[index].set_color(dim, half_period_ms, rapid=True)
            sleep(half_period_ms / 1000.0)
        for color in original_colors:
            bulb[index].set_color(color, half_period_ms, rapid=True)
            sleep(half_period_ms / 1000.0)
        if time() - start_time > duration_secs:
            raise KeyboardInterrupt


def breathe_lights_single(light):
    half_period_ms = 100
    duration_mins = 20
    duration_secs = duration_mins * 60
    print("Breathing...")
    start_time = time()
    while True:
        for color in anger_colors:
            dim = list(copy(color))
            half_bright = int(dim[2] / 2)
            dim[2] = half_bright if half_bright >= 1900 else 1900
            light.set_color(dim, half_period_ms, rapid=True)
            sleep(half_period_ms / 1000.0)
        for color in anger_colors:
            light.set_color(color, half_period_ms, rapid=True)
            sleep(half_period_ms / 1000.0)
        if time() - start_time > duration_secs:
            raise KeyboardInterrupt


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

front_group_names = ["Forest_01", "Forest_02", "Forest_03"]
middle_light_names = ["Forest_02", "Forest_05", "Forest_08", "Forest_11", "Forest_14"]
front_group = []
middle_group = []
current_bulb = {}
current_group = {}

import time

# Default port:
if __name__ == '__main__':
    retry_attempts = 5
    retry_count = 0

    print("Discovering lights...")
    lifx = LifxLAN(20)
    while True:

        # get devices
        try:
            devices = lifx.get_devices_by_group("Forest")
            if devices:
                # Setup flag for at home or at wildrence

                for device in devices.devices:
                    try:

                        device.set_power(65535)
                        device.set_color(BLUE)

                        #trigger_dance_party(devices)
                    except Exception as e:
                        print "hi"
                        print e
                #
                setWaveformsOnGroup(devices, "neutral")
                b = devices.devices[0]
                #
                # b.set_color([16173, 65535, 30000, 3500])
                # # b.set_waveform(1, PURPLE, 2000, 10, 0, 2)
                current_bulb = devices
                #current_group = current_bulb

            else:
                if retry_count > retry_attempts:
                    print "PROBLEM FINDING LIGHTS PLEASE CHECK YOUR NETWORK, YOU MAY BE USING 5G OR GUEST NETWORK WHICH CAUSES PROBLEMS"
                    exit()
                else:
                    print "PROBLEM FINDING LIGHTS ATTEMPTING TO RECONNECT"
                    time.sleep(5)
            app.run()
        except Exception as e:
            print "hiii"
            print e





# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''


def messWithSettings():
    print "hi"
    # single_bulb  = current_bulb.devices[random.randint(0,8)]
    # current_group.set_power(65535)
    # single_bulb.set_color([50486, 65535, 65535, 100])
    # # current_bulb.devices[random.randint(0,8)].set_color(PURPLE)
    # for device in current_group.devices:
    #     if device.get_label() in middle_light_names:
    #         middle_group.append(device)
    # while True:
    #     current_bulb.set_power(0)
    #     single_bulb = current_bulb.devices[random.randint(0, 8)]
    #     single_bulb.set_power(65535)
    #     single_bulb.set_color([50486, 65535, 65535, 100])
    #     time.sleep(1)
    # for bulb in middle_group:
    #     try:
    #         bulb.set_color([random.randint(40000, 65000), 65535, 65535, 5500])
    #     except Exception as e:
    #         print e
    #     # current_group.devices[random.randint(0, 8)].set_color([random.randint(30000, 50000), 65535, 65535, 3500])
    #     time.sleep(.1)
    # Group()
    #
    # for index,device in enumerate(current_group.devices):
    #
    #
    #     print device.get_label()
    #     device.set_color([4000*index, 65535, 65535, 3500])
    #     time.sleep(1)

    # for x in range(10000):
    # current_bulb.set_color(	[46634, 65535, 65535, 3500])
    # current_bulb.set_color(PURPLE)
    # g = lifx.get_devices_by_group("Forest")
    # breathe_lights(g)
    # breathe_lights_single(devices[0])
    # for device in devices:
    #     print "Checking"
    #     print device.get_label()
    #
    #     if device.get_label() == "Forest_05" or True:
    #         # if device.get_label() == "A Small Lamp":
    #         current_bulb = device
    #         # device.set_waveform(True, GREEN, 0.5, 3, 0.5, 3)
    #         breathe_lights()
    #
    #         # bulb = devices[2]
    #         print("Selected {}".format(current_bulb.get_label()))
