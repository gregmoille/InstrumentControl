#!/Users/greg/miniforge3/bin/python

import dash
import numpy as np
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
from yokogawa import Yokogawa
import threading
import time
from scipy import constants as cts
from plotlyServer import plotlyServer
from layout import create_layout
from callbacks import register_callbacks
from plot_config import create_osa_figure, get_color_palette
from trace_osa import TraceOSA

# Initialize Dash app
app = dash.Dash(__name__)

# Get color palette for use in threading class
clrway_ibm = get_color_palette()

# Create figure with modern styling
fig = create_osa_figure()

# Create OSA thread but don't start it yet
osa_thread = None
current_figurl = None  # Store current plotly figure URL object

# Set the app layout using the imported function
app.layout = create_layout(fig)

# Use references for global variables that callbacks need to modify
osa_thread_ref = [None]  # Use list to make it mutable reference
current_figurl_ref = [None]  # Use list to make it mutable reference

# Register all callbacks
register_callbacks(app, osa_thread_ref, fig, current_figurl_ref)

if __name__ == '__main__':
    # Don't start OSA thread automatically - let user control it
    try:
        app.run(
            debug=True, 
            use_reloader=False, 
            host='0.0.0.0',  # This is correct
            port=8050,       # Explicitly set port
            threaded=True    # Enable threading
        )
    finally:
        # Clean shutdown - disconnect OSA if still connected
        osa_thread = osa_thread_ref[0]
        if osa_thread and osa_thread.is_alive():
            osa_thread.stop()
            if osa_thread.osa.connected:
                osa_thread.osa.connected = False
