from PyQt5.QtWidgets import QApplication
import sys


def init_app():
    with open('init_app.py', 'r') as script_file:
        script = script_file.read()
        exec(script, globals())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    init_app()

    '''
    import core.ann_utils
    from pathlib import Path
    core.ann_utils.predict_on_nifti_model_slices(
        Path('D:/Temp/1_003_t1_se_tra_20130117_main/13-P_20130117_001_003_t1_se_tra.img'),
        Path('D:/Temp/BrainModel_Loss017_NoOpimizer.h5'),
        Path('D:/Temp/ResultBrainMask.nii.gz'))
    '''

    sys.exit(app.exec_())
