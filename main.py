import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.path as mpltPath
from pyproj import Proj
import numpy as np
import os
import sys
import time


COLOR_LIST = ['0000ffff', '0100ffff', '0200ffff', '0300ffff', '0400ffff', '0500ffff', '0600ffff', '0700ffff', '0800ffff', '0900ffff', '0a00ffff', '0b00ffff', '0c00ffff', '0d00ffff', '0e00ffff', '0f00ffff', '1000ffff', '1100ffff', '1200ffff', '1300ffff', '1400ffff', '1500ffff', '1600ffff', '1700ffff', '1800ffff', '1900ffff', '1a00ffff', '1b00ffff', '1c00ffff', '1d00ffff', '1e00ffff', '1f00ffff', '2000ffff', '2100ffff', '2200ffff', '2300ffff', '2400ffff', '2500ffff', '2600ffff', '2700ffff', '2800ffff', '2900ffff', '2a00ffff', '2b00ffff', '2c00ffff', '2d00ffff', '2e00ffff', '2f00ffff', '3000ffff', '3100ffff', '3200ffff', '3300ffff', '3400ffff', '3500ffff', '3600ffff', '3700ffff', '3800ffff', '3900ffff', '3a00ffff', '3b00ffff', '3c00ffff', '3d00ffff', '3e00ffff', '3f00ffff', '4000ffff', '4100ffff', '4200ffff', '4300ffff', '4400ffff', '4500ffff', '4600ffff', '4700ffff', '4800ffff', '4900ffff', '4a00ffff', '4b00ffff', '4c00ffff', '4d00ffff', '4e00ffff', '4e00feff', '4e00fdff', '4e00fcff', '4e00fbff', '4e00faff', '4e00f9ff', '4e00f8ff', '4e00f7ff', '4e00f6ff', '4e00f5ff', '4e00f4ff', '4e00f3ff', '4e00f2ff', '4e00f1ff', '4e00f0ff', '4e00efff', '4e00eeff', '4e00edff', '4e00ecff', '4e00ebff', '4e00eaff', '4e00e9ff', '4e00e8ff', '4e00e7ff', '4e00e6ff', '4e00e5ff', '4e00e4ff', '4e00e3ff', '4e00e2ff', '4e00e1ff', '4e00e0ff', '4e00dfff', '4e00deff', '4e00ddff', '4e00dcff', '4e00dbff', '4e00daff', '4e00d9ff', '4e00d8ff', '4e00d7ff', '4e00d6ff', '4e00d5ff', '4e00d4ff', '4e00d3ff', '4e00d2ff', '4e00d1ff', '4e00d0ff', '4e00cfff', '4e00ceff', '4e00cdff', '4e00cbff', '4e00caff', '4e00c9ff', '4e00c8ff', '4e00c7ff', '4e00c6ff', '4e00c5ff', '4e00c4ff', '4e00c3ff', '4e00c2ff', '4e00c1ff', '4e00c0ff', '4e00bfff', '4e00beff', '4e00bdff', '4e00bcff', '4e00bbff', '4e00baff', '4e00b9ff', '4e00b8ff', '4e00b7ff', '4e00b6ff', '4e00b5ff', '4e00b4ff', '4e00b3ff', '4e00b2ff', '4e00b1ff', '4e00b0ff', '4e00afff', '4e00aeff', '4e00adff', '4e00acff', '4e00abff', '4e00aaff', '4e00a9ff', '4e00a8ff', '4e00a7ff', '4e00a6ff', '4e00a5ff', '4e00a4ff', '4e00a3ff', '4e00a2ff', '4e00a1ff', '4e00a0ff', '4e009fff', '4e009eff', '4e009dff', '4e009cff', '4e009bff', '4e0099ff', '4e0098ff', '4e0097ff', '4e0096ff', '4e0095ff', '4e0094ff', '4e0093ff', '4e0092ff', '4e0091ff', '4e0090ff', '4e008fff', '4e008eff', '4e008dff', '4e008cff', '4e008bff', '4e008aff', '4e0089ff', '4e0088ff', '4e0087ff', '4e0086ff', '4e0085ff', '4e0084ff', '4e0083ff', '4e0082ff', '4e0081ff', '4e0080ff', '4e007fff', '4e007eff', '4e007dff', '4e007cff', '4e007bff', '4e007aff', '4e0079ff', '4e0078ff', '4e0077ff', '4e0076ff', '4e0075ff', '4e0074ff', '4e0073ff', '4e0072ff', '4e0071ff', '4e0070ff', '4e006fff', '4e006eff', '4e006dff', '4e006cff', '4e006bff', '4e006aff', '4e0069ff', '4e0068ff', '4e0066ff', '4e0065ff', '4e0064ff', '4e0063ff', '4e0062ff', '4e0061ff', '4e0060ff', '4e005fff', '4e005eff', '4e005dff', '4e005cff', '4e005bff', '4e005aff', '4e0059ff', '4e0058ff', '4e0057ff', '4e0056ff', '4e0055ff', '4e0054ff', '4e0053ff', '4e0052ff', '4e0051ff', '4e0050ff', '4e004fff', '4e004eff', '4e004dff', '4e004cff', '4e004bff', '4e004aff', '4e0049ff', '4e0048ff', '4e0047ff', '4e0046ff', '4e0045ff', '4e0044ff', '4e0043ff', '4e0042ff', '4e0041ff', '4e0040ff', '4e003fff', '4e003eff', '4e003dff', '4e003cff', '4e003bff', '4e003aff', '4e0039ff', '4e0038ff', '4e0037ff', '4e0036ff', '4e0035ff', '4e0033ff', '4e0032ff', '4e0031ff', '4e0030ff', '4e002fff', '4e002eff', '4e002dff', '4e002cff', '4e002bff', '4e002aff', '4e0029ff', '4e0028ff', '4e0027ff', '4e0026ff', '4e0025ff', '4e0024ff', '4e0023ff', '4e0022ff', '4e0021ff', '4e0020ff', '4e001fff', '4e001eff', '4e001dff', '4e001cff', '4e001bff', '4e001aff', '4e0019ff', '4e0018ff', '4e0017ff', '4e0016ff', '4e0015ff', '4e0014ff', '4e0013ff', '4e0012ff', '4e0011ff', '4e0010ff', '4e000fff', '4e000eff', '4e000dff', '4e000cff', '4e000bff', '4e000aff', '4e0009ff', '4e0008ff', '4e0007ff', '4e0006ff', '4e0005ff', '4e0004ff', '4e0003ff', '4e0002ff', '4e0000ff', '4e0000fe', '4e0100fc', '4e0200fa', '4e0200f9', '4e0300f7', '4e0400f5', '4e0400f4', '4e0500f2', '4e0600f0', '4e0600ee', '4e0700ed', '4e0800eb', '4e0800e9', '4e0900e8', '4e0a00e6', '4e0a00e4', '4e0b00e3', '4e0c00e1', '4e0c00df', '4e0d00dd', '4e0e00dc', '4e0e00da', '4e0f00d8', '4e1000d7', '4e1100d5', '4e1100d3', '4e1200d2', '4e1300d0', '4e1300ce', '4e1400cc', '4e1500cb', '4e1500c9', '4e1600c7', '4e1700c6', '4e1700c4', '4e1800c2', '4e1900c1', '4e1900bf', '4e1a00bd', '4e1b00bb', '4e1b00ba', '4e1c00b8', '4e1d00b6', '4e1d00b5', '4e1e00b3', '4e1f00b1', '4e1f00b0', '4e2000ae', '4e2100ac', '4e2200aa', '4e2200a9', '4e2300a7', '4e2400a5', '4e2400a4', '4e2500a2', '4e2600a0', '4e26009f', '4e27009d', '4e28009b', '4e28009a', '4e290098', '4e2a0096', '4e2a0094', '4e2b0093', '4e2c0091', '4e2c008f', '4e2d008e', '4e2e008c', '4e2e008a', '4e2f0089', '4e300087', '4e300085', '4e310083', '4e320082', '4e330080', '4e33007e', '4e34007d', '4e35007b', '4e350079', '4e360077', '4e370076', '4e370074', '4e380072', '4e390071', '4e39006f', '4e3a006d', '4e3b006c', '4e3b006a', '4e3c0068', '4e3d0066', '4e3d0065', '4e3e0063', '4e3f0061', '4e3f0060', '4e40005e', '4e41005c', '4e41005b', '4e420059', '4e430057', '4e440055']

