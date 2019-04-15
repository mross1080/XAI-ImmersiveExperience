# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from copy import copy
import random

from flask import Flask, render_template, request, jsonify
from lifxlan import BLUE, GREEN, LifxLAN, sleep, RED, ORANGE, YELLOW, CYAN, PURPLE, PINK, time, Group, WHITE

BEIGE = [10500, 20000, 65535, 3500]
SADNESS_VIOLET = [46634, 65535, 65535, 3500]
DARK_GREEN = [16173, 65535, 20000, 1500]
MUTED_YELLOW = [9000, 65535, 65535, 3500]


import logging
from logging import Formatter, FileHandler



# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


last_enabled = 1
last = 3
mood_lookup = {"happy": 1, "sadness": 2, "angry": 3, "fear": 4, "trust": 5, "amazement": 6,"neutral":7,"rage":3,"ecstasy":10,"musicoff":11,"start":12}
current = ""




@app.route('/changeMood')
def register():
    # print 'changing'
    # print request.args
    print request.data
    # print request.values
    mood = request.args.get("mood", "")
    lightTargets = request.args.get("lightTargets", "")
    try:
        if mood is not "musicoff":
            setWaveformsOnGroup(active_bulbs, mood,lightTargets)
        # search_lights(mood)
    except Exception as e:
        print "problms "
        print e

    return jsonify({"state": mood})


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
    "previous" : "default",
    "happy": {
        "light_animation_type": "smooth",
        "default_color": YELLOW,
        "cycle_color": [15500, 30000, 65535, 3500]
    },
    "starkwhite": {
        "light_animation_type": "stark",
        "default_color": WHITE,
        "cycle_color": [15500, 30000, 65535, 3500]
    },
    "rage": {
        "light_animation_type": "smooth",
        "default_color": [65535, 65535, 65535, 2000],
        "cycle_color": ORANGE
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
        "light_animation_type": "single",
        "default_color": ORANGE,
        "cycle_color": CYAN
    },
    "end": {
        "light_animation_type": "urgency",
        "default_color": ORANGE,
        "cycle_color": CYAN
    },
    "trust": {
        "light_animation_type": "smooth",
        "default_color": PURPLE,
        "cycle_color": WHITE
    },
    "neutral": {
        "light_animation_type": "smooth",
        "default_color": BEIGE,
        "cycle_color": MUTED_YELLOW
    },
    "ambiance": {
        "light_animation_type": "smooth",
        "default_color": WHITE,
        "cycle_color": BEIGE
    },
    "ecstasy": {
        "light_animation_type": "smooth",
        "default_color": MUTED_YELLOW,
        "cycle_color": SADNESS_VIOLET
    },
    "delight": {
        "light_animation_type": "smooth",
        "default_color": YELLOW,
        "cycle_color": ORANGE
    },
    "neutralcuriosity": {
        "light_animation_type": "smooth",
        "default_color": MUTED_YELLOW,
        "cycle_color": CYAN
    },
    "tension": {
        "light_animation_type": "smooth",
        "default_color": BLUE,
        "cycle_color": SADNESS_VIOLET
    },
    "darkneutral": {
        "light_animation_type": "single",
        "default_color": CYAN,
        "cycle_color": BLUE
    },
    "flash": {
        "light_animation_type": "flash",
        "default_color": CYAN,
        "cycle_color": BLUE
    },
    "sadness": {
        "light_animation_type": "single",
        "default_color": PURPLE,
        "cycle_color": BLUE
    }

}




def setWaveformsOnGroup(bulb_group, mood, lightTargets):
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
    # There is no way to get any acknowledgements of state change from the LIFX bulbs without acutally making a request and asking what it's state is
    # For now I'm using a fire multiple times that just sends the request three times to each bulb to up the probablility that it will be recieved
    devices_to_control = bulb_group
    if (lightTargets == "single" or lightTargets == "start"):
        # devices_to_control = single_group
        devices_to_control = middle_group
        try:
            turn_of_all_lights()
        except Exception as e:
            print e
            print "Problem in turning off lights Reconnecting"
            devices = lifx.get_devices_by_group("Forest")
            active_bulbs = devices
            bulb_group = active_bulbs
            count -= 1

    elif (lightTargets == "middle"):
        try:
            turn_of_all_lights()
        except Exception as e:
            print e
            print "Problem in turning off lights Reconnecting"
            devices = lifx.get_devices_by_group("Forest")
            active_bulbs = devices
            bulb_group = active_bulbs
            count-=1

        devices_to_control = middle_group





    # if light_animation_type == "start":
    #     devices_to_control = [lifx.get_device_by_name(single_group_name[0])]
    #
    #     turn_of_all_lights()

    # if light_animation_type == "smooth":
    #     turn_of_all_lights()
    if (count <= 2 ):
        for device in devices_to_control:
            try:
                device.set_power(65535)

                device.set_color(default_color,rapid=False)

                if light_animation_type == "smooth":
                    device.set_waveform(1, cycle_color, 5000, 6, 10000, 3)
                elif light_animation_type == "urgency":
                    device.set_waveform(0, cycle_color, 2500, 10, 0, 3)
                elif light_animation_type == "strobe":
                     device.set_color(default_color)
                     device.set_waveform(1, cycle_color, 300, 40, 0, 4)
                elif light_animation_type == "flash":
                     device.set_color(ORANGE)
                elif light_animation_type == "stark":
                     device.set_color(WHITE)
                elif light_animation_type == "single":
                    turn_of_all_lights()

                    device.set_power(65535)
                    device.set_color(default_color)
                    device.set_waveform(1, cycle_color, 5000, 10, 10000, 3)
                    break
                elif light_animation_type == "start":


                    # single_device = lifx.get_device_by_name("Forest_08")
                    device.set_power(65535)
                    device.set_color(default_color)
                    device.set_waveform(1, [0, 0, 0, 0], 3000, 7, -20000, 3)

                elif light_animation_type == "dance_party":
                    trigger_dance_party(bulb_group)
                    break
            except Exception as e:
                print e
                print "Problem in setting light waveform Reconnecting"
                devices = lifx.get_devices_by_group("Forest")
                active_bulbs = devices
                bulb_group = active_bulbs
                count -= 1

        count+=1
        time.sleep(4)
    mood_light_config["previous"] = light_animation_type
    print("Done setting up new light sequence")
    # previous_state = light_animation_type

