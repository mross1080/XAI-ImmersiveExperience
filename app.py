#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
from flask import Flask, render_template, request, jsonify
from lifxlan import BLUE, GREEN, LifxLAN, sleep

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

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


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


mood_lookup = {"happy":1,"default":2,"angry":3}

@app.route('/register')
def register():
    print 'changing'
    print request.args
    print request.data
    print request.values
    mood = request.args.get("mood","")
    if mood:
        control_channel = mood_lookup[mood]


    outport.send(mido.Message('control_change', control=control_channel, value=70, channel=2))
    try:
        search_lights()
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

def search_lights():
    num_lights = None
    if len(sys.argv) != 2:
        print("\nDiscovery will go much faster if you provide the number of lights on your LAN:")
        print("  python {} <number of lights on LAN>\n".format(sys.argv[0]))
    else:
        num_lights = int(sys.argv[1])

    # instantiate LifxLAN client, num_lights may be None (unknown).
    # In fact, you don't need to provide LifxLAN with the number of bulbs at all.
    # lifx = LifxLAN() works just as well. Knowing the number of bulbs in advance
    # simply makes initial bulb discovery faster.
    print("Discovering lights...")
    lifx = LifxLAN(num_lights)

    # get devices
    devices = lifx.get_lights()
    bulb = devices[0]
    print("Selected {}".format(bulb.get_label()))

    # get original state
    original_power = bulb.get_power()
    original_color = bulb.get_color()
    bulb.set_power("on")

    sleep(0.2) # to look pretty

    print("Toggling power...")
    toggle_device_power(bulb, 0.2)

    print("Toggling color...")
    toggle_light_color(bulb, 0.2)

    # restore original color
    # color can be restored after the power is turned off as well
    print("Restoring original color and power...")
    bulb.set_color(original_color)

    sleep(1) # to look pretty.

    # restore original power
    bulb.set_power(original_power)

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


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