MIN_SCALE = 0
LEVELS = 400
VARIABLE = 'Odor'
NAME = 'Prova'
ZONE = '32'
PROJIN = 'utm'
PROJOUT = 'WGS84'
STATIC = False
MAX_SCALE = 130
X_COL = 'x_km'
Y_COL = 'y_km'
VAL_COL = 'value'
SCALE = 1
BASE = None
Y_SHIFT = 0
X_SHIFT = 0
X_SCALE_FACTOR = 1
Y_SCALE_FACTOR = 1

def resourcePath(relativePath):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

class poligoni:
    def __init__(self, level):
        self.level = level
        self.poligono = []

def inside(poly, point):
    """
    Checks if a point is inside a polygon.

    Args:
        poly : list of (x,y) pairs defining the polygon
        point : (x,y) pair defining the point

    Returns:
        bool : True if point is inside polygon, False otherwise
    """
    path = mpltPath.Path(poly)
    return path.contains_point(point)

def load_csv_file_conf(csv_file):
    """
    Reads a CSV file and returns a dataframe.
    """
    with open(csv_file, 'r') as csv_f:
        content = csv_f.readlines()
        dataframe = []
    for i,line in enumerate(content):
        if X_COL in line or X_COL.upper() in line or X_COL.capitalize() in line:
            start = i
            break
    for line in content[start:]:
        line = line.strip()
        if line:
            # Normalize column names to standard format (case-insensitive)
            line = (line.replace(X_COL, 'x_km').replace(X_COL.lower(), 'x_km')
                       .replace(X_COL.upper(), 'x_km').replace(X_COL.capitalize(), 'x_km'))
            line = (line.replace(Y_COL, 'y_km').replace(Y_COL.lower(), 'y_km')
                       .replace(Y_COL.upper(), 'y_km').replace(Y_COL.capitalize(), 'y_km'))
            line = (line.replace(VAL_COL, 'value').replace(VAL_COL.lower(), 'value')
                       .replace(VAL_COL.upper(), 'value').replace(VAL_COL.capitalize(), 'value'))
            dataframe.append(line.split(',')[:])
    dataframe = pd.DataFrame(dataframe[1:], columns=dataframe[0])
    for column in dataframe.columns:
        dataframe[column] = dataframe[column].astype(float)
    if SCALE != 1:
        dataframe['value'] = dataframe['value'] * SCALE
    return dataframe