def trigger_dance_party(bulb_group):
    for i in range(60):
        try:
            print("Here")
            note = random.randint(50, 70)
            bulb_group.set_color([random.randint(10000, 50000), 65535, 65535, 3500])

            time.sleep(.3)


        except Exception as e:
            print e


def turn_of_all_lights():
    for device in active_bulbs:
        device.set_power(0)



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
back_group_names = ["Forest_14"]
front_group_names = ["Forest_01", "Forest_02", "Forest_03"]
# middle_light_names = ["Forest_08",  "Forest_11","Forest_14"]
middle_light_names = ["Forest_08",  "Forest_02","Forest_14"]




single_group_name = "Forest_02"
front_group = []
middle_group = []
single_group = []
active_bulbs = {}
current_group = {}


def reconnect_to_bulbs():
    devices = lifx.get_devices_by_group("Forest")
    # previous_state = "default"
    if devices:
        try:

            # These pseudo groups are used because we are unable to create new groups at the theater space
            single_group = [lifx.get_device_by_name(single_group_name)]

            for light_name in middle_light_names:
                middle_group.append(lifx.get_device_by_name(light_name))
            active_bulbs = devices
        except Exception as e:
            print "Exception in setting up individual grouped areas "
            print e
        return True
    else:
        return False

import time
currently_running = False
# Default port:
if __name__ == '__main__':
    retry_attempts = 5
    retry_count = 0
    NOT_NEAR_BULBS = False

    print("Discovering lights...")
    lifx = LifxLAN(20)
    while True:
        print("At top of start app loop")

        # get devices
        try:
            # if reconnect_to_bulbs():

            devices = lifx.get_devices_by_group("Forest")
            # # previous_state = "default"
            if devices:
                print "Operating with {} LIFX Bulbs".format(len(devices.devices))

                # These pseudo groups are used because we are unable to create new groups at the theater space
                single_group = [lifx.get_device_by_name(single_group_name)]

                for light_name in middle_light_names:
                    middle_group.append(lifx.get_device_by_name(light_name))

                active_bulbs = devices.devices
                setWaveformsOnGroup(active_bulbs, "starkwhite","all")
                
                print("Starting app")
                app.run(use_reloader=False)
                time.sleep(5)

            else:
                if retry_count > retry_attempts:
                    print "PROBLEM FINDING LIGHTS PLEASE CHECK YOUR NETWORK, YOU MAY BE USING 5G OR GUEST NETWORK WHICH CAUSES PROBLEMS"
                    exit()
                else:
                    print "PROBLEM FINDING LIGHTS ATTEMPTING TO RECONNECT"

                    time.sleep(5)


        except Exception as e:
            if NOT_NEAR_BULBS:
                print "Flag Enabled for not near LIFX Bulbs, nothing will happen right now with lighting"
                app.run()
                break
            print "Exception Found in Initializing Group Bulbs Array"
            print e
            time.sleep(4)





# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''


def messWithSettings():
    print "hi"
    # single_bulb  = active_bulbs.devices[random.randint(0,8)]
    # current_group.set_power(65535)
    # single_bulb.set_color([50486, 65535, 65535, 100])
    # # active_bulbs.devices[random.randint(0,8)].set_color(PURPLE)
    # for device in current_group.devices:
    #     if device.get_label() in middle_light_names:
    #         middle_group.append(device)
    # while True:
    #     active_bulbs.set_power(0)
    #     single_bulb = active_bulbs.devices[random.randint(0, 8)]
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
    # active_bulbs.set_color(	[46634, 65535, 65535, 3500])
    # active_bulbs.set_color(PURPLE)
    # g = lifx.get_devices_by_group("Forest")
    # breathe_lights(g)
    # breathe_lights_single(devices[0])
    # for device in devices:
    #     print "Checking"
    #     print device.get_label()
    #
    #     if device.get_label() == "Forest_05" or True:
    #         # if device.get_label() == "A Small Lamp":
    #         active_bulbs = device
    #         # device.set_waveform(True, GREEN, 0.5, 3, 0.5, 3)
    #         breathe_lights()
    #
    #         # bulb = devices[2]
    #         print("Selected {}".format(active_bulbs.get_label()))


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

