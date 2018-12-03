import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

# import nibabel as nib
# from nibabel.testing import data_path

'''
def load_nii():
    print('load_nii')

    example_filename = 'test_data/Series_2_Image.nii.gz'  #os.path.join(data_path, 'example4d.nii.gz')
    img = nib.load(example_filename)
    print(img.shape)
    print(img.get_data_dtype())
    # print(img.get_fdata())
    # print(img.header)
    data = img.dataobj
    print(data.shape)
    print(np.min(data), np.max(data))

    for i in range(data.shape[2]):
        slice = data[..., i]
        slice = slice / np.max(slice)
        cv2.imwrite('test_data/slices/slice' + str(i) + '.png', slice * 255)
'''


def run_script():
    # print(globals())
    # print(locals())
    print('run_script')
    # exec('print(dir())\nprint(__builtins__)')
    # exec('print(dir())', {'__builtins__': None}, {'print': print, 'dir': dir})

    with open('test_data/script.py', 'r') as content_file:
        content = content_file.read()
        exec(content)


def init_app():
    with open('init_app.py', 'r') as script_file:
        script = script_file.read()
        exec(script, globals())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    init_app()


    """
    viewer = ImageViewer(w)
    w.setCentralWidget(viewer)    

    menu_bar = w.menuBar()
    '''
    nibabel_menu = menu_bar.addMenu('NiBabel')
    load_action = nibabel_menu.addAction('Load', load_nii)
    '''

    script_menu = menu_bar.addMenu('Script')
    run_script_action = script_menu.addAction('Run', run_script)
    """
    sys.exit(app.exec_())