def dataframe_contures(dataframe):
    """
    Creates a graph from a dataframe.
    """
    X = dataframe['x_km'][:]
    unique_x = sorted(list(set(X)))
    Y = dataframe['y_km'][:]
    unique_y = sorted(list(set(Y)))
    Z = np.array(dataframe['value'][:])
    if X[0] == X[1]:
        Z = Z.reshape(len(unique_x), len(unique_y))
        Z = Z.T
    else:
        Z = Z.reshape(len(unique_y), len(unique_x))
    Z[0,:] = 0
    Z[:,0] = 0
    Z[-1,:] = 0
    Z[:,-1] = 0
    list_x =  sorted(X.unique())
    list_y =  sorted(Y.unique())
    cs = plt.contour(unique_x, unique_y, Z, LEVELS)
    all_data = []
    
    # Use allsegs which works across matplotlib versions
    for i, level in enumerate(cs.levels):
        pol = poligoni(level)
        for seg in cs.allsegs[i]:
            if len(seg) > 0:
                # Vectorized conversion - much faster
                x = seg[:,0]
                y = seg[:,1]
                dec_coords = converter_UTM_DEC(x, y)
                poligon = list(zip(dec_coords[0], dec_coords[1]))
                pol.poligono.append(poligon)
        all_data.append(pol)
    
    plt.close()
    return all_data, list_x, list_y

