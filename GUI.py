from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import threading
from tkinter import Tk, Toplevel, Frame, Label, Entry, Button, Text, StringVar, Canvas
from tkinter import filedialog, messagebox
from tkinter import ttk
from typing import Optional
import json
import os
from datetime import datetime
import numpy as np

from main import from_csv_to_kml_configurated


@dataclass
class AppConfig:
    """Application configuration settings."""
    levels: int = 400
    variable: str = 'Odor'
    zone: str = '32'
    projin: str = 'utm'
    projout: str = 'WGS84'
    static: bool = False
    max_scale: int = 130
    min_scale: int = 0
    x_col: str = 'x_km'
    y_col: str = 'y_km'
    val_col: str = 'value'
    scale: float = 1.0
    base: Optional[str] = None
    x_shift: float = 0.0
    y_shift: float = 0.0
    x_scale_factor: float = 1.0
    y_scale_factor: float = 1.0
    file_list: list[str] = field(default_factory=list)
    config_window_open: bool = False


@dataclass
class SprayConfig:
    """Spray .nc file configuration settings."""
    specie: int = 0  # NO2 = 0, PM10 = 1
    level: int = 0
    tot_specie: int = 4
    cut_map: bool = False
    lat_min: float = 44.371366
    lat_max: float = 44.492199
    lon_min: float = 8.807603
    lon_max: float = 9.039093
    easting_start: int = 484671
    northing_start: int = 4913138
    easting_end: int = 503097
    northing_end: int = 4926569
    zone : str = '32'
    norm_value: bool = False
    cut_date: bool = False
    date: str = '2024-12-17 15:00'
    date_after_good: str = '2024-12-17 15:00'
    colors: str = 'log'  # 'norm' or 'log'
    kml_output: bool = True
    kml_output_dir: str = 'kml_output'
    scale_output: bool = True
    scale_orientation: str = 'vertical'  # 'horizontal' or 'vertical'
    multiplier: float = 1.0
    # KML generation parameters
    kml_levels: int = 400
    kml_variable: str = 'Spray'
    kml_static: bool = False
    kml_max_scale: int = 100
    kml_min_scale: int = 0
    kml_scale: float = 1.0
    kml_x_shift: float = 0.0
    kml_y_shift: float = 0.0
    kml_x_scale_factor: float = 1.0
    kml_y_scale_factor: float = 1.0
    file_list: list[str] = field(default_factory=list)
    spray_config_window_open: bool = False
    kml_config_window_open: bool = False


def show_error(parent: Tk | Toplevel, message: str) -> None:
    """Display an error message dialog."""
    messagebox.showerror("Error", message, parent=parent)


def save_spray_config_to_file(config: SprayConfig, parent: Tk | Toplevel) -> None:
    """Save SprayConfig to a JSON file."""
    filename = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Save Spray Configuration"
    )
    if filename:
        config_dict = {
            'specie': config.specie,
            'level': config.level,
            'tot_specie': config.tot_specie,
            'cut_map': config.cut_map,
            'lat_min': config.lat_min,
            'lat_max': config.lat_max,
            'lon_min': config.lon_min,
            'lon_max': config.lon_max,
            'easting_start': config.easting_start,
            'northing_start': config.northing_start,
            'easting_end': config.easting_end,
            'northing_end': config.northing_end,
            'zone': config.zone,
            'norm_value': config.norm_value,
            'cut_date': config.cut_date,
            'date': config.date,
            'date_after_good': config.date_after_good,
            'colors': config.colors,
            'kml_output': config.kml_output,
            'kml_output_dir': config.kml_output_dir,
            'scale_output': config.scale_output,
            'scale_orientation': config.scale_orientation,
            'multiplier': config.multiplier,
            'kml_levels': config.kml_levels,
            'kml_variable': config.kml_variable,
            'kml_static': config.kml_static,
            'kml_max_scale': config.kml_max_scale,
            'kml_min_scale': config.kml_min_scale,
            'kml_scale': config.kml_scale,
            'kml_x_shift': config.kml_x_shift,
            'kml_y_shift': config.kml_y_shift,
            'kml_x_scale_factor': config.kml_x_scale_factor,
            'kml_y_scale_factor': config.kml_y_scale_factor
        }
        try:
            with open(filename, 'w') as f:
                json.dump(config_dict, f, indent=4)
            messagebox.showinfo("Success", f"Configuration saved to {Path(filename).name}", parent=parent)
        except Exception as e:
            show_error(parent, f"Failed to save configuration: {e}")


def load_spray_config_from_file(config: SprayConfig, parent: Tk | Toplevel, output: Text) -> None:
    """Load SprayConfig from a JSON file."""
    filename = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Load Spray Configuration"
    )
    if filename:
        try:
            with open(filename, 'r') as f:
                config_dict = json.load(f)
            
            config.specie = config_dict.get('specie', 0)
            config.level = config_dict.get('level', 0)
            config.tot_specie = config_dict.get('tot_specie', 4)
            config.cut_map = config_dict.get('cut_map', False)
            config.lat_min = config_dict.get('lat_min', 44.371366)
            config.lat_max = config_dict.get('lat_max', 44.492199)
            config.lon_min = config_dict.get('lon_min', 8.807603)
            config.lon_max = config_dict.get('lon_max', 9.039093)
            config.easting_start = config_dict.get('easting_start', 484671)
            config.northing_start = config_dict.get('northing_start', 4913138)
            config.easting_end = config_dict.get('easting_end', 503097)
            config.northing_end = config_dict.get('northing_end', 4926569)
            config.zone = config_dict.get('zone', '32')
            config.norm_value = config_dict.get('norm_value', False)
            config.cut_date = config_dict.get('cut_date', False)
            config.date = config_dict.get('date', '2024-12-17 15:00')
            config.date_after_good = config_dict.get('date_after_good', '2024-12-17 15:00')
            config.colors = config_dict.get('colors', 'log')
            config.kml_output = config_dict.get('kml_output', True)
            config.kml_output_dir = config_dict.get('kml_output_dir', 'kml_output')
            config.scale_output = config_dict.get('scale_output', True)
            config.scale_orientation = config_dict.get('scale_orientation', 'vertical')
            config.multiplier = config_dict.get('multiplier', 1.0)
            config.kml_levels = config_dict.get('kml_levels', 400)
            config.kml_variable = config_dict.get('kml_variable', 'Spray')
            config.kml_static = config_dict.get('kml_static', False)
            config.kml_max_scale = config_dict.get('kml_max_scale', 100)
            config.kml_min_scale = config_dict.get('kml_min_scale', 0)
            config.kml_scale = config_dict.get('kml_scale', 1.0)
            config.kml_x_shift = config_dict.get('kml_x_shift', 0.0)
            config.kml_y_shift = config_dict.get('kml_y_shift', 0.0)
            config.kml_x_scale_factor = config_dict.get('kml_x_scale_factor', 1.0)
            config.kml_y_scale_factor = config_dict.get('kml_y_scale_factor', 1.0)
            
            output.insert('end', f'Loaded configuration from {Path(filename).name}\n')
            messagebox.showinfo("Success", f"Configuration loaded from {Path(filename).name}", parent=parent)
        except Exception as e:
            show_error(parent, f"Failed to load configuration: {e}")


