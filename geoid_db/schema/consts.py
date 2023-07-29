class Keys:
  #: Used in import and export. Internally, the name given by the attribute
  #: name in lowercase is used (postal_code instead of kode_pos)

  #: Query keys
  QUERY_ID            = 'query_id'
  QUERY_TERM          = 'query_term'
  QUERY_LOCATION      = 'query_location'
  QUERY_KEYWORD       = 'query_keyword'
  QUERY_LANG          = 'query_lang'
  QUERY_TIMESTAMP     = 'query_timestamp'
  QUERY_STATUS        = 'query_status'
  QUERY_RESULTS_COUNT = 'query_results_count'
  QUERY_RESULTS       = 'query_results'

  #: Places keys
  RESULT_ID     = 'result_id'
  LOCATION_NAME = 'location_name'
  LOCATION_TYPE = 'location_type'
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


class Status:
  #: Query status
  QUERY_INCOMPLETE                      = 'incomplete'
  QUERY_COMPLETE                        = 'completed'
  QUERY_COMPLETE_MUNICIPALITIES_MISSING = 'completed_municipalities_missing'
  QUERY_ERRORED                         = 'errored_during_query'
  QUERY_MISSING                         = 'missing_fields'