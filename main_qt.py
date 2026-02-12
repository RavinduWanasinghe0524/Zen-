import sys
import os
import signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt, QPoint, QSize, QPropertyAnimation, Slot, QTimer, QThread, Signal

from gui.widgets.orb import NeuralOrb
from core.worker_listen import WorkerListen

# WorkerBrain is now a QObject, so we import it
from core.worker_brain import WorkerBrain

class ModernZenWindow(QMainWindow):
    # Signal to send text from UI thread to Brain Worker thread
    signal_user_input = Signal(str)

    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(500, 120)  # Compact bar mode by default
        
        # Center on screen (bottom area)
        screen_geo = QApplication.primaryScreen().availableGeometry()
        self.move(screen_geo.width() // 2 - 250, screen_geo.height() - 200)

        # Main Layout container
        self.central_widget = QWidget()
        self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)
        
        self.layout_main = QVBoxLayout(self.central_widget)
        self.layout_main.setContentsMargins(15, 15, 15, 15)
        
        # Header (Status + Controls)
        self.setup_header()
        
        # Content (Neural Orb + Text)
        self.setup_content()
        
        # Load Styles
        self.load_styles()
        
        # Dragging logic
        self.old_pos = None

        # --- Initialize Workers (Brain & Ears) ---
        
        # 1. LISTENER (Already a QThread subclass)
        self.worker_listen = WorkerListen()
        
        # 2. BRAIN (QObject needing a QThread)
        self.thread_brain = QThread()
        self.worker_brain = WorkerBrain()
        self.worker_brain.moveToThread(self.thread_brain)
        
        # Connect Signals
        
        # Listener -> UI
        self.worker_listen.signal_listening_started.connect(self.on_listening_start)
        self.worker_listen.signal_listening_stopped.connect(self.on_listening_stop)
        self.worker_listen.signal_text_recognized.connect(self.on_speech_recognized)
        self.worker_listen.signal_error.connect(self.on_error)

        # UI -> Brain (via Signal to cross thread boundary safely)
        self.signal_user_input.connect(self.worker_brain.process_text)
        
        # Brain -> UI
        self.worker_brain.signal_response_ready.connect(self.on_ai_response)
        self.worker_brain.signal_error.connect(self.on_error)

        # Start listening immediately
        self.worker_listen.start()
        
        # Start Brain Thread
        self.thread_brain.start()

    def setup_header(self):
        header_layout = QHBoxLayout()
        
        self.status_label = QLabel("● ONLINE")
        self.status_label.setObjectName("statusLabel")
        
        self.min_btn = QPushButton("─")
        self.min_btn.setObjectName("minBtn")
        self.min_btn.setFixedSize(30, 30)
        self.min_btn.clicked.connect(self.showMinimized)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.close)
        
        header_layout.addWidget(self.status_label)
        header_layout.addStretch()
        header_layout.addWidget(self.min_btn)
        header_layout.addWidget(self.close_btn)
        
        self.layout_main.addLayout(header_layout)

    def setup_content(self):
        content_layout = QHBoxLayout()
        
        # Updated: Use Custom Neural Orb widget
        self.orb = NeuralOrb(size=60)
        
        # Main updates text
        self.main_text = QLabel("Initializing systems...")
        self.main_text.setObjectName("mainText")
        self.main_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.main_text.setWordWrap(True) 
        
        content_layout.addWidget(self.orb)
        content_layout.addWidget(self.main_text, stretch=1)
        
        self.layout_main.addLayout(content_layout)

    def load_styles(self):
        # Load QSS file
        style_path = os.path.join(os.path.dirname(__file__), "gui", "styles.qss")
        if os.path.exists(style_path):
            try:
                with open(style_path, "r") as f:
                    self.setStyleSheet(f.read())
            except Exception as e:
                print(f"Error loading style: {e}")
        else:
            print(f"Warning: Style file not found at {style_path}")

    # --- Worker Slots ---
    @Slot()
    def on_listening_start(self):
        self.orb.set_state("listening")
        self.status_label.setText("● LISTENING")

    @Slot()
    def on_listening_stop(self):
        self.orb.set_state("thinking")
        self.status_label.setText("● PROCESSING")

    @Slot(str)
    def on_speech_recognized(self, text):
        self.main_text.setText(f"You: {text}")
        # Send to brain via signal (thread-safe)
        self.signal_user_input.emit(text)

    @Slot(str)
    def on_ai_response(self, response_text):
        self.orb.set_state("speaking")
        self.status_label.setText("● SPEAKING")
        self.main_text.setText(f"Zen: {response_text}")
        
        # TODO: Trigger TTS here (non-blocking)
        
        QTimer.singleShot(3000, lambda: self.orb.set_state("idle"))
        QTimer.singleShot(3000, lambda: self.status_label.setText("● ONLINE"))

    @Slot(str)
    def on_error(self, error_msg):
        self.orb.set_state("idle")
        self.status_label.setText("● ERROR")
        # Log to console but keep UI clean unless critical
        print(f"Error signal: {error_msg}")

    # --- Mouse Dragging Logic ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None
    
    def closeEvent(self, event):
        # Stop workers
        if self.worker_listen.isRunning():
            self.worker_listen.stop()
        if self.thread_brain.isRunning():
            self.thread_brain.quit()
            self.thread_brain.wait()
        event.accept()

if __name__ == "__main__":
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal.SIG_DFL) 

    app = QApplication(sys.argv)
    window = ModernZenWindow()
    window.show()
    sys.exit(app.exec())
