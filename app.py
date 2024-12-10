
import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSizePolicy, QFileDialog, QMessageBox, QHeaderView, QSlider, QLabel, QTextEdit, QSpinBox, QDialog, QScrollArea, QGroupBox

)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import matplotlib
matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  



class AnalysisThread(QThread):
    progress = pyqtSignal(str, str)  

    def __init__(self, ref_video_path, enc_video_path, codec_type, params, parent=None):
        super().__init__(parent)
        self.ref_video_path = ref_video_path
        self.enc_video_path = enc_video_path
        self.codec_type = codec_type
        self.params = params

    def run(self):
        self.calculate_metrics(self.ref_video_path, self.enc_video_path)

    def calculate_metrics(self, ref_video_path, enc_video_path):
        try:
            cmd = [
                'python3', 'Vmaf_calculator/Vmaf_calculator.py',  # Update this path accordingly
                '-d', enc_video_path,
                '-r', ref_video_path,                                                                           
                '-sw', str(self.params['sync_window']),
                '-ss', str(self.params['sync_start_time']),
                '-fps', str(self.params['frame_rate']),
                '-subsample', str(self.params['subsample']),
                '-threads', str(self.params['threads'])
            ]

            print("Executing Command:", ' '.join(cmd))  # Debugging line
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Handle output
            stdout, stderr = process.communicate()  # Wait for the process to finish
            self.progress.emit(self.codec_type, stdout.strip())
            if stderr:
                self.progress.emit(self.codec_type, stderr.strip())
        
            if process.returncode != 0:
                self.progress.emit(self.codec_type, f"Error: Process exited with code {process.returncode}")

        except Exception as e:
            self.progress.emit(self.codec_type, f"Error: {str(e)}")


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.setGeometry(200, 200, 900, 900)

        # Create a scrollable area for the help text
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setGeometry(10, 10, 480, 380)

        help_text = """
        <html>
        <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                color: #333;
                line-height: 1.6;
            }
            h1 {
                color: #D91656;  /* Pink color for headings */
                font-size: 20px;
            }
            h2 {
                color: #78B3CE;  /* Blue color for subheadings */
                font-size: 18px;
            }
            p {
                font-size: 14px;
                margin-bottom: 10px;
            }
            ul {
                margin-top: 5px;
                margin-left: 20px;
            }
            li {
                font-size: 14px;
                margin-bottom: 5px;
            }
            .highlight {
                color: #D91656;  /* Pink color for highlighted terms */
                font-weight: bold;
            }
        </style>
        </head>
        <body>
            <h1>Welcome to the H.264 vs H.265 Video Analyzer</h1>
            <p>This application allows you to compare <span class="highlight">H.264</span> and <span class="highlight">H.265</span> video encodings.</p>

            <h2>Parameters:</h2>
            <p><span class="highlight">Sync Window:</span> This parameter sets a window of time (in seconds) for automatic synchronization of the reference and distorted videos. It helps align the videos for proper comparison.</p>
            <p><span class="highlight">Sync Start Time:</span> Defines the starting point (in seconds) of the reference video to begin the synchronization.</p>
            <p><span class="highlight">Frame Rate:</span> This is the number of frames per second in the video. The application can adjust frame rate to standardize the videos for analysis.</p>
            <p><span class="highlight">Subsample:</span> Controls the number of frames to use for the analysis. A lower value speeds up processing at the cost of accuracy.</p>
            <p><span class="highlight">Threads:</span> Defines the number of processor cores to use during video analysis.</p>

            <h2>Technical Terms:</h2>
            <ul>
                <li><span class="highlight">VMAF:</span> Video Multimethod Assessment Fusion. A metric for measuring the perceived quality of video.</li>
                <li><span class="highlight">PSNR:</span> Peak Signal-to-Noise Ratio. A metric for assessing video quality based on signal and noise.</li>
                <li><span class="highlight">SSIM:</span> Structural Similarity Index. A metric for comparing two videos based on their structural similarity (the brightness, contrast, and texture of the image).</li>
                <li><span class="highlight">Sync:</span> The process of aligning two videos to start at the same time or to match frame-by-frame.</li>
            </ul>
        <br>
        <br>
            <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
            <thead>
            <tr>
                <th style="padding: 8px; background-color: #88C0D0; color: white;">Metric</th>
                <th style="padding: 8px; background-color: #88C0D0; color: white;">Optimal Range</th>
                <th style="padding: 8px; background-color: #88C0D0; color: white;">Ideal Value</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td style="padding: 8px;">VMAF</td>
                <td style="padding: 8px;">0-100</td>
                <td style="padding: 8px;">100</td>
            </tr>
            <tr>
                <td style="padding: 8px;">PSNR</td>
                <td style="padding: 8px;">&gt;40 dB</td>
                <td style="padding: 8px;">&gt;50 dB</td>
            </tr>
            <tr>
                <td style="padding: 8px;">SSIM</td>
                <td style="padding: 8px;">0-1</td>
                <td style="padding: 8px;">1.0</td>
            </tr>
            </tbody>
            </table>
        </body>
        </html>
        """


        help_label = QLabel(help_text)
        help_label.setTextFormat(Qt.RichText)  # Ensures that the HTML content is rendered correctly
        scroll_area.setWidget(help_label)

        
        # Layout for Help dialog
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)
        

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("H.264 vs H.265 Video Analyzer")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 800)
        self.results = {}

        # Initialize video paths
        self.ref_video_path = ''
        self.video_path_1 = ''
        self.video_path_2 = ''
        
        # Track analysis completion
        self.h264_done = False
        self.h265_done = False

        # Create video widgets
        self.reference_video_widget = QVideoWidget()
        self.video_widget_1 = QVideoWidget()  # H.264
        self.video_widget_2 = QVideoWidget()  # H.265
        
        # Create media players
        self.ref_player = QMediaPlayer()
        self.player_1 = QMediaPlayer()
        self.player_2 = QMediaPlayer()

        self.ref_player.setVideoOutput(self.reference_video_widget)
        self.player_1.setVideoOutput(self.video_widget_1)
        self.player_2.setVideoOutput(self.video_widget_2)

        # Connect media status changed signal to handle video end
        self.ref_player.mediaStatusChanged.connect(self.handle_media_status)
        self.player_1.mediaStatusChanged.connect(self.handle_media_status)
        self.player_2.mediaStatusChanged.connect(self.handle_media_status)
        
        # Text display for analysis results with a scrollbar
        self.h264_results_box = QTextEdit()
        self.h264_results_box.setReadOnly(True)
        self.h264_results_box.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.h265_results_box = QTextEdit()
        self.h265_results_box.setReadOnly(True)
        self.h265_results_box.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Initialize the table
        self.comparison_results_table = QTableWidget()
        self.comparison_results_table.setRowCount(3)  # 3 rows for PSNR, SSIM, VMAF results
        self.comparison_results_table.setColumnCount(2)  # 2 columns for H.264 and H.265 results
        self.comparison_results_table.setHorizontalHeaderLabels(["H.264", "H.265"])  # Column headers
        self.comparison_results_table.setVerticalHeaderLabels(["PSNR", "SSIM", "VMAF"])  # Row headers

        # Set the table to be read-only
        self.comparison_results_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Adjust the stretch of the table to fit the space
        self.comparison_results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.comparison_results_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Comparison result section will also hold the graph
        self.comparison_graph_widget = QWidget()  # To hold the graph
        self.comparison_graph_layout = QVBoxLayout(self.comparison_graph_widget)  # Layout for graph

        # Create buttons
        self.play_button = QPushButton("Play Videos")
        self.pause_button = QPushButton("Pause Videos")
        self.stop_button = QPushButton("Stop Videos")
        self.analyze_button = QPushButton("Analyze Videos")
        self.plot_button = QPushButton("Show Graphical Comparison")

        # Set initial button states
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.analyze_button.setEnabled(False)
        self.plot_button.setEnabled(False)

        # Connect buttons to functions
        self.play_button.clicked.connect(self.play_videos)
        self.pause_button.clicked.connect(self.pause_videos)
        self.stop_button.clicked.connect(self.stop_videos)
        self.analyze_button.clicked.connect(self.analyze_videos)
        self.plot_button.clicked.connect(self.plot_comparison)

        # Slider for seeking
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setEnabled(False)
        self.seek_slider.sliderMoved.connect(self.set_position)

        # Input fields for additional parameters
        self.sync_window_input = QSpinBox()
        self.sync_start_time_input = QSpinBox()
        self.frame_rate_input = QSpinBox()
        self.subsample_input = QSpinBox()
        self.threads_input = QSpinBox()

        # Set input ranges and initial values for sliders and spinboxes
        self.sync_window_input.setRange(1, 100)
        self.sync_start_time_input.setRange(1, 100)
        self.frame_rate_input.setRange(1, 120)
        self.subsample_input.setRange(1, 10)
        self.threads_input.setRange(1, 32)

        # Set initial values closer to the slider's range
        self.sync_window_input.setValue(1)
        self.sync_start_time_input.setValue(1)
        self.frame_rate_input.setValue(30)
        self.subsample_input.setValue(1)
        self.threads_input.setValue(8)

        # Adjust sliders to match initial values and set the range
        self.sync_window_slider = QSlider(Qt.Horizontal)
        self.sync_window_slider.setRange(1, 100)
        self.sync_window_slider.setValue(self.sync_window_input.value())
        
        self.sync_start_time_slider = QSlider(Qt.Horizontal)
        self.sync_start_time_slider.setRange(1, 100)
        self.sync_start_time_slider.setValue(self.sync_start_time_input.value())
        
        self.frame_rate_slider = QSlider(Qt.Horizontal)
        self.frame_rate_slider.setRange(1, 120)
        self.frame_rate_slider.setValue(self.frame_rate_input.value())
        
        self.subsample_slider = QSlider(Qt.Horizontal)
        self.subsample_slider.setRange(1, 10)
        self.subsample_slider.setValue(self.subsample_input.value())
        
        self.threads_slider = QSlider(Qt.Horizontal)
        self.threads_slider.setRange(1, 32)
        self.threads_slider.setValue(self.threads_input.value())

        # Connect sliders to the corresponding spinboxes
        self.sync_window_slider.valueChanged.connect(lambda: self.sync_window_input.setValue(self.sync_window_slider.value()))
        self.sync_start_time_slider.valueChanged.connect(lambda: self.sync_start_time_input.setValue(self.sync_start_time_slider.value()))
        self.frame_rate_slider.valueChanged.connect(lambda: self.frame_rate_input.setValue(self.frame_rate_slider.value()))
        self.subsample_slider.valueChanged.connect(lambda: self.subsample_input.setValue(self.subsample_slider.value()))
        self.threads_slider.valueChanged.connect(lambda: self.threads_input.setValue(self.threads_slider.value()))
 
        # Create logo label
        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap("Logo.png")  # Path to your logo image
        self.logo_pixmap = self.logo_pixmap.scaled(200, 200, Qt.KeepAspectRatio)  # Resize logo to fit the window
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignLeft)  # Position logo at the top-left corner

        # Create help button
        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.show_help)

        # Top Layout: Horizontal layout for logo and help button (no padding)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)  # Remove any margins for no padding
        top_layout.addWidget(self.logo_label)  # Add logo to the left
        top_layout.addStretch()  # Push the help button to the right
        top_layout.addWidget(self.help_button)  # Add help button to the right

        # Main layout for the window
        main_layout = QVBoxLayout()

        # Add the top layout (containing logo and help button)
        main_layout.addLayout(top_layout)

        # Cards Layout (Horizontal Layout for the three cards with added spacing between them)
        card_layout = QHBoxLayout()
        card_layout.setSpacing(20)  # Add spacing between cards

        # Reference Video Card
        ref_card = self.create_video_card("Reference Video", self.reference_video_widget, self.load_reference_video)
        card_layout.addWidget(ref_card)

        # H.264 Video Card
        h264_card = self.create_video_card("H.264 Encoded Video", self.video_widget_1, self.load_video_1)
        card_layout.addWidget(h264_card)

        # H.265 Video Card
        h265_card = self.create_video_card("H.265 Encoded Video", self.video_widget_2, self.load_video_2)
        card_layout.addWidget(h265_card)

        # Add card layout to main layout
        main_layout.addLayout(card_layout)

        # Continue with other layouts like the seek slider, parameter inputs, and buttons...

        # Seek slider layout
        main_layout.addWidget(QLabel("Seek:"))
        main_layout.addWidget(self.seek_slider)

        # Parameter Inputs Layout (horizontal row with spacing)
        param_layout = QHBoxLayout()
        param_layout.setSpacing(10)  # Add gap between inputs
        
        # Add parameters with descriptions using the helper function
        self.add_info_icon("Sync Window:", "Defines the time window used to synchronize streams or video frames in the analysis process.", param_layout)
        param_layout.addWidget(self.sync_window_input)  
        param_layout.addWidget(self.sync_window_slider)

        self.add_info_icon("Sync Start Time:", "Specifies the starting point in time for synchronization to align streams or frames from a common reference.", param_layout)
        param_layout.addWidget(self.sync_start_time_input)
        param_layout.addWidget(self.sync_start_time_slider)

        self.add_info_icon("Frame Rate:", "Determines the number of frames per second (FPS) used to process and display video or data streams.", param_layout)
        param_layout.addWidget(self.frame_rate_input)
        param_layout.addWidget(self.frame_rate_slider)

        self.add_info_icon("Subsample:", "Refers to the reduction of data by selecting a subset of frames or samples for faster processing or analysis.", param_layout)
        param_layout.addWidget(self.subsample_input)
        param_layout.addWidget(self.subsample_slider)

        self.add_info_icon("Threads:", " Controls the number of concurrent threads used to speed up data processing and improve performance.", param_layout)
        param_layout.addWidget(self.threads_input)
        param_layout.addWidget(self.threads_slider)

        # Buttons for Play, Pause, Stop, Analyze, Graph (spacing between buttons)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # Add gap between buttons
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.analyze_button)
        button_layout.addWidget(self.plot_button)

        # Add Parameter layout and Button layout to main layout
        main_layout.addLayout(param_layout)
        main_layout.addLayout(button_layout)

        # Result cards layout (H.264, H.265, and Comparison with spacing between results)
        result_layout = QHBoxLayout()
        result_layout.setSpacing(15)  # Add gap between result cards
        
         # H.264 Result Card
        h264_card_result = self.create_result_card("H.264 Analysis Result", self.h264_results_box)
        result_layout.addWidget(h264_card_result,1)

        # H.265 Result Card
        h265_card_result = self.create_result_card("H.265 Analysis Result", self.h265_results_box)
        result_layout.addWidget(h265_card_result,1)

        # Comparison Result Card
        comparison_card_result = QGroupBox()
        comparison_card_result.setStyleSheet("QGroupBox { border: 2px solid #78B3CE; border-radius: 10px; padding: 10px; }")
        comparison_layout = QHBoxLayout(comparison_card_result)
        comparison_layout.addWidget(self.comparison_results_table, 1)  # Table area
        comparison_layout.addWidget(self.comparison_graph_widget, 2)  # Graph area (takes more space)
        result_layout.addWidget(comparison_card_result, 3)

        # Add results layout to main layout
        main_layout.addLayout(result_layout)
        
        self.setStyleSheet("""
        QWidget {
            background-color: white;
        }
        QPushButton {
            font-weight:bold;
            background-color: #78B3CE ;
            color: white;
            font-size: 16px;
            padding: 10px;
            border-radius: 15px;
            border: 3px solid transparent;
            border-color: #78B3CE;
        }
        QPushButton:hover {
            background-color: #78B3CE;
            color: #D91656;
            border-color: #78B3CE;
        }
        QSlider {
            background-color: white;
            border-color: #78B3CE;
        }
        QTextEdit {
            background-color: white;
            border: 2px solid #D91656;
            padding: 10px;
        }
        QLabel {
            color: #D91656;
        }
        QLabel:hover {
            color: #78B3CE;
        }
        """)
        
        # Set the main layout
        self.setLayout(main_layout)
        
        self.player_1.positionChanged.connect(self.update_seek_slider)
        self.player_2.positionChanged.connect(self.update_seek_slider)

    def create_video_card(self, title, video_widget, browse_function):
        # Create the card for each video with title, video widget, and browse button
        card = QGroupBox()  # Use QGroupBox to visually separate the video sections
        card.setStyleSheet("QGroupBox { border: 2px solid #78B3CE; border-radius: 10px; padding: 10px; }")
        
        card_layout = QVBoxLayout()

        # Title label (only one title is added here)
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: #D91656; padding-bottom: 5px;")
        card_layout.addWidget(title_label)

        # Video widget
        video_widget.setFixedSize(550, 400)  # Set a fixed size for consistency
        card_layout.addWidget(video_widget)

        # Browse button with reduced size and centered
        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(120, 40)  # Reduce the size of the browse button
        browse_button.clicked.connect(browse_function)
        
        # Center the browse button within the card
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add space on the left
        button_layout.addWidget(browse_button)
        button_layout.addStretch()  # Add space on the right
        card_layout.addLayout(button_layout)

        # Add padding around the card's content
        card.setLayout(card_layout)
        
        return card


    def load_reference_video(self):
        self.ref_video_path, _ = QFileDialog.getOpenFileName(self, "Select Reference Video", "", "Video Files (*.mp4 *.avi *.mkv *.ts)")
        if self.ref_video_path:
            self.ref_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.ref_video_path)))
            self.check_playability()
            self.sender().setEnabled(False)  # Hide the browse button for reference video
            self.sender().setVisible(False)  # Hide the browse button completely

    def load_video_1(self):
        self.video_path_1, _ = QFileDialog.getOpenFileName(self, "Select H.264 Video", "", "Video Files (*.mp4 *.avi *.mkv *.ts)")
        if self.video_path_1:
            self.player_1.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_path_1)))
            self.check_playability()
            self.sender().setEnabled(False)  # Hide the browse button for H.264 video
            self.sender().setVisible(False)  # Hide the browse button completely

    def load_video_2(self):
        self.video_path_2, _ = QFileDialog.getOpenFileName(self, "Select H.265 Video", "", "Video Files (*.mp4 *.avi *.mkv *.ts)")
        if self.video_path_2:
            self.player_2.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_path_2)))
            self.check_playability()
            self.sender().setEnabled(False)  # Hide the browse button for H.265 video
            self.sender().setVisible(False)  # Hide the browse button completely

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            # Reset the position of the video to the start
            sender = self.sender()  # Get the player that triggered the signal
            sender.setPosition(0)  # Rewind to the beginning

        # Enable the play button again
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.seek_slider.setEnabled(False)
    
    def show_help(self):
        # Create and display a Help dialog
        help_dialog = HelpDialog(self)
        help_dialog.exec_()
        
    def create_result_card(self, title, text_edit):
        card = QGroupBox(title)
        card_layout = QVBoxLayout()
        card_layout.addWidget(text_edit)
        card.setLayout(card_layout)
        return card

    def check_playability(self):
        # Ensure that the paths are set before enabling buttons
        if self.ref_video_path and self.video_path_1 and self.video_path_2:
            self.play_button.setEnabled(True)
            self.analyze_button.setEnabled(True)

    def play_videos(self):
        self.ref_player.play()
        self.player_1.play()
        self.player_2.play()
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.seek_slider.setEnabled(True)

    def pause_videos(self):
        self.ref_player.pause()
        self.player_1.pause()
        self.player_2.pause()
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def stop_videos(self):
        self.ref_player.stop()
        self.player_1.stop()
        self.player_2.stop()
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.seek_slider.setEnabled(False)
        self.seek_slider.setValue(0)

    def update_seek_slider(self, position):
        # Synchronize slider position across players (assuming they all play together)
        if self.player_1.duration() > 0:
            self.seek_slider.setMaximum(self.player_1.duration())
            self.seek_slider.setValue(position)

    def set_position(self, position):
        # Set the same position for all players
        self.ref_player.setPosition(position)
        self.player_1.setPosition(position)
        self.player_2.setPosition(position)

    def analyze_videos(self):
        if self.ref_video_path and self.video_path_1 and self.video_path_2:
            self.h264_results_box.clear()
            self.h264_results_box.append("Starting H.264 analysis...\n")

            params = {
                'sync_window': self.sync_window_input.value(),
                'sync_start_time': self.sync_start_time_input.value(),
                'frame_rate': self.frame_rate_input.value(),
                'subsample': self.subsample_input.value(),
                'threads': self.threads_input.value()
            }

            # Start analysis for H.264
            self.thread_h264 = AnalysisThread(self.ref_video_path, self.video_path_1, "H.264", params)
            self.thread_h264.progress.connect(self.on_analysis_progress)
            self.thread_h264.progress.connect(self.update_h264_result_box)
            self.thread_h264.finished.connect(self.start_h265_analysis)  # Start H.265 when H.264 finishes
            self.thread_h264.start()

    def start_h265_analysis(self):
        self.h264_results_box.append("\nH.264 analysis completed.\n")
        self.h264_done = True  # Mark H.264 as completed
        self.h265_results_box.append("Starting H.265 analysis...\n")

        params = {
            'sync_window': self.sync_window_input.value(),
            'sync_start_time': self.sync_start_time_input.value(),
            'frame_rate': self.frame_rate_input.value(),
            'subsample': self.subsample_input.value(),
            'threads': self.threads_input.value()
        }

        # Start analysis for H.265
        self.thread_h265 = AnalysisThread(self.ref_video_path, self.video_path_2, "H.265", params)
        self.thread_h265.progress.connect(self.on_analysis_progress)
        self.thread_h265.progress.connect(self.update_h265_result_box)
        self.thread_h265.finished.connect(self.on_h265_finished)  # Update when H.265 finishes
        self.thread_h265.finished.connect(self.display_comparison)
        self.thread_h265.start()


    def on_h265_finished(self):
        self.h265_results_box.append("\nH.265 analysis completed.\n")
        self.h265_done = True  # Mark H.265 as completed
        # Enable plot button if both analyses are done
        if self.h264_done and self.h265_done:
            self.plot_button.setEnabled(True)
    
    def on_analysis_progress(self, codec_type, output):
        try:
            # Initialize the extracted metrics
            psnr = None
            ssim = None
            vmaf = None

            # Split the output by lines to process each line separately
            lines = output.splitlines()

            # Loop through each line to extract the relevant metrics
            for line in lines:
                if "psnr:" in line:
                    psnr = float(line.split("psnr:")[-1].strip())
                elif "SSIM Score:" in line:
                    ssim = float(line.split("SSIM Score:")[-1].strip())
                elif "VMAF HD:" in line:
                    vmaf = line.split("VMAF HD:")[-1].strip()

            # Update the results box with the extracted metrics
            if psnr is not None and ssim is not None and vmaf is not None:
                # Store the extracted values for comparison later
                self.results[codec_type] = {"psnr": psnr, "ssim": ssim, "vmaf": vmaf}

        except Exception as e:
            self.comparison_results_box.append(f"Error parsing {codec_type} output: {str(e)}")
            
    def display_comparison(self):
        if "H.264" in self.results and "H.265" in self.results:
            h264 = self.results["H.264"]
            h265 = self.results["H.265"]

            # Fill the table with formatted results (up to 10 decimal places)
            self.comparison_results_table.setItem(0, 0, QTableWidgetItem(f"{h264['psnr']:.10f}"))
            self.comparison_results_table.setItem(0, 1, QTableWidgetItem(f"{h265['psnr']:.10f}"))

            self.comparison_results_table.setItem(1, 0, QTableWidgetItem(f"{h264['ssim']:.10f}"))
            self.comparison_results_table.setItem(1, 1, QTableWidgetItem(f"{h265['ssim']:.10f}"))

            self.comparison_results_table.setItem(2, 0, QTableWidgetItem(f"{h264['vmaf']}"))
            self.comparison_results_table.setItem(2, 1, QTableWidgetItem(f"{h265['vmaf']}"))

            # Call plot_comparison_graph after displaying the results
            self.plot_comparison_graph()

            # Enable the plot button
            self.plot_button.setEnabled(True)
        
    def plot_comparison(self):
        if "H.264" in self.results and "H.265" in self.results:
            h264 = self.results["H.264"]
            h265 = self.results["H.265"]

            # Data for plotting
            metrics = ['PSNR', 'SSIM', 'VMAF HD']
            h264_values = [h264['psnr'], h264['ssim'], float(h264['vmaf'])]
            h265_values = [h265['psnr'], h265['ssim'], float(h265['vmaf'])]

            # Create a bar chart for comparison
            bar_width = 0.35
            index = range(len(metrics))

            fig, ax = plt.subplots()
            bars1 = ax.bar(index, h264_values, bar_width, label='H.264')
            bars2 = ax.bar([i + bar_width for i in index], h265_values, bar_width, label='H.265')

            # Add labels and title
            ax.set_xlabel('Metrics')
            ax.set_ylabel('Values')
            ax.set_title('H.264 vs H.265 Comparison')
            ax.set_xticks([i + bar_width / 2 for i in index])
            ax.set_xticklabels(metrics)
            ax.legend()

            plt.tight_layout()
            plt.show()

    def plot_comparison_graph(self):
        # Ensure that both H.264 and H.265 results are available
        if "H.264" in self.results and "H.265" in self.results:
            h264 = self.results["H.264"]
            h265 = self.results["H.265"]

            # Data for plotting
            metrics = ['PSNR', 'SSIM', 'VMAF']
            h264_values = [h264['psnr'], h264['ssim'], float(h264['vmaf'])]
            h265_values = [h265['psnr'], h265['ssim'], float(h265['vmaf'])]

            # Create a bar chart for comparison
            bar_width = 0.35
            index = range(len(metrics))

            fig, ax = plt.subplots(figsize=(7, 3))  # Adjusted figure size for better visibility
            bars1 = ax.bar(index, h264_values, bar_width, label='H.264', color='#D91656')
            bars2 = ax.bar([i + bar_width for i in index], h265_values, bar_width, label='H.265', color='#78B3CE')

            # Add labels and title
            ax.set_xlabel('Metrics')
            ax.set_ylabel('Values')
            ax.set_title('H.264 vs H.265 Comparison')
            ax.set_xticks([i + bar_width / 2 for i in index])
            ax.set_xticklabels(metrics)
            ax.legend()

            # Ensure layout is tight
            plt.tight_layout()
            # Create a canvas widget to display the figure inside the Qt layout
            canvas = FigureCanvas(fig)
            # Set the canvas to be responsive
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # Add the canvas to the comparison graph layout
            self.comparison_graph_layout.addWidget(canvas)  # Add the canvas to the layout
            # Ensure the layout is updated
            self.comparison_graph_layout.update()
            # Render the canvas
            canvas.draw()

    def update_h264_result_box(self):
        if "H.264" in self.results:
            h264 = self.results["H.264"]
            self.h264_results_box.clear()
            self.h264_results_box.append("H.264 Analysis Results:\n")
            self.h264_results_box.append(f"PSNR: {h264['psnr']:.10f}")
            self.h264_results_box.append(f"SSIM Score: {h264['ssim']:.10f}")
            self.h264_results_box.append(f"VMAF: {h264['vmaf']}")
    
    def update_h265_result_box(self):
        if "H.265" in self.results:
            h265 = self.results["H.265"]
            self.h265_results_box.clear()
            self.h265_results_box.append("H.265 Analysis Results:\n")
            self.h265_results_box.append(f"PSNR: {h265['psnr']:.10f}")
            self.h265_results_box.append(f"SSIM Score: {h265['ssim']:.10f}")
            self.h265_results_box.append(f"VMAF: {h265['vmaf']}")

    def create_result_card(self, title, results_box=None, is_graph=False):
        card = QGroupBox()  # Use QGroupBox to visually separate the sections
        card.setStyleSheet("QGroupBox { border: 2px solid #78B3CE; border-radius: 10px; padding: 10px; }")

        card_layout = QVBoxLayout()

        # Title label (only one title is added here)
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: #D91656; padding-bottom: 5px;")
        card_layout.addWidget(title_label)

        # If this is a graph, add the graph widget instead of results box
        if is_graph:
            # Create an empty layout for the graph (no text box here)
            self.comparison_graph_layout = QVBoxLayout()
            card_layout.addLayout(self.comparison_graph_layout)  # Add the layout for the graph to the card
        else:
            # Otherwise, use the results box for analysis results
            if results_box:
                results_box.setReadOnly(True)
                results_box.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                card_layout.addWidget(results_box)

        card.setLayout(card_layout)

        return card

    def add_info_icon(self, label_text, description_text, layout):
        """
        Adds an info icon next to a label and displays a message on click using QLabel.
        """
        # Create a label for the description text
        label = QLabel(label_text)
        
        # Create a label for the icon (clickable)
        info_icon_label = QLabel()
        
        # Set the icon using a QPixmap
        info_icon_pixmap = QPixmap(QIcon.fromTheme("help").pixmap(16, 16))
        info_icon_label.setPixmap(info_icon_pixmap)
        
        # Set the label to be clickable by using mouse events
        info_icon_label.setAlignment(Qt.AlignCenter)
        
        # Function to show the description when clicked
        def show_description(event):
            if event.button() == Qt.LeftButton:  # Check if it's a left-click
                QMessageBox.information(self, "Info", description_text)

        # Install the event handler for mouse clicks
        info_icon_label.mousePressEvent = show_description

        # Add the label and the icon label to the layout
        layout.addWidget(label)
        layout.addWidget(info_icon_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())