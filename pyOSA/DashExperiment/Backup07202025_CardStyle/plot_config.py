import plotly.graph_objs as go
import plotly.io as pio

# Define color schemes
nord = {
    "PolarNight": ["#2e3440", "#3b4252", "#434c5e", "#4c566a"],
    "SnowStorm": ["#d8dee9", "#e5e9f0", "#eceff4"],
    "Frost": ["#8fbcbb", "#88c0d0", "#81a1c1", "#5e81ac"],
    "Aurora": ["#bf616a", "#d08770", "#ebcb8b", "#a3be8c", "#b48ead"]
}

# IBM color palette mock (simplified)
class IBMColors:
    def __init__(self):
        self.palette = {
            "ultramarine": {
                "1": "#e7e9f7",
                "10": "#d1d7f4",
                "20": "#b0bef3",
                "30": "#89a2f6",
                "40": "#648fff",
                "50": "#3c6df0",
                "60": "#3151b7",
                "70": "#2e3f8f",
                "80": "#252e6a",
                "90": "#20214f",
            },
            "blue": {
                "1": "#e1ebf7",
                "10": "#c8daf4",
                "20": "#a8c0f3",
                "30": "#79a6f6",
                "40": "#5392ff",
                "50": "#2d74da",
                "60": "#1f57a4",
                "70": "#25467a",
                "80": "#1d3458",
                "90": "#19273c",
            },
            "cerulean": {
                "1": "#deedf7",
                "10": "#c2dbf4",
                "20": "#95c4f3",
                "30": "#56acf2",
                "40": "#009bef",
                "50": "#047cc0",
                "60": "#175d8d",
                "70": "#1c496d",
                "80": "#1d364d",
                "90": "#1b2834",
            },
            "aqua": {
                "1": "#d1f0f7",
                "10": "#a0e3f0",
                "20": "#71cddd",
                "30": "#00b6cb",
                "40": "#12a3b4",
                "50": "#188291",
                "60": "#17616b",
                "70": "#164d56",
                "80": "#13393e",
                "90": "#122a2e",
            },
            "teal": {
                "1": "#c0f5e8",
                "10": "#8ee9d4",
                "20": "#40d5bb",
                "30": "#00baa1",
                "40": "#00a78f",
                "50": "#008673",
                "60": "#006456",
                "70": "#124f44",
                "80": "#133a32",
                "90": "#122b26",
            },
            "green": {
                "1": "#cef3d1",
                "10": "#89eda0",
                "20": "#57d785",
                "30": "#34bc6e",
                "40": "#00aa5e",
                "50": "#00884b",
                "60": "#116639",
                "70": "#12512e",
                "80": "#123b22",
                "90": "#112c1b",
            },
            "lime": {
                "1": "#d7f4bd",
                "10": "#b4e876",
                "20": "#95d13c",
                "30": "#81b532",
                "40": "#73a22c",
                "50": "#5b8121",
                "60": "#426200",
                "70": "#374c1a",
                "80": "#283912",
                "90": "#1f2a10",
            },
            "yellow": {
                "1": "#fbeaae",
                "10": "#fed500",
                "20": "#e3bc13",
                "30": "#c6a21a",
                "40": "#b3901f",
                "50": "#91721f",
                "60": "#70541b",
                "70": "#5b421a",
                "80": "#452f18",
                "90": "#372118",
            },
            "gold": {
                "1": "#f5e8db",
                "10": "#ffd191",
                "20": "#ffb000",
                "30": "#e39d14",
                "40": "#c4881c",
                "50": "#9c6d1e",
                "60": "#74521b",
                "70": "#5b421c",
                "80": "#42301b",
                "90": "#2f261c",
            },
            "orange": {
                "1": "#f5e8de",
                "10": "#fdcfad",
                "20": "#fcaf6d",
                "30": "#fe8500",
                "40": "#db7c00",
                "50": "#ad6418",
                "60": "#814b19",
                "70": "#653d1b",
                "80": "#482e1a",
                "90": "#33241c",
            },
            "peach": {
                "1": "#f7e7e2",
                "10": "#f8d0c3",
                "20": "#faad96",
                "30": "#fc835c",
                "40": "#fe6100",
                "50": "#c45433",
                "60": "#993a1d",
                "70": "#782f1c",
                "80": "#56251a",
                "90": "#3a201b",
            },
            "red": {
                "1": "#f7e6e6",
                "10": "#fccec7",
                "20": "#ffaa9d",
                "30": "#ff806c",
                "40": "#ff5c49",
                "50": "#e62325",
                "60": "#aa231f",
                "70": "#83231e",
                "80": "#5c1f1b",
                "90": "#3e1d1b",
            },
            "magenta": {
                "1": "#f5e7eb",
                "10": "#f5cedb",
                "20": "#f7aac3",
                "30": "#f87eac",
                "40": "#ff509e",
                "50": "#dc267f",
                "60": "#a91560",
                "70": "#831b4c",
                "80": "#5d1a38",
                "90": "#401a29",
            },
            "purple": {
                "1": "#f7e4fb",
                "10": "#efcef3",
                "20": "#e4adea",
                "30": "#d68adf",
                "40": "#cb71d7",
                "50": "#c22dd5",
                "60": "#9320a2",
                "70": "#71237c",
                "80": "#501e58",
                "90": "#3b1a40",
            },
            "violet": {
                "1": "#ece8f5",
                "10": "#e2d2f4",
                "20": "#d2b5f0",
                "30": "#bf93eb",
                "40": "#b07ce8",
                "50": "#9753e1",
                "60": "#7732bb",
                "70": "#602797",
                "80": "#44216a",
                "90": "#321c4c",
            },
            "indigo": {
                "1": "#e9e8ff",
                "10": "#dcd4f7",
                "20": "#c7b6f7",
                "30": "#ae97f4",
                "40": "#9b82f3",
                "50": "#785ef0",
                "60": "#5a3ec8",
                "70": "#473793",
                "80": "#352969",
                "90": "#272149",
            },
            "gray": {
                "1": "#eaeaea",
                "10": "#d8d8d8",
                "20": "#c0bfc0",
                "30": "#a6a5a6",
                "40": "#949394",
                "50": "#777677",
                "60": "#595859",
                "70": "#464646",
                "80": "#343334",
                "90": "#272727",
            },
            "cool-gray": {
                "1": "#e3ecec",
                "10": "#d0dada",
                "20": "#b8c1c1",
                "30": "#9fa7a7",
                "40": "#8c9696",
                "50": "#6f7878",
                "60": "#535a5a",
                "70": "#424747",
                "80": "#343334",
                "90": "#272727",
            },
            "warm-gray": {
                "1": "#efe9e9",
                "10": "#e2d5d5",
                "20": "#ccbcbc",
                "30": "#b4a1a1",
                "40": "#9e9191",
                "50": "#7d7373",
                "60": "#5f5757",
                "70": "#4b4545",
                "80": "#373232",
                "90": "#2a2626",
            },
            "neutral-white": {
                "1": "#fcfcfc",
                "2": "#f9f9f9",
                "3": "#f6f6f6",
                "4": "#f3f3f3",
            },
            "cool-white": {
                "1": "#fbfcfc",
                "2": "#f8fafa",
                "3": "#f4f7f7",
                "4": "#f0f4f4",
            },
            "warm-white": {
                "1": "#fdfcfc",
                "2": "#fbf8f8",
                "3": "#f9f6f6",
                "4": "#f6f3f3",
            },
            "black": {
                "100": "#000",
            },
            "white": {
                "0": "#fff",
            },
        }

    def _get(self, color, shade):
        shade = str(shade)
        try:
            return self.palette[color][shade]
        except KeyError:
            raise ValueError(f"Invalid shade '{shade}' for color '{color}'")

    def ultramarine(self, shade=50):
        return self._get("ultramarine", shade)

    def blue(self, shade=50):
        return self._get("blue", shade)

    def cerulean(self, shade=50):
        return self._get("cerulean", shade)

    def aqua(self, shade=50):
        return self._get("aqua", shade)

    def teal(self, shade=50):
        return self._get("teal", shade)

    def green(self, shade=50):
        return self._get("green", shade)

    def lime(self, shade=50):
        return self._get("lime", shade)

    def yellow(self, shade=50):
        return self._get("yellow", shade)

    def gold(self, shade=50):
        return self._get("gold", shade)

    def orange(self, shade=50):
        return self._get("orange", shade)

    def peach(self, shade=50):
        return self._get("peach", shade)

    def red(self, shade=50):
        return self._get("red", shade)

    def magenta(self, shade=50):
        return self._get("magenta", shade)

    def purple(self, shade=50):
        return self._get("purple", shade)

    def violet(self, shade=50):
        return self._get("violet", shade)

    def indigo(self, shade=50):
        return self._get("indigo", shade)

    def gray(self, shade=50):
        return self._get("gray", shade)

    def cool_gray(self, shade=50):
        return self._get("cool-gray", shade)

    def warm_gray(self, shade=50):
        return self._get("warm-gray", shade)

    def neutral_white(self, shade=1):
        return self._get("neutral-white", shade)

    def cool_white(self, shade=1):
        return self._get("cool-white", shade)

    def warm_white(self, shade=1):
        return self._get("warm-white", shade)

    def black(self, shade=100):
        return self._get("black", shade)

    def white(self, shade=0):
        return self._get("white", shade)