# Cache Proj object for better performance
_proj_cache = {}

def get_proj():
    """Get cached Proj object."""
    key = (PROJIN, ZONE, PROJOUT)
    if key not in _proj_cache:
        _proj_cache[key] = Proj(proj=PROJIN, zone=ZONE, ellps=PROJOUT)
    return _proj_cache[key]

def converter_UTM_DEC(utm_x, utm_y):
    """
    Converts UTM coordinates to DEC coordinates.
    Supports both single values and arrays.
    """
    p = get_proj()
    
    # Handle arrays or single values
    is_array = hasattr(utm_x, '__iter__') and not isinstance(utm_x, str)
    
    if PROJIN.lower() == 'utm':
        if is_array:
            dec_x, dec_y = p(np.array(utm_x) * 1000, np.array(utm_y) * 1000, inverse=True)
        else:
            dec_x, dec_y = p(float(utm_x) * 1000, float(utm_y) * 1000, inverse=True)
    else:
        if is_array:
            dec_x, dec_y = p(np.array(utm_x), np.array(utm_y), inverse=True)
        else:
            dec_x, dec_y = p(float(utm_x), float(utm_y), inverse=True)
    
    return dec_x, dec_y

def dataframe_manipulation(dataframe):
    """
    Takes a dataframe and returns a dataframe with the data manipoled.

    Args:
        dataframe : dataframe containing the data

    Returns:
        dataframe : dataframe 
    """
    # Sort by value 
    dataframe['value'] = dataframe['value'].astype(float)
    dataframe = dataframe.sort_values(by=['value'], ascending=True)
    dataframe.reset_index(drop=True, inplace=True)
    
    # Vectorized conversion - much faster than list comprehension
    dec_coords = converter_UTM_DEC(dataframe['x_km'].values, dataframe['y_km'].values)
    dataframe['dec_x'] = dec_coords[0]
    dataframe['dec_y'] = dec_coords[1]
    
    dataframe.drop(['x_km', 'y_km'], axis=1, inplace=True)
    return dataframe

def write_first_chunk(kml_f, lim):
    """
    Writes the first chunk of the KML file.

    Args:
        kml_f : file to write the KML to
        lim : limit of the dataframe
    """
    kml_f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    kml_f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    kml_f.write('<Document id="root_doc">\n')
    kml_f.write(f'<Schema name="{NAME}" id="{NAME}">\n')
    kml_f.write('<SimpleField name="Primary" type="string"></SimpleField>\n')
    kml_f.write('<SimpleField name="Secondary" type="string"></SimpleField>\n')
    kml_f.write('<SimpleField name="ID3" type="string"></SimpleField>\n')
    kml_f.write('<SimpleField name="ID4" type="string"></SimpleField>\n')
    kml_f.write('<SimpleField name="ZLEVEL" type="float"></SimpleField>\n')
    kml_f.write('</Schema>\n')
    kml_f.write('\t<Style id=\"failed\">\n')
    kml_f.write('\t<LineStyle>\n')
    kml_f.write('\t\t<color>ff000000</color>\n')
    kml_f.write('\t</LineStyle>\n')
    kml_f.write('\t<PolyStyle>\n')
    kml_f.write('\t\t<color>ff000000</color>\n')
    kml_f.write('\t</PolyStyle>\n')
    kml_f.write('</Style>\n')
    kml_f.write('<Style id="failed0">\n')
    kml_f.write('\t<LineStyle>\n')
    kml_f.write('\t\t<color>ff000000</color>\n')
    kml_f.write('\t</LineStyle>\n')
    kml_f.write('\t<PolyStyle>\n')
    kml_f.write('\t\t<color>ff000000</color>\n')
    kml_f.write('\t</PolyStyle>\n')
    kml_f.write('</Style>\n')
    kml_f.write('<StyleMap id="failed1">\n')
    kml_f.write('	<Pair>\n')
    kml_f.write('		<key>normal</key>\n')
    kml_f.write('		<styleUrl>#failed0</styleUrl>\n')
    kml_f.write('	</Pair>\n')
    kml_f.write('	<Pair>\n')
    kml_f.write('		<key>highlight</key>\n')
    kml_f.write('		<styleUrl>#failed</styleUrl>\n')
    kml_f.write('	</Pair>\n')
    kml_f.write('</StyleMap>\n')
    kml_f.write(f'<Folder><name>{NAME}</name>\n')
    kml_f.write('<Placemark>\n')
    kml_f.write("<name>Receptor's Grid</name>\n")
    kml_f.write('<Style><LineStyle><color>ff000000</color><width>10</width></LineStyle><PolyStyle><color>0000ffff</color><fill>0</fill></PolyStyle></Style>\n')
    kml_f.write(f'<ExtendedData><SchemaData schemaUrl="#{NAME}">\n')
    kml_f.write('<SimpleData name=" Conc(ug/m3)">0</SimpleData>\n')
    kml_f.write('</SchemaData></ExtendedData>\n')
    kml_f.write(f'<MultiGeometry><Polygon><outerBoundaryIs><LinearRing><coordinates>{lim[0]},{lim[2]} {lim[1]},{lim[2]} {lim[1]},{lim[3]} {lim[0]},{lim[3]} {lim[0]},{lim[2]} </coordinates></LinearRing></outerBoundaryIs></Polygon></MultiGeometry>\n')
    kml_f.write('</Placemark>\n')

