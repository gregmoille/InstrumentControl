from dash import dcc, html

def create_layout(fig):
    """Create and return the modern Dash app layout"""
    
    # Modern color scheme and styling
    COLORS = {
        'primary': '#2563eb',      # Blue
        'secondary': '#64748b',    # Slate
        'success': '#10b981',      # Emerald
        'warning': '#f59e0b',      # Amber
        'danger': '#ef4444',       # Red
        'info': '#06b6d4',         # Cyan
        'dark': '#1e293b',         # Dark slate
        'light': '#f8fafc',        # Very light gray
        'white': '#ffffff',
        'background': '#f1f5f9',   # Light slate
        'card': '#ffffff',
        'border': '#e2e8f0',       # Light border
        'text': '#334155',         # Dark text
        'muted': '#64748b'         # Muted text
    }
    
    # Common button styles
    PRIMARY_BUTTON = {
        'backgroundColor': COLORS['primary'],
        'color': COLORS['white'],
        'border': 'none',
        'borderRadius': '8px',
        'padding': '10px 20px',
        'fontWeight': '500',
        'fontSize': '14px',
        'cursor': 'pointer',
        'transition': 'all 0.2s ease',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }
    
    SUCCESS_BUTTON = {**PRIMARY_BUTTON, 'backgroundColor': COLORS['success']}
    WARNING_BUTTON = {**PRIMARY_BUTTON, 'backgroundColor': COLORS['warning']}
    DANGER_BUTTON = {**PRIMARY_BUTTON, 'backgroundColor': COLORS['danger']}
    INFO_BUTTON = {**PRIMARY_BUTTON, 'backgroundColor': COLORS['info']}
    SECONDARY_BUTTON = {**PRIMARY_BUTTON, 'backgroundColor': COLORS['secondary']}
    
    # Card styles
    CARD_STYLE = {
        'backgroundColor': COLORS['card'],
        'border': f"1px solid {COLORS['border']}",
        'borderRadius': '12px',
        'padding': '24px',
        'marginBottom': '24px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.05)',
        'transition': 'box-shadow 0.2s ease'
    }
    
    # Input styles
    INPUT_STYLE = {
        'border': f"2px solid {COLORS['border']}",
        'borderRadius': '8px',
        'padding': '8px 12px',
        'fontSize': '14px',
        'backgroundColor': COLORS['white'],
        'transition': 'border-color 0.2s ease',
        'outline': 'none'
    }
    
    # Label styles
    LABEL_STYLE = {
        'fontSize': '14px',
        'fontWeight': '500',
        'color': COLORS['text'],
        'marginBottom': '8px',
        'display': 'block'
    }
    
    return html.Div([
        # Main Container
        html.Div([
            # Connection Controls Card
            html.Div([
                html.H2("Connection", style={
                    'color': COLORS['dark'],
                    'fontSize': '20px',
                    'fontWeight': '600',
                    'margin': '0 0 20px 0'
                }),
                
                html.Div([
                    html.Div([
                        html.Label("OSA IP Address", style=LABEL_STYLE),
                        dcc.Dropdown(
                            id='ip-dropdown',
                            options=[
                                {'label': '10.0.0.20', 'value': '10.0.0.20'},
                                {'label': '10.0.0.21', 'value': '10.0.0.21'}
                            ],
                            value='10.0.0.21',
                            style={
                                'border': 'none',
                                'borderRadius': '8px',
                                'fontSize': '14px'
                            }
                        )
                    ], style={'width': '200px', 'marginRight': '24px'}),
                    
                    html.Div([
                        html.Button('Start OSA', id='toggle-btn', n_clicks=0, style=SUCCESS_BUTTON),
                        html.Div(id='status', style={
                            'marginLeft': '16px',
                            'display': 'inline-block',
                            'fontSize': '14px',
                            'fontWeight': '500',
                            'color': COLORS['muted']
                        })
                    ], style={'display': 'flex', 'alignItems': 'center'})
                ], style={'display': 'flex', 'alignItems': 'end'})
            ], style=CARD_STYLE),
            
            # Scan Mode Controls Card
            html.Div([
                html.H2("Scan Mode", style={
                    'color': COLORS['dark'],
                    'fontSize': '20px',
                    'fontWeight': '600',
                    'margin': '0 0 20px 0'
                }),
                
                html.Div([
                    html.Button('Repeat', id='scan-repeat-btn', n_clicks=0, 
                               style={**SECONDARY_BUTTON, 'marginRight': '12px'}),
                    html.Button('Single', id='scan-single-btn', n_clicks=0, 
                               style={**SECONDARY_BUTTON, 'marginRight': '12px'}),
                    html.Button('Stop', id='scan-stop-btn', n_clicks=0, 
                               style={**DANGER_BUTTON, 'marginRight': '24px'}),
                    html.Div(id='scan-status', style={
                        'display': 'inline-block',
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'color': COLORS['primary'],
                        'padding': '8px 16px',
                        'backgroundColor': f"{COLORS['primary']}15",
                        'borderRadius': '20px'
                    })
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], style=CARD_STYLE),
        
            # OSA Settings Panel Card
            html.Div([
                html.H2("OSA Settings", style={
                    'color': COLORS['dark'],
                    'fontSize': '20px',
                    'fontWeight': '600',
                    'margin': '0 0 20px 0'
                }),
                
                # Preset Buttons Section
                html.Div([
                    html.H3("Quick Presets", style={
                        'fontSize': '16px',
                        'fontWeight': '500',
                        'color': COLORS['text'],
                        'margin': '0 0 16px 0'
                    }),
                    html.Div([
                        html.Button('Fine Octave Spanning', id='fine-preset-btn', n_clicks=0, 
                                   style={**INFO_BUTTON, 'marginRight': '12px'}),
                        html.Button('Coarse Octave Spanning', id='coarse-preset-btn', n_clicks=0, 
                                   style={**SECONDARY_BUTTON, 'marginRight': '20px'}),
                        html.Div(id='preset-status', style={
                            'display': 'inline-block',
                            'fontSize': '14px',
                            'fontWeight': '500',
                            'color': COLORS['success']
                        })
                    ], style={'display': 'flex', 'alignItems': 'center'})
                ], style={
                    'backgroundColor': f"{COLORS['info']}08",
                    'padding': '20px',
                    'borderRadius': '8px',
                    'border': f"1px solid {COLORS['info']}30",
                    'marginBottom': '24px'
                }),
                
                # Settings Grid
                html.Div([
                    # Row 1
                    html.Div([
                        html.Div([
                            html.Label("Center Wavelength (nm)", style=LABEL_STYLE),
                            dcc.Input(id='centwlgth', type='number', value=1550, step=0.1, 
                                     style={**INPUT_STYLE, 'width': '100%'})
                        ], style={'width': '48%'}),
                        html.Div([
                            html.Label("Span (nm)", style=LABEL_STYLE),
                            dcc.Input(id='span', type='number', value=100, step=0.1, 
                                     style={**INPUT_STYLE, 'width': '100%'})
                        ], style={'width': '48%'})
                    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),
                    
                    # Row 2
                    html.Div([
                        html.Div([
                            html.Label("Resolution (nm)", style=LABEL_STYLE),
                            dcc.Input(id='resolution', type='number', value=0.02, step=0.01, 
                                     style={**INPUT_STYLE, 'width': '100%'})
                        ], style={'width': '48%'}),
                        html.Div([
                            html.Label("Sensitivity", style=LABEL_STYLE),
                            dcc.Dropdown(
                                id='sensitivity',
                                options=[
                                    {'label': 'Norm/hold', 'value': 0},
                                    {'label': 'Norm/auto', 'value': 1},
                                    {'label': 'Normal', 'value': 6},
                                    {'label': 'Mid', 'value': 2},
                                    {'label': 'High 1', 'value': 3},
                                    {'label': 'High 2', 'value': 4},
                                    {'label': 'High 3', 'value': 5},
                                ],
                                value=1,
                                style={'borderRadius': '8px', 'fontSize': '14px'}
                            )
                        ], style={'width': '48%'})
                    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),
                    
                    # Row 3
                    html.Div([
                        html.Div([
                            html.Label("Points Mode", style=LABEL_STYLE),
                            dcc.RadioItems(
                                id='pts-auto',
                                options=[
                                    {'label': 'Automatic', 'value': True},
                                    {'label': 'Manual', 'value': False}
                                ],
                                value=True,
                                inline=True,
                                style={'fontSize': '14px', 'color': COLORS['text']}
                            )
                        ], style={'width': '48%'}),
                        html.Div([
                            html.Label("Number of Points", style=LABEL_STYLE),
                            dcc.Input(id='pts', type='number', value=1001, step=1, min=51, max=50001, 
                                     disabled=True, style={**INPUT_STYLE, 'width': '100%'})
                        ], style={'width': '48%'})
                    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '24px'}),
                    
                    # Apply Button
                    html.Div([
                        html.Button('Apply Settings', id='apply-settings-btn', n_clicks=0, 
                                   style=PRIMARY_BUTTON),
                        html.Div(id='settings-status', style={
                            'marginLeft': '16px',
                            'display': 'inline-block',
                            'fontSize': '14px',
                            'fontWeight': '500',
                            'color': COLORS['success']
                        })
                    ], style={'display': 'flex', 'alignItems': 'center'})
                ])
            ], style=CARD_STYLE),
            
            # Data Export Panel Card
            html.Div([
                html.H2("Data Export", style={
                    'color': COLORS['dark'],
                    'fontSize': '20px',
                    'fontWeight': '600',
                    'margin': '0 0 20px 0'
                }),
                
                html.Div([
                    # Export type and path
                    html.Div([
                        html.Div([
                            html.Label("Export Type", style=LABEL_STYLE),
                            dcc.Dropdown(
                                id='export-type',
                                options=[
                                    {'label': 'CSV File', 'value': 'csv'},
                                    {'label': 'Plotly Server', 'value': 'plotly'}
                                ],
                                value='csv',
                                style={'borderRadius': '8px', 'fontSize': '14px'}
                            )
                        ], style={'width': '200px', 'marginRight': '20px'}),
                        
                        html.Div([
                            html.Label("Save Path", style=LABEL_STYLE),
                            dcc.Input(id='save-path', type='text', 
                                     value='/Users/greg/Desktop/DashExperiment/',
                                     style={**INPUT_STYLE, 'width': '100%'})
                        ], style={'flex': '1', 'marginRight': '20px'})
                    ], style={'display': 'flex', 'alignItems': 'end', 'marginBottom': '20px'}),
                    
                    # Filename and buttons
                    html.Div([
                        html.Div([
                            html.Label("Filename", style=LABEL_STYLE),
                            dcc.Input(id='filename', type='text', value='trace_data',
                                     style={**INPUT_STYLE, 'width': '100%'})
                        ], style={'width': '200px', 'marginRight': '12px'}),
                        
                        html.Div(id='file-extension', children='.csv', style={
                            'fontSize': '14px',
                            'color': COLORS['muted'],
                            'padding': '8px 0',
                            'marginRight': '20px'
                        }),
                        
                        html.Button('Save/Upload', id='save-btn', n_clicks=0, 
                                   style={**PRIMARY_BUTTON, 'marginRight': '12px'}),
                        html.Button('Delete from Server', id='delete-btn', n_clicks=0, 
                                   style={**DANGER_BUTTON, 'display': 'none'})
                    ], style={'display': 'flex', 'alignItems': 'end', 'marginBottom': '16px'}),
                    
                    # Status messages
                    html.Div(id='save-status', style={
                        'fontSize': '14px',
                        'color': COLORS['primary'],
                        'marginBottom': '8px'
                    }),
                    html.Div(id='plotly-url', style={'marginBottom': '8px'}),
                    html.Div(id='delete-status', style={
                        'fontSize': '14px',
                        'color': COLORS['danger']
                    })
                ])
            ], style=CARD_STYLE),
            
            # Plot Card
            html.Div([
                html.H2("Spectrum Display", style={
                    'color': COLORS['dark'],
                    'fontSize': '20px',
                    'fontWeight': '600',
                    'margin': '0 0 20px 0'
                }),
                
                dcc.Graph(
                    id='trace-graph', 
                    figure=fig,
                    style={'height': '600px'},
                    config={
                        'modeBarButtonsToAdd': [
                            'drawline',
                            'drawopenpath',
                            'drawclosedpath',
                            'drawcircle',
                            'drawrect',
                            'eraseshape'
                        ],
                        'modeBarButtonsToRemove': [],
                        'displayModeBar': True,
                        'displaylogo': False,
                        'editable': True,
                        'scrollZoom': True,
                        'doubleClick': 'reset',
                        'showTips': True,
                        'edits': {
                            'annotationPosition': True,
                            'annotationTail': True,
                            'annotationText': True,
                            'axisTitleText': True,
                            'colorbarPosition': True,
                            'colorbarTitleText': True,
                            'legendPosition': True,
                            'legendText': True,
                            'shapePosition': True,
                            'titleText': True
                        },
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': 'osa_trace_with_annotations',
                            'height': 600,
                            'width': 1000,
                            'scale': 1
                        }
                    }
                ),
                
                # Display Controls
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label("X-Axis Display:", style={
                                'fontSize': '14px',
                                'fontWeight': '500',
                                'color': COLORS['text'],
                                'marginRight': '12px'
                            }),
                            html.Button('Wavelength (nm)', id='wavelength-btn', n_clicks=0, 
                                       style={**SUCCESS_BUTTON, 'fontSize': '13px', 'padding': '6px 14px', 'marginRight': '8px'}),
                            html.Button('Frequency (THz)', id='frequency-btn', n_clicks=0, 
                                       style={**SECONDARY_BUTTON, 'fontSize': '13px', 'padding': '6px 14px'})
                        ], style={'display': 'flex', 'alignItems': 'center'}),
                        
                        html.Button('Clear All Annotations', id='clear-annotations-btn', n_clicks=0, 
                                   style={**DANGER_BUTTON, 'fontSize': '13px', 'padding': '8px 16px'})
                    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'})
                ], style={'marginTop': '16px'})
            ], style=CARD_STYLE),
            
            # Update Interval
            dcc.Interval(
                id='interval-component',
                interval=10,
                n_intervals=0
            )
        ], style={
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': '0 24px 32px 24px'
        })
        
    ], style={
        'backgroundColor': COLORS['background'],
        'minHeight': '100vh',
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        'lineHeight': '1.5'
    })