ibm = IBMColors()

# Create custom template
def setup_plot_template():
    ibm = IBMColors()
    tmplt = pio.templates["plotly_white"].layout
    tmplt.title.update(
        x=0.05,
        font=dict(
            family="IBM Plex Sans Condensed, Open Sans, verdana, arial, sans-serif", size=18
        ),
    )
    tmplt.font.update(
        family="IBM Plex Sans Condensed, Open Sans, verdana, arial, sans-serif",
        color=nord["PolarNight"][0],
    )
    tmplt.xaxis.tickfont.update(family="Decima, Open Sans, verdana, arial, sans-serif")
    tmplt.yaxis.tickfont.update(family="Decima, Open Sans, verdana, arial, sans-serif")
    tmplt.yaxis.title.font.update(
        family="IBM Plex Sans Condensed, Open Sans, verdana, arial, sans-serif", size=16
    )
    tmplt.xaxis.title.font.update(
        family="IBM Plex Sans Condensed, Open Sans, verdana, arial, sans-serif", size=16
    )

    tmplt.yaxis.update(zeroline=False)

    tmplt.xaxis.update(
        showline=True,
        title_standoff=0,
        linecolor=nord["PolarNight"][0],
        linewidth=0.5 / 0.5,
        ticks="outside",
        zeroline=False,
        tickcolor=nord["PolarNight"][0],
        tickwidth=0.5 / 0.5,
        ticklen=2 / 0.5,
    )

    tmplt.yaxis.update(
        showline=True,
        linecolor=nord["PolarNight"][0],
        linewidth=0.5 / 0.5,
        ticks="outside",
        zeroline=False,
        tickcolor=nord["PolarNight"][0],
        tickwidth=0.5 / 0.5,
        ticklen=2 / 0.5,
        title_standoff=0,
        showgrid=False,
    )

    tmplt.xaxis.update(showline=True, showgrid=False)
    tmplt.update(margin_pad=0)

    clrs_nords = [
        "#356BA0",
        "#D18F98",
        "#499E4B",
        "#7181A3",
        "#844A84",
        "#7181A3",
        "#BC394C",
    ]

    clrway_ibm = [
        ibm.cerulean(shade=60),
        ibm.peach(shade=20),
        ibm.violet(shade=50),
        ibm.green(shade=20),
        ibm.red(shade=60),
        ibm.gold(shade=30),
        ibm.blue(shade=50),
        ibm.teal(shade=40),
        ibm.purple(shade=50),  
    ]

    pio.templates["nord"] = go.layout.Template(layout_colorway=clrway_ibm, layout=tmplt)
    pio.templates["nord"].data.scatter = [go.Scatter(line_width=1.5)]
    pio.templates["nord"].layout.legend.update(borderwidth=0, font_size=12, tracegroupgap=2)

    # Set the default template
    pio.templates.default = "nord"
    
    return clrway_ibm