def process_spray_files(config: SprayConfig, output: Text, root: Tk) -> None:
    """Process .nc spray files and generate KML output using CSV engine."""
    if not config.file_list:
        messagebox.showwarning("No Files", "Please select .nc files to process first", parent=root)
        return
    
    from netCDF4 import Dataset
    from pyproj import Proj, Transformer
    import tempfile
    import pandas as pd
    
    # Create progress window
    total_files = len(config.file_list)
    progress_window = ProgressWindow(root, total_files)
    
    output.insert('end', 'Starting Spray processing...\n')
    root.update()
    
    try:
        for file_idx, file_path in enumerate(config.file_list, 1):
            file_name = Path(file_path).name
            
            output.insert('end', f'Processing {file_name}...\n')
            root.update()
            
            try:
                # Read NetCDF file
                ds = Dataset(file_path)
                concentration = ds.variables['concentration'][:]
                conc_shape = concentration.shape
                
                # Get dimensions
                time_frames = conc_shape[0]
                num_species_total = conc_shape[1]
                num_levels = conc_shape[2]
                nlat = conc_shape[3]
                nlon = conc_shape[4]
                
                # Calculate number of sources
                num_sources = num_species_total // config.tot_specie
                
                # Get lat/lon grid from UTM coordinates
                utm_proj = Proj(proj='utm', zone=int(config.zone), ellps='WGS84')
                geo_proj = Proj(proj='latlong', datum='WGS84')
                transformer = Transformer.from_proj(utm_proj, geo_proj)
                
                lon_start, lat_start = transformer.transform(config.easting_start, config.northing_start)
                lon_end, lat_end = transformer.transform(config.easting_end, config.northing_end)
                
                latitudes = np.linspace(lat_start, lat_end, nlat)
                longitudes = np.linspace(lon_start, lon_end, nlon)
                
                # Create output directory
                os.makedirs(config.kml_output_dir, exist_ok=True)
                
                # Get start time
                start_time = datetime.strptime(config.date, '%Y-%m-%d %H:%M').timestamp()
                good_time = datetime.strptime(config.date_after_good, '%Y-%m-%d %H:%M').timestamp()
                
                # Apply subsetting to lat/lon if needed
                if config.cut_map:
                    lat_inds = [i for i, lat in enumerate(latitudes) if config.lat_min <= lat <= config.lat_max]
                    lon_inds = [j for j, lon in enumerate(longitudes) if config.lon_min <= lon <= config.lon_max]
                    if not lat_inds or not lon_inds:
                        raise ValueError('No grid points found within the specified lat/lon bounds')
                    i_start, i_end = min(lat_inds), max(lat_inds)
                    j_start, j_end = min(lon_inds), max(lon_inds)
                    latitudes = latitudes[i_start:i_end+1]
                    longitudes = longitudes[j_start:j_end+1]
                    lat_slice = slice(i_start, i_end+1)
                    lon_slice = slice(j_start, j_end+1)
                else:
                    lat_slice = slice(None)
                    lon_slice = slice(None)
                
                # Get species indices
                idxs = [config.specie + i * config.tot_specie for i in range(num_sources)]
                
                # Process each time frame
                output.insert('end', f'Processing {time_frames} time frames...\n')
                root.update()
                
                for t in range(time_frames):
                    timestamp = start_time + t * 3600
                    readable_time = datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H%M')
                    
                    # Update progress
                    progress_window.update_progress(file_idx, f'{file_name} - Frame {t+1}/{time_frames}')
                    
                    # Skip if before good time
                    if config.cut_date and timestamp < good_time:
                        continue
                    
                    # Aggregate concentrations from all sources (using same logic as cut_filer_json_kml.py)
                    grid = concentration[t][idxs[0]][config.level][lat_slice, lon_slice].copy()
                    for k in idxs[1:]:
                        grid += concentration[t][k][config.level][lat_slice, lon_slice]
                    
                    lats_subset = latitudes
                    lons_subset = longitudes
                    
                    # Create temporary CSV file with ALL grid points (CSV engine needs complete grid)
                    csv_data = []
                    has_nonzero = False
                    for i in range(len(lats_subset)):
                        for j in range(len(lons_subset)):
                            value = float(grid[i, j]) * config.multiplier
                            if value > 0:
                                has_nonzero = True
                            csv_data.append({
                                'x_km': lons_subset[j],
                                'y_km': lats_subset[i],
                                'value': value
                            })
                    
                    # Skip frames with no data
                    if not has_nonzero:
                        continue
                    
                    # Create temporary CSV file
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp_csv:
                        df = pd.DataFrame(csv_data)
                        df.to_csv(tmp_csv.name, index=False)
                        temp_csv_path = tmp_csv.name
                    
                    try:
                        # Use CSV to KML converter with WGS84 coordinates
                        params = (
                            config.kml_levels,  # levels
                            config.kml_variable,  # variable
                            config.zone,  # zone (not used for latlong)
                            'latlong',  # projin - geographic coordinates
                            'WGS84',  # projout
                            config.kml_static,  # static
                            config.kml_max_scale,  # max_scale
                            config.kml_min_scale,  # min_scale
                            'x_km',  # x_col
                            'y_km',  # y_col
                            'value',  # val_col
                            config.kml_scale,  # scale
                            config.kml_output_dir,  # base output directory
                            config.kml_x_shift,  # x_shift
                            config.kml_y_shift,  # y_shift
                            config.kml_x_scale_factor,  # x_scale_factor
                            config.kml_y_scale_factor   # y_scale_factor
                        )
                        
                        base_name = Path(file_path).stem
                        # Generate KML
                        new_kml =  new_kml = Path(config.kml_output_dir) / f'{base_name}_{config.kml_variable}_{readable_time}.kml'
                        from_csv_to_kml_configurated(temp_csv_path, params, new_kml)
                        

                        
                    finally:
                        # Clean up temporary CSV
                        if os.path.exists(temp_csv_path):
                            os.unlink(temp_csv_path)
                
                ds.close()
                output.insert('end', f'✓ Completed {file_name}\n')
                
            except Exception as e:
                import traceback
                output.insert('end', f'✗ Error in {file_name}: {e}\n')
                output.insert('end', f'{traceback.format_exc()}\n')
            finally:
                root.update()
        
        output.insert('end', 'All Spray files processed!\n')
    finally:
        # Close progress window
        progress_window.close()
        config.file_list.clear()


