# Utils
import pandas

from django_api.utils.serializers.upload_file import UploadFileCsvExcelSerializer


class UploadCsvExcel:

    def __init__(self, data, header=None, usecols=None, names=None, dtype=None, parse_dates=None):

        self.serializer = UploadFileCsvExcelSerializer(data=data)
        self.serializer.is_valid(raise_exception=True)

        self.data = data
        self.header = header
        self.usecols = usecols
        self.names = names
        self.dtype = dtype
        self.parse_dates = parse_dates
        self.file = data['archivo']
        self.extension = self.serializer.data['extension']

    def upload_file(self):

        if self.extension in self.serializer.EXTENSION_EXCEL:
            data_frame = pandas.read_excel(
                self.file,
                engine='openpyxl',
                header=self.header,
                usecols=self.usecols,
                names=self.names,
                dtype=self.dtype,
                parse_dates=self.parse_dates
            )
        else:
            data_frame = pandas.read_csv(
                self.file,
                encoding="iso-8859-1",
                sep=';',
                header=self.header,
                usecols=self.usecols,
                names=self.names,
                dtype=self.dtype,
                parse_dates=self.parse_dates
            )

        data_frame = data_frame.fillna('')

        return data_frame
