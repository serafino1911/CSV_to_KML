from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import threading
from tkinter import Tk, Toplevel, Frame, Label, Entry, Button, Text, StringVar
from tkinter import filedialog, messagebox
from tkinter import ttk
from typing import Optional

from main import from_csv_to_kml_configurated


@dataclass
class AppConfig:
    """Application configuration settings."""
    levels: int = 400
    variable: str = 'Odor'
    zone: str = '32 T'
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


def show_error(parent: Tk | Toplevel, message: str) -> None:
    """Display an error message dialog."""
    messagebox.showerror("Error", message, parent=parent)


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


def main() -> None:
    """Main application entry point."""
    config = AppConfig()
    
    root = Tk()
    root.title("CSV to KML Converter")
    root.geometry("680x680")
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
        text="📊 CSV to KML Converter", 
        font=('Segoe UI', 14, 'bold'),
        fg='#64B5F6',
        bg='#2d2d2d'
    )
    title_label.pack(anchor='w')
    
    subtitle_label = Label(
        header_content,
        text="Transform your CSV data into KML geospatial files",
        font=('Segoe UI', 9),
        fg='#90CAF9',
        bg='#2d2d2d'
    )
    subtitle_label.pack(anchor='w', pady=(3, 0))
    
    # Output card with shadow effect
    output_card = Frame(main_container, bg=CARD_BG, relief='flat', borderwidth=1)
    output_card.pack(fill='both', expand=True, pady=(0, 15))
    
    # Output header
    output_header = Frame(output_card, bg=CARD_BG)
    output_header.pack(fill='x', padx=15, pady=(12, 8))
    
    Label(
        output_header,
        text="📋 Output Log",
        font=('Segoe UI', 10, 'bold'),
        fg=TEXT_COLOR,
        bg=CARD_BG
    ).pack(side='left')
    
    # Output text widget
    output_container = Frame(output_card, bg=CARD_BG)
    output_container.pack(fill='both', expand=True, padx=15, pady=(0, 12))
    
    output = Text(
        output_container, 
        height=18, 
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
    scrollbar = ttk.Scrollbar(output_container, orient='vertical', command=output.yview)
    output.configure(yscrollcommand=scrollbar.set)
    output.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    def start_processing():
        """Start processing the selected files."""
        if config.config_window_open:
            output.insert('end', 'Configuration open, load configuration first\n')
            return
            
        if not config.file_list:
            messagebox.showwarning("No Files", "Please select files to process first", parent=root)
            return
        
        # Create progress window
        total_files = len(config.file_list)
        progress_window = ProgressWindow(root, total_files)
        
        output.insert('end', 'Starting processing...\n')
        root.update()
        
        try:
            for idx, file_path in enumerate(config.file_list, 1):
                file_name = Path(file_path).name
                
                # Update progress window
                progress_window.update_progress(idx, file_name)
                
                output.insert('end', f'Processing {file_name}...\n')
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
                    output.insert('end', f'✓ Completed {file_name}\n')
                except Exception as e:
                    output.insert('end', f'✗ Error in {file_name}: {e}\n')
                finally:
                    root.update()
            
            output.insert('end', 'All files processed!\n')
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
            output.insert('end', f'Loaded {len(filenames)} file(s)\n')
    
    def clear_output():
        """Clear the output text and file list."""
        output.delete('1.0', 'end')
        config.file_list.clear()
        output.insert('end', 'Output cleared\n')
    
    # Action buttons with modern card-based design
    actions_card = Frame(main_container, bg=CARD_BG, relief='flat', borderwidth=1)
    actions_card.pack(fill='x')
    
    actions_content = Frame(actions_card, bg=CARD_BG)
    actions_content.pack(fill='x', padx=15, pady=15)
    
    # First row buttons
    button_frame1 = Frame(actions_content, bg=CARD_BG)
    button_frame1.pack(fill='x', pady=(0, 8))
    
    select_btn = Button(
        button_frame1, 
        text="📂 Select Files",
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
        button_frame1, 
        text="🗑️ Clear",
        command=clear_output,
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
    button_frame2 = Frame(actions_content, bg=CARD_BG)
    button_frame2.pack(fill='x')
    
    start_btn = Button(
        button_frame2, 
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
        button_frame2, 
        text="⚙️ Configuration",
        command=lambda: open_configuration(root, config, output),
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