class ProgressWindow:
    """Progress window with progress bar."""
    def __init__(self, parent: Tk, total_files: int):
        self.window = Toplevel(parent)
        self.window.title("Processing...")
        self.window.geometry("380x190")
        self.window.configure(bg='#1e1e1e')
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (380 // 2)
        y = (self.window.winfo_screenheight() // 2) - (140 // 2)
        self.window.geometry(f'380x140+{x}+{y}')
        
        # Main frame
        main_frame = Frame(self.window, bg='#1e1e1e', padx=18, pady=18)
        main_frame.pack(fill='both', expand=True)
        
        # Title with icon
        self.title_label = Label(
            main_frame,
            text="⚡ Processing Files...",
            font=('Segoe UI', 11, 'bold'),
            fg='#64B5F6',
            bg='#1e1e1e'
        )
        self.title_label.pack(pady=(0, 10))
        
        # Status label
        self.status_label = Label(
            main_frame,
            text="Starting...",
            font=('Segoe UI', 9),
            fg='#B0B0B0',
            bg='#1e1e1e'
        )
        self.status_label.pack(pady=(0, 8))
        
        # Progress bar with custom style
        style = ttk.Style()
        style.configure('Modern.Horizontal.TProgressbar',
                       troughcolor='#333333',
                       background='#42A5F5',
                       borderwidth=0,
                       thickness=6)
        
        self.progress = ttk.Progressbar(
            main_frame,
            mode='determinate',
            style='Modern.Horizontal.TProgressbar',
            length=340,
            maximum=total_files
        )
        self.progress.pack(pady=(0, 8))
        
        # Progress text
        self.progress_text = Label(
            main_frame,
            text="0 / 0",
            font=('Segoe UI', 8, 'bold'),
            fg='#808080',
            bg='#1e1e1e'
        )
        self.progress_text.pack()
        
        self.total_files = total_files
        self.current = 0
    
    def update_progress(self, current: int, filename: str):
        """Update progress bar and status."""
        self.current = current
        self.progress['value'] = current
        self.status_label.config(text=f"Processing: {filename}")
        self.progress_text.config(text=f"{current} / {self.total_files}")
        self.window.update()
    
    def close(self):
        """Close the progress window."""
        self.window.grab_release()
        self.window.destroy()

def collect_data(config: AppConfig, var_data: list[str], window: Toplevel, output: Text) -> None:
    """Collect and validate configuration data from the GUI."""
    try:
        config.levels = int(var_data[0])
    except ValueError:
        show_error(window, 'Levels must be an integer')
        return

    config.variable = var_data[1]
    config.zone = var_data[2]
    config.projin = var_data[3]
    config.projout = var_data[4]
    config.static = var_data[5] == 'True'
    
    if config.static:
        try:
            config.max_scale = int(var_data[6])
        except ValueError:
            show_error(window, 'Max Scale must be an integer')
            return
    
    config.x_col = var_data[7]
    config.y_col = var_data[8]
    config.val_col = var_data[9]
    config.base = var_data[10] if var_data[10] else None
    config.config_window_open = False
    
    window.destroy()
    output.insert('end', 'Loaded Configuration\n')

def open_configuration(root: Tk, config: AppConfig, output: Text) -> None:
    """Open the configuration window."""
    config.config_window_open = True
    config_window = Toplevel(root)
    config_window.title('⚙️ Configuration Settings')
    config_window.geometry("480x580")
    config_window.configure(bg='#1e1e1e')
    config_window.resizable(False, False)
    
    # Main frame with padding
    main_frame = Frame(config_window, bg='#1e1e1e', padx=20, pady=18)
    main_frame.pack(fill='both', expand=True)
    
    # Header with gradient effect simulation
    header_frame = Frame(main_frame, bg='#2d2d2d', height=45)
    header_frame.pack(fill='x', pady=(0, 18))
    header_frame.pack_propagate(False)
    
    title = Label(
        header_frame,
        text="⚙️ Configuration Settings",
        font=('Segoe UI', 12, 'bold'),
        fg='#64B5F6',
        bg='#2d2d2d'
    )
    title.pack(pady=10)

    # Configuration fields with card-like container
    fields_frame = Frame(main_frame, bg='#1e1e1e')
    fields_frame.pack(fill='both', expand=True)
    
    fields = [
        ('Levels:', str(config.levels)),
        ('Variable:', config.variable),
        ('Projection CSV:', config.projin),
        ('TimeZone:', config.zone),
        ('Projection KML:', config.projout),
        ('Static Scale:', str(config.static)),
        ('Max Scale:', str(config.max_scale)),
        ('X Column:', config.x_col),
        ('Y Column:', config.y_col),
        ('Value Column:', config.val_col),
    ]
    
    entries = []
    for idx, (label_text, default_value) in enumerate(fields):
        Label(
            fields_frame, 
            text=label_text,
            font=('Segoe UI', 8, 'bold'),
            fg='#B0B0B0',
            bg='#1e1e1e'
        ).grid(row=idx, column=0, sticky='w', pady=5, padx=(0, 12))
        
        entry = Entry(fields_frame, width=32, font=('Segoe UI', 9),
                     bg='#2d2d2d', fg='#E0E0E0', relief='flat',
                     borderwidth=1, highlightthickness=1,
                     highlightbackground='#3d3d3d', highlightcolor='#42A5F5',
                     insertbackground='#E0E0E0')
        entry.insert(0, default_value)
        entry.grid(row=idx, column=1, sticky='ew', pady=5)
        entries.append(entry)
    
    fields_frame.columnconfigure(1, weight=1)
    
    # Separator
    Frame(main_frame, bg='#3d3d3d', height=1).pack(fill='x', pady=10)
    
    # Folder selection with improved styling
    folder_container = Frame(main_frame, bg='#1e1e1e')
    folder_container.pack(fill='x', pady=(0, 10))
    
    Label(
        folder_container, 
        text='📁 Saving Folder:',
        font=('Segoe UI', 8, 'bold'),
        fg='#B0B0B0',
        bg='#1e1e1e'
    ).pack(anchor='w', pady=(0, 6))
    
    folder_frame = Frame(folder_container, bg='#1e1e1e')
    folder_frame.pack(fill='x')
    
    folder_entry = Entry(folder_frame, width=32, font=('Segoe UI', 9),
                        bg='#2d2d2d', fg='#E0E0E0', relief='flat',
                        borderwidth=1, highlightthickness=1,
                        highlightbackground='#3d3d3d', highlightcolor='#42A5F5',
                        insertbackground='#E0E0E0')
    folder_entry.pack(side='left', fill='x', expand=True, padx=(0, 8))
    
    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_entry.delete(0, 'end')
            folder_entry.insert(0, folder)
        config_window.lift()
        config_window.focus_force()
    
    browse_btn = Button(
        folder_frame, 
        text="Browse",
        command=browse_folder,
        bg='#3d3d3d',
        fg='#E0E0E0',
        font=('Segoe UI', 8, 'bold'),
        relief='flat',
        padx=15,
        pady=6,
        cursor='hand2',
        activebackground='#4d4d4d',
        activeforeground='white'
    )
    browse_btn.pack(side='left')
    
    # Load button with modern styling
    def load_config():
        var_data = [entry.get() for entry in entries] + [folder_entry.get()]
        collect_data(config, var_data, config_window, output)
    
    button_frame = Frame(main_frame, bg='#1e1e1e')
    button_frame.pack(fill='x', pady=(10, 0))
    
    load_btn = Button(
        button_frame, 
        text="✓ Load Configuration",
        command=load_config,
        bg='#388E3C',
        fg='white',
        font=('Segoe UI', 9, 'bold'),
        relief='flat',
        padx=18,
        pady=8,
        cursor='hand2',
        activebackground='#2E7D32',
        activeforeground='white'
    )
    load_btn.pack(side='left', fill='x', expand=True, padx=(0, 6))
    
    cancel_btn = Button(
        button_frame,
        text="Cancel",
        command=lambda: [setattr(config, 'config_window_open', False), config_window.destroy()],
        bg='#3d3d3d',
        fg='#B0B0B0',
        font=('Segoe UI', 9),
        relief='flat',
        padx=15,
        pady=8,
        cursor='hand2',
        activebackground='#4d4d4d',
        activeforeground='#E0E0E0'
    )
    cancel_btn.pack(side='left', padx=(6, 0))
    
    config_window.focus_set()


def open_kml_configuration(root: Tk, config: SprayConfig, output: Text) -> None:
    """Open the KML parameters configuration window for Spray."""
    config.kml_config_window_open = True
    kml_window = Toplevel(root)
    kml_window.title('🎨 KML Generation Settings')
    kml_window.geometry("480x520")
    kml_window.configure(bg='#1e1e1e')
    kml_window.resizable(False, False)
    
    # Main frame with padding
    main_frame = Frame(kml_window, bg='#1e1e1e', padx=20, pady=18)
    main_frame.pack(fill='both', expand=True)
    
    # Header
    header_frame = Frame(main_frame, bg='#2d2d2d', height=45)
    header_frame.pack(fill='x', pady=(0, 18))
    header_frame.pack_propagate(False)
    
    title = Label(
        header_frame,
        text="🎨 KML Generation Settings",
        font=('Segoe UI', 12, 'bold'),
        fg='#81C784',
        bg='#2d2d2d'
    )
    title.pack(pady=10)

    # Configuration fields
    fields_frame = Frame(main_frame, bg='#1e1e1e')
    fields_frame.pack(fill='both', expand=True)
    
    fields = [
        ('Levels:', str(config.kml_levels)),
        ('Variable Name:', config.kml_variable),
        ('Static Scale (True/False):', str(config.kml_static)),
        ('Max Scale:', str(config.kml_max_scale)),
        ('Min Scale:', str(config.kml_min_scale)),
        ('Scale Factor:', str(config.kml_scale)),
        ('X Shift:', str(config.kml_x_shift)),
        ('Y Shift:', str(config.kml_y_shift)),
        ('X Scale Factor:', str(config.kml_x_scale_factor)),
        ('Y Scale Factor:', str(config.kml_y_scale_factor)),
    ]
    
    entries = []
    for idx, (label_text, default_value) in enumerate(fields):
        Label(
            fields_frame, 
            text=label_text,
            font=('Segoe UI', 8, 'bold'),
            fg='#B0B0B0',
            bg='#1e1e1e'
        ).grid(row=idx, column=0, sticky='w', pady=5, padx=(0, 12))
        
        entry = Entry(fields_frame, width=32, font=('Segoe UI', 9),
                     bg='#2d2d2d', fg='#E0E0E0', relief='flat',
                     borderwidth=1, highlightthickness=1,
                     highlightbackground='#3d3d3d', highlightcolor='#81C784',
                     insertbackground='#E0E0E0')
        entry.insert(0, default_value)
        entry.grid(row=idx, column=1, sticky='ew', pady=5)
        entries.append(entry)
    
    fields_frame.columnconfigure(1, weight=1)
    
    # Separator
    Frame(main_frame, bg='#3d3d3d', height=1).pack(fill='x', pady=15)
    
    # Load button
    def load_kml_config():
        try:
            config.kml_levels = int(entries[0].get())
            config.kml_variable = entries[1].get()
            config.kml_static = entries[2].get() == 'True'
            config.kml_max_scale = int(entries[3].get())
            config.kml_min_scale = int(entries[4].get())
            config.kml_scale = float(entries[5].get())
            config.kml_x_shift = float(entries[6].get())
            config.kml_y_shift = float(entries[7].get())
            config.kml_x_scale_factor = float(entries[8].get())
            config.kml_y_scale_factor = float(entries[9].get())
            config.kml_config_window_open = False
            kml_window.destroy()
            output.insert('end', 'Loaded KML Configuration\n')
        except ValueError as e:
            show_error(kml_window, f'Invalid value: {e}')
    
    button_frame = Frame(main_frame, bg='#1e1e1e')
    button_frame.pack(fill='x', pady=(10, 0))
    
    load_btn = Button(
        button_frame, 
        text="✓ Load Configuration",
        command=load_kml_config,
        bg='#388E3C',
        fg='white',
        font=('Segoe UI', 9, 'bold'),
        relief='flat',
        padx=18,
        pady=8,
        cursor='hand2',
        activebackground='#2E7D32',
        activeforeground='white'
    )
    load_btn.pack(side='left', fill='x', expand=True, padx=(0, 6))
    
    cancel_btn = Button(
        button_frame,
        text="Cancel",
        command=lambda: [setattr(config, 'kml_config_window_open', False), kml_window.destroy()],
        bg='#3d3d3d',
        fg='#B0B0B0',
        font=('Segoe UI', 9),
        relief='flat',
        padx=15,
        pady=8,
        cursor='hand2',
        activebackground='#4d4d4d',
        activeforeground='#E0E0E0'
    )
    cancel_btn.pack(side='left', padx=(6, 0))
    
    kml_window.focus_set()


def open_spray_configuration(root: Tk, config: SprayConfig, output: Text) -> None:
    """Open the Spray configuration window."""
    config.spray_config_window_open = True
    config_window = Toplevel(root)
    config_window.title('🌫️ Spray Configuration')
    config_window.geometry("640x580")
    config_window.configure(bg='#1e1e1e')
    config_window.resizable(False, False)
    
    # Main frame with padding
    main_frame = Frame(config_window, bg='#1e1e1e', padx=15, pady=12)
    main_frame.pack(fill='both', expand=True)
    
    # Header - more compact
    header_frame = Frame(main_frame, bg='#2d2d2d', height=38)
    header_frame.pack(fill='x', pady=(0, 10))
    header_frame.pack_propagate(False)
    
    title = Label(
        header_frame,
        text="🌫️ Spray Configuration",
        font=('Segoe UI', 11, 'bold'),
        fg='#64B5F6',
        bg='#2d2d2d'
    )
    title.pack(pady=8)

    # Create scrollable canvas for all fields
    canvas = Canvas(main_frame, bg='#1e1e1e', highlightthickness=0, height=420)
    scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
    fields_container = Frame(canvas, bg='#1e1e1e')
    
    fields_container.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.create_window((0, 0), window=fields_container, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    # Mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    # Organize fields in compact 2-column layout
    entries = []
    
    # Section 1: Data Selection (compact)
    section1 = Frame(fields_container, bg='#1e1e1e')
    section1.pack(fill='x', pady=(0, 8))
    Label(section1, text="📊 Data Selection", font=('Segoe UI', 9, 'bold'), fg='#81C784', bg='#1e1e1e').pack(anchor='w')
    
    grid1 = Frame(section1, bg='#1e1e1e')
    grid1.pack(fill='x', pady=(4, 0))
    
    fields_row1 = [
        ('Specie:', str(config.specie), 0, 0),
        ('Level:', str(config.level), 0, 2),
        ('Total Species:', str(config.tot_specie), 1, 0),
        ('Zone:', str(config.zone), 1, 2),
    ]
    
    for label_text, default_value, row, col in fields_row1:
        Label(grid1, text=label_text, font=('Segoe UI', 7), fg='#B0B0B0', bg='#1e1e1e').grid(row=row, column=col, sticky='w', padx=(0, 4), pady=2)
        entry = Entry(grid1, width=12, font=('Segoe UI', 8), bg='#2d2d2d', fg='#E0E0E0', relief='flat', insertbackground='#E0E0E0')
        entry.insert(0, default_value)
        entry.grid(row=row, column=col+1, sticky='ew', padx=(0, 10), pady=2)
        entries.append(entry)
    
    grid1.columnconfigure(1, weight=1)
    grid1.columnconfigure(3, weight=1)
    
    # Section 2: Map Bounds
    section2 = Frame(fields_container, bg='#1e1e1e')
    section2.pack(fill='x', pady=(0, 8))
    Label(section2, text="🗺️ Map Bounds", font=('Segoe UI', 9, 'bold'), fg='#81C784', bg='#1e1e1e').pack(anchor='w')
    
    grid2 = Frame(section2, bg='#1e1e1e')
    grid2.pack(fill='x', pady=(4, 0))
    
    fields_row2 = [
        ('Cut Map:', str(config.cut_map), 0, 0),
        ('Lat Min:', str(config.lat_min), 0, 2),
        ('Lat Max:', str(config.lat_max), 1, 0),
        ('Lon Min:', str(config.lon_min), 1, 2),
        ('Lon Max:', str(config.lon_max), 2, 0),
    ]
    
    for label_text, default_value, row, col in fields_row2:
        Label(grid2, text=label_text, font=('Segoe UI', 7), fg='#B0B0B0', bg='#1e1e1e').grid(row=row, column=col, sticky='w', padx=(0, 4), pady=2)
        entry = Entry(grid2, width=12, font=('Segoe UI', 8), bg='#2d2d2d', fg='#E0E0E0', relief='flat', insertbackground='#E0E0E0')
        entry.insert(0, default_value)
        entry.grid(row=row, column=col+1, sticky='ew', padx=(0, 10), pady=2)
        entries.append(entry)
    
    grid2.columnconfigure(1, weight=1)
    grid2.columnconfigure(3, weight=1)
    
    # Section 3: UTM Coordinates
    section3 = Frame(fields_container, bg='#1e1e1e')
    section3.pack(fill='x', pady=(0, 8))
    Label(section3, text="📍 UTM Coordinates", font=('Segoe UI', 9, 'bold'), fg='#81C784', bg='#1e1e1e').pack(anchor='w')
    
    grid3 = Frame(section3, bg='#1e1e1e')
    grid3.pack(fill='x', pady=(4, 0))
    
    fields_row3 = [
        ('Easting Start:', str(config.easting_start), 0, 0),
        ('Northing Start:', str(config.northing_start), 0, 2),
        ('Easting End:', str(config.easting_end), 1, 0),
        ('Northing End:', str(config.northing_end), 1, 2),
    ]
    
    for label_text, default_value, row, col in fields_row3:
        Label(grid3, text=label_text, font=('Segoe UI', 7), fg='#B0B0B0', bg='#1e1e1e').grid(row=row, column=col, sticky='w', padx=(0, 4), pady=2)
        entry = Entry(grid3, width=12, font=('Segoe UI', 8), bg='#2d2d2d', fg='#E0E0E0', relief='flat', insertbackground='#E0E0E0')
        entry.insert(0, default_value)
        entry.grid(row=row, column=col+1, sticky='ew', padx=(0, 10), pady=2)
        entries.append(entry)
    
    grid3.columnconfigure(1, weight=1)
    grid3.columnconfigure(3, weight=1)
    
    # Section 4: Time & Processing
    section4 = Frame(fields_container, bg='#1e1e1e')
    section4.pack(fill='x', pady=(0, 8))
    Label(section4, text="⏰ Time & Processing", font=('Segoe UI', 9, 'bold'), fg='#81C784', bg='#1e1e1e').pack(anchor='w')
    
    grid4 = Frame(section4, bg='#1e1e1e')
    grid4.pack(fill='x', pady=(4, 0))
    
    fields_row4 = [
        ('Cut Date:', str(config.cut_date), 0, 0),
        ('Normalize:', str(config.norm_value), 0, 2),
        ('Start Date:', config.date, 1, 0),
        ('After Good:', config.date_after_good, 1, 2),
    ]
    
    for label_text, default_value, row, col in fields_row4:
        Label(grid4, text=label_text, font=('Segoe UI', 7), fg='#B0B0B0', bg='#1e1e1e').grid(row=row, column=col, sticky='w', padx=(0, 4), pady=2)
        entry = Entry(grid4, width=12, font=('Segoe UI', 8), bg='#2d2d2d', fg='#E0E0E0', relief='flat', insertbackground='#E0E0E0')
        entry.insert(0, default_value)
        entry.grid(row=row, column=col+1, sticky='ew', padx=(0, 10), pady=2)
        entries.append(entry)
    
    grid4.columnconfigure(1, weight=1)
    grid4.columnconfigure(3, weight=1)
    
    # Section 5: Output Settings
    section5 = Frame(fields_container, bg='#1e1e1e')
    section5.pack(fill='x', pady=(0, 8))
    Label(section5, text="🎨 Output Settings", font=('Segoe UI', 9, 'bold'), fg='#81C784', bg='#1e1e1e').pack(anchor='w')
    
    grid5 = Frame(section5, bg='#1e1e1e')
    grid5.pack(fill='x', pady=(4, 0))
    
    fields_row5 = [
        ('Colors:', config.colors, 0, 0),
        ('Multiplier:', str(config.multiplier), 0, 2),
        ('KML Output:', str(config.kml_output), 1, 0),
        ('Scale Output:', str(config.scale_output), 1, 2),
        ('Orientation:', config.scale_orientation, 2, 0),
    ]
    
    for label_text, default_value, row, col in fields_row5:
        Label(grid5, text=label_text, font=('Segoe UI', 7), fg='#B0B0B0', bg='#1e1e1e').grid(row=row, column=col, sticky='w', padx=(0, 4), pady=2)
        entry = Entry(grid5, width=12, font=('Segoe UI', 8), bg='#2d2d2d', fg='#E0E0E0', relief='flat', insertbackground='#E0E0E0')
        entry.insert(0, default_value)
        entry.grid(row=row, column=col+1, sticky='ew', padx=(0, 10), pady=2)
        entries.append(entry)
    
    grid5.columnconfigure(1, weight=1)
    grid5.columnconfigure(3, weight=1)
    
    # Output folder - compact inline
    folder_frame = Frame(fields_container, bg='#1e1e1e')
    folder_frame.pack(fill='x', pady=(4, 0))
    
    Label(folder_frame, text='📁 Output:', font=('Segoe UI', 7), fg='#B0B0B0', bg='#1e1e1e').pack(side='left', padx=(0, 4))
    
    folder_entry = Entry(folder_frame, font=('Segoe UI', 8), bg='#2d2d2d', fg='#E0E0E0', relief='flat', insertbackground='#E0E0E0')
    folder_entry.insert(0, config.kml_output_dir)
    folder_entry.pack(side='left', fill='x', expand=True, padx=(0, 4))
    
    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_entry.delete(0, 'end')
            folder_entry.insert(0, folder)
        config_window.lift()
        config_window.focus_force()
    
    Button(folder_frame, text="...", command=browse_folder, bg='#3d3d3d', fg='#E0E0E0', 
           font=('Segoe UI', 7, 'bold'), relief='flat', padx=8, pady=4, cursor='hand2',
           activebackground='#4d4d4d').pack(side='left')
    
    # Load config function
    def load_spray_config():
        try:
            config.specie = int(entries[0].get())
            config.level = int(entries[1].get())
            config.tot_specie = int(entries[2].get())
            config.zone = entries[3].get()
            config.cut_map = entries[4].get() == 'True'
            config.lat_min = float(entries[5].get())
            config.lat_max = float(entries[6].get())
            config.lon_min = float(entries[7].get())
            config.lon_max = float(entries[8].get())
            config.easting_start = int(entries[9].get())
            config.northing_start = int(entries[10].get())
            config.easting_end = int(entries[11].get())
            config.northing_end = int(entries[12].get())
            config.cut_date = entries[13].get() == 'True'
            config.norm_value = entries[14].get() == 'True'
            config.date = entries[15].get()
            config.date_after_good = entries[16].get()
            config.colors = entries[17].get()
            config.multiplier = float(entries[18].get())
            config.kml_output = entries[19].get() == 'True'
            config.scale_output = entries[20].get() == 'True'
            config.scale_orientation = entries[21].get()
            config.kml_output_dir = folder_entry.get()
            config.spray_config_window_open = False
            config_window.destroy()
            output.insert('end', 'Loaded Spray Configuration\n')
        except ValueError as e:
            show_error(config_window, f'Invalid value: {e}')
    
    def update_entries():
        """Update entry fields with current config values."""
        entries[0].delete(0, 'end'); entries[0].insert(0, str(config.specie))
        entries[1].delete(0, 'end'); entries[1].insert(0, str(config.level))
        entries[2].delete(0, 'end'); entries[2].insert(0, str(config.tot_specie))
        entries[3].delete(0, 'end'); entries[3].insert(0, str(config.zone))
        entries[4].delete(0, 'end'); entries[4].insert(0, str(config.cut_map))
        entries[5].delete(0, 'end'); entries[5].insert(0, str(config.lat_min))
        entries[6].delete(0, 'end'); entries[6].insert(0, str(config.lat_max))
        entries[7].delete(0, 'end'); entries[7].insert(0, str(config.lon_min))
        entries[8].delete(0, 'end'); entries[8].insert(0, str(config.lon_max))
        entries[9].delete(0, 'end'); entries[9].insert(0, str(config.easting_start))
        entries[10].delete(0, 'end'); entries[10].insert(0, str(config.northing_start))
        entries[11].delete(0, 'end'); entries[11].insert(0, str(config.easting_end))
        entries[12].delete(0, 'end'); entries[12].insert(0, str(config.northing_end))
        entries[13].delete(0, 'end'); entries[13].insert(0, str(config.cut_date))
        entries[14].delete(0, 'end'); entries[14].insert(0, str(config.norm_value))
        entries[15].delete(0, 'end'); entries[15].insert(0, config.date)
        entries[16].delete(0, 'end'); entries[16].insert(0, config.date_after_good)
        entries[17].delete(0, 'end'); entries[17].insert(0, config.colors)
        entries[18].delete(0, 'end'); entries[18].insert(0, str(config.multiplier))
        entries[19].delete(0, 'end'); entries[19].insert(0, str(config.kml_output))
        entries[20].delete(0, 'end'); entries[20].insert(0, str(config.scale_output))
        entries[21].delete(0, 'end'); entries[21].insert(0, config.scale_orientation)
        folder_entry.delete(0, 'end'); folder_entry.insert(0, config.kml_output_dir)
    
    # Separator
    Frame(main_frame, bg='#3d3d3d', height=1).pack(fill='x', pady=(8, 6))
    
    # Compact button row
    button_frame = Frame(main_frame, bg='#1e1e1e')
    button_frame.pack(fill='x')
    
    Button(button_frame, text="💾 Save", command=lambda: save_spray_config_to_file(config, config_window),
           bg='#1976D2', fg='white', font=('Segoe UI', 8, 'bold'), relief='flat', padx=10, pady=6,
           cursor='hand2', activebackground='#1565C0').pack(side='left', fill='x', expand=True, padx=(0, 3))
    
    Button(button_frame, text="📂 Load", command=lambda: [load_spray_config_from_file(config, config_window, output), update_entries()],
           bg='#5E35B1', fg='white', font=('Segoe UI', 8, 'bold'), relief='flat', padx=10, pady=6,
           cursor='hand2', activebackground='#512DA8').pack(side='left', fill='x', expand=True, padx=(3, 3))
    
    Button(button_frame, text="✓ Apply", command=load_spray_config,
           bg='#388E3C', fg='white', font=('Segoe UI', 8, 'bold'), relief='flat', padx=10, pady=6,
           cursor='hand2', activebackground='#2E7D32').pack(side='left', fill='x', expand=True, padx=(3, 3))
    
    Button(button_frame, text="Cancel", command=lambda: [setattr(config, 'spray_config_window_open', False), config_window.destroy()],
           bg='#3d3d3d', fg='#B0B0B0', font=('Segoe UI', 8, 'bold'), relief='flat', padx=10, pady=6,
           cursor='hand2', activebackground='#4d4d4d').pack(side='left', fill='x', expand=True, padx=(3, 0))
    
    config_window.focus_set()


def main() -> None:
    """Main application entry point."""
    config = AppConfig()
    spray_config = SprayConfig()
    
    root = Tk()
    root.title("CSV & Spray to KML Converter")
    root.geometry("720x820")
    root.configure(bg='#1e1e1e')
    root.resizable(True, True)
    
    # Dark mode color scheme
    BG_COLOR = '#1e1e1e'
    CARD_BG = '#2d2d2d'
    ACCENT_COLOR = '#42A5F5'
    SUCCESS_COLOR = '#66BB6A'
    TEXT_COLOR = '#E0E0E0'
    SECONDARY_TEXT = '#B0B0B0'
    
    # Main container with modern card-based layout
    main_container = Frame(root, bg=BG_COLOR, padx=20, pady=18)
    main_container.pack(fill='both', expand=True)
    
    # Header card with gradient-like effect
    header_card = Frame(main_container, bg='#2d2d2d', relief='flat')
    header_card.pack(fill='x', pady=(0, 18))
    
    header_content = Frame(header_card, bg='#2d2d2d')
    header_content.pack(fill='x', padx=18, pady=14)
    
    title_label = Label(
        header_content, 
        text="🗺️ Geospatial Data Converter", 
        font=('Segoe UI', 14, 'bold'),
        fg='#64B5F6',
        bg='#2d2d2d'
    )
    title_label.pack(anchor='w')
    
    subtitle_label = Label(
        header_content,
        text="Transform CSV and NetCDF Spray data into KML geospatial files",
        font=('Segoe UI', 9),
        fg='#90CAF9',
        bg='#2d2d2d'
    )
    subtitle_label.pack(anchor='w', pady=(3, 0))
    
    # Configure ttk Notebook style
    style = ttk.Style()
    style.theme_use('default')
    style.configure('TNotebook', 
                   background=BG_COLOR, 
                   borderwidth=0,
                   tabmargins=[0, 0, 0, 0])
    style.configure('TNotebook.Tab', 
                   background=CARD_BG, 
                   foreground=TEXT_COLOR,
                   padding=[20, 10],
                   font=('Segoe UI', 10, 'bold'),
                   borderwidth=0)
    style.map('TNotebook.Tab',
             background=[('selected', '#1976D2'), ('!selected', CARD_BG)],
             foreground=[('selected', 'white'), ('!selected', SECONDARY_TEXT)],
             expand=[('selected', [1, 1, 1, 0])])
    
    # Create notebook (tabbed interface)
    notebook = ttk.Notebook(main_container)
    notebook.pack(fill='both', expand=True, pady=(0, 15))
    
    # =============================================================================
    # CSV TAB
    # =============================================================================
    csv_tab = Frame(notebook, bg=BG_COLOR)
    notebook.add(csv_tab, text='  📊 CSV Files  ')
    
    csv_content = Frame(csv_tab, bg=BG_COLOR, padx=15, pady=15)
    csv_content.pack(fill='both', expand=True)
    
    # CSV Info panel
    csv_info_card = Frame(csv_content, bg=CARD_BG, relief='flat')
    csv_info_card.pack(fill='x', pady=(0, 15))
    
    csv_info_content = Frame(csv_info_card, bg=CARD_BG)
    csv_info_content.pack(fill='x', padx=18, pady=12)
    
    Label(
        csv_info_content,
        text="CSV to KML Conversion",
        font=('Segoe UI', 11, 'bold'),
        fg='#64B5F6',
        bg=CARD_BG
    ).pack(anchor='w')
    
    Label(
        csv_info_content,
        text="Process CSV files containing geospatial point data",
        font=('Segoe UI', 9),
        fg=SECONDARY_TEXT,
        bg=CARD_BG
    ).pack(anchor='w', pady=(3, 0))
    
    # CSV Output card
    csv_output_card = Frame(csv_content, bg=CARD_BG, relief='flat', borderwidth=1)
    csv_output_card.pack(fill='both', expand=True, pady=(0, 15))
    
    # Output header
    csv_output_header = Frame(csv_output_card, bg=CARD_BG)
    csv_output_header.pack(fill='x', padx=15, pady=(12, 8))
    
    Label(
        csv_output_header,
        text="📋 Processing Log",
        font=('Segoe UI', 10, 'bold'),
        fg=TEXT_COLOR,
        bg=CARD_BG
    ).pack(side='left')
    
    # Output text widget for CSV
    csv_output_container = Frame(csv_output_card, bg=CARD_BG)
    csv_output_container.pack(fill='both', expand=True, padx=15, pady=(0, 12))
    
    csv_output = Text(
        csv_output_container, 
        height=15, 
        width=70, 
        bg="#1e1e1e",
        fg=TEXT_COLOR,
        font=('Consolas', 9),
        relief='flat',
        borderwidth=0,
        highlightthickness=1,
        highlightbackground='#3d3d3d',
        highlightcolor=ACCENT_COLOR,
        wrap='word',
        padx=8,
        pady=8,
        insertbackground='#E0E0E0'
    )
    csv_scrollbar = ttk.Scrollbar(csv_output_container, orient='vertical', command=csv_output.yview)
    csv_output.configure(yscrollcommand=csv_scrollbar.set)
    csv_output.pack(side='left', fill='both', expand=True)
    csv_scrollbar.pack(side='right', fill='y')
    
    def start_processing():
        """Start processing the selected CSV files."""
        if config.config_window_open:
            csv_output.insert('end', 'Configuration open, load configuration first\n')
            return
            
        if not config.file_list:
            messagebox.showwarning("No Files", "Please select files to process first", parent=root)
            return
        
        # Create progress window
        total_files = len(config.file_list)
        progress_window = ProgressWindow(root, total_files)
        
        csv_output.insert('end', 'Starting processing...\n')
        root.update()
        
        try:
            for idx, file_path in enumerate(config.file_list, 1):
                file_name = Path(file_path).name
                
                # Update progress window
                progress_window.update_progress(idx, file_name)
                
                csv_output.insert('end', f'Processing {file_name}...\n')
                root.update()
                
                try:
                    params = (
                        config.levels, config.variable, config.zone, 
                        config.projin, config.projout, config.static, 
                        config.max_scale, config.min_scale, config.x_col, 
                        config.y_col, config.val_col, config.scale,
                        config.base, config.x_shift, config.y_shift,
                        config.x_scale_factor, config.y_scale_factor
                    )
                    from_csv_to_kml_configurated(file_path, params)
                    csv_output.insert('end', f'✓ Completed {file_name}\n')
                except Exception as e:
                    csv_output.insert('end', f'✗ Error in {file_name}: {e}\n')
                finally:
                    root.update()
            
            csv_output.insert('end', 'All files processed!\n')
        finally:
            # Close progress window
            progress_window.close()
            config.file_list.clear()
    
    def select_files():
        """Open file dialog to select CSV files."""
        filenames = filedialog.askopenfilenames(
            initialdir="/",
            title="Select CSV Files",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filenames:
            config.file_list.extend(filenames)
            csv_output.insert('end', f'Loaded {len(filenames)} file(s)\n')
    
    def clear_csv_output():
        """Clear the CSV output text and file list."""
        csv_output.delete('1.0', 'end')
        config.file_list.clear()
        csv_output.insert('end', 'Output cleared\n')
    
    # CSV Action buttons
    csv_actions_card = Frame(csv_content, bg=CARD_BG, relief='flat', borderwidth=1)
    csv_actions_card.pack(fill='x')
    
    csv_actions_content = Frame(csv_actions_card, bg=CARD_BG)
    csv_actions_content.pack(fill='x', padx=15, pady=15)
    
    # First row buttons
    csv_button_frame1 = Frame(csv_actions_content, bg=CARD_BG)
    csv_button_frame1.pack(fill='x', pady=(0, 8))
    
    select_btn = Button(
        csv_button_frame1, 
        text="📂 Select CSV Files",
        command=select_files,
        bg='#1976D2',
        fg='white',
        font=('Segoe UI', 9, 'bold'),
        relief='flat',
        padx=15,
        pady=9,
        cursor='hand2',
        activebackground='#1565C0',
        activeforeground='white'
    )
    select_btn.pack(side='left', fill='x', expand=True, padx=(0, 6))
    
    clear_btn = Button(
        csv_button_frame1, 
        text="🗑️ Clear",
        command=clear_csv_output,
        bg='#424242',
        fg='white',
        font=('Segoe UI', 9, 'bold'),
        relief='flat',
        padx=15,
        pady=9,
        cursor='hand2',
        activebackground='#5d5d5d',
        activeforeground='white'
    )
    clear_btn.pack(side='left', fill='x', expand=True, padx=(6, 0))
    
    # Second row buttons
    csv_button_frame2 = Frame(csv_actions_content, bg=CARD_BG)
    csv_button_frame2.pack(fill='x')
    
    start_btn = Button(
        csv_button_frame2, 
        text="▶️ Start Processing",
        command=start_processing,
        bg='#388E3C',
        fg='white',
        font=('Segoe UI', 9, 'bold'),
        relief='flat',
        padx=15,
        pady=9,
        cursor='hand2',
        activebackground='#2E7D32',
        activeforeground='white'
    )
    start_btn.pack(side='left', fill='x', expand=True, padx=(0, 6))
    
    config_btn = Button(
        csv_button_frame2, 
        text="⚙️ Configuration",
        command=lambda: open_configuration(root, config, csv_output),
        bg='#1976D2',
        fg='white',
        font=('Segoe UI', 9, 'bold'),
        relief='flat',
        padx=15,
        pady=9,
        cursor='hand2',
        activebackground='#1565C0',
        activeforeground='white'
    )
    config_btn.pack(side='left', fill='x', expand=True, padx=(6, 0))
    
    # =============================================================================
    # SPRAY TAB
    # =============================================================================
    spray_tab = Frame(notebook, bg=BG_COLOR)
    notebook.add(spray_tab, text='  🌫️ Spray Files  ')
    
    spray_content = Frame(spray_tab, bg=BG_COLOR, padx=15, pady=15)
    spray_content.pack(fill='both', expand=True)
    
    # Spray Info panel
    spray_info_card = Frame(spray_content, bg=CARD_BG, relief='flat')
    spray_info_card.pack(fill='x', pady=(0, 15))
    
    spray_info_content = Frame(spray_info_card, bg=CARD_BG)
    spray_info_content.pack(fill='x', padx=18, pady=12)
    
    Label(
        spray_info_content,
        text="Spray NetCDF to KML Conversion",
        font=('Segoe UI', 11, 'bold'),
        fg='#81C784',
        bg=CARD_BG
    ).pack(anchor='w')
    
    Label(
        spray_info_content,
        text="Process NetCDF (.nc) Spray simulation files into KML format",
        font=('Segoe UI', 9),
        fg=SECONDARY_TEXT,
        bg=CARD_BG
    ).pack(anchor='w', pady=(3, 0))
    
    # Spray Output card
    spray_output_card = Frame(spray_content, bg=CARD_BG, relief='flat', borderwidth=1)
    spray_output_card.pack(fill='both', expand=True, pady=(0, 15))
    
    # Output header
    spray_output_header = Frame(spray_output_card, bg=CARD_BG)
    spray_output_header.pack(fill='x', padx=15, pady=(12, 8))
    
    Label(
        spray_output_header,
        text="📋 Processing Log",
        font=('Segoe UI', 10, 'bold'),
        fg=TEXT_COLOR,
        bg=CARD_BG
    ).pack(side='left')
    
    # Output text widget for Spray
    spray_output_container = Frame(spray_output_card, bg=CARD_BG)
    spray_output_container.pack(fill='both', expand=True, padx=15, pady=(0, 12))
    
    spray_output = Text(
        spray_output_container, 
        height=12, 
        width=70, 
        bg="#1e1e1e",
        fg=TEXT_COLOR,
        font=('Consolas', 9),
        relief='flat',
        borderwidth=0,
        highlightthickness=1,
        highlightbackground='#3d3d3d',
        highlightcolor=ACCENT_COLOR,
        wrap='word',
        padx=8,
        pady=8,
        insertbackground='#E0E0E0'
    )
    spray_scrollbar = ttk.Scrollbar(spray_output_container, orient='vertical', command=spray_output.yview)
    spray_output.configure(yscrollcommand=spray_scrollbar.set)
    spray_output.pack(side='left', fill='both', expand=True)
    spray_scrollbar.pack(side='right', fill='y')
    
    def select_spray_files():
        """Open file dialog to select .nc files."""
        filenames = filedialog.askopenfilenames(
            initialdir="/",
            title="Select NetCDF Files",
            filetypes=[("NetCDF Files", "*.nc"), ("All Files", "*.*")]
        )
        if filenames:
            spray_config.file_list.extend(filenames)
            spray_output.insert('end', f'Loaded {len(filenames)} Spray file(s)\n')
    
    def clear_spray_output():
        """Clear the spray file list."""
        spray_output.delete('1.0', 'end')
        spray_config.file_list.clear()
        spray_output.insert('end', 'Spray output cleared\n')
    
    def start_spray_processing():
        """Start processing the selected spray files."""
        if spray_config.spray_config_window_open:
            spray_output.insert('end', 'Spray configuration open, load configuration first\n')
            return
        if spray_config.kml_config_window_open:
            spray_output.insert('end', 'KML configuration open, load configuration first\n')
            return
        process_spray_files(spray_config, spray_output, root)
    
    # Spray action buttons
    spray_actions_card = Frame(spray_content, bg=CARD_BG, relief='flat', borderwidth=1)
    spray_actions_card.pack(fill='x')
    
    spray_actions_content = Frame(spray_actions_card, bg=CARD_BG)
    spray_actions_content.pack(fill='x', padx=15, pady=12)
    
    # Griglia 3x2 per i bottoni Spray
    # Prima riga: Select, Clear, Start
    spray_button_frame1 = Frame(spray_actions_content, bg=CARD_BG)
    spray_button_frame1.pack(fill='x', pady=(0, 6))
    
    spray_select_btn = Button(
        spray_button_frame1, 
        text="📂 Select Files",
        command=select_spray_files,
        bg='#388E3C',
        fg='white',
        font=('Segoe UI', 8, 'bold'),
        relief='flat',
        padx=10,
        pady=8,
        cursor='hand2',
        activebackground='#2E7D32',
        activeforeground='white'
    )
    spray_select_btn.pack(side='left', fill='x', expand=True, padx=(0, 4))
    
    spray_clear_btn = Button(
        spray_button_frame1, 
        text="🗑️ Clear",
        command=clear_spray_output,
        bg='#424242',
        fg='white',
        font=('Segoe UI', 8, 'bold'),
        relief='flat',
        padx=10,
        pady=8,
        cursor='hand2',
        activebackground='#5d5d5d',
        activeforeground='white'
    )
    spray_clear_btn.pack(side='left', fill='x', expand=True, padx=(4, 4))
    
    spray_start_btn = Button(
        spray_button_frame1, 
        text="▶️ Process",
        command=start_spray_processing,
        bg='#1976D2',
        fg='white',
        font=('Segoe UI', 8, 'bold'),
        relief='flat',
        padx=10,
        pady=8,
        cursor='hand2',
        activebackground='#1565C0',
        activeforeground='white'
    )
    spray_start_btn.pack(side='left', fill='x', expand=True, padx=(4, 0))
    
    # Seconda riga: Spray Config, KML Settings, (spazio vuoto o altro)
    spray_button_frame2 = Frame(spray_actions_content, bg=CARD_BG)
    spray_button_frame2.pack(fill='x')
    
    spray_config_btn = Button(
        spray_button_frame2, 
        text="⚙️ Spray Config",
        command=lambda: open_spray_configuration(root, spray_config, spray_output),
        bg='#388E3C',
        fg='white',
        font=('Segoe UI', 8, 'bold'),
        relief='flat',
        padx=10,
        pady=8,
        cursor='hand2',
        activebackground='#2E7D32',
        activeforeground='white'
    )
    spray_config_btn.pack(side='left', fill='x', expand=True, padx=(0, 4))
    
    kml_config_btn = Button(
        spray_button_frame2, 
        text="🎨 KML Settings",
        command=lambda: open_kml_configuration(root, spray_config, spray_output),
        bg='#5E35B1',
        fg='white',
        font=('Segoe UI', 8, 'bold'),
        relief='flat',
        padx=10,
        pady=8,
        cursor='hand2',
        activebackground='#512DA8',
        activeforeground='white'
    )
    kml_config_btn.pack(side='left', fill='x', expand=True, padx=(4, 0))
    
    # Footer with exit button
    footer_frame = Frame(main_container, bg=BG_COLOR)
    footer_frame.pack(fill='x', pady=(15, 0))
    
    exit_btn = Button(
        footer_frame, 
        text="❌ Exit Application",
        command=root.destroy,
        bg='#3d3d3d',
        fg='#B0B0B0',
        font=('Segoe UI', 8),
        relief='flat',
        padx=12,
        pady=7,
        cursor='hand2',
        activebackground='#4d4d4d',
        activeforeground='#E0E0E0'
    )
    exit_btn.pack(fill='x')
    
    root.mainloop()

if __name__ == "__main__":
    main()