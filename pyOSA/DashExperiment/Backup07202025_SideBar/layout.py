from dash import dcc, html

# Color scheme and styling constants
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

def get_button_styles():
    """Return minimal button style dictionaries - most styling is in CSS"""
    return {
        'PRIMARY': {'backgroundColor': COLORS['primary'], 'color': COLORS['white']},
        'SUCCESS': {'backgroundColor': COLORS['success'], 'color': COLORS['white']},
        'WARNING': {'backgroundColor': COLORS['warning'], 'color': COLORS['white']},
        'DANGER': {'backgroundColor': COLORS['danger'], 'color': COLORS['white']},
        'INFO': {'backgroundColor': COLORS['info'], 'color': COLORS['white']},
        'SECONDARY': {
            'backgroundColor': 'transparent',
            'color': COLORS['primary'],
            'border': f"2px solid {COLORS['primary']}"
        }
    }

def get_common_styles():
    """Return common style dictionaries"""
    return {
        'CARD': {
            'backgroundColor': COLORS['card'],
            'border': f"1px solid {COLORS['border']}",
            'borderRadius': '12px',
            'padding': '24px',
            'marginBottom': '24px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.05)'
        },
        'LABEL': {
            'fontSize': '14px',
            'fontWeight': '500',
            'color': COLORS['text'],
            'marginBottom': '8px',
            'display': 'block'
        },
        'TAB': {
            'borderBottom': '1px solid #d6d6d6',
            'padding': '12px 24px',
            'fontWeight': '500',
            'backgroundColor': COLORS['light'],
            'cursor': 'pointer'
        },
        'TAB_SELECTED': {
            'borderTop': '1px solid #d6d6d6',
            'borderBottom': '1px solid #d6d6d6',
            'backgroundColor': COLORS['white'],
            'color': COLORS['primary'],
            'padding': '12px 24px',
            'fontWeight': '600'
        },
        'SECTION_DIVIDER': {
            'borderBottom': f"1px solid {COLORS['border']}",
            'paddingBottom': '20px',
            'marginBottom': '20px'
        }
    }

def create_section_header(title):
    """Create a consistent section header"""
    return html.H3(title, style={
        'color': COLORS['dark'],
        'fontSize': '18px',
        'fontWeight': '600',
        'margin': '0 0 16px 0'
    })

def create_connection_section():
    """Create the connection control section"""
    button_styles = get_button_styles()
    styles = get_common_styles()
    
    return html.Div([
        create_section_header("Connection"),
        
        html.Div([
            html.Div([
                html.Label("OSA IP Address", style=styles['LABEL']),
                dcc.Dropdown(
                    id='ip-dropdown',
                    options=[
                        {'label': '10.0.0.20', 'value': '10.0.0.20'},
                        {'label': '10.0.0.21', 'value': '10.0.0.21'}
                    ],
                    value='10.0.0.21'
                )
            ], style={'marginBottom': '12px'}),
            
            html.Div([
                html.Button('Start OSA', id='toggle-btn', n_clicks=0, 
                           style={**button_styles['SUCCESS'], 'width': '100%'}),
                html.Div(id='status', style={
                    'marginTop': '8px',
                    'fontSize': '14px',
                    'fontWeight': '500',
                    'color': COLORS['muted'],
                    'textAlign': 'center'
                })
            ])
        ])
    ], style=styles['SECTION_DIVIDER'])

def create_scan_mode_section():
    """Create the scan mode control section"""
    styles = get_common_styles()
    
    return html.Div([
        create_section_header("Scan Mode"),
        
        html.Div([
            html.Button('Repeat', id='scan-repeat-btn', n_clicks=0, 
                       style={'width': '32%', 'marginRight': '2%'}),
            html.Button('Single', id='scan-single-btn', n_clicks=0, 
                       style={'width': '32%', 'marginRight': '2%'}),
            html.Button('Stop', id='scan-stop-btn', n_clicks=0, 
                       style={'width': '32%'}),
        ], style={'display': 'flex', 'marginBottom': '12px'})
    ], style=styles['SECTION_DIVIDER'])