def a_b(LAST):
    posibi = ['outer', 'inner']
    if LAST == 'outer':
        a = posibi[0]
        b = posibi[1]
    else:
        a = posibi[1]
        b = posibi[0]
    return a, b

def write_middle_chuncks(kml_f, poly_list: list[poligoni]):
    """
    Writes the middle chuncks of the KML file.

    Args:
        kml_f : file to write the KML to
        poly_list : list of polygons to write to the KML file
    """
    MAX_SCALE_DYN = MAX_SCALE if STATIC else max(lev.level for lev in poly_list)
    LAST = 'outer'

    steps = np.linspace(MIN_SCALE, MAX_SCALE_DYN, num=429)
    for i, pol in enumerate(poly_list):
        stop = False
        lev = pol.level
        if lev < MIN_SCALE:
            continue
        ind = min(range(len(steps)), key=lambda i: abs(steps[i] - lev))
        color = COLOR_LIST[-1] if lev >= MAX_SCALE_DYN else COLOR_LIST[ind]
        kml_f.write('<Placemark>\n')
        kml_f.write(f"<name>Level {i + 1}: Conc({VARIABLE})={lev}</name>\n")
        kml_f.write(f'<Style><LineStyle><color>{color}</color><width>1</width></LineStyle><PolyStyle><color>{color}</color><fill>1</fill></PolyStyle></Style>\n')
        kml_f.write(f'<ExtendedData><SchemaData schemaUrl="#{NAME}">\n')
        kml_f.write(f'<SimpleData name=" Conc({VARIABLE})">{lev}</SimpleData>\n')
        kml_f.write('</SchemaData></ExtendedData>\n')
        kml_f.write('<MultiGeometry><Polygon><outerBoundaryIs><LinearRing><coordinates>\n')
        
        LAST = 'outer'

        if i == 0:  
                
            num_pol = len(pol.poligono)
            for j, poligon in enumerate(pol.poligono):
                if j < num_pol - 1 and j > 0:
                    a, b = a_b(LAST)
                    LAST = b                    
                    kml_f.write(f'</coordinates></LinearRing></{a}BoundaryIs></Polygon><Polygon><{b}BoundaryIs><LinearRing><coordinates>')                
                for position in poligon:
                    kml_f.write(f'{position[0]},{position[1]} ')
        
        elif i > 0 and i < len(poly_list) - 1:
            pre = poly_list[i - 1]
            num_pol = len(pre.poligono)
            if num_pol == 1:
                for position in pre.poligono[-1]:
                    kml_f.write(f'{position[0]},{position[1]} ')
                a, b = a_b(LAST)
                LAST = b    
                kml_f.write(f'</coordinates></LinearRing></{a}BoundaryIs></Polygon><Polygon><{b}BoundaryIs><LinearRing><coordinates>')                
                for poligon in pol.poligono:
                    for position in poligon:
                        kml_f.write(f'{position[0]},{position[1]} ')
                    if poligon != pol.poligono[-1]:
                        a, b = a_b(LAST)
                        LAST = b
                        kml_f.write(f'</coordinates></LinearRing></{a}BoundaryIs></Polygon><Polygon><{b}BoundaryIs><LinearRing><coordinates>')
            
            elif num_pol > 1:
                for poligon in pol.poligono:
                    shape_polys = [inside(p, poligon[0]) for p in pre.poligono[:]]
                    if True in shape_polys:
                        index_True = shape_polys.index(True)
                        pre_pol = pre.poligono[index_True]
                        for position in pre_pol:
                            kml_f.write(f'{position[0]},{position[1]} ')
                        a, b = a_b(LAST)
                        LAST = b
                        kml_f.write(f'</coordinates></LinearRing></{a}BoundaryIs></Polygon><Polygon><{b}BoundaryIs><LinearRing><coordinates>')                        
                        for position in poligon:
                            kml_f.write(f'{position[0]},{position[1]} ')
                    if poligon != pol.poligono[-1]:
                        a, b = a_b(LAST)
                        LAST = b
                        kml_f.write(f'</coordinates></LinearRing></{a}BoundaryIs></Polygon><Polygon><{b}BoundaryIs><LinearRing><coordinates>')
        else:
            stop = True

        a, b = a_b(LAST)
        LAST = b
        kml_f.write(f'</coordinates></LinearRing></{a}BoundaryIs></Polygon></MultiGeometry>\n')        
        kml_f.write('</Placemark>\n')
    return MAX_SCALE_DYN

