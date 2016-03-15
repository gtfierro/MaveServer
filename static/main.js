$(document).ready(function() {
    console.log("running");
    var uploader = new plupload.Uploader({
      runtimes : 'html5,flash,silverlight,html4',
      browse_button : 'pickfiles', // you can pass in id...
      container: document.getElementById('container'), 
      url : "/",
      filters : {
        max_file_size : '10mb',
        mime_types: [
          {title : "Data files", extensions : "csv"}
        ]
      },
   
      // Flash settings
      flash_swf_url : 'static/bower_components/plupload/js/Moxie.swf',
   
      // Silverlight settings
      silverlight_xap_url : 'static/bower_components/plupload/js/Moxie.xap',
   
      init: {
        PostInit: function() {
          document.getElementById('filelist').innerHTML = '';
          document.getElementById('uploadfiles').onclick = function() {
            uploader.start();
            return false;
          };
        },
   
        FilesAdded: function(up, files) {
          plupload.each(files, function(file) {
            document.getElementById('filelist').innerHTML += '<div id="' + file.id 
              + '">' + file.name + ' (' + plupload.formatSize(file.size) + ') <b></b></div>';
          });
        },
   
        UploadProgress: function(up, file) {
          document.getElementById(file.id).getElementsByTagName('b')[0].innerHTML = '<span>' + file.percent + "%</span>";
        },
   
        Error: function(up, err) {
          document.getElementById('console').innerHTML += "\nError #" + err.code + ": " + err.message;
        }
      }
    });
     
    console.log("init?");
    uploader.init();
});
