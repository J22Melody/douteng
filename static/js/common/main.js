require.config({
    baseUrl: "/static/js/lib",
    paths: {
        "jquery": "jquery-2.0.3.min",
        "handlebars": "handlebars"
    },
    shim: {
        'handlebars':{
            exports: 'handlebars'
        }
    }
});


