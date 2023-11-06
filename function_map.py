import functions.dates
import functions.location
import functions.search
import functions.text

fns_map = {
    "get_zipcode": functions.location.get_zipcode,
    "get_unicode_point": functions.text.get_unicode_point,
    "get_weekday": functions.dates.get_weekday,
    "get_date": functions.dates.get_date,
    "search_google": functions.search.search_google
}