def create_osa_figure():
    """Create the main OSA figure with modern styling"""
    clrway_ibm = setup_plot_template()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[], 
        y=[], 
        mode='lines', 
        name='OSA Trace',
        line=dict(width=2, color=clrway_ibm[0]),
        hovertemplate='<b>Wavelength:</b> %{x:.3f} nm<br><b>Power:</b> %{y:.2f} dBm<extra></extra>'
    ))

    fig.update_layout(
        xaxis_title="Wavelength (nm)",
        yaxis_title="Power (dBm)",
        uirevision='constant',  # This preserves zoom/pan state
        template="nord",
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=60, r=40, t=40, b=50),
        font=dict(
            family="IBM Plex Sans Condensed, Open Sans, verdana, arial, sans-serif",
            color=nord["PolarNight"][0]
        ),
        xaxis=dict(
            showgrid=False,
            title_font_size=16,
            tickfont_size=12,
            showspikes=True,
            spikecolor="grey",
            spikesnap="data",
            spikemode="across",
            spikethickness=1
        ),
        yaxis=dict(
            showgrid=False,
            title_font_size=16,
            tickfont_size=12,
            showspikes=True,
            spikecolor="grey",
            spikesnap="data",
            spikemode="across",
            spikethickness=1
        ),
        hovermode='closest',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font_size=12,
            borderwidth=0
        )
    )
    
    return fig

# Export the colors for use in other modules
def get_color_palette():
    return setup_plot_template()
