from django.urls import path
from . import musicReportViews

urlpatterns = [
    
    path("musicreport/login/", musicReportViews.login,name ="update"),
    path("musicreport/getToken/", musicReportViews.getTokenEnd,name ="get_token"),
    path("musicreport/userStats/", musicReportViews.getStats,name ="get_token"),
    path("musicreport/setsongrange/", musicReportViews.setSongRange,name ="get_token"),
    path("musicreport/setartistrange/", musicReportViews.setArtistRange,name ="get_token"),
    path("musicreport/debug/", musicReportViews.deleteAll,name ="get_token"),
    
    path("musicreport/searchquery/", musicReportViews.getResults,name ="get_card"),
    path("musicreport/getCard/", musicReportViews.getCard,name ="get_card"),
    path("musicreport/deleteCurrentCard/", musicReportViews.deleteCurrentCard,name ="delete_current"),
    path("musicreport/createNewCard/", musicReportViews.createNewCard,name ="create_new"),
    
    
    path("musicreport/imagelist/", musicReportViews.getimageresults,name ="create_new"),
    path("musicreport/setdesignimage/", musicReportViews.setdesignimage,name ="create_new"),

    path('', musicReportViews.backend_server_view, name='backend_server')

    
]