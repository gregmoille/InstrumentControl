#!/Users/greg/miniforge3/bin/python

import dash
import numpy as np
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
from yokogawa import Yokogawa
import time
from scipy import constants as cts
from plotlyServer import plotlyServer

def register_callbacks(app, osa_thread_ref, fig, current_figurl_ref):
    """Register all Dash callbacks with the app"""
    
    @app.callback(
        [Output('status', 'children'),
         Output('toggle-btn', 'children')],
        [Input('toggle-btn', 'n_clicks'),
         Input('ip-dropdown', 'value')]
    )
    def control_osa(n_clicks, selected_ip):
        from trace_osa import TraceOSA
        
        # Get the current osa_thread from the reference
        osa_thread = osa_thread_ref[0]
        
        # Determine current state
        is_running = osa_thread and osa_thread.is_alive() and osa_thread._running
        
        if n_clicks > 0:  # Button was clicked
            if not is_running:
                # Start OSA with selected IP
                if osa_thread is None or not osa_thread.is_alive():
                    # Create new thread and start it with selected IP
                    osa_thread = TraceOSA(ip=selected_ip, fig=fig)
                    osa_thread.start()
                    osa_thread_ref[0] = osa_thread  # Update the reference
                else:
                    # Thread exists but paused, resume it
                    osa_thread._running = True
                return f"OSA Running ({selected_ip})", "Stop OSA"
            else:
                # Stop OSA
                if osa_thread and osa_thread.is_alive():
                    osa_thread._running = False
                return "OSA Stopped", "Start OSA"
        
        # Initial state
        return "OSA Status", "Start OSA"

    @app.callback(
        [Output('scan-repeat-btn', 'style'),
        Output('scan-single-btn', 'style'),
        Output('scan-stop-btn', 'style')],
        [Input('scan-repeat-btn', 'n_clicks'),
        Input('scan-single-btn', 'n_clicks'),
        Input('scan-stop-btn', 'n_clicks')]
    )
    def control_scan_mode(repeat_clicks, single_clicks, stop_clicks):
        osa_thread = osa_thread_ref[0]
        
        # Import button styles from layout
        from layout import get_button_styles, COLORS
        button_styles = get_button_styles()
        
        # Define active and inactive styles based on your button styles
        info_inactive = {**button_styles['INFO'], 'width': '32%', 'marginRight': '2%', 'opacity': '0.6'}
        info_active = {**button_styles['INFO'], 'width': '32%', 'marginRight': '2%', 'boxShadow': '0 0 0 3px rgba(6, 182, 212, 0.3)'}
        
        danger_inactive = {**button_styles['DANGER'], 'width': '32%', 'opacity': '0.6'}
        danger_active = {**button_styles['DANGER'], 'width': '32%', 'boxShadow': '0 0 0 3px rgba(239, 68, 68, 0.3)'}
        
        # Check if OSA is connected
        if not (osa_thread and osa_thread.is_alive() and osa_thread.osa.connected):
            return info_inactive, info_inactive, danger_inactive
        
        # Get the context to see which button was clicked
        ctx = dash.callback_context
        if not ctx.triggered:
            # Show current mode based on thread state (for initial load)
            if hasattr(osa_thread, 'current_scan_mode'):
                current_mode = osa_thread.current_scan_mode
                if current_mode == "repeat":
                    return info_active, info_inactive, danger_inactive
                elif current_mode == "single":
                    return info_inactive, info_active, danger_inactive
                elif current_mode == "stop":
                    return info_inactive, info_inactive, danger_active
            return info_inactive, info_inactive, danger_inactive
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        try:
            if button_id == 'scan-repeat-btn':
                osa_thread.osa.scan = "repeat"
                osa_thread.current_scan_mode = "repeat"
                return info_active, info_inactive, danger_inactive
            elif button_id == 'scan-single-btn':
                osa_thread.osa.scan = "single"
                osa_thread.current_scan_mode = "single"
                return info_inactive, info_active, danger_inactive
            elif button_id == 'scan-stop-btn':
                osa_thread.osa.scan = "stop"
                osa_thread.current_scan_mode = "stop"
                return info_inactive, info_inactive, danger_active
        except Exception as e:
            print(f"Error setting scan mode: {e}")
            return info_inactive, info_inactive, danger_inactive
        
        return info_inactive, info_inactive, danger_inactive




    # Separate callback to update scan mode display when OSA connects
    @app.callback(
        [Output('scan-repeat-btn', 'style', allow_duplicate=True),
        Output('scan-single-btn', 'style', allow_duplicate=True),
        Output('scan-stop-btn', 'style', allow_duplicate=True)],
        [Input('interval-component', 'n_intervals')],
        prevent_initial_call=True
    )
    def update_scan_mode_display(n_intervals):
        osa_thread = osa_thread_ref[0]
        # Import button styles from layout
        from layout import get_button_styles, COLORS
        button_styles = get_button_styles()
        
        # Define active and inactive styles
        info_inactive = {**button_styles['INFO'], 'width': '32%', 'marginRight': '2%', 'opacity': '0.6'}
        info_active = {**button_styles['INFO'], 'width': '32%', 'marginRight': '2%', 'boxShadow': '0 0 0 3px rgba(6, 182, 212, 0.3)'}
        
        danger_inactive = {**button_styles['DANGER'], 'width': '32%', 'opacity': '0.6'}
        danger_active = {**button_styles['DANGER'], 'width': '32%', 'boxShadow': '0 0 0 3px rgba(239, 68, 68, 0.3)'}
        
        # Check if OSA is connected and show initial mode
        if (osa_thread and osa_thread.is_alive() and osa_thread.osa.connected and 
            hasattr(osa_thread, 'current_scan_mode')):
            
            osa_thread.scan_mode_updated = True  # Mark as updated
            current_mode = osa_thread.current_scan_mode
            
            if current_mode == "repeat":
                return info_active, info_inactive, danger_inactive
            elif current_mode == "single":
                return info_inactive, info_active, danger_inactive
            elif current_mode == "stop":
                return info_inactive, info_inactive, danger_active
        
        return dash.no_update, dash.no_update, dash.no_update




    @app.callback(
        [Output('preset-status', 'children'),
         Output('centwlgth', 'value', allow_duplicate=True),
         Output('span', 'value', allow_duplicate=True),
         Output('resolution', 'value', allow_duplicate=True),
         Output('sensitivity', 'value', allow_duplicate=True),
         Output('pts-auto', 'value', allow_duplicate=True)],
        [Input('fine-preset-btn', 'n_clicks'),
         Input('coarse-preset-btn', 'n_clicks')],
        [dash.dependencies.State('ip-dropdown', 'value')],
        prevent_initial_call=True
    )
    def apply_preset_settings(fine_clicks, coarse_clicks, selected_ip):
        osa_thread = osa_thread_ref[0]
        
        # Determine which button was clicked
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'fine-preset-btn':
            # Fine Octave Spanning preset
            preset_params = {
                'centwlgth': 1.21e-06,  # 1210 nm
                'span': 9.8e-07,        # 980 nm
                'pts_auto': True,
                'resolution': 0.02e-9,  # 0.02 nm
                'sensitivity': 3,       # High 1
                'calib_zero': False
            }
            preset_name = "Fine Octave Spanning"
            
        elif button_id == 'coarse-preset-btn':
            # Coarse Octave Spanning preset
            preset_params = {
                'centwlgth': 1.21e-06,  # 1210 nm
                'span': 9.8e-07,        # 980 nm
                'pts_auto': True,
                'resolution': 1e-9,     # 1 nm
                'sensitivity': 1,       # Norm/auto
                'calib_zero': False
            }
            preset_name = "Coarse Octave Spanning"
        else:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        try:
            # Apply settings to OSA
            if osa_thread and osa_thread.is_alive() and osa_thread.osa.connected:
                # Apply to running OSA
                # Set flag to pause trace acquisition
                osa_thread.applying_settings = True

                while not osa_thread.got_trace:
                    pass
                osa_thread.osa.settings = preset_params
                time.sleep(0.25)  # Wait for settings to apply
                
                # Read back the actual settings to update UI
                actual_settings = osa_thread.osa.settings
                
                # Clear flag to resume trace acquisition
                time.sleep(0.25)
                osa_thread.applying_settings = False
                print(f"Applied {preset_name} preset to running OSA")
            else:
                # Apply to OSA via temporary connection
                temp_osa = Yokogawa(ip=selected_ip)
                temp_osa.connected = True
                try:
                    temp_osa.settings = preset_params
                    time.sleep(0.5)
                    actual_settings = temp_osa.settings
                    print(f"Applied {preset_name} preset via temporary connection")
                finally:
                    temp_osa.connected = False
            
            # Update UI with actual settings from OSA
            return (
                f"{preset_name} applied successfully!",
                actual_settings['centwlgth'] * 1e9,  # Convert m to nm
                actual_settings['span'] * 1e9,       # Convert m to nm
                actual_settings['resolution'] * 1e9,  # Convert m to nm
                actual_settings['sensitivity'],
                actual_settings.get('pts_auto', True)
            )
            
        except Exception as e:
            print(f"Error applying {preset_name} preset: {e}")
            return f"Error applying {preset_name}: {str(e)}", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    @app.callback(
        Output('pts', 'disabled'),
        Input('pts-auto', 'value')
    )
    def toggle_pts_input(pts_auto):
        # Ensure pts_auto is treated as boolean
        return bool(pts_auto) if pts_auto is not None else True

    @app.callback(
        [Output('settings-status', 'children'),
         Output('centwlgth', 'value', allow_duplicate=True),
         Output('span', 'value', allow_duplicate=True),
         Output('resolution', 'value', allow_duplicate=True),
         Output('sensitivity', 'value', allow_duplicate=True),
         Output('pts-auto', 'value', allow_duplicate=True),
         Output('pts', 'value', allow_duplicate=True)],
        Input('apply-settings-btn', 'n_clicks'),
        [dash.dependencies.State('centwlgth', 'value'),
         dash.dependencies.State('span', 'value'), 
         dash.dependencies.State('resolution', 'value'),
         dash.dependencies.State('sensitivity', 'value'),
         dash.dependencies.State('pts-auto', 'value'),
         dash.dependencies.State('pts', 'value'),
         dash.dependencies.State('ip-dropdown', 'value')],
        prevent_initial_call=True
    )
    def settings_osa(n_clicks, centwlgth, span, resolution, sensitivity, pts_auto, pts, selected_ip):
        osa_thread = osa_thread_ref[0]    
        if n_clicks == 0:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

        try:
            # Check if we have a running OSA thread with connection
            if osa_thread and osa_thread.is_alive() and osa_thread.osa.connected:
                # Set flag to pause trace acquisition
                osa_thread.applying_settings = True
                
                # Apply settings directly to the existing connection
                settings_dict = {
                    'centwlgth': centwlgth * 1e-9,  # Convert nm to m
                    'span': span * 1e-9,  # Convert nm to m  
                    'resolution': resolution * 1e-9,  # Convert nm to m
                    'sensitivity': sensitivity,
                    'pts_auto': pts_auto,
                    'pts': int(pts) if not pts_auto and pts is not None else None,  # Convert to int and only set if manual mode
                    'calib_zero': True  # Enable auto calibration
                }
                while not osa_thread.got_trace:
                    pass
                osa_thread.osa.settings = settings_dict
                time.sleep(0.25)
                
                # Read back the actual settings to update UI
                actual_settings = osa_thread.osa.settings
                time.sleep(0.25)
                # Clear flag to resume trace acquisition
                osa_thread.applying_settings = False
                print("Settings applied to running OSA")
            else:
                # No running connection, create temporary connection to apply settings
                temp_osa = Yokogawa(ip=selected_ip)
                temp_osa.connected = True
                try:
                    settings_dict = {
                        'centwlgth': centwlgth * 1e-9,  # Convert nm to m
                        'span': span * 1e-9,  # Convert nm to m  
                        'resolution': resolution * 1e-9,  # Convert nm to m
                        'sensitivity': sensitivity,
                        'pts_auto': pts_auto,
                        'pts': int(pts) if not pts_auto and pts is not None else None,  # Convert to int and only set if manual mode
                        'calib_zero': True  # Enable auto calibration
                    }
                    temp_osa.settings = settings_dict
                    time.sleep(0.5)
                    
                    # Read back the actual settings to update UI
                    actual_settings = temp_osa.settings
                    print("Settings applied via temporary connection")
                finally:
                    temp_osa.connected = False
            
            # Update UI with actual settings from OSA
            return (
                f"Settings applied: {actual_settings['centwlgth']*1e9:.1f}nm center, {actual_settings['span']*1e9:.1f}nm span, {actual_settings['resolution']*1e9:.3f}nm res",
                actual_settings['centwlgth'] * 1e9,  # Convert m to nm
                actual_settings['span'] * 1e9,       # Convert m to nm
                actual_settings['resolution'] * 1e9,  # Convert m to nm
                actual_settings['sensitivity'],
                actual_settings.get('pts_auto', True),
                int(actual_settings.get('pts', 1001))
            )
            
        except Exception as e:
            print(f"Error applying settings: {e}")
            return f"Error: {str(e)}", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    @app.callback(
        Output('file-extension', 'children'),
        Input('export-type', 'value')
    )
    def update_file_extension(export_type):
        if export_type == 'csv':
            return '.csv'
        elif export_type == 'plotly':
            return ' (Plotly Server)'
        return '.csv'

    @app.callback(
        [Output('save-status', 'children'),
        Output('plotly-url', 'children'),
        Output('delete-btn', 'style')],
        Input('save-btn', 'n_clicks'),
        [dash.dependencies.State('export-type', 'value'),
        dash.dependencies.State('save-path', 'value'),
        dash.dependencies.State('filename', 'value'),
        dash.dependencies.State('trace-graph', 'figure')]
    )
    def save_trace_data(n_clicks, export_type, save_path, filename, current_figure):
        osa_thread = osa_thread_ref[0]
        current_figurl = current_figurl_ref[0]
        
        if n_clicks == 0:
            return "", "", {'backgroundColor': '#ff5757', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'padding': '8px 16px', 'marginLeft': '10px', 'cursor': 'pointer', 'fontWeight': '500', 'fontSize': '14px', 'display': 'none', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}
        
        try:
            # Check if OSA is connected and has trace data
            if not (osa_thread and osa_thread.is_alive() and osa_thread.trace is not None):
                return "Error: No trace data available. Please connect OSA and acquire trace first.", "", {'backgroundColor': '#ff5757', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'padding': '8px 16px', 'marginLeft': '10px', 'cursor': 'pointer', 'fontWeight': '500', 'fontSize': '14px', 'display': 'none', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}
            
            if export_type == 'csv':
                # CSV Export
                # Ensure the path ends with a slash
                if not save_path.endswith('/'):
                    save_path += '/'
                
                # Create the full file path
                full_path = f"{save_path}{filename}.csv"
                
                # Save the trace data to CSV
                osa_thread.trace.to_csv(full_path, index=False)
                
                return f"CSV data saved successfully to: {full_path}", "", {'backgroundColor': '#ff5757', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'padding': '8px 16px', 'marginLeft': '10px', 'cursor': 'pointer', 'fontWeight': '500', 'fontSize': '14px', 'display': 'none', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}
                
            elif export_type == 'plotly':
                # Plotly Server Upload
                figHTML = go.Figure()
                trace_data = osa_thread.trace.copy()
                
                # Apply power threshold and create frequency column
                trace_data.S[trace_data.S < -85] = -85
                freq_thz = 1e-12 * cts.c / trace_data.lbd
                
                # Create the figure
                figHTML.add_trace(go.Scatter(x=freq_thz, y=trace_data.S, mode='lines', name='OSA Trace'))
                figHTML.update_xaxes(title='Frequency [THz]')
                figHTML.update_yaxes(title='Power [dBm]')
                figHTML.update_layout(
                    title=f"{filename}",
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                
                # Copy markers from current figure to export figure
                if current_figure and 'layout' in current_figure:
                    if 'shapes' in current_figure['layout'] and current_figure['layout']['shapes']:
                        figHTML.layout.shapes = current_figure['layout']['shapes']
                    if 'annotations' in current_figure['layout'] and current_figure['layout']['annotations']:
                        figHTML.layout.annotations = current_figure['layout']['annotations']
                
                # Upload to Plotly server
                figurl = plotlyServer(fig=figHTML, figname=filename)
                current_figurl_ref[0] = figurl  # Update the reference
                
                # Create clickable link for the URL
                url_link = html.A(
                    figurl.figurl,
                    href=figurl.figurl,
                    target="_blank",
                    style={'color': '#2196F3', 'textDecoration': 'underline'}
                )
                
                # Show delete button when plot is uploaded
                delete_style = {'backgroundColor': '#ff5757', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'padding': '8px 16px', 'marginLeft': '10px', 'cursor': 'pointer', 'fontWeight': '500', 'fontSize': '14px', 'display': 'inline-block', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'transition': 'all 0.2s ease'}
                
                return "Plot uploaded to Plotly server successfully!", url_link, delete_style
            
        except Exception as e:
            return f"Error: {str(e)}", "", {'backgroundColor': '#ff5757', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'padding': '8px 16px', 'marginLeft': '10px', 'cursor': 'pointer', 'fontWeight': '500', 'fontSize': '14px', 'display': 'none', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}


    @app.callback(
        [Output('delete-status', 'children'),
         Output('delete-btn', 'style', allow_duplicate=True),
         Output('plotly-url', 'children', allow_duplicate=True)],
        Input('delete-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def delete_plotly_figure(n_clicks):
        current_figurl = current_figurl_ref[0]
        
        if n_clicks == 0:
            return "", {'backgroundColor': '#ff5757', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'padding': '8px 16px', 'marginLeft': '10px', 'cursor': 'pointer', 'fontWeight': '500', 'fontSize': '14px', 'display': 'none', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, ""
        
        try:
            if current_figurl is not None:
                # Delete the figure from Plotly server
                current_figurl.removeHTML()
                current_figurl_ref[0] = None  # Clear the stored figurl
                
                # Hide the delete button and clear the URL
                hide_style = {'backgroundColor': '#ff5757', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'padding': '8px 16px', 'marginLeft': '10px', 'cursor': 'pointer', 'fontWeight': '500', 'fontSize': '14px', 'display': 'none', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}
                
                return "Plot successfully deleted from Plotly server!", hide_style, ""
            else:
                return "Error: No plot to delete!", {'backgroundColor': '#ff5757', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'padding': '8px 16px', 'marginLeft': '10px', 'cursor': 'pointer', 'fontWeight': '500', 'fontSize': '14px', 'display': 'none', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, ""
                
        except Exception as e:
            return f"Error deleting plot: {str(e)}", {'backgroundColor': '#ff5757', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'padding': '8px 16px', 'marginLeft': '10px', 'cursor': 'pointer', 'fontWeight': '500', 'fontSize': '14px', 'display': 'inline-block', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}, ""

    @app.callback(
        [Output('centwlgth', 'value'),
         Output('span', 'value'),
         Output('resolution', 'value'),
         Output('sensitivity', 'value'),
         Output('pts-auto', 'value'),
         Output('pts', 'value')],
        Input('interval-component', 'n_intervals')
    )
    def update_settings_display(n):
        osa_thread = osa_thread_ref[0]
        
        # Only update UI settings once when OSA first connects and reads settings
        if (osa_thread and osa_thread.is_alive() and 
            osa_thread.current_settings and not osa_thread.settings_updated):
            
            settings = osa_thread.current_settings
            osa_thread.settings_updated = True  # Mark as updated so we don't update again
            
            return (
                settings['centwlgth']*1e9,  # Convert m to nm
                settings['span']*1e9,
                settings['resolution']*1e9,
                settings['sensitivity'],
                settings.get('pts_auto', True),
                int(settings.get('pts', 1001))
            )
        
        # Return current values (no change)
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    @app.callback(
        Output('trace-graph', 'figure', allow_duplicate=True),
        Input('clear-annotations-btn', 'n_clicks'),
        [dash.dependencies.State('trace-graph', 'figure')],
        prevent_initial_call=True
    )
    def clear_annotations(n_clicks, current_figure):
        if n_clicks > 0:
            # Create a fresh figure with only the trace data
            updated_fig = go.Figure()
            
            # Copy only the trace data from the current figure
            if current_figure and 'data' in current_figure:
                for trace in current_figure['data']:
                    updated_fig.add_trace(trace)
            
            # Apply the layout from the original figure but without shapes/annotations
            if current_figure and 'layout' in current_figure:
                layout_copy = dict(current_figure['layout'])
                layout_copy['shapes'] = []
                layout_copy['annotations'] = []
                updated_fig.update_layout(layout_copy)
            
            # Update the global fig object as well
            fig.layout.shapes = []
            fig.layout.annotations = []
            
            return updated_fig
        return dash.no_update



    @app.callback(
        [Output('wavelength-btn', 'style'),
        Output('frequency-btn', 'style'),
        Output('trace-graph', 'figure', allow_duplicate=True),
        Output('vline-position', 'value'),
        Output('display-mode-store', 'data')],
        [Input('wavelength-btn', 'n_clicks'),
        Input('frequency-btn', 'n_clicks')],
        [dash.dependencies.State('vline-position', 'value'),
        dash.dependencies.State('trace-graph', 'figure'),
        dash.dependencies.State('display-mode-store', 'data')],
        prevent_initial_call=True
    )
    def toggle_display_mode(wavelength_clicks, frequency_clicks, vline_pos, current_figure, current_mode):
        osa_thread = osa_thread_ref[0]
        
        # Button styles
        COLORS = {
            'primary': '#2563eb',
            'secondary': '#64748b',
            'success': '#10b981',
            'white': '#ffffff'
        }
        
        base_style = {
            'color': COLORS['white'],
            'border': 'none',
            'borderRadius': '8px',
            'fontWeight': '500',
            'cursor': 'pointer',
            'transition': 'all 0.2s ease',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'fontSize': '13px', 
            'padding': '6px 14px'
        }
        
        active_style = {**base_style, 'backgroundColor': COLORS['success']}
        inactive_style = {**base_style, 'backgroundColor': COLORS['secondary']}
        
        # Get the context to see which button was clicked
        ctx = dash.callback_context
        if not ctx.triggered:
            # Initial state - default to wavelength
            return active_style, inactive_style, dash.no_update, dash.no_update, 'wavelength'
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Set default current_mode if None
        if current_mode is None:
            current_mode = 'wavelength'
        
        # Get current figure
        updated_fig = go.Figure(current_figure)
        
        # Convert existing trace data between wavelength and frequency
        if updated_fig.data and len(updated_fig.data) > 0:
            try:
                # Check if x data exists and is valid
                x_data = updated_fig.data[0]['x']
                y_data = updated_fig.data[0]['y']
                
                print(f"X data type: {type(x_data)}")
                
                # Handle case where data might be None or empty
                if x_data is None:
                    print("X data is None, skipping conversion")
                    if current_mode == 'wavelength':
                        return active_style, inactive_style, dash.no_update, dash.no_update, 'wavelength'
                    else:
                        return inactive_style, active_style, dash.no_update, dash.no_update, 'frequency'
                
                # Check if x_data is a Plotly data structure (dictionary with _inputArray)
                if isinstance(x_data, dict):
                    if '_inputArray' in x_data:
                        # Get the actual number of data points from shape
                        shape = int(x_data['_inputArray'].get('shape', '0'))
                        # Extract actual numeric values from _inputArray using the shape
                        x_values = []
                        for i in range(shape):
                            if str(i) in x_data['_inputArray']:
                                x_values.append(float(x_data['_inputArray'][str(i)]))
                        
                        print(f"Extracted {len(x_values)} values from _inputArray (shape: {shape})")
                        
                        if len(x_values) == 0:
                            print("No valid numeric data found in _inputArray")
                            if current_mode == 'wavelength':
                                return active_style, inactive_style, dash.no_update, dash.no_update, 'wavelength'
                            else:
                                return inactive_style, active_style, dash.no_update, dash.no_update, 'frequency'
                            
                    else:
                        print("Warning: X data is a dictionary but no _inputArray found, skipping conversion")
                        if current_mode == 'wavelength':
                            return active_style, inactive_style, dash.no_update, dash.no_update, 'wavelength'
                        else:
                            return inactive_style, active_style, dash.no_update, dash.no_update, 'frequency'
                else:
                    # x_data is already a list/array
                    x_values = x_data
                
                # Do the same for y_data if needed
                if isinstance(y_data, dict) and '_inputArray' in y_data:
                    y_shape = int(y_data['_inputArray'].get('shape', '0'))
                    y_values = []
                    for i in range(y_shape):
                        if str(i) in y_data['_inputArray']:
                            y_values.append(float(y_data['_inputArray'][str(i)]))
                else:
                    y_values = y_data
                
                # Check if we have valid data
                if not x_values or len(x_values) == 0:
                    print("No valid x values found")
                    if current_mode == 'wavelength':
                        return active_style, inactive_style, dash.no_update, dash.no_update, 'wavelength'
                    else:
                        return inactive_style, active_style, dash.no_update, dash.no_update, 'frequency'
                
                # Convert to numpy arrays
                current_x_data = np.array(x_values, dtype=np.float64)
                current_y_data = np.array(y_values, dtype=np.float64)
                
                print(f"Successfully converted to numpy. X length: {len(current_x_data)}")
                print(f"X range: {current_x_data[0]:.2f} to {current_x_data[-1]:.2f}")
                
                if current_x_data is not None and len(current_x_data) > 0:
                    if button_id == 'wavelength-btn' and current_mode != 'wavelength':
                        # Converting from frequency (THz) to wavelength (nm)
                        # Current x is in THz, convert to nm
                        new_x_data = [cts.c / (freq * 1e12) * 1e9 if freq > 0 else 0 for freq in current_x_data]
                        updated_fig.data[0]['x'] = new_x_data
                        updated_fig.update_xaxes(title='Wavelength (nm)')
                        
                        # Convert existing markers (vertical lines) from THz to nm
                        try:
                            if updated_fig.layout.shapes:
                                converted_shapes = []
                                for shape in updated_fig.layout.shapes:
                                    # Create a new shape dictionary with all the original properties
                                    new_shape = {
                                        'type': shape.get('type', shape.type if hasattr(shape, 'type') else 'line'),
                                        'x0': shape.get('x0', shape.x0 if hasattr(shape, 'x0') else None),
                                        'x1': shape.get('x1', shape.x1 if hasattr(shape, 'x1') else None),
                                        'y0': shape.get('y0', shape.y0 if hasattr(shape, 'y0') else None),
                                        'y1': shape.get('y1', shape.y1 if hasattr(shape, 'y1') else None),
                                        'xref': shape.get('xref', shape.xref if hasattr(shape, 'xref') else 'x'),
                                        'yref': shape.get('yref', shape.yref if hasattr(shape, 'yref') else 'y'),
                                        'line': shape.get('line', shape.line if hasattr(shape, 'line') else {}),
                                    }
                                    
                                    # Check if it's a vertical line (x0 == x1)
                                    if (new_shape['x0'] is not None and new_shape['x1'] is not None and 
                                        new_shape['x0'] == new_shape['x1']):
                                        # Convert vertical line position from THz to nm
                                        freq_thz = float(new_shape['x0'])
                                        if freq_thz > 0:
                                            new_x_pos = cts.c / (freq_thz * 1e12) * 1e9
                                            new_shape['x0'] = new_x_pos
                                            new_shape['x1'] = new_x_pos
                                            print(f"Converted vline from {freq_thz:.3f} THz to {new_x_pos:.1f} nm")
                                    
                                    converted_shapes.append(new_shape)
                                
                                updated_fig.layout.shapes = converted_shapes
                                print(f"Successfully converted {len(converted_shapes)} shapes")
                        except Exception as marker_error:
                            print(f"Error converting markers: {marker_error}")
                            # Continue without marker conversion if there's an error
                        
                        # Update OSA thread display mode if it exists
                        if osa_thread and osa_thread.is_alive():
                            osa_thread.display_mode = "wavelength"
                        
                        # Convert vline position from THz to nm
                        if vline_pos is not None and vline_pos > 0:
                            new_vline_pos = cts.c / (vline_pos * 1e12) * 1e9
                        else:
                            new_vline_pos = vline_pos
                        
                        return active_style, inactive_style, updated_fig, new_vline_pos, 'wavelength'
                        
                    elif button_id == 'frequency-btn' and current_mode != 'frequency':
                        # Converting from wavelength (nm) to frequency (THz)
                        # Current x is in nm, convert to THz
                        new_x_data = [cts.c / (wl * 1e-9) * 1e-12 if wl > 0 else 0 for wl in current_x_data]
                        updated_fig.data[0]['x'] = new_x_data
                        updated_fig.update_xaxes(title='Frequency (THz)')
                        
                        # Convert existing markers (vertical lines) from nm to THz
                        try:
                            if updated_fig.layout.shapes:
                                converted_shapes = []
                                for shape in updated_fig.layout.shapes:
                                    # Create a new shape dictionary with all the original properties
                                    new_shape = {
                                        'type': shape.get('type', shape.type if hasattr(shape, 'type') else 'line'),
                                        'x0': shape.get('x0', shape.x0 if hasattr(shape, 'x0') else None),
                                        'x1': shape.get('x1', shape.x1 if hasattr(shape, 'x1') else None),
                                        'y0': shape.get('y0', shape.y0 if hasattr(shape, 'y0') else None),
                                        'y1': shape.get('y1', shape.y1 if hasattr(shape, 'y1') else None),
                                        'xref': shape.get('xref', shape.xref if hasattr(shape, 'xref') else 'x'),
                                        'yref': shape.get('yref', shape.yref if hasattr(shape, 'yref') else 'y'),
                                        'line': shape.get('line', shape.line if hasattr(shape, 'line') else {}),
                                    }
                                    
                                    # Check if it's a vertical line (x0 == x1)
                                    if (new_shape['x0'] is not None and new_shape['x1'] is not None and 
                                        new_shape['x0'] == new_shape['x1']):
                                        # Convert vertical line position from nm to THz
                                        wavelength_nm = float(new_shape['x0'])
                                        if wavelength_nm > 0:
                                            new_x_pos = cts.c / (wavelength_nm * 1e-9) * 1e-12
                                            new_shape['x0'] = new_x_pos
                                            new_shape['x1'] = new_x_pos
                                            print(f"Converted vline from {wavelength_nm:.1f} nm to {new_x_pos:.3f} THz")
                                    
                                    converted_shapes.append(new_shape)
                                
                                updated_fig.layout.shapes = converted_shapes
                                print(f"Successfully converted {len(converted_shapes)} shapes")
                        except Exception as marker_error:
                            print(f"Error converting markers: {marker_error}")
                            # Continue without marker conversion if there's an error
                        
                        # Update OSA thread display mode if it exists
                        if osa_thread and osa_thread.is_alive():
                            osa_thread.display_mode = "frequency"
                        
                        # Convert vline position from nm to THz
                        if vline_pos is not None and vline_pos > 0:
                            new_vline_pos = cts.c / (vline_pos * 1e-9) * 1e-12
                        else:
                            new_vline_pos = vline_pos
                        
                        return inactive_style, active_style, updated_fig, new_vline_pos, 'frequency'
            
            except Exception as e:
                print(f"Error processing figure data: {e}")
                print(f"X data type: {type(x_data)}")
                # Return current state on error
                if current_mode == 'wavelength':
                    return active_style, inactive_style, dash.no_update, dash.no_update, 'wavelength'
                else:
                    return inactive_style, active_style, dash.no_update, dash.no_update, 'frequency'
        
        # No mode change or no data - just update button styles based on current mode
        if current_mode == 'wavelength':
            return active_style, inactive_style, dash.no_update, dash.no_update, 'wavelength'
        else:
            return inactive_style, active_style, dash.no_update, dash.no_update, 'frequency'




            
            # Rest of your conversion code stays the same...




    ########
    @app.callback(
        [Output('trace-graph', 'figure', allow_duplicate=True),
        Output('markers-status', 'children')],
        [Input('add-vline-btn', 'n_clicks'),
        Input('add-hline-btn', 'n_clicks')],
        [dash.dependencies.State('vline-position', 'value'),
        dash.dependencies.State('vline-color', 'value'),
        dash.dependencies.State('vline-dash', 'value'),
        dash.dependencies.State('hline-position', 'value'),
        dash.dependencies.State('hline-color', 'value'),
        dash.dependencies.State('hline-dash', 'value'),
        dash.dependencies.State('trace-graph', 'figure'),
        dash.dependencies.State('display-mode-store', 'data')],
        prevent_initial_call=True
    )
    def add_markers(vline_clicks, hline_clicks, vline_pos, vline_color, vline_dash, 
                    hline_pos, hline_color, hline_dash, current_figure, display_mode):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update, ""
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Get current figure
        updated_fig = go.Figure(current_figure)
        
        if button_id == 'add-vline-btn' and vline_pos is not None:
            # Add vertical line at the position (already in the correct units)
            updated_fig.add_vline(
                x=vline_pos,
                line_color=vline_color,
                line_width=2,
                line_dash=vline_dash
            )
            
            # Also update the global fig object
            fig.add_vline(
                x=vline_pos,
                line_color=vline_color,
                line_width=2,
                line_dash=vline_dash
            )
            
            unit = "nm" if display_mode == "wavelength" else "THz"
            return updated_fig, f"Vertical line added at {vline_pos} {unit}"
        
        elif button_id == 'add-hline-btn' and hline_pos is not None:
            # Add horizontal line
            updated_fig.add_hline(
                y=hline_pos,
                line_color=hline_color,
                line_width=2,
                line_dash=hline_dash
            )
            
            # Also update the global fig object
            fig.add_hline(
                y=hline_pos,
                line_color=hline_color,
                line_width=2,
                line_dash=hline_dash
            )
            
            return updated_fig, f"Horizontal line added at {hline_pos} dBm"
        
        return dash.no_update, ""



    @app.callback(
        Output('vline-unit', 'children'),
        Input('wavelength-btn', 'n_clicks'),
        Input('frequency-btn', 'n_clicks')
    )
    def update_vline_unit(wavelength_clicks, frequency_clicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            return "nm"
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'wavelength-btn':
            return "nm"
        elif button_id == 'frequency-btn':
            return "THz"
        
        return "nm"


    @app.callback(
        Output('trace-graph', 'figure'),
        Input('interval-component', 'n_intervals'),
        [dash.dependencies.State('trace-graph', 'figure')]
    )
    def update_graph(n, current_figure):
        osa_thread = osa_thread_ref[0]
        
        # Always return no update if no OSA thread
        if not (osa_thread and osa_thread.is_alive()):
            return dash.no_update
        
        # Check if we have data in the current figure
        has_data = (current_figure and 'data' in current_figure and 
                    len(current_figure['data']) > 0 and 
                    current_figure['data'][0] and 
                    'x' in current_figure['data'][0] and 
                    current_figure['data'][0]['x'] is not None and
                    len(current_figure['data'][0]['x']) > 0)
        
        # If scan is stopped AND we already have data, don't override (preserve manual conversions)
        if (hasattr(osa_thread, 'current_scan_mode') and 
            osa_thread.current_scan_mode == 'stop' and has_data):
            return dash.no_update
        
        # Allow update if:
        # - We're actively scanning, OR
        # - We don't have data yet (initial population)
        return fig


