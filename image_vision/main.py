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
        Path('D:/Projects/Temp/ImReg/Dicoms/New/1_002_t1_se_tra_20111116/O9-P_20111116_001_002_t1_se_tra.hdr'),
        Path('D:/Temp/BrainModel_Loss017_NoOpimizer.h5'),
        Path('D:/Projects/Temp/ImReg/Dicoms/New/1_002_t1_se_tra_20111116/ResultBrainMask.nii.gz'))
    '''
    '''
    import nibabel as nib
    import pydicom
    from skimage.io import imsave
    dcm = pydicom.dcmread('D:/Projects/Temp/UlaAdrDevelopment/sheet 0.16 Hole1_Notch1_130kV_300uA_30FA_1FPS_3.5X.dcm')
    print(dcm.pixel_array)
    print(dcm.pixel_array.shape)
    imsave('D:/Projects/Temp/UlaAdrDevelopment/1.png', dcm.pixel_array)
    '''

    sys.exit(app.exec_())
