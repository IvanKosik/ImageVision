import pydicom
from pydicom.filereader import read_dicomdir, read_dataset
from pydicom.data import get_testdata_files
from os.path import dirname, join
from pprint import pprint
import matplotlib.pyplot as plt
from pydicom.dataset import Dataset
from pathlib import Path


class DicomRecord(Dataset):
    def __init__(self):
        self.children = {}  # { id: DicomRecord }


class DicomDir(DicomRecord):
    def __init__(self, path):
        super().__init__()

        self.path = path


class DicomLoader:
    def __init__(self):
        pass

    def load_dicom(self):
        print('load_dicom')


        data = Path('D:/Projects/C++/Qt/5/BodySnitches/Builds/BodySnitches/!DicomDatasets/FantasticNine/09-Kydryavcev/2011.12.09/DICOM')
        dicom_file_paths = list(data.glob('**/*.dcm'))
        print(dicom_file_paths)

        return


        test_dict = {'a': 10, 'b': 20}
        for v in test_dict:
            print('vvv:', v)

        ddd = pydicom.dcmread('D:/Projects/C++/Qt/5/BodySnitches/Builds/BodySnitches/!DicomDatasets/FantasticNine/09-Kydryavcev/2011.12.09/DICOM/11111611/53120000/88851906')
        print('ddd.type', type(ddd))
        # print('shape', ddd.pixel_array.shape)
        # print('READ', ddd)
        # plt.imshow(ddd.pixel_array, cmap=plt.cm.bone)
        # plt.show()

        a = Dataset()
        a.children = []
        print('datasettt', a.children)

        # fetch the path to the test data
        # filepath = get_testdata_files('DICOMDIR')[0]
        filepath = 'D:/Projects/C++/Qt/5/BodySnitches/Builds/BodySnitches/!DicomDatasets/FantasticNine/09-Kydryavcev/2011.12.09/DICOMDIR'
        print('Path to the DICOM directory: {}'.format(filepath))
        # load the data
        dicom_dir = read_dicomdir(filepath)
        print('dicom_dir', dicom_dir)
        base_dir = dirname(filepath)
        print('base_dir', base_dir)

        # go through the patient record and print information
        print('patient_records type', type(dicom_dir.patient_records))
        for patient_record in dicom_dir.patient_records:
            print('rrr:', type(patient_record))
            if (hasattr(patient_record, 'PatientID') and
                    hasattr(patient_record, 'PatientName')):
                print("Patient: {}: {}".format(patient_record.PatientID,
                                               patient_record.PatientName))
            studies = patient_record.children
            # got through each serie
            for study in studies:
                print('sss:', type(study))
                print(" " * 4 + "Study {}: {}: {}".format(study.StudyID,
                                                          study.StudyDate,
                                                          study.StudyDescription))
                all_series = study.children
                # go through each serie
                for series in all_series:
                    image_count = len(series.children)
                    plural = ('', 's')[image_count > 1]

                    # Write basic series info and image count

                    # Put N/A in if no Series Description
                    if 'SeriesDescription' not in series:
                        series.SeriesDescription = "N/A"
                    print(" " * 8 + "Series {}: {}: {} ({} image{})".format(
                        series.SeriesNumber, series.Modality, series.SeriesDescription,
                        image_count, plural))

                    # Open and read something from each image, for demonstration
                    # purposes. For simple quick overview of DICOMDIR, leave the
                    # following out
                    print(" " * 12 + "Reading images...")
                    image_records = series.children
                    image_filenames = [join(base_dir, *image_rec.ReferencedFileID)
                                       for image_rec in image_records]

                    datasets = [pydicom.dcmread(image_filename)
                                for image_filename in image_filenames]

                    patient_names = set(ds.PatientName for ds in datasets)
                    patient_IDs = set(ds.PatientID for ds in datasets)

                    # List the image filenames
                    print("\n" + " " * 12 + "Image filenames:")
                    print(" " * 12, end=' ')
                    pprint(image_filenames, indent=12)

                    # Expect all images to have same patient name, id
                    # Show the set of all names, IDs found (should each have one)
                    print(" " * 12 + "Patient Names in images..: {}".format(
                        patient_names))
                    print(" " * 12 + "Patient IDs in images..: {}".format(
                        patient_IDs))