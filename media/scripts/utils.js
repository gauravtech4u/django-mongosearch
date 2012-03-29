function ajaxcall(url,div,params) {
  $.get(url, params,function(data){$(div).html(data)});
}

function get_keys(value)
{
    ajaxcall('/search/get-keys/','#keys_ids',{'collection_name':value})
}