def make_scale(dx, sx, file_name, MAX_SCALE_DYN = MAX_SCALE):
    """
    Makes the scale KML file.

    Args:
        dx : the bottom point of the grid in the x-axis on the right
        sx : the bottom point of the grid in the x-axis on the left
        file_name : the name of the KML scale file
        MAX_SCALE_DYN : the maximum of scale
    """

    list_x = [dx[0] + (sx[0]- dx[0])*(i/50) + X_SHIFT for i in range(51)]
    list_y = [dx[1] + (sx[1]- dx[1])*(i/50) + Y_SHIFT for i in range(51)]
    mx = sum(list_x)/len(list_x)

    list_x = [mx + (i-mx)* X_SCALE_FACTOR for i in list_x]

    list_y_up = [y - 0.00124488953312607 for y in list_y]
    list_y_down = [y - 0.00124488953312607 for y in list_y_up]

    list_y_mean = [(i+j)/2 for i,j in zip(list_y_up, list_y_down)]
    list_y_up = [ my + (i-my) * Y_SCALE_FACTOR for i, my in zip(list_y_up, list_y_mean)]
    list_y_down = [ my + (i-my) * Y_SCALE_FACTOR for i, my in zip(list_y_down, list_y_mean)]

    strings = []
    for i in range(50):
        point_1 = f'{list_x[i+1]},{list_y_down[i+1]},0' 
        point_5 = '\t\t\t\t' + point_1
        point_2 = f'\t\t\t\t{list_x[i]},{list_y_down[i]},0' 
        point_3 = f'\t\t\t\t{list_x[i]},{list_y_up[i]},0' 
        point_4 = f'\t\t\t\t{list_x[i+1]},{list_y_up[i+1]},0'  
        points = [point_1, point_2, point_3, point_4, point_5]
        stringa = '\n'.join(points)
        strings.append(stringa)
        
    with open(os.path.join('configurations', 'scale_new_new_color.txt'), 'r') as f:
        base = f.read()
    for i, stringo in enumerate(strings):
        base = base.replace(f'[coord_{i}]', stringo)

    list_point_x = [dx[0] + (sx[0]- dx[0])*(i/6) + X_SHIFT for i in range(7)]
    mx = sum(list_point_x)/len(list_point_x)
    list_point_x = [mx + (i-mx)* X_SCALE_FACTOR for i in list_point_x]

    list_point_y = [dx[1] + (sx[1]- dx[1])*(i/6) + Y_SHIFT for i in range(7)]
    list_point_y = [y - 0.00124488953312607*3 for y in list_point_y]
    my = sum(list_point_y)/len(list_point_y)
    list_point_y = [my + (i-my)* Y_SCALE_FACTOR for i in list_point_y]

    #arry of values from min to max
    list_values = [value(MAX_SCALE_DYN,MIN_SCALE,i) for i in range(7)]
    #list_values = [round(i*(MAX_SCALE_DYN/6),6) for i in range(7)]
    for i in range(7):
        val = str(list_values[i])
        val = float(val)
        #scientific notation if the value is too big or too small
        val = f'{val:.2e}' if val > 99 or val < 0.1 else f'{val:.2f}'
        val = str(val)
        val = val.replace('e+00', '')
        #if val ends with 0, remove it
        if val[-3:-1] == '.00':
            val = val[:-3]
        if i == 6:
            mid = ''
            if STATIC:
                mid = '>= '
            val = mid + val
        base = base.replace(f'[val_{i}]', val)
        point_str = f'{list_point_x[i]}, {list_point_y[i]}, 0'
        base = base.replace(f'[point_{i}]', point_str)
    base = base.replace("[name_file]", os.path.basename(file_name).replace('.kml', '_scale.kml'))
    scale_name = str(file_name).replace('.kml', '_scale.kml')
    with open(scale_name, 'w') as f:
        f.write(base)

