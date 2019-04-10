# Schema Detector

Infers ANSI data types from datasets stored in flat files

## Dependencies
* Python 3.6+
* pandas 0.23+

## Usage Examples
```python
schema_detect('https://www.denvergov.org/media/gis/DataCatalog/business_improvement_districts/csv/business_improvement_districts.csv')
```
Result:

| table_name | column_name | ansi_type |
| --- | --- | --- |
| business_improvement_districts | DISTRICT_ID | smallint |
| business_improvement_districts | ACTIVE_OR_HISTORIC | nvarchar(6) |
| business_improvement_districts | DISTRICT_NAME | nvarchar(54) |
| business_improvement_districts | CREATION_ORDINANCE | nvarchar(15) |
| business_improvement_districts | BNDRY_LAST_MODIFIED_DATE | date |
| ... | ... | ... |