def create_osa_settings_section():
    """Create the OSA settings section"""
    button_styles = get_button_styles()
    styles = get_common_styles()
    
    return html.Div([
        create_section_header("OSA Settings"),
        
        # Preset Buttons
        html.Div([
            html.Label("Quick Presets", style={**styles['LABEL'], 'marginBottom': '12px'}),
            html.Div([
                html.Button('Fine Octave', id='fine-preset-btn', n_clicks=0, 
                           style={'width': '48%', 'marginRight': '4%'}),
                html.Button('Coarse Octave', id='coarse-preset-btn', n_clicks=0, 
                           style={**button_styles['SECONDARY'], 'width': '48%'}),
            ], style={'display': 'flex', 'marginBottom': '8px'}),
            html.Div(id='preset-status', style={
                'fontSize': '13px',
                'fontWeight': '500',
                'color': COLORS['success'],
                'textAlign': 'center',
                'marginBottom': '16px'
            })
        ]),
        
        # Settings Form
        create_osa_settings_form(button_styles, styles)
    ])

def create_osa_settings_form(button_styles, styles):
    """Create the OSA settings form fields"""
    return html.Div([
        # Row 1: Center Wavelength and Span
        html.Div([
            html.Div([
                html.Label("Center λ (nm)", style={**styles['LABEL'], 'fontSize': '13px'}),
                dcc.Input(id='centwlgth', type='number', value=1550, step=0.1, 
                         style={'width': '100%'})
            ], style={'width': '48%'}),
            html.Div([
                html.Label("Span (nm)", style={**styles['LABEL'], 'fontSize': '13px'}),
                dcc.Input(id='span', type='number', value=100, step=0.1, 
                         style={'width': '100%'})
            ], style={'width': '48%'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '12px'}),
        
        # Row 2: Resolution and Sensitivity
        html.Div([
            html.Div([
                html.Label("Resolution (nm)", style={**styles['LABEL'], 'fontSize': '13px'}),
                dcc.Input(id='resolution', type='number', value=0.02, step=0.01, 
                         style={'width': '100%'})
            ], style={'width': '48%'}),
            html.Div([
                html.Label("Sensitivity", style={**styles['LABEL'], 'fontSize': '13px'}),
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
                    style={'width': '100%'}
                )
            ], style={'width': '48%'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '12px'}),
        
        # Points settings
        html.Div([
            html.Label("Points Mode", style={**styles['LABEL'], 'fontSize': '13px'}),
            dcc.RadioItems(
                id='pts-auto',
                options=[
                    {'label': 'Auto', 'value': True},
                    {'label': 'Manual', 'value': False}
                ],
                value=True,
                inline=True,
                style={'fontSize': '13px', 'color': COLORS['text'], 'marginBottom': '8px'}
            ),
            dcc.Input(id='pts', type='number', value=1001, step=1, min=51, max=50001, 
                     disabled=True, style={'width': '100%'})
        ], style={'marginBottom': '16px'}),
        
        # Apply Button
        html.Button('Apply Settings', id='apply-settings-btn', n_clicks=0, 
                   style={**button_styles['PRIMARY'], 'width': '100%'}),
        html.Div(id='settings-status', style={
            'marginTop': '8px',
            'fontSize': '14px',
            'fontWeight': '500',
            'color': COLORS['success'],
            'textAlign': 'center'
        })
    ])


def create_export_section():
    """Create the data export section"""
    button_styles = get_button_styles()
    styles = get_common_styles()
    
    return html.Div([
        create_section_header("Data Export"),
        
        html.Div([
            # Export type
            html.Div([
                html.Label("Export Type", style=styles['LABEL']),
                dcc.Dropdown(
                    id='export-type',
                    options=[
                        {'label': 'CSV File', 'value': 'csv'},
                        {'label': 'Plotly Server', 'value': 'plotly'}
                    ],
                    value='csv',
                    style={'width': '100%'}
                )
            ], style={'marginBottom': '16px'}),
            
            # Save path
            html.Div([
                html.Label("Save Path", style=styles['LABEL']),
                dcc.Input(id='save-path', type='text', 
                         value='/Users/greg/Desktop/DashExperiment/',
                         style={'width': '100%'})
            ], style={'marginBottom': '16px'}),
            
            # Filename
            html.Div([
                html.Label("Filename", style=styles['LABEL']),
                html.Div([
                    dcc.Input(id='filename', type='text', value='trace_data',
                             style={'width': 'calc(100% - 40px)'}),
                    html.Div(id='file-extension', children='.csv', style={
                        'display': 'inline-block',
                        'fontSize': '14px',
                        'color': COLORS['muted'],
                        'marginLeft': '8px'
                    })
                ], style={'display': 'flex', 'alignItems': 'center'})
            ], style={'marginBottom': '20px'}),
            
            # Buttons
            html.Div([
                html.Button('Save/Upload', id='save-btn', n_clicks=0, 
                           style={**button_styles['PRIMARY'], 'width': '48%', 'marginRight': '4%'}),
                html.Button('Delete from Server', id='delete-btn', n_clicks=0, 
                           style={**button_styles['DANGER'], 'width': '48%', 'display': 'none'})
            ], style={'display': 'flex', 'marginBottom': '16px'}),
            
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
    ], style={'padding': '20px'})


def create_plot_card(fig):
    """Create the plot display card"""
    button_styles = get_button_styles()
    styles = get_common_styles()
    
    return html.Div([
        dcc.Graph(
            id='trace-graph', 
            figure=fig,
            style={'height': 'calc(100vh - 160px)'},
            config=get_graph_config(),
            responsive=True
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
                               style={**button_styles['SUCCESS'], 'marginRight': '8px'}),
                    html.Button('Frequency (THz)', id='frequency-btn', n_clicks=0, 
                               style=button_styles['SECONDARY'])
                ], style={'display': 'flex', 'alignItems': 'center'}),
                
                html.Button('Clear All Annotations', id='clear-annotations-btn', n_clicks=0, 
                           style=button_styles['DANGER'])
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'})
        ], style={'marginTop': '16px'})
    ], style={
        **styles['CARD'],
        'height': 'calc(100vh - 48px)',
        'display': 'flex',
        'flexDirection': 'column',
        'marginBottom': '0'
    })

def get_graph_config():
    """Return the graph configuration"""
    return {
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

def create_sidebar():
    """Create the sidebar with tabs"""
    styles = get_common_styles()
    
    # Controls tab content
    controls_content = html.Div([
        create_connection_section(),
        create_scan_mode_section(),
        create_osa_settings_section()
    ], style={'padding': '20px'})
    
    # Export tab content
    export_content = create_export_section()
    
    return html.Div([
        dcc.Tabs(
            id="sidebar-tabs",
            value='controls-tab',
            style={'height': '100%'},
            children=[
                dcc.Tab(
                    label='Controls',
                    value='controls-tab',
                    style=styles['TAB'],
                    selected_style=styles['TAB_SELECTED'],
                    children=[controls_content]
                ),
                dcc.Tab(
                    label='Data Export',
                    value='export-tab',
                    style=styles['TAB'],
                    selected_style=styles['TAB_SELECTED'],
                    children=[export_content]
                ),
            ]
        )
    ], style={
        'width': '400px',
        'minWidth': '400px',
        'maxWidth': '400px',
        'flexShrink': 0,
        'backgroundColor': COLORS['card'],
        'border': f"1px solid {COLORS['border']}",
        'borderRadius': '12px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.05)',
        'marginRight': '24px',
        'height': 'fit-content',
        'maxHeight': 'calc(100vh - 48px)',
        'overflowY': 'auto',
        'overflowX': 'hidden'
    })

def create_layout(fig):
    """Create and return the modern Dash app layout"""
    return html.Div([
        # Main Container
        html.Div([
            # Left Sidebar
            create_sidebar(),
            
            # Right Content Area - Plot
            html.Div([
                create_plot_card(fig)
            ], style={
                'flex': '1',
                'minWidth': '0',
                'height': 'calc(100vh - 48px)',
                'display': 'flex',
                'flexDirection': 'column'
            })
        ], style={
            'display': 'flex',
            'maxWidth': '100%',
            'width': '100%',
            'height': '100vh',
            'margin': '0',
            'padding': '24px',
            'boxSizing': 'border-box',
            'alignItems': 'stretch'
        }),
        
        # Update Interval
        dcc.Interval(
            id='interval-component',
            interval=10,
            n_intervals=0
        )
        
    ], style={
        'backgroundColor': COLORS['background'],
        'minHeight': '100vh',
        'height': '100vh',
        'overflow': 'hidden',
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        'lineHeight': '1.5'
    })