def value(max,min,i):
    return round(min + (max - min)*(i/6),6)

def from_csv_to_kml_configurated(csv_file, configuration, kml_file_name =None):
    """
    Reads a CSV file and writes a KML file.

    Args:
        csv_file : the CSV file to read
        kml_file : the KML file to write
    """
    global LEVELS
    global VARIABLE
    global NAME 
    global ZONE
    global PROJIN
    global PROJOUT
    global STATIC
    global MAX_SCALE  
    global MIN_SCALE  
    global X_COL
    global Y_COL
    global VAL_COL
    global SCALE 
    global BASE
    global X_SHIFT
    global Y_SHIFT
    global X_SCALE_FACTOR
    global Y_SCALE_FACTOR


    LEVELS = configuration[0]
    VARIABLE = configuration[1]
    ZONE= configuration[2]
    PROJIN = configuration[3]
    PROJOUT = configuration[4]
    STATIC = configuration[5]
    MAX_SCALE = configuration[6]
    MIN_SCALE = configuration[7]
    X_COL = configuration[8]
    Y_COL = configuration[9]
    VAL_COL = configuration[10]
    SCALE = configuration[11]
    BASE = configuration[12]
    X_SHIFT = configuration[13]
    Y_SHIFT = configuration[14]
    X_SCALE_FACTOR = configuration[15]
    Y_SCALE_FACTOR = configuration[16]

    get_proj()
    
    NAME = os.path.basename(csv_file).split('.')[0]
    if BASE is None:
        kml_file = csv_file.lower().replace('.csv', '.kml')
    else:
        kml_file = os.path.join(BASE, os.path.basename(csv_file).lower().replace('.csv', '.kml'))

    timestap = time.time()
    kml_file = kml_file.replace('.kml', f'_{int(timestap)}.kml')
    dataframe = load_csv_file_conf(csv_file)
    poly, list_x, list_y = dataframe_contures(dataframe)
    dataframe = dataframe_manipulation(dataframe)
    lim = [dataframe['dec_x'].min(), dataframe['dec_x'].max(), dataframe['dec_y'].min(), dataframe['dec_y'].max()]
    e_ne = (lim[0],lim[2]) 
    e_nw = (lim[1],lim[2])
    
    if kml_file_name:
        kml_file = kml_file_name

    with open(kml_file, 'w') as kml_f:
        write_first_chunk(kml_f, lim)
        MAX_SCALE_DYN = write_middle_chuncks(kml_f, poly)
        kml_f.write('</Folder>\n')
        kml_f.write('</Document>')
        kml_f.write('</kml>\n')

    make_scale(e_ne, e_nw, kml_file, MAX_SCALE_DYN)
