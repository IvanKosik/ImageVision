def init_app():
    with open('init_app.py', 'r') as script_file:
        script = script_file.read()
        exec(script, {}, {})


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    init_app()



    # from plugins.image_loading.image_format_loaders.nifti.nifti_image_format_loader import NiftiImageFormatLoader
    # from plugins.image_loading.image_format_loaders.simple.simple_image_format_loader import SimpleImageFormatLoader
    # l = NiftiImageFormatLoader()
    # s = SimpleImageFormatLoader()
    # # NiftiImageFormatLoader._FORMATS = ('m', 'a')
    # # l.formats = ('2', '3')
    # print(l.formats)
    # print(NiftiImageFormatLoader.formats)
    # print(s.formats)
    # print(SimpleImageFormatLoader.formats)



    # from plugins.image_format_loaders.image_format_loader import ImageFormatLoaderRegistry, ImageFormatLoader
    # from plugins.image_format_loaders.nifti.nifti_image_format_loader import NiftiImageFormatLoader
        # without this import registry has nothing

    # im_reg = ImageFormatLoader()
    # print('1:', ImageFormatLoader.registry())
    # print('2:', ImageFormatLoaderRegistry.registry())




    '''
    import core.ann_utils
    from pathlib import Path
    core.ann_utils.predict_on_nifti_model_slices(
        Path('D:/Projects/BsAnn/Brain/Data/Temp/Series/18_-p_20130307_001_003_t2_tse_tra_448.nii.gz'),
        Path('D:/Projects/BsAnn/Brain/Models/t2_tse_tra/2019.01.18_Model_Loss008_n4.h5'),
        Path('D:/Projects/BsAnn/Brain/Data/Temp/Masks/18_-p_20130307_001_003_t2_tse_tra_448.nii.gz'))
    '''


    '''
    import nibabel as nib
    import numpy as np
    nifti_image = nib.load('D:/Projects/Temp/ImReg/1.nii.gz')
    im = nifti_image.get_fdata()
    print(im.shape)
    print(im.min(), im.max(), np.average(im))
    print(np.unique(im))
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

    # sys.exit(app.exec_())
