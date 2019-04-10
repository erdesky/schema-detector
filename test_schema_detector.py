import schema_detector
import pandas as pd

files = {
    'https://www.denvergov.org/media/gis/DataCatalog/business_improvement_districts/csv/business_improvement_districts.csv':
        ['smallint', 'nvarchar(6)', 'nvarchar(54)', 'nvarchar(15)', 'date', 'date', 'numeric(0,0)', 'numeric(0,0)', 'nvarchar(10)', 'nvarchar(88)', 'numeric(0,0)', 'nvarchar(245)', 'numeric(0,0)', 'numeric(0,0)', 'nvarchar(142)', 'numeric(0,0)'],
    'https://www.denvergov.org/media/gis/DataCatalog/licensed_child_care_facilities/csv/licensed_child_care_facilities.csv':
        ['nvarchar(18)', 'nvarchar(75)', 'nvarchar(52)', 'nvarchar(23)', 'nvarchar(17)', 'datetime', 'datetime', 'numeric(9,2)', 'numeric(9,2)', 'numeric(8,0)', 'nvarchar(32)', 'nvarchar(8)', 'nvarchar(6)', 'nvarchar(2)', 'nvarchar(5)']
}

def schema_detect_tests():
    for k, v in files.items():
        assert schema_detector.schema_detect(k)['ansi_type'].tolist() == v

def prec_scale_tests():
    def wrap(x):
        return list(schema_detector.prec_scale(x).values)
    assert wrap(1234.567) == [7, 3]
    assert wrap(1) == [1, 0]
    assert wrap('abc') == [0, 0]
