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
            hasattr(osa_thread, 'current_scan_mode') and not osa_thread.scan_mode_updated):
            
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
         dash.dependencies.State('filename', 'value')]
    )
    def save_trace_data(n_clicks, export_type, save_path, filename):
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
                
                # Add reference lines
                figHTML.add_vline(x=192.642283, line_color='gray', line_width=1, line_dash='dot')
                figHTML.add_vline(x=2*192.642283, line_color='gray', line_width=1, line_dash='dot')
                
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
            # Get the current figure and clear shapes/annotations
            updated_fig = go.Figure(current_figure)
            updated_fig.update_layout(
                shapes=[],
                annotations=[]
            )
            
            # Also update the global fig object to keep it in sync
            fig.update_layout(
                shapes=[],
                annotations=[]
            )
            
            return updated_fig
        return dash.no_update

    @app.callback(
        [Output('wavelength-btn', 'style'),
         Output('frequency-btn', 'style'),
         Output('trace-graph', 'figure', allow_duplicate=True)],
        [Input('wavelength-btn', 'n_clicks'),
         Input('frequency-btn', 'n_clicks')],
        prevent_initial_call=True
    )
    def toggle_display_mode(wavelength_clicks, frequency_clicks):
        osa_thread = osa_thread_ref[0]
        
        # Button styles - define locally to avoid import issues
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
            # Default state - wavelength mode
            return active_style, inactive_style, dash.no_update
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Update OSA thread display mode if it exists
        if osa_thread and osa_thread.is_alive():
            if button_id == 'wavelength-btn':
                osa_thread.display_mode = "wavelength"
                # Update figure axis title
                fig.update_layout(xaxis_title="Wavelength (nm)")
                return active_style, inactive_style, fig
            elif button_id == 'frequency-btn':
                osa_thread.display_mode = "frequency"
                # Update figure axis title
                fig.update_layout(xaxis_title="Frequency (THz)")
                return inactive_style, active_style, fig
        else:
            # No OSA running, just update button styles and figure
            if button_id == 'wavelength-btn':
                fig.update_layout(xaxis_title="Wavelength (nm)")
                return active_style, inactive_style, fig
            elif button_id == 'frequency-btn':
                fig.update_layout(xaxis_title="Frequency (THz)")
                return inactive_style, active_style, fig
        
        # Default state
        return active_style, inactive_style, dash.no_update

    @app.callback(
        Output('trace-graph', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_graph(n):
        return fig
