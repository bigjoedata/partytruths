import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

def set_styles(df):
    table_styles = [
        dict(
            selector="table",
            props=[("font-size", "150%"), ("text-align", "center"), ("color", "red")],
        ),
        dict(selector="caption", props=[("caption-side", "bottom")]),
    ]
    return (
        df.style.set_table_styles(table_styles)
        .set_properties(**{"background-color": "blue", "color": "white"})
        .set_caption("This is a caption")
    )

def writecss():
    st.markdown(
    """
<style>
.reportview-container .markdown-text-container {
    font-family: Arial, Helvetica, sans-serif;
}
.sidebar .sidebar-content {
    background-image: linear-gradient(#f0f0ff,#000000);
    color: white;
}
.Widget>label {
    color: white;
    font-family: monospace;
}
[class^="st-b"]  {
    color: white;
    font-family: monospace;
}
.st-bb {
    background-color: transparent;
}
.st-at {
    background-color: #f1f0ff;
}
footer {
    font-family: monospace;
}
.reportview-container .main footer, .reportview-container .main footer a {
    color: #0c0080;
}
header .decoration {
    background-image: none;
}

</style>
""",
    unsafe_allow_html=True,
)

def reduce_mem_usage(df):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.        
    """
    start_mem = df.memory_usage().sum() / 1024**2
    #print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2
    #print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    #print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    return df

def import_data(file):
    """create a dataframe and optimize its memory usage"""
    df = pd.read_csv(file, parse_dates=True, keep_date_col=True)
    df = reduce_mem_usage(df)
    return df

def sideshift(df, shift):
    cols = df.columns.tolist()
    cols = cols[-shift:] + cols[:-shift]
    df = df[cols]
    return df

def unpivoter(df, idv):
    df1 = df.melt(id_vars=inv, var_name='vars', value_name='value').dropna()
    return df1


def lagcols(df, laggards, lagyrs):
    if lagyrs > 0:
        for lag in laggards:
            df[lag] = df[lag].shift(lagyrs)
        df = df.iloc[lagyrs:]
    return df


def cattoobj(df):
    carvars = df.select_dtypes(include='category').columns.tolist()
    for column_name in carvars:
        try:
            df[column_name] = df[column_name].astype('object')
        except KeyError:
            pass
    return df


def numtofloat64(df):
    mVarNames = df.select_dtypes(include=np.number).columns.tolist()
    for column_name in mVarNames:
        try:
            df[column_name] = df[column_name].astype(np.float64)
        except KeyError:
            pass
    return df


def getKeysByValues(dictOfElements, listOfValues):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] in listOfValues:
            listOfKeys.append(item[0])
    return  listOfKeys 


def MergeDict(dict1, dict2): 
    res = {**dict1, **dict2} 
    return res 


# @st.cache
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


def truncate_time(dt_time,period = 3600):
    '''
    Given a period in minute truncates the datetime to the nearest lowest divisor for that minute:
    For Example: 
    Given dt_time='2020-03-27 02:32:19.684443' and period = 5 the function returns '2020-03-27 02:30:00.0'
    Given dt_time='2020-03-27 02:35:19.684443' and period = 5 the function returns '2020-03-27 02:35:00.0'
    '''

    # 1. Find nearest floor of minute to the current time minute
    new_minute_part = math.floor(dt_time.minute/period)*period

    # 2. Replace minute part in curr_time with nearest floored down minute 
    dt_time = dt_time.replace(minute=new_minute_part,second=0, microsecond=0)
    return dt_time

def load_quandl(quandlCodes, qcolumns):
    quandl.ApiConfig.api_key = QUANDL_API_KEY
    mydata=quandl.get(quandlCodes, paginate=True)
    mydata.columns = qcolumns
    mydata = mydata.dropna(axis=1, how='all')
    mydata = mydata.sort_index()
    mydata['dateYear']=mydata.index.year.astype(int)
    mydata = mydata.groupby(mydata.index.year).mean()
    mydata.index = mydata['dateYear']
    mydata = numtofloat64(mydata)
    return mydata

def custom1_theme():
    font = "IBM Plex Mono"
    primary_color = "#F63366"
    font_color = "#262730"
    grey_color = "#f0f2f6"
    base_size = 16
    lg_font = base_size * 1.25
    sm_font = base_size * 0.8  # st.table size
    xl_font = base_size * 1.75

    config = {
        "config": {
            "arc": {"fill": primary_color},
            "area": {"fill": primary_color},
            "circle": {"fill": primary_color, "stroke": font_color, "strokeWidth": 0.5},
            "line": {"stroke": primary_color},
            "path": {"stroke": primary_color},
            "point": {"stroke": primary_color},
            "rect": {"fill": primary_color},
            "shape": {"stroke": primary_color},
            "symbol": {"fill": primary_color},
            "title": {
                "font": font,
                "color": font_color,
                "fontSize": lg_font,
                "anchor": "start",
            },
            "axis": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
                "gridColor": grey_color,
                "domainColor": font_color,
                "tickColor": "#fff",
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": base_size,
                "titleFontSize": base_size,
            },
            "legend": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
            },
            "range": {
                "category": [
                    "#0068c9",
                    "#f63366",
                    "#fffd80",
                    "#7c61b0",
                    "#ffd37b",
                    "#ae5897",
                    "#ffa774",
                    "#d44a7e",
                    "#fd756d",
                ],
                "diverging": [
                    "#850018",
                    "#cd1549",
                    "#f6618d",
                    "#fbafc4",
                    "#f5f5f5",
                    "#93c5fe",
                    "#5091e6",
                    "#1d5ebd",
                    "#002f84",
                ],
                "heatmap": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ramp": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ordinal": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
            },
        }
    }
    return config

def custom2_theme():
    font = "IBM Plex Mono"
    primary_color = "#F63366"
    font_color = "#262730"
    grey_color = "#f0f2f6"
    base_size = 16
    lg_font = base_size * 1.25
    sm_font = base_size * 0.8  # st.table size
    xl_font = base_size * 1.75

    config = {
        "config": {
            "view": {"fill": grey_color},
            "arc": {"fill": primary_color},
            "area": {"fill": primary_color},
            "circle": {"fill": primary_color, "stroke": font_color, "strokeWidth": 0.5},
            "line": {"stroke": primary_color},
            "path": {"stroke": primary_color},
            "point": {"stroke": primary_color},
            "rect": {"fill": primary_color},
            "shape": {"stroke": primary_color},
            "symbol": {"fill": primary_color},
            "title": {
                "font": font,
                "color": font_color,
                "fontSize": lg_font,
                "anchor": "start",
            },
            "axis": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
                "grid": True,
                "gridColor": "#fff",
                "gridOpacity": 1,
                "domain": False,
                # "domainColor": font_color,
                "tickColor": font_color,
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": base_size,
                "titleFontSize": base_size,
            },
            "legend": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
            },
            "range": {
                "category": [
                    "#0068c9",
                    "#f63366",
                    "#fffd80",
                    "#7c61b0",
                    "#ffd37b",
                    "#ae5897",
                    "#ffa774",
                    "#d44a7e",
                    "#fd756d",
                ],
                "diverging": [
                    "#850018",
                    "#cd1549",
                    "#f6618d",
                    "#fbafc4",
                    "#f5f5f5",
                    "#93c5fe",
                    "#5091e6",
                    "#1d5ebd",
                    "#002f84",
                ],
                "heatmap": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ramp": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ordinal": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
            },
        }
    }
    return config

def default_theme():
    font = "Benton Gothic, sans-serif"
    primary_color = "#0000000"
    font_color = "#262730"
    grey_color = "#eeffff"
    base_size = 12
    lg_font = base_size * 1.25
    sm_font = base_size * 0.8  # st.table size
    xl_font = base_size * 1.75

    config = {
        "config": {
            "arc": {"fill": primary_color},
            "area": {"fill": primary_color},
            "circle": {"fill": primary_color, "stroke": font_color, "strokeWidth": 0.5},
            "line": {"stroke": primary_color},
            "path": {"stroke": primary_color},
            "point": {"fill": primary_color, "stroke": primary_color},
            "rect": {"fill": primary_color},
            "shape": {"stroke": primary_color},
            "symbol": {"fill": primary_color},
            "title": {
                "font": font,
                "color": font_color,
                "fontSize": lg_font,
                "anchor": "start",
            },
            "axis": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
                "gridColor": grey_color,
                "domainColor": font_color,
                "tickColor": "#000",
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": sm_font,
                "titleFontSize": sm_font,
            },
            "legend": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
            },
            "range": {
                "category": [
                    "#f63366",
                    "#0068c9",
                    "#fffd80",
                    "#7c61b0",
                    "#ffd37b",
                    "#ae5897",
                    "#ffa774",
                    "#d44a7e",
                    "#fd756d",
                ],
                "diverging": [
                    "#850018",
                    "#cd1549",
                    "#f6618d",
                    "#fbafc4",
                    "#f5f5f5",
                    "#93c5fe",
                    "#5091e6",
                    "#1d5ebd",
                    "#002f84",
                ],
                "heatmap": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ramp": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ordinal": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
            },
        }
    }
    return config


def urban_theme():
    markColor = "#1696d2"
    axisColor = "#000000"
    backgroundColor = "#FFFFFF"
    font = "Lato"
    labelFont = "Lato"
    sourceFont = "Lato"
    gridColor = "#DEDDDD"
    main_palette = ["#1696d2", 
                    "#d2d2d2",
                    "#000000", 
                    "#fdbf11", 
                    "#ec008b", 
                    "#55b748", 
                    "#5c5859", 
                    "#db2b27", 
                   ]
    sequential_palette = ["#cfe8f3", 
                          "#a2d4ec", 
                          "#73bfe2", 
                          "#46abdb", 
                          "#1696d2", 
                          "#12719e", 
                         ]
    return {
        "width": 685,
        "height": 380,   
#        "autosize": "fit",
        "config": {
            "title": {
                "anchor": "start",
                "fontSize": 18,
                "font": font,
                "fontColor": "#000000"
            },
            "axisX": {
               "domain": True,
               "domainColor": axisColor,
               "domainWidth": 1,
               "grid": False,
               "labelFontSize": 12,
               "labelFont": labelFont,
               "labelAngle": 0,
               "tickColor": axisColor,
               "tickSize": 5,
               "titleFontSize": 12,
               "titlePadding": 10,
               "titleFont": font,
               "title": "",
           },
           "axisY": {
               "domain": False,
               "grid": True,
               "gridColor": gridColor,
               "gridWidth": 1,
               "labelFontSize": 12,
               "labelFont": labelFont,
               "labelPadding": 8,
               "ticks": False,
               "titleFontSize": 12,
               "titlePadding": 10,
               "titleFont": font,
               "titleAngle": 0,
               "titleY": -10,
               "titleX": 18,
           },
           "background": backgroundColor,
           "legend": {
               "labelFontSize": 12,
               "labelFont": labelFont,
               "symbolSize": 100,
               "symbolType": "square",
               "titleFontSize": 12,
               "titlePadding": 10,
               "titleFont": font,
               "title": "",
               "orient": "top-left",
               "offset": 0,
           },
           "view": {
               "stroke": "transparent",
           },
           "range": {
               "category": main_palette,
               "diverging": sequential_palette,
           },
           "area": {
               "fill": markColor,
           },
           "line": {
               "color": markColor,
               "stroke": markColor,
               "strokewidth": 5,
           },
           "trail": {
               "color": markColor,
               "stroke": markColor,
               "strokeWidth": 0,
               "size": 1,
           },
           "path": {
               "stroke": markColor,
               "strokeWidth": 0.5,
           },
           "point": {
               "filled": True,
           },
           "text": {
               "font": sourceFont,
               "color": markColor,
               "fontSize": 11,
               "align": "right",
               "fontWeight": 400,
               "size": 11,
            }, 
           "bar": {
                "size": 40,
                "binSpacing": 1,
                "continuousBandSize": 30,
                "discreteBandSize": 30,
                "fill": markColor,
                "stroke": False,
            }, 
       },
    }