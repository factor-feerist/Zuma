import sys
from PyQt6.QtWidgets import QApplication
import utils
from UI.widgets.game_widget import GameWidget
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect


app = QApplication([])

# effect = QSoundEffect()
# effect.setSource(utils.Sounds.SPIT)
# # effect.setVolume(100)
# effect.setLoopCount(3)
# effect.play()

player = QMediaPlayer()
aud = QAudioOutput()
player.setAudioOutput(aud)
player.setSource(utils.Sounds.SPIT)
# aud.setVolume(50)
player.play()

#window = MainWindow()
# frog_widget = GameWidget(lambda x: print(f'game ended with {x}'))
# frog_widget.run_game(utils.Levels.FIRST)
# #window.show()
# frog_widget.show()
sys.exit(app.exec())
