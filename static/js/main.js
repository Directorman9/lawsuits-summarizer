summarizer.controller('mainCtrl',function($scope, $http, $interval, $window, Upload){  
  


  var angularInterval = "";
  $scope.pdfFile = ""
  $scope.text  = ""

  $scope.init = function(){

  };

  $scope.summarize = function(){

    if ($scope.text.trim()){
       $scope.sendPrompt($scope.text)
       angularInterval = $interval(getProgress, 10000);
       $scope.heading = null;
       $scope.summary = null;
       $scope.progress = "Initializing process ..."
    }
       
    else if($scope.pdfFile){
       $scope.uploadFile($scope.pdfFile)
       angularInterval = $interval(getProgress, 10000);
       $scope.heading = null;
       $scope.summary = null;
       $scope.progress = "Initializing process ..."
    }
       
    else $window.alert("Neither text nor file is selected"); 
  };


  function getProgress(){
        $http.get('/progress')
            .then(function(resp) {

                if (resp.data.progress == "finished"){
                   $scope.progress = null;
                   $scope.heading = resp.data.heading;
                   $scope.summary = resp.data.summary;
                   $interval.cancel(angularInterval);
                }

                else{
                   $scope.progress = resp.data.progress;
                }
            })
            .catch(function(err){
                $scope.error = err.data;
                $window.alert(err.data);
            });

  };

  
  $scope.uploadFile = function(pdfFile){
        Upload.upload({url: '/summarize', data:{file:pdfFile} })
            .then(function(resp) {
               $scope.summary = resp.data.summary;
            })
            .catch(function(err) {
               $window.alert(err.data);
            });
 };




  $scope.sendPrompt = function(text){
      prompt = {"inpt":text}
      $http.post('/summarize', prompt)
           .then(function(resp) {
              $scope.summary = resp.data.summary;
           })
           .catch(function(err){
              $window.alert(err.data);
           });
  };



});


  



