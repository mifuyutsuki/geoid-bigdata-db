class Keys:
  ID            = 'id'

  #: Field keys
  LOCATION_NAME = 'location_name'
  LOCATION_TYPE = 'location_type'
  COORDINATES   = 'coordinates'
  LATITUDE      = 'latitude'
  LONGITUDE     = 'longitude'
  PROVINCE_ID   = 'id_provinsi'
  PROVINCE_NAME = 'nama_provinsi'
  CITY_ID       = 'id_kabupaten_kota'
  CITY_NAME     = 'nama_kabupaten_kota'
  DISTRICT_ID   = 'id_kecamatan'
  DISTRICT_NAME = 'nama_kecamatan'
  VILLAGE_ID    = 'id_kelurahan_desa'
  VILLAGE_NAME  = 'nama_kelurahan_desa'
  POSTAL_CODE   = 'kode_pos'
  RATING        = 'rating'
  REVIEWS       = 'reviews'
  DESCRIPTION   = 'description'
  LOCATION_LINK = 'location_link'
  IMAGE_LINK    = 'image_link'

  #: Query results keys
  QUERY_TERM          = 'query_term'
  QUERY_LOCATION      = 'query_location'
  QUERY_KEYWORD       = 'query_keyword'
  QUERY_LANG          = 'query_lang'
  QUERY_TIMESTAMP     = 'query_timestamp'
  QUERY_STATUS        = 'query_status'
  QUERY_RESULTS_COUNT = 'query_results_count'
  QUERY_RESULTS       = 'query_results'

  #: Query status report keys
  REPORT_NO     = 'no'
  REPORT_QUERY  = 'query'
  REPORT_STATUS = 'status'


class Queries:
  CREATE = (
    f'CREATE TABLE IF NOT EXISTS `queries` ('
    f'  `{Keys.ID}` INT AUTO_INCREMENT,'
    f'  `{Keys.QUERY_TERM}` VARCHAR(127) NOT NULL,'
    f'  `{Keys.QUERY_LOCATION}` VARCHAR(127) NOT NULL,'
    f'  `{Keys.QUERY_KEYWORD}` VARCHAR(255) NOT NULL,'
    f'  `{Keys.QUERY_LANG}` CHAR(2) NOT NULL,'
    f'  `{Keys.QUERY_TIMESTAMP}` BIGINT NOT NULL,'
    f'  `{Keys.LOCATION_NAME}` TEXT NOT NULL,'
    f'  `{Keys.LOCATION_TYPE}` VARCHAR(255),'
    f'  `{Keys.COORDINATES}` POINT SRID 4326 NOT NULL,'
    f'  `{Keys.PROVINCE_ID}` INT,'
    f'  `{Keys.PROVINCE_NAME}` VARCHAR(255),'
    f'  `{Keys.CITY_ID}` INT,'
    f'  `{Keys.CITY_NAME}` VARCHAR(255),'
    f'  `{Keys.DISTRICT_ID}` INT,'
    f'  `{Keys.DISTRICT_NAME}` VARCHAR(255),'
    f'  `{Keys.VILLAGE_ID}` INT,'
    f'  `{Keys.VILLAGE_NAME}` VARCHAR(255),'
    f'  `{Keys.POSTAL_CODE}` INT,'
    f'  `{Keys.RATING}` DECIMAL(2,1),'
    f'  `{Keys.REVIEWS}` INT,'
    f'  `{Keys.DESCRIPTION}` TEXT CHARACTER SET utf8mb4,'
    f'  `{Keys.LOCATION_LINK}` TEXT,'
    f'  PRIMARY KEY (`{Keys.ID}`),'
    f'  KEY (`{Keys.QUERY_TERM}`),'
    f'  KEY (`{Keys.QUERY_LOCATION}`),'
    f'  SPATIAL KEY (`{Keys.COORDINATES}`)'
    f');'
  )

  ADD = (
    'INSERT INTO `queries` ('
    f'`{Keys.QUERY_TERM}`, '
    f'`{Keys.QUERY_LOCATION}`, '
    f'`{Keys.QUERY_KEYWORD}`, '
    f'`{Keys.QUERY_LANG}`, '
    f'`{Keys.QUERY_TIMESTAMP}`, '
    f'`{Keys.LOCATION_NAME}`, '
    f'`{Keys.LOCATION_TYPE}`, '
    f'`{Keys.COORDINATES}`, '
    f'`{Keys.PROVINCE_ID}`, '
    f'`{Keys.PROVINCE_NAME}`, '
    f'`{Keys.CITY_ID}`, '
    f'`{Keys.CITY_NAME}`, '
    f'`{Keys.DISTRICT_ID}`, '
    f'`{Keys.DISTRICT_NAME}`, '
    f'`{Keys.VILLAGE_ID}`, '
    f'`{Keys.VILLAGE_NAME}`, '
    f'`{Keys.POSTAL_CODE}`, '
    f'`{Keys.RATING}`, '
    f'`{Keys.REVIEWS}`, '
    f'`{Keys.DESCRIPTION}`, '
    f'`{Keys.LOCATION_LINK}`'
    ') '
    'VALUES ('
    f'%({Keys.QUERY_TERM})s, '
    f'%({Keys.QUERY_LOCATION})s, '
    f'%({Keys.QUERY_KEYWORD})s, '
    f'%({Keys.QUERY_LANG})s, '
    f'%({Keys.QUERY_TIMESTAMP})s, '
    f'%({Keys.LOCATION_NAME})s, '
    f'%({Keys.LOCATION_TYPE})s, '
    f'POINT(%({Keys.LATITUDE})s %({Keys.LONGITUDE})s), '
    f'%({Keys.PROVINCE_ID})s, '
    f'%({Keys.PROVINCE_NAME})s, '
    f'%({Keys.CITY_ID})s, '
    f'%({Keys.CITY_NAME})s, '
    f'%({Keys.DISTRICT_ID})s, '
    f'%({Keys.DISTRICT_NAME})s, '
    f'%({Keys.VILLAGE_ID})s, '
    f'%({Keys.VILLAGE_NAME})s, '
    f'%({Keys.POSTAL_CODE})s, '
    f'%({Keys.RATING})s, '
    f'%({Keys.REVIEWS})s, '
    f'%({Keys.DESCRIPTION})s, '
    f'%({Keys.LOCATION_LINK})s'
    ');'
  )