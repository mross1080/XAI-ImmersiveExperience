#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys

from copy import copy
import random

from flask import Flask, render_template, request, jsonify
from lifxlan import BLUE, GREEN, LifxLAN, sleep, RED, ORANGE, YELLOW, CYAN, PURPLE, PINK, time

# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import mido


outport = mido.open_output('To Live Live')

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)



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
last  = 3
mood_lookup = {"happy":1,"default":2,"angry":3,"fear":4,"trust":5,"amazement":6}

# enabled_channel_disable_map = {1:12}
enabled_channel_disable_map = {1:10,2:12,3:11}
# enabled_channel_disable_map = {1:11}




@app.route('/register')
def register():
    print 'changing'
    print request.args
    print request.data
    print request.values
    mood = request.args.get("mood","")
    if mood:
        control_channel = mood_lookup[mood]
        # Turn on new track

        # #Turn off other channels
        # for key in enabled_channel_disable_map.keys():
        #
        #     outport.send(mido.Message('control_change', control=enabled_channel_disable_map[key], value=70, channel=2))

        # Trigger new scene
        outport.send(mido.Message('control_change', control=control_channel, value=70, channel=2))

        # last_enabled = control_channel
        # last = last_enabled
    try:
        search_lights(mood)
    except Exception as e:
        print "problms "

    return jsonify({"hello":"you"})


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
    #db_session.rollback()
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

def search_lights(mood):
    # num_lights = None
    # if len(sys.argv) != 2:
    #     print("\nDiscovery will go much faster if you provide the number of lights on your LAN:")
    #     print("  python {} <number of lights on LAN>\n".format(sys.argv[0]))
    # else:
    #     num_lights = int(sys.argv[1])
    #
    # # instantiate LifxLAN client, num_lights may be None (unknown).
    # # In fact, you don't need to provide LifxLAN with the number of bulbs at all.
    # # lifx = LifxLAN() works just as well. Knowing the number of bulbs in advance
    # # simply makes initial bulb discovery faster.
    # print("Discovering lights...")
    # lifx = LifxLAN(num_lights)
    #
    # # get devices
    # devices = lifx.get_lights()
    # bulb = devices[2]
    # print("Selected {}".format(bulb.get_label()))
    #
    # # get original state
    # original_power = bulb.get_power()
    # original_color = bulb.get_color()
    # bulb.set_power("on")
    #
    # sleep(0.2) # to look pretty

    bulb = current_bulb
    a = True
    if mood == "happy":
        bulb.set_color(GREEN)
    elif mood == "angry":
        bulb.set_color(RED)
    elif mood == "amazement":
        bulb.set_color(CYAN)
    elif mood == "fear":
        bulb.set_color(ORANGE)
    elif mood == "trust":
        bulb.set_color(PURPLE)
    else:
        bulb.set_color(BLUE)


    # rainbow(bulb, 0.1)
    # print("Toggling power...")
    # toggle_device_power(bulb, 0.2)
    #
    # print("Toggling color...")
    # toggle_light_color(bulb, 0.2)
    #
    # # restore original color
    # # color can be restored after the power is turned off as well
    # print("Restoring original color and power...")
    # bulb.set_color()
    #
    # sleep(1) # to look pretty.
    #
    # # restore original power
    # bulb.set_power(original_power)


def rainbow(bulb, duration_secs=0.5, smooth=False):
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
    colors = [RED, ORANGE]

    transition_time_ms = duration_secs*1000 if smooth else 0
    rapid = True if duration_secs < 1 else False
    for color in colors:
        bulb.set_color(color, transition_time_ms, rapid)
        sleep(duration_secs)
def toggle_device_power(device, interval=0.5, num_cycles=3): #TEST
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
original_colors = [BLUE, PURPLE,PINK]
anger_colors = [RED, ORANGE,PINK]



def breathe_lights(group):

    half_period_ms = 500
    duration_mins = 20
    duration_secs = duration_mins*60
    print("Breathing...")
    bulb = group.devices
    start_time = time()
    while True:
        for color in original_colors:
            index = random.randint(0,len(group.devices)) -1
            dim = list(copy(color))
            half_bright = int(dim[2]/2)
            dim[2] = half_bright if half_bright >= 1900 else 1900
            bulb[index].set_color(dim, half_period_ms, rapid=True)
            sleep(half_period_ms/1000.0)
        for  color in original_colors:
            bulb[index].set_color(color, half_period_ms, rapid=True)
            sleep(half_period_ms/1000.0)
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


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

current_bulb = {}

# Default port:
if __name__ == '__main__':
    print("Discovering lights...")
    lifx = LifxLAN(1)

    # get devices
    devices = lifx.get_lights()
    if devices:
        current_bulb = devices[0]
    else:
        print "PROBLEM FINDING LIGHTS PLEASE CHECK YOUR NETWORK"
        exit()
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

    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
